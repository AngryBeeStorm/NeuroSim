from neurosim.factory import create_neuron
from neurosim.lif import LIFneuron
import random

from experiments.evolutionary_functions import score_spikes
from experiments.visualizer_functions import visualize_spike_times


times = []
voltages = []
stimulation_length = 500

target_spikes = []


def apply_noise(current, noise_std):
    if noise_std <= 0:
        return current

    return current + random.gauss(
        0.0,
        noise_std
    )


def add_pulse(stimulation, start_time, end_time, amplitude):
    for t in range(start_time, end_time):
        stimulation[t] = amplitude


def random_candidate(simulation_length=500, num_pulses=3):
    candidate = []

    for _ in range(num_pulses):
        start = random.randint(0, simulation_length - 20)
        duration = random.randint(1, 15)
        amplitude = random.uniform(0, 100)

        end = min(start + duration, simulation_length)

        candidate.append([start, duration, amplitude])

    candidate.sort(key=lambda pulse: pulse[0])

    return candidate


def candidate_to_stimulation(
    candidate,
    simulation_length=500
):
    stimulation = [0.0] * simulation_length

    for start, duration, amplitude in candidate:
        end = min(start + duration, simulation_length)

        for t in range(start, end):
            stimulation[t] = amplitude

    return stimulation


def run_simulation(stimulation, visual=False, print_spike_stats=False, neuron_model="LIF", neuron_params=None, noise_std=0.0,):
    if neuron_params is None:
        neuron_params = {}

    neuron = create_neuron(
        model_name=neuron_model,
        **neuron_params
    )

    spike_times = []

    for t in range(stimulation_length):

        

        noisy_current = apply_noise(stimulation[t], noise_std)
        spiked, voltage = neuron.step(current = noisy_current)

        times.append(t)

        if spiked:
            spike_times.append(t)
            if neuron_model == "LIF":
                voltages.append(neuron.v_threshold)
        else:
            voltages.append(voltage)

    if print_spike_stats:
        print(f"Total spikes: {len(spike_times)}")
        print(f"Spike times: {spike_times}")


    if visual:
        visualize_spike_times(spike_times, target_spikes, neuron, stimulation)

    return spike_times


def stimulation_cost(stimulation, max_amplitude=100.0):
    if not stimulation:
        return 0.0

    total = sum(abs(value) for value in stimulation)
    maximum_possible = len(stimulation) * max_amplitude

    return total / maximum_possible



def evaluate_candidate(candidate, target_spikes, stimulation_penalty=0.01, neuron_model="LIF", neuron_params=None, noise_std = 0.0):
    stimulation = candidate_to_stimulation(candidate, simulation_length=stimulation_length)
    actual_spikes = run_simulation(stimulation, neuron_model=neuron_model, neuron_params=neuron_params, noise_std=noise_std)
    fitness = score_spikes(target_spikes, actual_spikes)
    cost = stimulation_cost(stimulation)
    fitness -= stimulation_penalty * cost
    fitness = max(0.0, fitness)
    return fitness, actual_spikes