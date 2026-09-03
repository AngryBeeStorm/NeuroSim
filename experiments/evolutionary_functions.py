import copy
import random

#stimulation_length = 500


def score_spikes(target_spikes, actual_spikes, tolerance=10):
    matches = 0
    matched_actual = set()
    targets = len(target_spikes)

    for target in target_spikes:
        for idx, actual in enumerate(actual_spikes):
            if idx in matched_actual:
                continue
            if abs(target - actual) <= tolerance:
                matches += 1
                matched_actual.add(idx)
                break

    precision = matches / len(actual_spikes) if actual_spikes else 0.0
    recall = matches / targets if targets > 0 else 0.0

    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0


def mutate(candidate, chance=0.5, stimulation_length=500):
    child = copy.deepcopy(candidate)

    for pulse in child:

        # mutate start time
        if random.random() < chance:
            pulse[0] += random.randint(-10, 10)

        # mutate duration
        if random.random() < chance:
            pulse[1] += random.randint(-3, 3)

        # mutate amplitude
        if random.random() < chance:
            pulse[2] += random.uniform(-15, 15)

        pulse[0] = max(0, min(pulse[0], stimulation_length - 1))
        pulse[1] = max(1, min(pulse[1], 15))
        pulse[2] = max(0, min(pulse[2], 100))

    child.sort(key=lambda pulse: pulse[0])

    return child


def crossover(parent_a, parent_b):
    child = []

    for pulse_a, pulse_b in zip(parent_a, parent_b):
        if random.random() < 0.5:
            child.append(copy.deepcopy(pulse_a))
        else:
            child.append(copy.deepcopy(pulse_b))

    child.sort(key=lambda pulse: pulse[0])

    return child
