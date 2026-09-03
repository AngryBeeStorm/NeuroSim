import streamlit as st

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
    value="100, 200, 400"
)

if st.button("Find stimulation"):
    st.write("searching...")

target_spikes = parse_spike_times(target_text)

st.write("Parsed target:", target_spikes)