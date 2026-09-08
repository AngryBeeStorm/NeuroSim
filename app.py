import streamlit as st

simulator = st.Page(
    "pages/simulator.py",
    title="Neural Simulator",
    icon="🧠",
    default=True
)

benchmarks = st.Page(
    "pages/benchmark.py",
    title="Benchmark Lab",
    icon="📊"
)

about = st.Page(
    "pages/about.py",
    title="About NeuroSim",
    icon="ℹ️"
)

navigation = st.navigation([
    simulator,
    benchmarks,
    about
])

navigation.run()