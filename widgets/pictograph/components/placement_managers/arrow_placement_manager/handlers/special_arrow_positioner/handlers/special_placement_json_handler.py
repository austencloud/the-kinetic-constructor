import json
import logging
import os
import re


class SpecialPlacementJsonHandler:
    """Handles read/write JSON file operations."""

    @staticmethod
    def load_json_data(file_path) -> dict:
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            return {}
        except Exception as e:
            logging.error(f"Error loading JSON data from {file_path}: {e}")
            return {}

    @staticmethod
    def write_json_data(data, file_path) -> None:
        """Write JSON data to a file with specific formatting."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)
            # logging.info(f"Data successfully written to {file_path}")
        except IOError as e:
            logging.error(f"Failed to write to {file_path}: {e}")
