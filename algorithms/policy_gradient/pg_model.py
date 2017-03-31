import logging
import numpy as np

from relaax.common.algorithms.decorators import define_subgraph

from pg_config import config
from lib.models import BaseModel
from lib.weights import Weights
from lib.losses import SimpleLoss
from lib.networks import FullyConnected
from lib.utils import assemble_and_show_graphs, Placeholder, Placeholders
from lib.optimizers import Adam
from lib.gradients import Gradients
from lib.initializers import Xavier


log = logging.getLogger("policy_gradient")


# Weights of the policy are shared across
# all agents and stored on the parameter server
class SharedParameters(BaseModel):
    def assemble(self):
        # Build TF graph
        self.weights.assemble()
        self.gradients.assemble()
        self.apply_gradients.assemble()

    @define_subgraph
    def weights(self):
        return Weights.assemble(shapes=config.hidden_layers, initializer=Xavier()).op

    @define_subgraph
    def gradients(self):
        # placeholders to apply gradients to shared parameters
        return Placeholders.assemble(variables=self.weights.op).op

    @define_subgraph
    def apply_gradients(self):
        # apply gradients to weights
        optimizer = Adam(learning_rate=config.learning_rate)
        return optimizer.apply_gradients().assemble(self.gradients.op, self.weights.op).op


# Policy run by Agent(s)
class PolicyModel(BaseModel):
    def assemble(self):
        # Build TF graph
        self.weights.assemble()
        self.state.assemble()
        self.discounted_reward.assemble()
        self.shared_weights.assemble()
        self.policy.assemble()
        self.partial_gradients.assemble()
        self.assign_weights.assemble()

    @define_subgraph
    def state(self):
        return Placeholder().assemble(dtype=np.float32, shape=(None, config.state_size)).tensor

    @define_subgraph
    def discounted_reward(self):
        return Placeholder().assemble(dtype=np.float32, shape=None).tensor

    @define_subgraph
    def weights(self):
        return Weights().assemble(shapes=config.hidden_layers).tensor

    @define_subgraph
    def policy(self):
        return FullyConnected().assemble_from_weights(input=self.state, weigths=self.weights.op).op

    @define_subgraph
    def loss(self):
        return SimpleLoss().assemble(
            output=self.action, weights=self.weights.op, discounted_reward=self.discounted_reward.op).op

    @define_subgraph
    def partial_gradients(self):
        return Gradients().assemble(loss=self.loss.op, variables=self.weights.tensor).op

    @define_subgraph
    def shared_weights(self):
        # placeholders to apply weights to shared parameters
        return Placeholders().assemble(variables=self.weights.op)

    @define_subgraph
    def assign_weights(self):
        return Assign.assemble(self.weights.op, self.shared_weights.op)


if __name__ == '__main__':
    assemble_and_show_graphs(
        parameter_server=SharedParameters, agent=PolicyModel)
