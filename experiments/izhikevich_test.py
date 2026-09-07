from neurosim.izhikevich import IzhikevichNeuron
import matplotlib.pyplot as plt


def plot_voltage(voltages, spikes):
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
    plt.title("Izhikevich Neuron spike plot")
    plt.legend()

    plt.tight_layout()
    plt.show()



neuron = IzhikevichNeuron()

voltages = []
spikes = []

for t in range(500):

    current = 10

    spike = neuron.step(current)

    voltages.append(neuron.v)

    if spike:
        spikes.append(t)

print(spikes)

plot_voltage(voltages, spikes)