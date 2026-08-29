from neurosim.neuron import LIFneuron


neuron = LIFneuron()
spike_count = 0

for t in range(100): 
    spiked = neuron.step(input_current=5.0)

    if spiked:
        spike_count += 1

    print(
        f"Time: {t} ms",
        f"Voltage: {neuron.voltage:.2f} mV",
        f"Spiked: {spiked}"
    )

print(f"Total spikes: {spike_count}")