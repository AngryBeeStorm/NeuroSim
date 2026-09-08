from neurosim.lif import LIFneuron
from neurosim.izhikevich import IzhikevichNeuron


def create_neuron(model_name, **kwargs):
    if model_name == "LIF":
        return LIFneuron(**kwargs)

    if model_name == "Izhikevich":
        return IzhikevichNeuron(**kwargs)

    raise ValueError(
        f"Unknown neuron model: {model_name}"
    )