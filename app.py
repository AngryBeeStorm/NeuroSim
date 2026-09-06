import streamlit as st
from experiments.crossover_search_reusable import run_evolution
import matplotlib.pyplot as plt
from neurosim.presets import PRESETS

def parse_spike_times(text):
    return [
        int(value.strip())
        for value in text.split(",")
        if value.strip()
    ]

def draw_target_timeline(spikes, stimulation_length=500):

    fig, ax = plt.subplots(figsize=(10, 2))

    ax.set_xlim(0, stimulation_length)
    ax.set_ylim(0, 1)

    ax.axhline(
        0.5,
        linewidth=1
    )

    for spike in spikes:
        ax.vlines(
            spike,
            0.25,
            0.75,
            linewidth=3
        )

    ax.set_xlabel("Time (ms)")
    ax.set_yticks([])

    ax.set_title("Desired Neural Response")

    return fig


def apply_preset():
    preset_name = st.session_state.preset_name

    if preset_name == "Custom":
        return

    preset = PRESETS[preset_name]

    st.session_state.target_spikes = preset["spikes"].copy()
    st.session_state.num_spikes = len(preset["spikes"])

    for i, spike in enumerate(preset["spikes"]):
        st.session_state[f"spike_slider_{i}"] = spike




if "target_spikes" not in st.session_state:
    st.session_state.target_spikes = [100, 200, 400]

if "num_spikes" not in st.session_state:
    st.session_state.num_spikes = 3

if "stimulation_length" not in st.session_state:
    st.session_state.stimulation_length = 500





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

    result = run_evolution(
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



    fig, axes = plt.subplots(
        3,
        1,
        figsize=(12, 7),
        sharex=True,
        facecolor="#111827"
    )

    fig.subplots_adjust(hspace=0.22, top=0.84, bottom=0.11, left=0.1, right=0.98)
    panel_color = "#182235"
    text_color = "#e5edf7"
    muted_color = "#8fa3bb"
    colors = {
        "target": "#55d6be",
        "stimulation": "#ffbd59",
        "response": "#ff6b9d",
    }

    ax_target = axes[0]
    ax_stim = axes[1]
    ax_response = axes[2]

    for axis in axes:
        axis.set_facecolor(panel_color)
        axis.tick_params(colors=muted_color, labelsize=9)
        axis.grid(
            axis="x",
            color="#52647d",
            alpha=0.25,
            linestyle="--",
            linewidth=0.7,
        )
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["left"].set_color("#40516a")
        axis.spines["bottom"].set_color("#40516a")
        axis.xaxis.label.set_color(text_color)
        axis.yaxis.label.set_color(text_color)


    ax_target.eventplot(
        target_spikes,
        lineoffsets=1,
        linelengths=0.8,
        linewidths=3.5,
        colors=colors["target"],
    )
    ax_target.set_ylabel("TARGET", fontweight="bold", color=colors["target"])
    ax_target.set_yticks([])


    ax_stim.step(
        range(len(result["stimulation"])),
        result["stimulation"],
        where="post",
        linewidth=3,
        color=colors["stimulation"],
    )
    ax_stim.fill_between(
        range(len(result["stimulation"])),
        result["stimulation"],
        step="post",
        color=colors["stimulation"],
        alpha=0.1,
    )
    ax_stim.set_ylabel("INPUT", fontweight="bold", color=colors["stimulation"])


    ax_response.eventplot(
        result["spikes"],
        lineoffsets=1,
        linelengths=0.8,
        linewidths=3.5,
        colors=colors["response"],
    )
    ax_response.set_ylabel("ACTUAL", fontweight="bold", color=colors["response"])
    ax_response.set_yticks([])
    ax_response.set_xlabel("Time (ms)")

    fig.suptitle(
        f"Best Stimulation  |  Fitness: {result['score']:.3f}  |  Generation: {result['generation']}",
        color=text_color,
        fontsize=16,
        fontweight="bold",
        x=0.1,
        ha="left",
    )

    st.pyplot(fig)



