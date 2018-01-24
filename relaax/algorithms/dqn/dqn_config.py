from relaax.common.python.config.loaded_config import options
from argparse import Namespace

config = options.get('algorithm')

config.avg_in_num_batches = options.get('algorithm/avg_in_num_batches', 200)
config.input.history = options.get('algorithm/input/history', 1)

for key, value in [('use_convolutions', [])]:
    if not hasattr(config, key):
        setattr(config, key, value)

config.max_global_step = options.get('algorithm/max_global_step', 1e8)
config.use_linear_schedule = options.get('algorithm/use_linear_schedule', False)

config.initial_learning_rate = options.get('algorithm/initial_learning_rate', 1e-4)
config.learning_rate_end = options.get('algorithm/learning_rate_end', 0.0)

config.optimizer = options.get('algorithm/optimizer', 'Adam')   # Adam | RMSProp
# RMSProp default parameters
if not hasattr(config, 'RMSProp'):
    config.RMSProp = options.get('algorithm/RMSProp', Namespace())
config.RMSProp.decay = options.get('algorithm/RMSProp/decay', 0.99)
config.RMSProp.epsilon = options.get('algorithm/RMSProp/epsilon', 0.1)

config.gradients_norm_clipping = options.get('algorithm/gradients_norm_clipping', False)

# check hidden sizes
if len(config.hidden_sizes) > 0:
    if config.hidden_sizes[-1] % 2 != 0:
        raise ValueError("Number of outputs in the last hidden layer must be divisible by 2")

config.output.q_values = options.get('algorithm/output/q_values', False)
config.alpha = options.get('algorithm/alpha', 1.0)

config.combine_gradients = options.get('algorithm/combine_gradients', 'fifo')
config.num_gradients = options.get('algorithm/num_gradients', 4)
config.dc_lambda = options.get('algorithm/dc_lambda', 0.05)
config.dc_history = options.get('algorithm/dc_history', 20)
