import streamlit as st

simulator = st.Page(
    "pages/simulator.py",
    title="Neural Simulator",
    icon="🧠",
    default=True
)


about = st.Page(
    "pages/about.py",
    title="About NeuroSim",
    icon="ℹ️"
)

navigation = st.navigation([
    simulator,
    about
])

navigation.run()