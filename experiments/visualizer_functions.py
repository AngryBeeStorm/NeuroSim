import matplotlib.pyplot as plt


times = []
voltages = []


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
    plt.title("Population Fitness by Generation")

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
