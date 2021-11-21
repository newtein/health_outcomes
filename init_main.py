from get_and_plot_wrapper import WrapperClass
from config import CONFIG
from plot_interval_plot import RegionWisePlot
from plot_three_years_together import RegionWisePlotThreeYears


class MainClass:
    def __init__(self):
        self.years = CONFIG.get("analysis_years")
        self.disease = CONFIG.get("disease")

    def execute(self):
        for year in self.years:
            print("Begin {}".format(year))
            obj = WrapperClass(year, self.disease, pop_type='ADULT')
            obj.calculate_prevalence_and_incidence_cases()
            obj = WrapperClass(year, self.disease, pop_type='CHILD')
            obj.calculate_prevalence_and_incidence_cases()
            print("Completed {}".format(year))

        # for year in self.years:
        #     obj1 = RegionWisePlot(self.disease, year, 'ADULT')
        #     obj1.plot(what='prevalence')
        #     obj1 = RegionWisePlot(self.disease, year, 'ADULT')
        #     obj1.plot(what='incidence')
        #
        #     obj2 = RegionWisePlot(self.disease, year, 'CHILD')
        #     obj2.plot(what='prevalence')
        #     obj2 = RegionWisePlot(self.disease, year, 'CHILD')
        #     obj2.plot(what='incidence')
        obj = RegionWisePlotThreeYears('ASTHMA', ['2016', '2017', '2018'], 'ADULT')
        obj.plot(what='prevalence')
        obj = RegionWisePlotThreeYears('ASTHMA', ['2016', '2017', '2018'], 'ADULT')
        obj.plot(what='incidence')

        obj = RegionWisePlotThreeYears('ASTHMA', ['2016', '2017', '2018'], 'CHILD')
        obj.plot(what='prevalence')
        obj = RegionWisePlotThreeYears('ASTHMA', ['2016', '2017', '2018'], 'CHILD')
        obj.plot(what='incidence')


if __name__ == "__main__":
    obj = MainClass()
    obj.execute()