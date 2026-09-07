from neurosim.izhikevich import IzhikevichNeuron
from neurosim.presets import IZHIKEVICH_PRESETS
import matplotlib.pyplot as plt


def plot_voltage(voltages, spikes, preset_name):
    time = range(len(voltages))

    plt.figure(figsize=(10, 4))

    plt.plot(time, voltages, label="Membrane voltage")

    for spike_time in spikes:
        plt.axvline(
            spike_time,
            linestyle="--",
            alpha=0.4
        )

    plt.axhline(
        30,
        linestyle=":",
        label="Spike threshold"
    )

    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane voltage  (mV)")
    plt.title(f"Izhikevich Neuron: {preset_name}")
    plt.legend()

    plt.tight_layout()
    plt.show()



simulation_length = 500
current = 10

for preset_name, parameters in IZHIKEVICH_PRESETS.items():
    neuron = IzhikevichNeuron(**parameters)
    voltages = []
    spikes = []

    for time in range(simulation_length):
        spike, display_voltage = neuron.step(current)
        voltages.append(display_voltage)

        if spike:
            spikes.append(time)

    print(f"{preset_name}: {spikes}")
    plot_voltage(voltages, spikes, preset_name)