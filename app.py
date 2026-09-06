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

navigation = st.navigation([
    simulator,
    benchmarks
])

navigation.run()