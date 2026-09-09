from sklearn.ensemble import RandomForestRegressor


def flatten_candidate(candidate):
    return [
        value
        for pulse in candidate
        for value in pulse
    ]

def train_surrogate(X, y, seed=42):
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=seed,
    )

    model.fit(X, y)

    return model