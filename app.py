import streamlit as st
from experiments.crossover_search_reusable import run_evolution

def parse_spike_times(text):
    return [
        int(value.strip())
        for value in text.split(",")
        if value.strip()
    ]






st.title("NeuroSim")
st.write("AI-assisted neural simulation sandbox")

target_text = st.text_input(
    "Target spike times (ms)",
    value="100, 200, 400, 430"
)

population_size = st.slider(
    "Population size",
    min_value=10,
    max_value=200,
    value=50,
    step=10
)

generations = st.slider(
    "Generations",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

if st.button("Find stimulation"):
    target_spikes = parse_spike_times(target_text)
    st.write("Parsed target:", target_spikes)

    result = run_evolution(
        target_spikes=target_spikes,
        num_pulses = len(target_spikes),
        population_size=population_size,
        generations=generations)

    st.write(
        f"Best fitness: {result['score']:.3f}"
    )

    st.write(
        f"Found at generation: "
        f"{result['generation']}"
    )

    st.write(
        "Actual spikes:",
        result["spikes"]
    )



