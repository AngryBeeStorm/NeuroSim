from experiments.crossover_search_reusable import run_evolution_crossover, run_ml_guided_evolution
import matplotlib.pyplot as plt

target_spikes = [150, 170, 210, 340, 360, 390]

normal = run_evolution_crossover(
    target_spikes=target_spikes,
    population_size=70,
    generations=50,
    stimulation_length=500,
    neuron_model="LIF"
)

ml = run_ml_guided_evolution(
    target_spikes=target_spikes,
    population_size=70,
    generations=50,
    stimulation_length=500,
    neuron_model="LIF",
    warmup_generations=5,
    candidate_multiplier=5
)

print(
    "Normal:",
    normal["score"],
    "generation:",
    normal["generation"]
)

print(
    "ML-guided:",
    ml["score"],
    "generation:",
    ml["generation"]
)

plt.figure()

plt.plot(
    normal["best_ever_history"],
    label="Evolutionary"
)

plt.plot(
    ml["best_ever_history"],
    label="ML-guided"
)

plt.xlabel("Generation")
plt.ylabel("Best fitness")
plt.title(
    "Evolutionary vs ML-Guided Search"
)

plt.legend()
plt.show()