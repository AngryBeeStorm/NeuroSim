


def preset_spikes(name, simulation_length):
    positions = PRESETS[name]["positions"]

    return [
        int(position * simulation_length)
        for position in positions
    ]


PRESETS = {
    "Regular": {
        "positions": [0.2, 0.4, 0.6, 0.8],
        "description": "Evenly spaced firing."
    },

    "Burst": {
        "positions": [0.40, 0.42, 0.44],
        "description": "A short cluster of rapid spikes."
    },

    "Double burst": {
        "positions": [
            0.20, 0.22, 0.24,
            0.70, 0.72, 0.74
        ],
        "description": "Two distinct bursts."
    },

    "Sparse": {
        "positions": [0.2, 0.8],
        "description": "Widely separated activity."
    }
}