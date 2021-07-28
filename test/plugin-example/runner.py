from iotronic_lightningrod.modules.plugins import Plugin
# from iotronic_lightningrod.modules.plugins import pluginApis as API

from oslo_log import log as logging
LOG = logging.getLogger(__name__)

# User imports
import time


class Worker(Plugin.Plugin):
    def __init__(self, uuid, name, q_result=None, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)

    def run(self):
        LOG.info("Plugin " + self.name + " starting...")
        LOG.info(self.params)

        while(self._is_running):
            LOG.info(self.params['message'])
            time.sleep(1)