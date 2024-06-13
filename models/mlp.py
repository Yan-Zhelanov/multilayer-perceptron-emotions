import sys

import numpy as np

from configs.mlp_config import ModelConfig
from modules.layers.activations import LeakyReLU, ReLU, Sigmoid, Tanh
from modules.layers.base import BaseLayer
from modules.layers.linear import Linear
from modules.utils.parameter_initialization import ParametersInit


class MLP:
    """A class for implementing Multilayer perceptron model."""

    def __init__(self, config: ModelConfig) -> None:
        """Initialize MLP model.

        Args:
            config: model configurations
        """
        self._config = config
        self._params_init = ParametersInit(config)
        self._layers = self._init_layers()

    def _init_layers(self) -> list[BaseLayer]:
        """MLP layers initialization.

        This method should include the following steps:
        1. Go through the layers ((layer_name, layer_params) tuples) defined in
            self.config.layers one by one.
        2. For each layer, get an instance of the layer class with layer_name
            and layer_params as:
            layer = getattr(sys.modules[__name__], layer_name)(**layer_params)
        3. For layer instance call self.params_init function to initialize
            layer parameters if it has those (!).
        4. Append the initialized layer to the layers list.
        5. Return list with all the initialized layers.

        Returns:
            list of initialized layers
        """
        # TODO: Implement this method
        layers = []
        raise NotImplementedError

    def train(self):
        """Sets the training mode for each layer."""
        for layer in self._layers:
            layer.train()

    def eval(self):
        """Sets the evaluation mode for each layer."""
        for layer in self._layers:
            layer.eval()

    def __call__(self, inputs: np.ndarray):
        """Forward propagation implementation.

        This method propagates inputs through all the layers from self.layers.
        It should include the following steps:
            1. Reshape inputs into a 2D array (first dimension is the mini-batch size)
            2. Update inputs sequentially by passing through each layer in self.layers (using layer's __call__() method)
            3. Return updated inputs

        Returns:
            np.ndarray: updated inputs
        """
        # TODO: Implement this method
        raise NotImplementedError

    def load_params(self, parameters):
        """Loads model parameters."""
        assert len(parameters) == len(self._layers)
        for i, layer in enumerate(self._layers):
            layer.load_params(parameters[i])

    def get_params(self):
        """Returns model parameters."""
        parameters = []
        for layer in self._layers:
            parameters.append(layer.get_params())
        return parameters
