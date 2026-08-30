from neurosim.neuron import LIFneuron
import matplotlib.pyplot as plt



def add_pulse(stimulation, start_time, end_time, amplitude):
    for t in range(start_time, end_time):
        stimulation[t] = amplitude




stimulation_length = 500  # milliseconds

times = []
voltages = []
spike_times = []

stimulation = [0.0] * stimulation_length


add_pulse(stimulation, 97, 103, 80.0)
add_pulse(stimulation, 245, 250, 90.0)
add_pulse(stimulation, 398, 400, 100.0)


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


fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    sharex=True
)


ax1.plot(times, stimulation)

ax1.set_ylabel("Input")
ax1.set_title("Stimulation")


ax2.plot(times, voltages)

ax2.axhline(
    neuron.v_threshold,
    linestyle="--",
    label="Spike threshold"
)

ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Membrane potential (mV)")
ax2.legend()

ax2.legend()
plt.show()