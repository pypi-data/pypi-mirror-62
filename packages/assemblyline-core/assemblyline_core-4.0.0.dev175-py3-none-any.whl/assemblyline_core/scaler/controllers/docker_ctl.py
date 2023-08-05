import os
import time
from assemblyline.odm.models.service import DockerConfig
from .interface import ControllerInterface, ServiceControlError

# How to identify the update volume as a whole, in a way that the underlying container system recognizes.
FILE_UPDATE_VOLUME = os.environ.get('FILE_UPDATE_VOLUME', None)

# Where to find the update directory inside this container.
FILE_UPDATE_DIRECTORY = os.environ.get('FILE_UPDATE_DIRECTORY', None)
INHERITED_VARIABLES = ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'no_proxy']

# Every this many seconds, check that the services can actually reach the service server.
NETWORK_REFRESH_INTERVAL = 60 * 3


class DockerController(ControllerInterface):
    """A controller for *non* swarm mode docker."""
    def __init__(self, logger, prefix='', labels=None, cpu_overallocation=1, memory_overallocation=1):
        """
        :param logger: A logger to report status and debug information.
        :param prefix: A prefix used to distinguish containers launched by this controller.
        :param cpu_overallocation: A multiplier on CPU usage. (2 means act like there are twice as many CPU present)
        :param memory_overallocation: A multiplier on memory usage. (2 means act like there is twice as much memory)
        """
        # Connect to the host docker port
        import docker
        self.client = docker.from_env()
        self.log = logger
        self.global_mounts = []
        self._prefix = prefix
        self._labels = labels

        for network in self.client.networks.list(names=['external']):
            self.external_network = network
            break
        else:
            self.external_network = self.client.networks.create(name='external', internal=False)
        self.networks = {}
        self._last_network_refresh = 0

        # CPU and memory reserved for the host
        self._reserved_cpu = 0.3
        self._reserved_mem = 500
        self.cpu_overallocation = cpu_overallocation
        self.memory_overallocation = memory_overallocation
        self._profiles = {}

        # Prefetch some info that shouldn't change while we are running
        self._info = self.client.info()

        # We aren't checking for swarm nodes
        assert not self._info['Swarm']['NodeID']

    def get_service_server(self):
        service_server_container = None
        while service_server_container is None:
            for container in self.client.containers.list():
                if 'service_server' in container.name:
                    service_server_container = container
                    self.log.info(f'Found the service server at: {container.id} [{container.name}]')
                    break
            if not service_server_container:
                time.sleep(1)
        return service_server_container

    def refresh_service_networks(self):
        service_server = self.get_service_server()
        for service_name in self.networks:
            network = self._get_network(service_name)
            if service_server.name not in {c.name for c in network.containers}:
                self.networks[service_name].connect(service_server, aliases=['service-server'])
        self._last_network_refresh = time.time()

    def add_profile(self, profile):
        """Tell the controller about a service profile it needs to manage."""
        self._profiles[profile.name] = profile

    def _start(self, service_name):
        """Launch a docker container in a manner suitable for Assembylyline."""
        container_name = self._name_container(service_name)
        prof = self._profiles[service_name]
        cfg = prof.container_config

        # Set the list of labels
        labels = dict(self._labels)
        labels.update({'component': service_name})

        # Prepare the volumes and folders
        volumes = {row[0]: {'bind': row[1], 'mode': 'ro'} for row in self.global_mounts}
        volumes[os.path.join(FILE_UPDATE_VOLUME, service_name)] = {'bind': '/mount/updates/', 'mode': 'ro'}
        if not os.path.exists(os.path.join(FILE_UPDATE_DIRECTORY, service_name)):
            os.makedirs(os.path.join(FILE_UPDATE_DIRECTORY, service_name), 0x777)

        container = self.client.containers.run(
            image=cfg.image,
            name=container_name,
            cpu_period=100000,
            cpu_quota=int(100000*cfg.cpu_cores),
            mem_limit=f'{cfg.ram_mb}m',
            labels=labels,
            restart_policy={'Name': 'always'},
            command=cfg.command,
            volumes=volumes,
            network=self._get_network(service_name).name,
            environment=[f'{_e.name}={_e.value}' for _e in cfg.environment] + ['UPDATE_PATH=/mount/updates/'] +
                        [f'{name}={os.environ[name]}' for name in INHERITED_VARIABLES if name in os.environ],
            detach=True,
        )

        if cfg.allow_internet_access:
            self.external_network.connect(container)

    def _start_container(self, name, labels, volumes, cfg: DockerConfig, network, hostname):
        """Launch a docker container."""
        # Take the port strings and convert them to a dictionary
        ports = {}
        for port_string in cfg.ports:
            # It might just be a port number, try that
            try:
                port_number = int(port_string)
                ports[port_number] = port_number
                continue
            except ValueError:
                pass

            # Then it might be "number:number"
            if ':' in port_string:
                a, b = port_string.split(':')
                ports[int(a)] = int(b)
                continue

            self.log.warning(f"Not sure how to parse port string {port_string} for container {name} not using it...")

        container = self.client.containers.run(
            image=cfg.image,
            name=name,
            cpu_period=100000,
            cpu_quota=int(100000*cfg.cpu_cores),
            mem_limit=f'{cfg.ram_mb}m',
            labels=labels,
            restart_policy={'Name': 'always'},
            command=cfg.command,
            volumes=volumes,
            network=network,
            environment=[f'{_e.name}={_e.value}' for _e in cfg.environment] +
                        [f'{name}={os.environ[name]}' for name in INHERITED_VARIABLES if name in os.environ],
            detach=True,
            ports=ports
        )
        if cfg.allow_internet_access:
            self.external_network.connect(container, aliases=[hostname])

    def _name_container(self, service_name):
        """Find an unused name for a container.

        Container names must be unique, but we want our names to be predictable and informative.
        Cycle through the pattern we want until we find the lowest free numerical suffix.
        """
        # Load all container names on the system now
        used_names = []
        for container in self.client.containers.list(all=True):
            used_names.append(container.name)

        # Try names until one works
        used_names = set(used_names)
        index = 0
        while True:
            name = f'{service_name}_{index}'
            if self._prefix:
                name = self._prefix + '_' + name
            if name not in used_names:
                return name
            index += 1

    def cpu_info(self):
        """Try to estimate how much CPU the docker host has unreserved.

        NOTE: There is probably a better way to do this.
        """
        # This network thing has nothing to do with cpu_info, its just here because this
        # is a method we know will run regularly.
        if time.time() - self._last_network_refresh > NETWORK_REFRESH_INTERVAL:
            self.refresh_service_networks()

        total_cpu = cpu = self._info['NCPU'] * self.cpu_overallocation - self._reserved_cpu
        for container in self.client.containers.list():
            if container.attrs['HostConfig']['CpuPeriod']:
                cpu -= container.attrs['HostConfig']['CpuQuota']/container.attrs['HostConfig']['CpuPeriod']
        self.log.debug(f'Total CPU available {cpu}/{self._info["NCPU"]}')
        return cpu, total_cpu

    def memory_info(self):
        """Try to estimate how much RAM the docker host has unreserved.

        NOTE: There is probably a better way to do this.
        """
        mega = 2**20
        total_mem = mem = self._info['MemTotal']/mega * self.memory_overallocation - self._reserved_mem
        for container in self.client.containers.list():
            mem -= container.attrs['HostConfig']['Memory']/mega
        self.log.debug(f'Total Memory available {mem}/{self._info["MemTotal"]/mega}')
        return mem, total_mem

    def get_target(self, service_name):
        """Get how many instances of a service we expect to be running.

        Since we start our containers with 'restart always' we just need to count how many
        docker is currently trying to keep running.
        """
        running = 0
        for container in self.client.containers.list(filters={'label': f'component={service_name}'}):
            if container.status in {'restarting', 'running'}:
                running += 1
            elif container.status in {'created', 'removing', 'paused', 'exited', 'dead'}:
                pass
            else:
                self.log.warning(f"Unknown docker status string: {container.status}")
        return running

    def set_target(self, service_name, target):
        """Change how many instances of a service docker is trying to keep up.

        This is managed by killing extra containers at random, or launching new ones.
        """
        try:
            running = self.get_target(service_name)
            self.log.debug(f"New target for {service_name}: {running} -> {target}")
            delta = target - running

            if delta < 0:
                # Kill off delta instances of of the service
                filters = {'label': f'component={service_name}'}
                running = [container for container in self.client.containers.list(filters=filters)
                           if container.status in {'restarting', 'running'}]
                running = running[0:-delta]
                for container in running:
                    container.kill()

            if delta > 0:
                # Start delta instances of the service
                for _ in range(delta):
                    self._start(service_name)

            # Every time we change our container allocation do a little clean up to keep things fresh
            self.client.containers.prune()
            self.client.volumes.prune()
        except Exception as error:
            raise ServiceControlError(str(error), service_name)

    def stop_container(self, service_name, container_id):
        import docker.errors
        container = None
        try:
            # First try the given container id in case its actually correct
            container = self.client.containers.get(container_id)
        except docker.errors.NotFound:
            for possible_container in self.client.containers.list(filters={'label': f'component={service_name}'}):
                if possible_container.id.startswith(container_id) or possible_container.name == container_id:
                    container = possible_container
                    break

        if container and container.labels.get('component') == service_name and container.status == 'running':
            container.kill()

    def restart(self, service):
        for container in self.client.containers.list(filters={'label': f'component={service.name}'}):
            container.kill()

    def get_running_container_names(self):
        out = []
        for container in self.client.containers.list():
            out.append(container.id)
            out.append(container.id[:12])
            out.append(container.name)
        return out

    def start_stateful_container(self, service_name, container_name, spec, labels):
        volumes = {_n: {'bind': _v.mount_path, 'mode': 'rw'} for _n, _v in spec.volumes.items()}
        deployment_name = f'{service_name}-dep-{container_name}'

        all_labels = dict(self._labels)
        all_labels.update({'component': service_name})
        all_labels.update(labels)

        self._start_container(name=deployment_name, labels=all_labels, volumes=volumes, hostname=container_name,
                              cfg=spec.container, network=self._get_network(service_name).name)

    def stop_containers(self, labels):
        label_strings = [f'{name}={value}' for name, value in labels.items()]
        for container in self.client.containers.list(filters={'label': label_strings}):
            container.stop()

    def _get_network(self, service_name):
        """Get a reference to the network a service uses.

        Since we need a reference to networks in docker we will do this setup
        dynamically rather than in prepare_network.
        """
        from docker.errors import NotFound
        # Create network for service
        network_name = f'service-net-{service_name}'
        try:
            network = self.client.networks.get(network_name)
            self.networks[service_name] = network
            network.reload()
        except NotFound:
            self.networks[service_name] = self.client.networks.create(name=network_name, internal=True)
        return self.networks[service_name]

    def prepare_network(self, service_name, internet):
        self._get_network(service_name)
        self.refresh_service_networks()

