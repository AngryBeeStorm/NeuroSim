import random
import copy

from experiments.evolutionary_functions import mutate
from experiments.stimulation_functions import evaluate_candidate, random_candidate
from experiments import evolutionary_functions, stimulation_functions, visualizer_functions
from experiments.visualizer_functions import plot_fitness_distribution, plot_fitness_history

random.seed(52)

stimulation_length = 500  # milliseconds
tolerance = 10
population_size = 50
times = []
voltages = []
best_score_history = []

target_spikes = [100, 200, 430]

stimulation_functions.stimulation_length = stimulation_length
stimulation_functions.target_spikes = target_spikes
stimulation_functions.times = times
stimulation_functions.voltages = voltages
visualizer_functions.times = times
visualizer_functions.voltages = voltages
evolutionary_functions.stimulation_length = stimulation_length

population = [random_candidate() for _ in range(population_size)]
elite_count = 20
generations = 50

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

        while len(new_population) < population_size:
            parent = random.choice(elites)[1]
            child = mutate(parent)
            new_population.append(child)

    population = new_population


plot_fitness_distribution(all_fitness, best_history, average_history)
