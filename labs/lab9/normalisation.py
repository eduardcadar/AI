
def statistical_normalisation(features, mean_value=None, std_dev_value=None):
    if mean_value is None:
        mean_value = sum(features) / len(features)
    features = [feat - mean_value for feat in features]
    if std_dev_value is None:
        std_dev_value = ((1 / len(features)) * sum([feat ** 2 for feat in features])) ** 0.5
    normalised_features = [feat / std_dev_value for feat in features]
    return normalised_features, mean_value, std_dev_value
