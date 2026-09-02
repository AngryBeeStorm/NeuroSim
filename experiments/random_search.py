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

target_spikes = [100, 200, 400]

stimulation_functions.stimulation_length = stimulation_length
stimulation_functions.target_spikes = target_spikes
stimulation_functions.times = times
stimulation_functions.voltages = voltages
visualizer_functions.times = times
visualizer_functions.voltages = voltages



best_score = -1
best_stimulation = None
best_spikes = None

for i in range(1000):

    candidate = random_candidate()
    print(candidate)

    score = evaluate_candidate(candidate, target_spikes)[0]
    best_score_history.append(score)

    if score > best_score:
        best_score = score
        #best_stimulation = stimulation
        #best_spikes = actual_spikes
        

        print(
            f"New best! Candidate {i}: "
            f"{best_score:.3f}"
        )

print(f"Best score: {best_score:.3f}")

plt.plot(best_score_history)

plt.xlabel("Candidate tested")
plt.ylabel("Best score so far")
plt.title("Random Search")
plt.show()

