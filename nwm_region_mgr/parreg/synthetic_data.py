"""Function to create synthetic data for training Unsupervised Random Forest (URF) models."""

import numpy


def create_synthetic_data(x, synthetic_data_type):
    """Create synthetic data for RR dissimilarity.

    :param X:
    :param kwargs:
    :return:
    """
    nof_objects = x.shape[0]
    if synthetic_data_type is None:
        synthetic_data_type = "default"
    if synthetic_data_type == "default":
        synthetic_x = default_synthetic_data(x)
        x_total = numpy.concatenate([x, synthetic_x])

    elif synthetic_data_type == "f":
        synthetic_x = f_synthetic_data(x)
        x_total = numpy.concatenate([numpy.hstack(x), synthetic_x])
    else:
        print("Bad synthetic data type")
        return -1

    y_total = numpy.concatenate([numpy.zeros(nof_objects), numpy.ones(nof_objects)])
    return x_total, y_total


def f_synthetic_data(x_list):
    """Synthetic data with same marginal distribution for each feature."""
    x = numpy.hstack(x_list)
    synthetic_x = numpy.zeros(x.shape)

    nof_chunks = len(x_list)
    nof_objects = x.shape[0]

    chunks_inds = numpy.random.choice(
        numpy.arange(nof_objects), [nof_objects, nof_chunks]
    )

    for i in range(nof_objects):
        x = [x_list[c][chunks_inds[i, c]] for c in range(nof_chunks)]

        synthetic_x[i] = numpy.hstack(x)

    return synthetic_x


def default_synthetic_data(x):
    """Synthetic data with same marginal distribution for each feature."""
    synthetic_x = numpy.zeros(x.shape)

    nof_features = x.shape[1]
    nof_objects = x.shape[0]

    for f in range(nof_features):
        feature_values = x[:, f]
        synthetic_x[:, f] += numpy.random.choice(feature_values, nof_objects)
    return synthetic_x
