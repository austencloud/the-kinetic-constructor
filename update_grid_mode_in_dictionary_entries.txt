import os
import json
from PIL import Image, PngImagePlugin
from typing import Optional, Dict, Any
from utilities.path_helpers import get_images_and_data_path


# Assuming GridModeChecker is in the same module or properly imported
class GridModeChecker:
    """Checks what grid a given pictograph is in by looking at its start and end positions"""

    def get_grid_mode(self, pictograph_dict) -> Optional[str]:
        box_mode_positions = self.get_box_mode_positions()
        diamond_mode_positions = self.get_diamond_mode_positions()

        start_pos = pictograph_dict.get("start_pos")
        end_pos = pictograph_dict.get("end_pos")

        if start_pos in box_mode_positions and end_pos in box_mode_positions:
            return "box"
        elif start_pos in diamond_mode_positions and end_pos in diamond_mode_positions:
            return "diamond"
        elif (
            start_pos in box_mode_positions and end_pos in diamond_mode_positions
        ) or (start_pos in diamond_mode_positions and end_pos in box_mode_positions):
            return "skewed"
        else:
            return None  # If positions don't match any known grid modes

    def get_diamond_mode_positions(self):
        return [
            "alpha1",
            "alpha3",
            "alpha5",
            "alpha7",
            "beta1",
            "beta3",
            "beta5",
            "beta7",
            "gamma1",
            "gamma3",
            "gamma5",
            "gamma7",
            "gamma9",
            "gamma11",
            "gamma13",
            "gamma15",
        ]

    def get_box_mode_positions(self):
        return [
            "alpha2",
            "alpha4",
            "alpha6",
            "alpha8",
            "beta2",
            "beta4",
            "beta6",
            "beta8",
            "gamma2",
            "gamma4",
            "gamma6",
            "gamma8",
            "gamma10",
            "gamma12",
            "gamma14",
            "gamma16",
        ]


def update_metadata_grid_mode(
    metadata: dict[str, Any], grid_mode_checker: GridModeChecker
) -> dict[str, Any]:
    # Check if 'grid_mode' is already present in the first item of 'sequence'
    if "sequence" in metadata and len(metadata["sequence"]) > 0:
        sequence_metadata = metadata["sequence"][0]
        if "grid_mode" not in sequence_metadata:
            # Try to determine the grid mode from the first pictograph in the sequence
            if len(metadata["sequence"]) > 1:
                first_pictograph = metadata["sequence"][2]
                grid_mode = grid_mode_checker.get_grid_mode(first_pictograph)
                if grid_mode:
                    sequence_metadata["grid_mode"] = grid_mode
                    print(
                        f"Set grid_mode to '{grid_mode}' in sequence '{sequence_metadata.get('word', 'Unknown')}'"
                    )
                else:
                    print(
                        f"Could not determine grid_mode for sequence '{sequence_metadata.get('word', 'Unknown')}'"
                    )
            else:
                print("No pictographs in sequence to determine grid_mode.")
    return metadata


def update_all_metadata():
    dictionary_dir = get_images_and_data_path("dictionary")
    grid_mode_checker = GridModeChecker()

    for root, dirs, files in os.walk(dictionary_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):  # Consider image files
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                try:
                    with Image.open(file_path) as img:
                        metadata = img.info.get("metadata")
                        if metadata:
                            metadata_dict = json.loads(metadata)
                            # Update the metadata with grid_mode if missing
                            updated_metadata = update_metadata_grid_mode(
                                metadata_dict, grid_mode_checker
                            )
                            # Save the image with updated metadata
                            pnginfo = PngImagePlugin.PngInfo()
                            pnginfo.add_text("metadata", json.dumps(updated_metadata))
                            img.save(file_path, pnginfo=pnginfo)
                            print(f"Updated metadata for {file_path}")
                        else:
                            print(f"No metadata found in {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    update_all_metadata()
