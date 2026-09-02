from neurosim.neuron import LIFneuron
import matplotlib.pyplot as plt
import random
import copy

random.seed(42)

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


def visualize_spike_times(spike_times, target_spikes, neuron, stimulation):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.step(times, stimulation, where="post")

    ax1.set_ylabel("Input")
    ax1.set_title("lif neuron simulation")

    ax2.plot(times, voltages)

    ax2.axhline(neuron.v_threshold, linestyle="--", label="Spike threshold")

    for spike_time in target_spikes:
        ax2.axvline(spike_time, linestyle=":", color="red", linewidth=4.5,)

    for spike_time in spike_times:
        ax2.vlines(spike_time, neuron.v_reset, neuron.v_threshold, alpha=0.5)

    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Membrane potential (mV)")
    ax2.legend()

    ax2.legend()
    plt.show()

def random_candidate(simulation_length=500, num_pulses=3):
    candidate = []

    for _ in range(num_pulses):
        start = random.randint(0, simulation_length - 20)
        duration = random.randint(1, 15)
        amplitude = random.uniform(0, 100)

        end = min(start + duration, simulation_length)

        candidate.append((start, duration, amplitude))

    candidate.sort(key=lambda pulse: pulse[0])

    return candidate


def candidate_to_stimulation(
    candidate,
    simulation_length=500
):
    stimulation = [0.0] * simulation_length

    for start, duration, amplitude in candidate:
        end = min(start + duration, simulation_length)

        for t in range(start, end):
            stimulation[t] = amplitude

    return stimulation



def run_simulation(stimulation, visual=False):
    neuron = LIFneuron()

    spike_times = []

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


    if visual:
        visualize_spike_times(spike_times, target_spikes, neuron, stimulation)

    return spike_times


def evaluate_candidate(candidate, target_spikes):
    stimulation = candidate_to_stimulation(candidate, simulation_length=stimulation_length)
    actual_spikes = run_simulation(stimulation)
    fitness = score_spikes(target_spikes, actual_spikes)
    return fitness, actual_spikes

def mutate(candidate, chance=0.5):
    child = copy.deepcopy(candidate)

    for pulse in child:

        # mutate start time
        if random.random() < chance:
            pulse[0] += random.randint(-10, 10)

        # mutate duration
        if random.random() < chance:
            pulse[1] += random.randint(-3, 3)

        # mutate amplitude
        if random.random() < chance:
            pulse[2] += random.uniform(-15, 15)

        pulse[0] = max(0, min(pulse[0], stimulation_length - 1))
        pulse[1] = max(1, min(pulse[1], 15))
        pulse[2] = max(0, min(pulse[2], 100))

    child.sort(key=lambda pulse: pulse[0])

    return child



stimulation_length = 500  # milliseconds
tolerance = 10
population_size = 50
times = []
voltages = []
best_score_history = []

target_spikes = [100, 200, 400]


population = [random_candidate() for _ in range(population_size)]
elite_count = 10

evaluated = []

for candidate in population:
    fitness, actual_spikes = evaluate_candidate(candidate, target_spikes)
    evaluated.append((fitness, candidate, actual_spikes))

evaluated.sort(key=lambda x: x[0], reverse=True)
elites = evaluated[:elite_count]

