from sklearn.preprocessing import StandardScaler


def normalise_by_tool(train_data, test_data):
    scaler = StandardScaler()
    if not isinstance(train_data[0], list):
        train_data = [[d] for d in train_data]
        test_data = [[d] for d in test_data]
        scaler.fit(train_data)
        normalised_train_data = scaler.transform(train_data)
        normalised_test_data = scaler.transform(test_data)

        normalised_train_data = [el[0] for el in normalised_train_data]
        normalised_test_data = [el[0] for el in normalised_test_data]
    else:
        scaler.fit(train_data)
        normalised_train_data = scaler.transform(train_data)
        normalised_test_data = scaler.transform(test_data)
    return normalised_train_data, normalised_test_data


def statistical_normalisation(features, mean_value=None, std_dev_value=None):
    if mean_value is None:
        mean_value = sum(features) / len(features)
    features = [feat - mean_value for feat in features]
    if std_dev_value is None:
        std_dev_value = ((1 / len(features)) * sum([feat ** 2 for feat in features])) ** 0.5
    normalised_features = [feat / std_dev_value for feat in features]
    return normalised_features, mean_value, std_dev_value
