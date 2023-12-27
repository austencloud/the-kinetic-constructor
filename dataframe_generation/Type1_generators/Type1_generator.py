from typing import List
import pandas as pd
from ABC_generator import ABC_Generator
from DEF_generator import DEF_Generator
from GHI_generator import GHI_Generator
from JKL_generator import JKL_Generator
from MNO_generator import MNO_Generator
from PQR_generator import PQR_Generator
from STUV_generator import STUV_Generator
from df_generator import DataFrameGenerator
from data.Enums import Location, PropRotDir, SpecificPosition
from data.constants import *
from data.positions_map import positions_map


class Type1_DataFrame_Generator_Manager:
    def __init__(self) -> None:
        super().__init__(letters=[])  # Initialize with an empty list
        self.type_name = "Type_1"
        self.generators = []
        self.ABC_Generator = ABC_Generator()
        self.DEF_Generator = DEF_Generator()
        self.GHI_Generator = GHI_Generator()
        self.JKL_Generator = JKL_Generator()
        self.MNO_Generator = MNO_Generator()
        self.PQR_Generator = PQR_Generator()
        self.STUV_Generator = STUV_Generator()

    def generate_Type1_dataframes(self) -> None:
        self.ABC_Generator.create_dataframes_for_ABC()
        self.DEF_Generator.create_dataframes_for_DEF()
        self.GHI_Generator.create_dataframes_for_GHI()
        self.JKL_Generator.create_dataframes_for_JKL()
        self.MNO_Generator.create_dataframes_for_MNO()
        self.PQR_Generator.create_dataframes_for_PQR()
        self.STUV_Generator.create_dataframes_for_STUV()

manager = Type1_DataFrame_Generator_Manager()
manager.generate_Type1_dataframes()