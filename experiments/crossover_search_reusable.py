import random
import copy
import matplotlib.pyplot as plt

from experiments.evolutionary_functions import crossover, mutate
from experiments.stimulation_functions import candidate_to_stimulation, evaluate_candidate, random_candidate
from experiments import evolutionary_functions, stimulation_functions, visualizer_functions
from experiments.visualizer_functions import plot_fitness_distribution
from neurosim.surrogate import flatten_candidate

random.seed(43)


def run_evolution_crossover(
    target_spikes,
    num_pulses=3,
    population_size=50,
    generations=100,
    stimulation_length=1000,
    elite_count=15,
    immigrant_count=5,
    manual = False,
    neuron_model="LIF",
    neuron_params=None,
    noise_std = 0.0
):

    times = []
    voltages = []


    training_X = []
    training_y = []


    stimulation_functions.stimulation_length = stimulation_length
    stimulation_functions.target_spikes = target_spikes
    stimulation_functions.times = times
    stimulation_functions.voltages = voltages
    evolutionary_functions.stimulation_length = stimulation_length

    population = [random_candidate(stimulation_length, num_pulses) for _ in range(population_size)]


    all_fitness = []
    best_history = []
    average_history = []
    worst_history = []
    best_ever_history = []

    best_ever_score = -1.0
    best_ever_candidate = None
    best_ever_spikes = None
    best_ever_generation = None

    #automaticaly make 30% of population size elites and 10% of population size immigrants
    if not manual:
        elite_count = max(1, int(population_size * 0.3))
        immigrant_count = max(1, int(population_size * 0.1))
    



    best_ever = 0.0

    for generation in range(generations):
        evaluated = []

        for candidate in population:
            fitness, actual_spikes = evaluate_candidate(candidate, target_spikes, stimulation_penalty=0.01, neuron_model=neuron_model, neuron_params=neuron_params, noise_std=noise_std)
            evaluated.append((fitness, candidate, actual_spikes))

            #ai training 
            training_X.append(flatten_candidate(candidate))
            training_y.append(fitness)

        evaluated.sort(key=lambda x: x[0], reverse=True)

        best_fitness = evaluated[0][0]

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
                child = mutate(child, stimulation_length=stimulation_length)
                new_population.append(child)

        for _ in range(immigrant_count):
            new_population.append(random_candidate(stimulation_length, num_pulses))

        population = new_population

    best_stimulation = candidate_to_stimulation(
        best_ever_candidate,
        simulation_length=stimulation_length
    )

    return {
    "score": best_ever_score,
    "candidate": best_ever_candidate,
    "spikes": best_ever_spikes,
    "generation": best_ever_generation,
    "stimulation": best_stimulation,
    "best_history": best_history,
    "average_history": average_history,
    "worst_history": worst_history,
    "best_ever_history": best_ever_history,

    "training_X": training_X,
    "training_y": training_y,   
    }

