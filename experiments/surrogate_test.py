from experiments.stimulation_functions import evaluate_candidate
from neurosim.surrogate import train_surrogate, flatten_candidate
from experiments.crossover_search_reusable import run_evolution_crossover
from experiments.evolutionary_functions import generate_offspring
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from scipy.stats import spearmanr

from neurosim.surrogate import (
    flatten_candidate,
    train_surrogate
)


# --------------------------------------------------
# Experiment settings
# --------------------------------------------------

TARGET_SPIKES = [150, 300, 420]
STIMULATION_LENGTH = 500

POPULATION_SIZE = 70
GENERATIONS = 120
NUM_PULSES = 3

NUM_TEST_OFFSPRING = 200
TOP_FRACTION = 0.20


# --------------------------------------------------
# 1. Run normal evolutionary search
# --------------------------------------------------

result = run_evolution_crossover(
    target_spikes=TARGET_SPIKES,
    num_pulses=NUM_PULSES,
    population_size=POPULATION_SIZE,
    generations=GENERATIONS,
    stimulation_length=STIMULATION_LENGTH,
    neuron_model="LIF"
)


# --------------------------------------------------
# 2. Get collected simulator data
# --------------------------------------------------

X = result["training_X"]
y = result["training_y"]

print("\nTraining data")
print("-----------------------")
print("Examples:", len(y))
print("Min fitness:", min(y))
print("Max fitness:", max(y))
print(
    "Average fitness:",
    sum(y) / len(y)
)


# --------------------------------------------------
# 3. Train / test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------------------------
# 4. Train surrogate
# --------------------------------------------------

model = train_surrogate(
    X_train,
    y_train,
)

print("\nModel trained.")


# --------------------------------------------------
# 5. Test on held-out evolutionary data
# --------------------------------------------------

heldout_predictions = model.predict(X_test)

heldout_mae = mean_absolute_error(
    y_test,
    heldout_predictions
)

print("\nHeld-out test")
print("-----------------------")
print(
    f"MAE: {heldout_mae:.4f}"
)


# --------------------------------------------------
# 6. Generate brand-new evolutionary offspring
# --------------------------------------------------

test_candidates = generate_offspring(
    result["final_elites"],
    count=NUM_TEST_OFFSPRING,
    stimulation_length=STIMULATION_LENGTH
)


# --------------------------------------------------
# 7. Ask surrogate to predict offspring fitness
# --------------------------------------------------

test_X = [
    flatten_candidate(candidate)
    for candidate in test_candidates
]

predicted_scores = model.predict(test_X)


# --------------------------------------------------
# 8. Actually simulate THE SAME offspring
# --------------------------------------------------

actual_scores = []

for candidate in test_candidates:

    fitness, _ = evaluate_candidate(
        candidate,
        TARGET_SPIKES,
        stimulation_penalty=0.01,
        neuron_model="LIF",
        neuron_params=None,
        noise_std=0.0
    )

    actual_scores.append(fitness)


# Convert to NumPy arrays
predicted_scores = np.array(
    predicted_scores
)

actual_scores = np.array(
    actual_scores
)


# --------------------------------------------------
# 9. Compare predictions with reality
# --------------------------------------------------

offspring_mae = mean_absolute_error(
    actual_scores,
    predicted_scores
)

spearman, _ = spearmanr(
    actual_scores,
    predicted_scores
)

print("\nNew offspring test")
print("-----------------------")
print(
    f"Offspring MAE: {offspring_mae:.4f}"
)
print(
    f"Spearman correlation: {spearman:.4f}"
)


# --------------------------------------------------
# 10. Show first 10 CORRECT prediction pairs
# --------------------------------------------------

print("\nFirst 10 offspring")
print("-----------------------")

for predicted, actual in zip(
    predicted_scores[:10],
    actual_scores[:10]
):

    print(
        f"Predicted: {predicted:.3f} | "
        f"Actual: {actual:.3f}"
    )


# --------------------------------------------------
# 11. Does ML actually select better candidates?
# --------------------------------------------------

top_count = max(
    1,
    int(
        len(test_candidates)
        * TOP_FRACTION
    )
)

top_indices = np.argsort(
    predicted_scores
)[-top_count:]

all_mean = actual_scores.mean()

ml_selected_mean = actual_scores[
    top_indices
].mean()

print("\nCandidate selection")
print("-----------------------")
print(
    f"All offspring mean fitness: "
    f"{all_mean:.4f}"
)

print(
    f"ML-selected top {TOP_FRACTION:.0%} "
    f"mean fitness: "
    f"{ml_selected_mean:.4f}"
)


# --------------------------------------------------
# 12. Optional: how good is the very best ML choice?
# --------------------------------------------------

best_predicted_index = np.argmax(
    predicted_scores
)

print("\nBest ML-ranked candidate")
print("-----------------------")
print(
    f"Predicted fitness: "
    f"{predicted_scores[best_predicted_index]:.4f}"
)

print(
    f"Actual fitness: "
    f"{actual_scores[best_predicted_index]:.4f}"
)


# --------------------------------------------------
# 13. Plot predicted vs actual
# --------------------------------------------------

plt.figure()

plt.scatter(
    predicted_scores,
    actual_scores,
    alpha=0.7
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("Predicted fitness")
plt.ylabel("Actual fitness")
plt.title(
    "Surrogate Predictions on New Evolutionary Offspring"
)

plt.xlim(0, 1)
plt.ylim(0, 1)

plt.show()