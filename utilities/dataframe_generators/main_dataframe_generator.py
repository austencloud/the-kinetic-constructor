from Type1_generator import Type1Generator
from Type2_generator import Type2Generator
from Type3_generator import Type3Generator
from Type4_generator import Type4Generator
from Type5_generator import Type5Generator
from Type6_generator import Type6Generator
import pandas as pd


class MainDataFrameGenerator:
    def __init__(self) -> None:
        self.init_generators()
        self.master_dataframe = pd.DataFrame()

    def init_generators(self) -> None:
        self.Type1_generator = Type1Generator()
        self.Type2_generator = Type2Generator()
        self.Type3_generator = Type3Generator()
        self.Type4_generator = Type4Generator()
        self.Type5_generator = Type5Generator()
        self.Type6_generator = Type6Generator()

    def generate_all_dataframes(self) -> None:
        self.collect_dataframes(self.Type1_generator.create_Type1_dataframes())
        self.collect_dataframes(self.Type2_generator.create_Type2_dataframes())
        self.collect_dataframes(self.Type3_generator.create_Type3_dataframes())
        self.collect_dataframes(self.Type4_generator.create_Type4_dataframes())
        self.collect_dataframes(self.Type5_generator.create_Type5_dataframes())
        self.collect_dataframes(self.Type6_generator.create_Type6_dataframes())
        self.master_dataframe.to_csv("PictographDataFrame.csv", index=False)

    def collect_dataframes(self, dataframes) -> None:
        self.master_dataframe = pd.concat(
            [self.master_dataframe, pd.DataFrame(dataframes)], ignore_index=True
        )


generator = MainDataFrameGenerator()
generator.generate_all_dataframes()
