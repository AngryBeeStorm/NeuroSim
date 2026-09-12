# NeuroSim

You choose the neural response. NeuroSim finds the stimulation.

NeuroSim is an interactive computational neuroscience sandbox that explores the inverse neural stimulation problem: given a desired neural spike pattern, what stimulation could produce it?

It combines neuron simulation, evolutionary optimization, and machine learning to search for stimulation patterns that reproduce a user-defined neural response.

## Features

- Interactive target spike painter
- Leaky Integrate-and-Fire (LIF) neuron model
- Izhikevich neuron model with multiple firing behaviors
- Evolutionary stimulation search
- ML-guided search using a Random Forest surrogate
- Configurable neural noise
- Visualization of stimulation, spikes, and optimization progress

## Run locally

Clone the repository and install the dependencies:
pip install -r requirements.txt

then sun the sreamlit app with:
python -m streamlit run app.py    