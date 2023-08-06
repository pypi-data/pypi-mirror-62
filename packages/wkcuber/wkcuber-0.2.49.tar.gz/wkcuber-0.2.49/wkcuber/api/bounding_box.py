from typing import Tuple, Union, List, Dict, Generator, Optional
import json
import numpy as np
from wkcuber.mag import Mag

Shape3D = Union[List[int], Tuple[int, int, int], np.ndarray]


class BoundingBox:
    def __init__(self, topleft: Shape3D, size: Shape3D):

        self.topleft = np.array(topleft, dtype=np.int)
        self.size = np.array(size, dtype=np.int)

    @property
    def bottomright(self):

        return self.topleft + self.size

    @staticmethod
    def from_wkw(bbox: Dict):
        return BoundingBox(
            bbox["topLeft"], [bbox["width"], bbox["height"], bbox["depth"]]
        )

    @staticmethod
    def from_config(bbox: Dict):
        return BoundingBox(bbox["topleft"], bbox["size"])

    @staticmethod
    def from_tuple6(tuple6: Tuple):
        return BoundingBox(tuple6[0:3], tuple6[3:6])

    @staticmethod
    def from_tuple2(tuple2: Tuple):
        return BoundingBox(tuple2[0], tuple2[1])

    @staticmethod
    def from_auto(obj):
        if isinstance(obj, BoundingBox):
            return obj
        elif isinstance(obj, str):
            return BoundingBox.from_auto(json.loads(obj))
        elif isinstance(obj, dict):
            return BoundingBox.from_wkw(obj)
        elif isinstance(obj, list) or isinstance(obj, tuple):
            if len(obj) == 2:
                return BoundingBox.from_tuple2(obj)
            elif len(obj) == 6:
                return BoundingBox.from_tuple6(obj)

        raise Exception("Unknown bounding box format.")

    def as_tuple2_string(self):
        return str([self.topleft, self.size])

    def as_wkw(self):

        width, height, depth = self.size.tolist()

        return {
            "topLeft": self.topleft.tolist(),
            "width": width,
            "height": height,
            "depth": depth,
        }

    def as_config(self):

        return {"topleft": self.topleft.tolist(), "size": self.size.tolist()}

    def as_checkpoint_name(self):

        x, y, z = self.topleft
        width, height, depth = self.size
        return "{x}_{y}_{z}_{width}_{height}_{depth}".format(
            x=x, y=y, z=z, width=width, height=height, depth=depth
        )

    def __repr__(self):

        return "BoundingBox(topleft={}, size={})".format(
            str(tuple(self.topleft)), str(tuple(self.size))
        )

    def __str__(self):

        return self.__repr__()

    def __eq__(self, other):

        return np.array_equal(self.topleft, other.topleft) and np.array_equal(
            self.size, other.size
        )

    def padded_with_margins(
        self, margins_left: Shape3D, margins_right: Optional[Shape3D] = None
    ) -> "BoundingBox":

        if margins_right is None:
            margins_right = margins_left

        margins_left = np.array(margins_left)
        margins_right = np.array(margins_right)

        return BoundingBox(
            topleft=self.topleft - margins_left,
            size=self.size + (margins_left + margins_right),
        )

    def intersected_with(
        self, other: "BoundingBox", dont_assert=False
    ) -> "BoundingBox":
        """ If dont_assert is set to False, this method may return empty bounding boxes (size == (0, 0, 0)) """

        topleft = np.maximum(self.topleft, other.topleft)
        bottomright = np.minimum(self.bottomright, other.bottomright)
        size = np.maximum(bottomright - topleft, (0, 0, 0))

        intersection = BoundingBox(topleft, size)

        if not dont_assert:
            assert (
                not intersection.is_empty()
            ), "No intersection between bounding boxes {} and {}.".format(self, other)

        return intersection

    def extended_by(self, other: "BoundingBox"):

        topleft = np.minimum(self.topleft, other.topleft)
        bottomright = np.maximum(self.bottomright, other.bottomright)
        size = bottomright - topleft

        return BoundingBox(topleft, size)

    def is_empty(self) -> bool:

        return not all(self.size > 0)

    def in_mag(self, mag: Mag) -> "BoundingBox":

        np_mag = np.array(mag.to_array())

        return BoundingBox(
            topleft=(self.topleft / np_mag).astype(np.int),
            size=(self.size / np_mag).astype(np.int),
        )

    def contains(self, coord: Shape3D) -> bool:

        coord = np.array(coord)

        return np.all(coord >= self.topleft) and np.all(
            coord < self.topleft + self.size
        )

    def chunk(
        self, chunk_size: Shape3D, chunk_border_alignments: Optional[List[int]] = None
    ) -> Generator["BoundingBox", None, None]:
        """Decompose the bounding box into smaller chunks of size `chunk_size`.

    Chunks at the border of the bounding box might be smaller than chunk_size.
    If `chunk_border_alignment` is set, all border coordinates
    *between two chunks* will be divisible by that value.
    """

        start = self.topleft.copy()
        chunk_size = np.array(chunk_size)

        start_adjust = np.array([0, 0, 0])
        if chunk_border_alignments is not None:

            chunk_border_alignments = np.array(chunk_border_alignments)
            assert np.all(
                chunk_size % chunk_border_alignments == 0
            ), "{} not divisible by {}".format(chunk_size, chunk_border_alignments)

            # Move the start to be aligned correctly. This doesn't actually change
            # the start of the first chunk, because we'll intersect with `self`,
            # but it'll lead to all chunk borders being aligned correctly.
            start_adjust = start % chunk_border_alignments

        for x in range(
            start[0] - start_adjust[0], start[0] + self.size[0], chunk_size[0]
        ):
            for y in range(
                start[1] - start_adjust[1], start[1] + self.size[1], chunk_size[1]
            ):
                for z in range(
                    start[2] - start_adjust[2], start[2] + self.size[2], chunk_size[2]
                ):

                    yield BoundingBox([x, y, z], chunk_size).intersected_with(self)

    def volume(self) -> int:

        return self.size.prod()

    def slice_array(self, array: np.ndarray) -> np.ndarray:

        return array[
            self.topleft[0] : self.bottomright[0],
            self.topleft[1] : self.bottomright[1],
            self.topleft[2] : self.bottomright[2],
        ]

    def copy(self) -> "BoundingBox":

        return BoundingBox(self.topleft.copy(), self.bottomright.copy())

    def offset(self, vector: Tuple[int, int, int]) -> "BoundingBox":

        return BoundingBox(self.topleft + np.array(vector), self.size.copy())
