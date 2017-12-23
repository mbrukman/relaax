from builtins import object
from relaax.common.python.config.loaded_config import options


class PGConfig(object):
    @classmethod
    def preprocess(cls):
        return options.get('algorithm')


config = PGConfig.preprocess()

config.combine_gradients = options.get('algorithm/combine_gradients', 'fifo')
config.num_gradients = options.get('algorithm/num_gradients', 4)
config.dc_lambda = options.get('algorithm/dc_lambda', 0.05)
config.dc_history = options.get('algorithm/dc_history', 20)

config.avg_in_num_batches = options.get('algorithm/avg_in_num_batches', 10)
