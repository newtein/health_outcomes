from read_county_population import ReadCountyCensus
from read_lur_no2 import ReadLUR
import pandas as pd

class MergeExAndPop:
    def __init__(self):
        self.lur_df = ReadLUR().get_df()
        self.pop_df = ReadCountyCensus().get_df()

    def get_df(self):
        pass