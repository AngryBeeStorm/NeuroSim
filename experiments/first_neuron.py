from neurosim.neuron import LIFneuron
import matplotlib.pyplot as plt


times = []
voltages = []
spike_times = []

neuron = LIFneuron()

for t in range(500):
    spiked = neuron.step(input_current=17.0)

    times.append(t)
    voltages.append(neuron.voltage)

    if spiked:
        spike_times.append(t)

print(f"Total spikes: {len(spike_times)}")
print(f"Spike times: {spike_times}")

plt.plot(times, voltages)

plt.xlabel("Time (ms)")
plt.ylabel("Membrane potential (mV)")
plt.title("LIF Neuron")

plt.axhline(
    y=neuron.v_threshold,
    linestyle="--",
    label="Spike threshold"
)

for spike_time in spike_times:
    plt.axvline(
        x=spike_time,
        alpha=0.25
    )

plt.legend()
plt.show()