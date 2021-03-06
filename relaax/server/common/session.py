from builtins import object
import tensorflow as tf

from relaax.common import profiling
from relaax.server.common.saver import tensorflow_checkpoint


profiler = profiling.get_profiler(__name__)


class Session(object):
    def __init__(self, *args, **kwargs):
        # Prevents TF from consuming all GPU RAM if running on GPU
        config = tf.ConfigProto()
        # TODO: parallelism cfg =
        # tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
        config.gpu_options.allow_growth = True
        self._parent_session = None
        self._tf_session = tf.Session(config=config)
        if len(args) == 0:
            assert len(kwargs) > 0
            self.model = SuperModel(kwargs)
        else:
            assert len(kwargs) == 0
            self.model, = args

    def __getattr__(self, name):
        return SessionMethod(self, name, getattr(self.model, name))

    def create_checkpoint(self):
        return tensorflow_checkpoint.TensorflowCheckpoint(self._tf_session)

    def create_scored_checkpoint(self):
        return tensorflow_checkpoint.TensorflowScoredCheckpoint(self._tf_session)


class SuperModel(object):
    def __init__(self, desc):
        for k, v in desc.items():
            if isinstance(v, dict):
                submodel = SuperModel(v)
            else:
                submodel = v
            setattr(self, k, submodel)


class SessionMethod(object):
    def __init__(self, parent_session, name, op_or_model):
        self._parent_session = parent_session
        self._tf_session = parent_session._tf_session
        self._op_or_model = op_or_model

    def __getattr__(self, name):
        return SessionMethod(self, name, getattr(self._op_or_model, name))

    @profiler.wrap
    def __call__(self, *args, **kwargs):
        return self._op_or_model(self._parent_session, *args, **kwargs)
