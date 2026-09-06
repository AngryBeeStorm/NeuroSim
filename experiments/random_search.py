import matplotlib.pyplot as plt
import random

from experiments.evolutionary_functions import score_spikes
from experiments.stimulation_functions import (
    add_pulse,
    candidate_to_stimulation,
    evaluate_candidate,
    random_candidate,
    run_simulation,
)
from experiments import stimulation_functions, visualizer_functions

random.seed(43)

stimulation_length = 500  # milliseconds
tolerance = 10

times = []
voltages = []
best_score_history = []

target_spikes = [100, 200, 430]


def run_evolution_random(
    target_spikes,
    num_pulses=3,
    population_size=50,
    generations=100,
    stimulation_length=1000,
    elite_count=15,
    immigrant_count=5,
    manual = False,
):


    stimulation_functions.stimulation_length = stimulation_length
    stimulation_functions.target_spikes = target_spikes
    stimulation_functions.times = times
    stimulation_functions.voltages = voltages
    visualizer_functions.times = times
    visualizer_functions.voltages = voltages



    best_score = -1
    best_stimulation = None
    best_spikes = None
    best_ever_candidate = None

    for i in range(population_size*generations):

        candidate = random_candidate(num_pulses=num_pulses, simulation_length=stimulation_length)
        print(candidate)

        result = evaluate_candidate(candidate, target_spikes)
        score = result[0]
        stimulation = candidate_to_stimulation(candidate, stimulation_length)
        actual_spikes = result[1]

        best_score_history.append(score)

        if score > best_score:
            best_score = score
            best_stimulation = stimulation
            best_ever_spikes = actual_spikes
            best_ever_candidate = candidate
            #best_spikes = actual_spikes
            

    return {
            "score": best_score,
            "candidate": best_ever_candidate,
            "spikes": best_ever_spikes,
            "generation": 1,
            "stimulation": best_stimulation,
            "best_history": best_score_history,
            "average_history": best_score_history,
            "worst_history": best_score_history,
            "best_ever_history": best_score_history,
        }

    #plt.plot(best_score_history)

    #plt.xlabel("Candidate tested")
    #plt.ylabel("Best score so far")
    #plt.title("Random Search")
    #plt.show()

