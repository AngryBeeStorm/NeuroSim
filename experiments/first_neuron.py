from neurosim.neuron import LIFneuron
import matplotlib.pyplot as plt



def add_pulse(stimulation, start_time, end_time, amplitude):
    for t in range(start_time, end_time):
        stimulation[t] = amplitude

def score_spikes(target_spikes, actual_spikes, tolerance=10):
    matches = 0
    matched_actual = set()
    targets = len(target_spikes)

    for target in target_spikes:
        for idx, actual in enumerate(actual_spikes):
            if idx in matched_actual:
                continue
            if abs(target - actual) <= tolerance:
                matches += 1
                matched_actual.add(idx)
                break

    precision = matches / len(actual_spikes) if actual_spikes else 0.0
    recall = matches / targets if targets > 0 else 0.0

    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0


stimulation_length = 500  # milliseconds
tolerance = 10


times = []
voltages = []
spike_times = []
target_spikes = [100, 200, 400]



stimulation = [0.0] * stimulation_length


add_pulse(stimulation, 98, 102, 60.0)
add_pulse(stimulation, 198, 202, 60.0)
#add_pulse(stimulation, 397, 402, 60.0)


neuron = LIFneuron()

for t in range(stimulation_length):
    spiked = neuron.step(input_current=stimulation[t])

    times.append(t)

    if spiked:
        spike_times.append(t)
        voltages.append(neuron.v_threshold)
    else:
        voltages.append(neuron.voltage)

print(f"Total spikes: {len(spike_times)}")
print(f"Spike times: {spike_times}")
print(f"Score: {score_spikes(target_spikes, spike_times, tolerance)}")

fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    sharex=True
)


ax1.step(times, stimulation, where="post")

ax1.set_ylabel("Input")
ax1.set_title("lif neuron simulation")


ax2.plot(times, voltages)

ax2.axhline(
    neuron.v_threshold,
    linestyle="--",
    label="Spike threshold"
)

for spike_time in target_spikes:
    ax2.axvline(
        spike_time,
        linestyle=":",
        color="red",
        linewidth=4.5,
    )


for spike_time in spike_times:
    ax2.vlines(spike_time, neuron.v_reset, neuron.v_threshold, alpha=0.5)

ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Membrane potential (mV)")
ax2.legend()

ax2.legend()
plt.show()