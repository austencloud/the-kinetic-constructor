from typing import Dict, List, Literal

ArrowAttributes = Dict[str, str | int]
StartEndPositions = Dict[str, str]
OptimalLocations = Dict[str, Dict[str, float]]
Variant = ArrowAttributes | StartEndPositions | OptimalLocations
Variants = List[List[Variant]]
LetterVariants = Dict[str, Variants]
LettersDict = Dict[str, Variants]
Direction = Literal["right", "left", "down", "up"]
