import numpy as np

from modules.losses.cross_entropy_loss import CrossEntropyLoss

_TOLERANCE = 0.001


def test_cross_entropy_loss():
    targets = np.array(
        [
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
        ], dtype=np.float32,
    )
    logits = np.array(
        [
            [10, 2, -1], [-1, 10, 2], [2, -1, 10],
        ], dtype=np.float32,
    )
    # Because our logits are such that the correct class has the highest logit,
    # so softmax will be [1, 0, 0], [0, 1, 0], [0, 0, 1] respectively.
    expected_loss = 0.00035208222

    loss = CrossEntropyLoss()
    computed_loss = loss(targets, logits)

    assert np.isclose(computed_loss, expected_loss, rtol=_TOLERANCE)


def test_cross_entropy_loss_numerical_stability():
    targets = np.array(
        [
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
        ], dtype=np.float32,
    )
    logits = np.array(
        [
            [2000, 2000, 2000], [2000, 2000, 2000], [2000, 2000, 2000],
        ], dtype=np.float32,
    )
    expected_loss = 1.0986123

    loss = CrossEntropyLoss()
    computed_loss = loss(targets, logits)

    assert np.isclose(computed_loss, expected_loss, rtol=_TOLERANCE)


def test_cross_entropy_loss_gradient():
    targets = np.array(
        [
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
        ], dtype=np.float32,
    )
    logits = np.array(
        [
            [2, 2, -1], [-1, 2, 2], [2, -1, 2],
        ], dtype=np.float32,
    )
    expected_gradient = np.array(
        [
            [-0.17071481, 0.16261852, 0.0080963],
            [0.0080963, -0.17071481, 0.16261852],
            [0.16261852, 0.0080963, -0.17071481],
        ], dtype=np.float32,
    )

    loss = CrossEntropyLoss()
    computed_gradient = loss.compute_backward_gradient(targets, logits)

    assert np.allclose(computed_gradient, expected_gradient, rtol=_TOLERANCE)
