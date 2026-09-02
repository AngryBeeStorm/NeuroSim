import random
import copy
import matplotlib.pyplot as plt

from experiments.evolutionary_functions import crossover, mutate
from experiments.stimulation_functions import candidate_to_stimulation, evaluate_candidate, random_candidate
from experiments import evolutionary_functions, stimulation_functions, visualizer_functions
from experiments.visualizer_functions import plot_fitness_distribution

random.seed(43)

stimulation_length = 500  # milliseconds
tolerance = 10
population_size = 50
times = []
voltages = []
best_score_history = []

target_spikes = [100, 200, 400]

stimulation_functions.stimulation_length = stimulation_length
stimulation_functions.target_spikes = target_spikes
stimulation_functions.times = times
stimulation_functions.voltages = voltages
visualizer_functions.times = times
visualizer_functions.voltages = voltages
evolutionary_functions.stimulation_length = stimulation_length

population = [random_candidate() for _ in range(population_size)]
elite_count = 15
generations = 100
immigrant_count = 5

all_fitness = []
best_history = []
average_history = []
worst_history = []
best_ever_history = []

best_ever_score = -1.0
best_ever_candidate = None
best_ever_spikes = None
best_ever_generation = None



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


    if best_fitness > best_ever_score:
        best_ever_score = best_fitness
        best_ever_candidate = copy.deepcopy(evaluated[0][1])
        best_ever_spikes = evaluated[0][2]
        best_ever_generation = generation

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

best_stimulation = candidate_to_stimulation(
    best_ever_candidate
)


fig, axes = plt.subplots(
    3,
    1,
    figsize=(12, 7),
    sharex=True
)

ax_target = axes[0]
ax_stim = axes[1]
ax_response = axes[2]


ax_target.eventplot(
    target_spikes,
    lineoffsets=1,
    linelengths=0.8,
    linewidths=2,
)
ax_target.set_ylabel("Target")
ax_target.set_yticks([])


ax_stim.step(
    range(len(best_stimulation)),
    best_stimulation,
    where="post",
    linewidth=2,
)
ax_stim.set_ylabel("Input")


ax_response.eventplot(
    best_ever_spikes,
    lineoffsets=1,
    linelengths=0.8,
    linewidths=2,
)
ax_response.set_ylabel("Actual")
ax_response.set_yticks([])
ax_response.set_xlabel("Time (ms)")

fig.suptitle(f"Best Stimulation \nFitness: {best_ever_score:.3f}, \nGeneration: {best_ever_generation}")

plt.tight_layout()
plt.show()