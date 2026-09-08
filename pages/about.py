import streamlit as st
from neurosim.izhikevich import IzhikevichNeuron
from neurosim.presets import IZHIKEVICH_PRESETS
import matplotlib.pyplot as plt


def plot_voltage(voltages, spikes, preset_name):
    time = range(len(voltages))
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(time, voltages, label="Membrane voltage")

    for spike_time in spikes:
        ax.axvline(
            spike_time,
            linestyle="--",
            alpha=0.4
        )

    ax.axhline(
        30,
        linestyle=":",
        label="Spike threshold"
    )

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane voltage (mV)")
    ax.set_title(f"Izhikevich Neuron: {preset_name}")
    ax.legend()

    fig.tight_layout()
    return fig




st.title("About NeuroSim")
st.write("NeuroSim is a tool for simulating neural activity and optimizing stimulation protocols.")

st.write("Here is a visualization of the Izhikevich neuron model under constant input:")

subtype = st.selectbox(
        "Izhikevich subtype",
        [
            "Regular spiking",
            "Intrinsically bursting",
            "Fast spiking",
            "Chattering"
        ]
    )
neuron_params = IZHIKEVICH_PRESETS[subtype]

neuron = IzhikevichNeuron(**neuron_params)

simulation_length = 500
current = 10

if st.button("Run Simulation"):
    voltages = []
    spikes = []

    for time in range(simulation_length):
        spike, display_voltage = neuron.step(current)
        voltages.append(display_voltage)

        if spike:
            spikes.append(time)

    fig = plot_voltage(voltages, spikes, subtype)
    st.pyplot(fig)
