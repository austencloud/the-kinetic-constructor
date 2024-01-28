from typing import Union


class MirroredTupleHandler:
    """Handles mirroring of turns tuples."""

    @staticmethod
    def mirror_turns_tuple(turns_tuple: str) -> Union[str, None]:
        x, y = turns_tuple.strip("()").split(", ")
        if x != y:
            return f"({y}, {x})"
        return None
