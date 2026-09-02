from neurosim.neuron import LIFneuron
import matplotlib.pyplot as plt
import random
import copy

random.seed(54)

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

        candidate.append([start, duration, amplitude])

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



def run_simulation(stimulation, visual=False, print_spike_stats=False):
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

    if print_spike_stats:
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


def crossover(parent_a, parent_b):
    child = []

    for pulse_a, pulse_b in zip(parent_a, parent_b):
        if random.random() < 0.5:
            child.append(copy.deepcopy(pulse_a))
        else:
            child.append(copy.deepcopy(pulse_b))

    child.sort(key=lambda pulse: pulse[0])

    return child


def plot_population_fitness(all_fitness):
    plt.figure(figsize=(12, 6))

    for generation, fitness_values in enumerate(all_fitness):

        x_values = [
            generation
            for _ in fitness_values
        ]

        plt.scatter(
            x_values,
            fitness_values,
            alpha=0.35,
            s=15
        )

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("NeuroSim — Population Fitness by Generation")

    plt.ylim(-0.05, 1.05)

    plt.show()


def plot_fitness_history(best_history, average_history, worst_history):
    generations_axis = range(
        len(best_history)
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        generations_axis,
        best_history,
        label="Best"
    )

    plt.plot(
        generations_axis,
        average_history,
        label="Average"
    )

    plt.plot(
        generations_axis,
        worst_history,
        label="Worst"
    )

    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.title(
        "NeuroSim — Evolutionary Fitness"
    )

    plt.ylim(-0.05, 1.05)

    plt.legend()

    plt.show()


def plot_best_solution(best_ever_history, best_history):
    generations_axis = range(len(best_history))

    plt.figure(figsize=(12, 6))

    plt.plot(
        generations_axis,
        best_ever_history
    )

    plt.xlabel("Generation")
    plt.ylabel("Best fitness discovered")

    plt.title(
        "NeuroSim — Best Solution Found"
    )

    plt.ylim(-0.05, 1.05)

    plt.show()



def plot_fitness_distribution(all_fitness, best_history, average_history):
    generations_axis = range(len(best_history))

    plt.figure(figsize=(12, 6))

    for generation, fitness_values in enumerate(all_fitness):

        x_values = [
            generation
            for _ in fitness_values
        ]

        plt.scatter(
            x_values,
            fitness_values,
            alpha=0.2,
            s=10
        )

    plt.plot(
        generations_axis,
        average_history,
        linewidth=2,
        label="Population average"
    )

    plt.plot(
        generations_axis,
        best_history,
        linewidth=2,
        label="Generation best"
    )

    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.title("Evolution of Neural Stimulation")

    plt.ylim(-0.05, 1.05)

    plt.legend()

    plt.show()





stimulation_length = 500  # milliseconds
tolerance = 10
population_size = 50
times = []
voltages = []
best_score_history = []

target_spikes = [100, 200, 400]


population = [random_candidate() for _ in range(population_size)]
elite_count = 15
generations = 50
immigrant_count = 5

all_fitness = []
best_history = []
average_history = []
worst_history = []
best_ever_history = []


best_ever = 0.0

for generation in range(generations):
    evaluated = []

    for candidate in population:
        fitness, actual_spikes = evaluate_candidate(candidate, target_spikes)
        evaluated.append((fitness, candidate, actual_spikes))

    evaluated.sort(key=lambda x: x[0], reverse=True)

    best_fitness = evaluated[0][0]
    print(
        f"Generation {generation}: "
        f"{best_fitness:.3f}"
        )

    #Stats for pretty graphs
    generation_fitness = [result[0] for result in evaluated]
    all_fitness.append(generation_fitness)
    best = max(generation_fitness)
    average = sum(generation_fitness) / len(generation_fitness)
    worst = min(generation_fitness)

    best_ever = max(best_ever, best)

    best_history.append (best)
    average_history.append(average)
    worst_history.append(worst)
    best_ever_history.append(best_ever)

    elites = evaluated[:elite_count]

    new_population = []

    for fitness, candidate, actual_spikes in elites:
        new_population.append(copy.deepcopy(candidate))

        while len(new_population) < population_size - immigrant_count:
            parent_a = random.choice(elites)[1]
            parent_b = random.choice(elites)[1]

            child = crossover(parent_a, parent_b)
            child = mutate(child)
            new_population.append(child)

    for _ in range(immigrant_count):
        new_population.append(random_candidate())

    population = new_population


plot_fitness_distribution(all_fitness, best_history, average_history)