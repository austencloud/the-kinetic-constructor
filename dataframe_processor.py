import pandas as pd
from typing import Literal


class PictographDataFrameProcessor:
    def __init__(self):
        self.filepath = "PictographDataframe.csv"
        self.df = None

    def load_data(self):
        """Load the DataFrame from the specified CSV file."""
        self.df = pd.read_csv(self.filepath)

    def process_dataframe(self):
        """Process the DataFrame to update motion relationships and structure."""
        # Assign timing and direction based on letter and start position
        timing_direction = self.df.apply(
            lambda row: self.determine_timing_and_direction(
                row["letter"], row["start_pos"]
            ),
            axis=1,
        )
        self.df.insert(3, "timing", timing_direction.str[0])
        self.df.insert(4, "direction", timing_direction.str[1])

    def determine_timing_and_direction(
        self, letter: str, start_pos: str
    ) -> tuple[
        Literal["split", "tog", "quarter", "none"], Literal["same", "opp", "none"]
    ]:
        """Determine the timing and direction attributes based on the letter and start position."""
        if letter in ["A", "B", "C"]:
            return ("split", "same")
        elif letter in ["D", "E", "F"]:
            if start_pos in ["beta2", "beta4"]:
                return ("split", "opp")
            elif start_pos in ["beta1", "beta3"]:
                return ("tog", "opp")
        elif letter in ["G", "H", "I"]:
            return ("tog", "same")
        elif letter in ["J", "K", "L"]:
            if start_pos in ["alpha1", "alpha3"]:
                return ("split", "opp")
            elif start_pos in ["alpha2", "alpha4"]:
                return ("tog", "opp")
        elif letter in ["M", "N", "O", "P", "Q", "R"]:
            return ("quarter", "opp")
        elif letter in ["S", "T", "U", "V"]:
            return ("quarter", "same")
        else:
            return ("none", "none")

    def save_data(self, output_path):
        """Save the processed DataFrame to a new CSV file."""
        self.df.to_csv(output_path, index=False)

#run it
processor = PictographDataFrameProcessor()
processor.load_data()
processor.process_dataframe()
processor.save_data("PictographDataframe_processed.csv")
print("Data processing complete.")