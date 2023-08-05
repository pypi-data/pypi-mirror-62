"""
    Copyright 2019 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import logging
import os
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional, TypeVar

import yaml

from inmanta.config import feature_file_config
from inmanta.util import get_compiler_version

if TYPE_CHECKING:
    from inmanta.server.protocol import ServerSlice


LOGGER = logging.getLogger(__name__)


class InvalidSliceNameException(Exception):
    """ This exception is raised when the name of the slice is not valid. For example when the extension and the slice name
        do not match.
    """


class InvalidFeature(Exception):
    """ This exception is raised when a feature is defined in another slice than it reports or the feature is not defined
        at all.
    """


T = TypeVar("T")


class Feature(Generic[T]):
    """ A feature offered by a slice """

    def __init__(self, slice: str, name: str, description: str = "", default_value: Optional[T] = None) -> None:
        self._name: str = name
        self._slice: str = slice
        self._description = description
        self._default_value: Optional[T] = default_value

    @property
    def name(self) -> str:
        return self._name

    @property
    def slice(self) -> str:
        return self._slice

    @property
    def default_value(self) -> T:
        return self._default_value

    def __str__(self) -> str:
        return f"{self._slice}:{self._name}"


class BoolFeature(Feature[bool]):
    """ A feature that is on or off. When no value is given it is enabled.
    """

    def __init__(self, slice: str, name: str, description: str = "") -> None:
        super().__init__(slice, name, description, True)


class StringListFeature(Feature[List[str]]):
    """ A feature that holds a list of allowed values. When the list contains "*" it matches everything.
    """

    def __init__(self, slice: str, name: str, description: str = "") -> None:
        super().__init__(slice, name, description, default_value=["*"])


class FeatureManager:
    """ This class allows to verify whether a feature should be enabled or not. This is determined based on a configuration
        file that is set with config.feature-file in the config. This feature file is a yaml with the following structure:

        .. code-block:: yaml

            slices:
                slice_name:
                    feature_name: bool

    """

    def __init__(self) -> None:
        self._features: Dict[str, Dict[str, Feature]] = defaultdict(lambda: {})
        self._feature_config: Dict[str, Dict[str, Any]] = self._load_feature_config()

    def get_features(self) -> List[Feature]:
        return [feature for slice in self._features.values() for feature in slice.values()]

    def _load_feature_config(self) -> Dict[str, Dict[str, Any]]:
        feature_file = feature_file_config.get()
        if feature_file is None:
            return {}

        if not os.path.exists(feature_file):
            LOGGER.warning("Feature file %s configured but file does not exist.", feature_file)
            return {}

        with open(feature_file, encoding="utf-8") as fd:
            result = yaml.safe_load(fd)

        if "slices" in result:
            return result["slices"]
        return {}

    def get_product_metadata(self) -> Dict[str, str]:
        return {
            "product": "Inmanta Service Orchestator",
            "edition": "Open Source Edition",
            "license": "Apache Software License 2",
            "version": get_compiler_version(),
        }

    def add_slice(self, slice: "ServerSlice") -> None:
        for feature in slice.define_features():
            if feature.slice != slice.name:
                raise InvalidFeature(
                    f"Feature {feature.name} defines slice {feature.slice} but is defined by slice {slice.name}"
                )

            self._features[feature.slice][feature.name] = feature
        slice.feature_manager = self

    def get_value(self, feature: Feature[T]) -> T:
        """ Get the value of a feature
        """
        if feature.slice not in self._features or feature.name not in self._features[feature.slice]:
            raise InvalidFeature("Feature should be defined be slices at boot time.")

        if feature.slice not in self._feature_config or feature.name not in self._feature_config[feature.slice]:
            return feature.default_value
        return self._feature_config[feature.slice][feature.name]

    def enabled(self, feature: BoolFeature) -> bool:
        value = self.get_value(feature)
        return value

    def contains(self, feature: StringListFeature, item: str) -> bool:
        """ Check if the value is contained in the list.
        """
        value = self.get_value(feature)
        if "*" in value:
            return True
        return item in value

    def stop(self):
        """ Called when the server is stopped
        """


class ApplicationContext:
    def __init__(self) -> None:
        self._slices: List[ServerSlice] = []
        self._feature_manager: Optional[FeatureManager] = None

    def register_slice(self, slice: "ServerSlice") -> None:
        assert slice is not None
        self._slices.append(slice)

    def get_slices(self) -> "List[ServerSlice]":
        return self._slices

    def set_feature_manager(self, feature_manager: FeatureManager):
        assert self._feature_manager is None
        self._feature_manager = feature_manager

    def get_feature_manager(self) -> FeatureManager:
        if self._feature_manager is None:
            self._feature_manager = FeatureManager()
        return self._feature_manager
