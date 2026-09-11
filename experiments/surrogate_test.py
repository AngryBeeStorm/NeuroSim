from neurosim.surrogate import train_surrogate, flatten_candidate
from experiments.crossover_search_reusable import run_evolution_crossover
from experiments.stimulation_functions import random_candidate
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error



result = run_evolution_crossover(
        target_spikes=[150, 300, 420],
        num_pulses = 3,
        population_size=70,
        generations=120,
        stimulation_length=500,
        neuron_model="LIF"
    )


X = result["training_X"]
y = result["training_y"]

print("Min:", min(result["training_y"]))
print("Max:", max(result["training_y"]))
print("Average:", sum(result["training_y"]) / len(result["training_y"]))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = train_surrogate(
    X_train,
    y_train,
    seed=42
)



print("Model trained.")



predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("Test MAE:", mae)

test_candidates = []

for _ in range(100):
    candidate = random_candidate(500,  num_pulses= 3)

    test_candidates.append(candidate)

test_X = [
    flatten_candidate(candidate)
    for candidate in test_candidates
]


predictions = model.predict(test_X)

for predicted, actual in zip(
    predictions,
    y[:10]
):
    print(
        f"Predicted: {predicted:.3f} | "
        f"Actual: {actual:.3f}"
    )