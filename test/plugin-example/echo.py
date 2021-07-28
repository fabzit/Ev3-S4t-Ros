from iotronic_lightningrod.modules.plugins import Plugin

from oslo_log import log as logging
LOG = logging.getLogger(__name__)

# User imports


class Worker(Plugin.Plugin):

    def __init__(self, uuid, name, q_result, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)

    def run(self):
        LOG.info("Input parameters: " + str(self.params['name']))
        LOG.info("Plugin " + self.name + " process completed!")
        self.q_result.put("ECHO RESULT: " + str(self.params['name']))