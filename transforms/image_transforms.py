import sys
from abc import ABC, abstractmethod

import cv2
import numpy as np
from numpy import typing as npt

from utils.enums import TransformsType

_MAX_VALUE = 255

_ImageType = npt.NDArray[np.integer | np.floating]


class ImageTransform(ABC):
    """Base class for image transforms."""

    @abstractmethod
    def transform(self, image: _ImageType) -> _ImageType:
        """Transform image.

        Args:
            image: The input image to transform.

        Returns:
            _ImageType: Transformed image.
        """


class Normalize(ImageTransform):
    """Transform image by scaling each pixel to a range [a, b]."""

    def __init__(
        self, min_value: float | int = -1, max_value: float | int = 1,
    ) -> None:
        self._min_value = min_value
        self._max_value = max_value

    def transform(self, image: _ImageType) -> _ImageType:
        """Transform image by scaling each pixel to a range [a, b].

        Args:
            image: The input image to transform.

        Returns:
            _ImageType: The image in the range [a, b].
        """
        return self._min_value + (self._max_value - self._min_value) * image


class Standardize(ImageTransform):
    """Standardize image with mean and std."""

    def __init__(
        self, mean: float | list | tuple, std: float | list | tuple,
    ) -> None:
        self._mean = np.array(mean)
        self._std = np.array(std)

    def transform(self, image: _ImageType) -> _ImageType:
        """Transform image by standardizing it.

        Args:
            image: The input image to transform.

        Returns:
            _ImageType: The image in the range [0, 1].
        """
        return (image - self._mean) / self._std


class ToFloat(ImageTransform):
    """Convert image from uint to float and scale it to [0, 1]."""

    def __init__(self) -> None:
        """Initialize the transform."""

    def transform(self, image: _ImageType) -> _ImageType:
        """Transform image by converting it to float and scaling it to [0, 1].

        Args:
            image: The input image to transform.

        Returns:
            _ImageType: The image in the range [0, 1].
        """
        return image.astype(np.float64) / _MAX_VALUE


class Resize(ImageTransform):
    """Image resize."""

    def __init__(self, size: tuple[int, int]) -> None:
        self._size = size

    def transform(self, image: _ImageType) -> _ImageType:
        """Transform image by resizing it.

        Args:
            image: The input image to transform.

        Returns:
            _ImageType: The image in the range [0, 1].
        """
        return cv2.resize(image, self._size)  # type: ignore


class Sequential(ImageTransform):
    """Compose several transforms together."""

    def __init__(
        self, transform_list: list[tuple[TransformsType, dict]],
    ) -> None:
        self._transforms: list[ImageTransform] = [
            getattr(
                sys.modules[__name__],
                transform.name.title().replace('_', ''),
            )(**transform_kwargs)
            for transform, transform_kwargs in transform_list
        ]

    def transform(self, image: _ImageType) -> _ImageType:
        """Transform image by applying several transforms together.

        Args:
            image: The input image to transform.

        Returns:
            _ImageType: The image with all transforms applied.
        """
        transformed_image = image.copy()
        for transform in self._transforms:
            transformed_image = transform.transform(transformed_image)
        return transformed_image
