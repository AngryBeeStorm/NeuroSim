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


def repair_candidate(
    candidate,
    stimulation_length,
    min_gap=2
):
    repaired = copy.deepcopy(candidate)

    # Sort by pulse start time
    repaired.sort(key=lambda pulse: pulse[0])

    for i in range(len(repaired)):
        start, duration, amplitude = repaired[i]

        # Clamp normal bounds first
        duration = max(1, min(duration, 15))
        amplitude = max(0, min(amplitude, 100))

        if i == 0:
            start = max(
                0,
                min(start, stimulation_length - duration)
            )

        else:
            previous_start = repaired[i - 1][0]
            previous_duration = repaired[i - 1][1]

            earliest_start = (previous_start + previous_duration + min_gap)
            start = max(start, earliest_start)

            start = min(start, stimulation_length - duration)

        repaired[i] = [start, duration, amplitude]

    return repaired



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
    repaired_child = repair_candidate(child, stimulation_length=stimulation_length, min_gap=2)

    return repaired_child


def crossover(parent_a, parent_b, stimulation_length = 500):
    child = []

    for pulse_a, pulse_b in zip(parent_a, parent_b):
        if random.random() < 0.5:
            child.append(copy.deepcopy(pulse_a))
        else:
            child.append(copy.deepcopy(pulse_b))

    child.sort(key=lambda pulse: pulse[0])
    repaired_child = repair_candidate(child, stimulation_length=stimulation_length, min_gap=2)
    return repaired_child


def generate_offspring(elites, count, stimulation_length):
    offspring = []

    while len(offspring) < count:
        parent_a = random.choice(elites)
        parent_b = random.choice(elites)

        child = crossover(parent_a, parent_b, stimulation_length)
        child = mutate(
            child,
            stimulation_length=stimulation_length
        )

        offspring.append(child)

    return offspring