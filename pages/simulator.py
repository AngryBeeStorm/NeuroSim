import streamlit as st
from experiments.crossover_search_reusable import run_evolution_crossover
import matplotlib.pyplot as plt
from experiments.evolutionary_search import run_evolution_mutation
from experiments.random_search import run_evolution_random
from neurosim.presets import PRESETS, preset_spikes
from neurosim.plotting import plot_best_solution_result, draw_target_timeline

if "target_spikes" not in st.session_state:
    st.session_state.target_spikes = [100, 200, 400]

if "num_spikes" not in st.session_state:
    st.session_state.num_spikes = 3

if "stimulation_length" not in st.session_state:
    st.session_state.stimulation_length = 500




def parse_spike_times(text):
    return [
        int(value.strip())
        for value in text.split(",")
        if value.strip()
    ]




def apply_preset():
    preset_name = st.session_state.preset_name

    if preset_name == "Custom":
        return

    spikes = preset_spikes(
        preset_name,
        st.session_state.stimulation_length
    )

    st.session_state.target_spikes = spikes
    st.session_state.num_spikes = len(spikes)

    for i, spike in enumerate(spikes):
        st.session_state[f"spike_slider_{i}"] = spike








st.title("NeuroSim")
st.write("AI-assisted neural simulation sandbox")

col1, col2 = st.columns([4, 1])


preset_name = st.selectbox(
    "Target preset",
    ["Custom"] + list(PRESETS.keys()),
    key="preset_name",
    on_change=apply_preset
)

st.number_input(
    "Simulation length (ms)",
    min_value=100,
    max_value=5000,
    step=50,
    key="stimulation_length",
)


num_spikes = st.slider(
    "Number of target spikes",
    min_value=1,
    max_value=8,
    value=st.session_state.num_spikes
)

st.session_state.num_spikes = num_spikes

# Resize the spike list if needed
current = st.session_state.target_spikes

if len(current) < num_spikes:
    while len(current) < num_spikes:
        current.append(250)

elif len(current) > num_spikes:
    current = current[:num_spikes]

new_spikes = []

for i in range(num_spikes):

    value = st.slider(
        f"Spike {i + 1}",
        min_value=0,
        max_value=st.session_state.stimulation_length,
        value=current[i],
        key=f"spike_slider_{i}"
    )

    new_spikes.append(value)


new_spikes.sort()

st.session_state.target_spikes = new_spikes


with col1:
    st.subheader("Target Painter")

with col2:
    if st.button("Reset"):
        st.session_state.target_spikes = [100, 200, 400]
        st.session_state.num_spikes = 3
        st.rerun()

fig = draw_target_timeline(
    st.session_state.target_spikes,
    stimulation_length=st.session_state.stimulation_length
)
st.pyplot(fig)
st.caption(
    f"{len(st.session_state.target_spikes)} target spikes "
    f"across {st.session_state.stimulation_length} ms"
)
if preset_name != "Custom":
    st.info(
        f"Preset description: {PRESETS[preset_name]['description']}"
    )

st.divider()




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


st.divider()


if st.button("Find stimulation"):
    target_spikes = st.session_state.target_spikes
    st.write("Parsed target:", target_spikes)

    result = run_evolution_crossover(
        target_spikes=target_spikes,
        num_pulses = num_spikes,
        population_size=population_size,
        generations=generations,
        stimulation_length=st.session_state.stimulation_length
    )

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



    fig = plot_best_solution_result(target_spikes, result)

    st.pyplot(fig)



