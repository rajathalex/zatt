import copy
import asyncio
import shutil
from multiprocessing import Process
from zatt.server.main import setup


class Pool:
    def __init__(self, server_ids):
        if type(server_ids) is int:
            server_ids = range(server_ids)
        self._generate_configs(server_ids)
        self.servers = {}
        for config in self.configs.values():
            print('Generating server', config['id'])
            self.servers[config['id']] = (Process(target=self._run_server,
                                                  args=(config,)))

    def start(self, n):
        if type(n) is int:
            n = [n]
        for x in n:
            print('Starting server', x)
            self.servers[x].start()

    def stop(self, n):
        if type(n) is int:
            n = [n]
        for x in n:
            print('Stopping server', x)
            if self.running[x]:
                self.servers[x].terminate()
                self.servers[x] = Process(target=self._run_server,
                                          args=(self.configs[x],))

    def rm(self, n):
        if type(n) is int:
            n = [n]
        for x in n:
            shutil.rmtree(self.configs[x]['storage'])
            print('Removing files related to server', x)

    @property
    def running(self):
        return {k: v.is_alive() for (k, v) in self.servers.items()}

    @property
    def ids(self):
        return list(self.configs.keys())

    def _generate_configs(self, server_ids):
        shared = {'cluster': {}, 'storage': 'zatt.{}.persist',
                'id': None, 'debug': False, 'save':False}

        for server_id in server_ids:
            shared['cluster'][server_id] = ('127.0.0.1', 9110 + server_id)

        self.configs = {}
        for server_id in server_ids:
            config = copy.deepcopy(shared)
            config['storage'] = config['storage'].format(server_id)
            config['id'] = server_id
            self.configs[server_id] = config

    def _run_server(self, config):
        print(config)
        setup(config)
        loop = asyncio.get_event_loop()
        loop.run_forever()