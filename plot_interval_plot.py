import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime
from copy import copy
from constants import *
import logging
import pandas as pd
import numpy as np
import seaborn as sns
import math
from scipy import stats


class RegionWisePlot:
    def __init__(self, disease, year, pop_type):
        self.year = year
        self.disease = disease
        self.pop_type = pop_type
        self.fname = self.get_fname()
        df = pd.read_csv(self.fname)
        df = df[df['CHILD'] == 1]
        self.df = df[~df['STATE'].isin(EXCLUDE_STATES)]
        self.df_carb = df[df['STATE'].isin(CARB)]
        self.df_noncarb = df[~df['STATE'].isin(CARB)]

    def get_fname(self):
        return "{}/{}.csv".format(OUTPUT_FILE, "{}_{}_{}".format(self.disease, self.year, self.pop_type))

    def get_rows_and_cols_for_counties(self):
        cols = 3
        rows = 2
        return rows, cols

    def get_annot(self, int):
        return "{})".format(chr(97 + int))

    def get_numbers(self, df, of='prevalence'):
        if of == "prevalence":
            a, b, c = df[
                ['prevalence_cases', 'prevalence_cases_high', 'prevalence_cases_low']].sum().tolist()
        else:
            a, b, c = df[
                ['incidence_cases', 'incidence_cases_high', 'incidence_cases_low']].sum().tolist()
        pop = df['POPEST{}_CIV'.format(self.year)].sum()
        return a, b, c, pop

    def get_super_title(self, ofwhat):
        s = "{} {} Rate in {} ({})"
        d = self.disease.lower().capitalize()
        ofw = ofwhat.capitalize()
        pop_type = "Adults" if self.pop_type=="ADULT" else "Children"
        s = s.format(d, ofw, pop_type, self.year)
        return s

    def plot(self, what='prevalence'):
        sns.set_style("white")
        rows, cols = self.get_rows_and_cols_for_counties()
        posCord = [(i, j) for i in range(0, rows) for j in range(0, cols)]
        plt.close()
        plt.figure(figsize=(13, 8), dpi=600)
        gs = gridspec.GridSpec(rows, cols)
        carb_regions = self.df_carb['EPA Region'].unique().tolist()
        noncarb_regions = self.df_noncarb['EPA Region'].unique().tolist()
        flag = 0
        for index, epa_region in enumerate([0,1,2,3,4,5,6,7,8,9,10]):
            ax = plt.subplot(gs[posCord[flag][0], posCord[flag][1]])
            ax.text(-0.07, 1, self.get_annot(flag), transform=ax.transAxes, size=15, color='black')
            if epa_region == 0 or (epa_region in carb_regions and epa_region in noncarb_regions):
                if epa_region == 0:
                    prevalence_carb, b_carb, c_carb, pop_carb = self.get_numbers(self.df_carb, of=what)
                    prevalence_noncarb, b_noncarb, c_noncarb, pop_noncarb = self.get_numbers(self.df_noncarb, of=what)
                    plt.title("US")
                else:
                    temp_carb = self.df_carb[self.df_carb['EPA Region'] == epa_region]
                    temp_noncarb = self.df_noncarb[self.df_noncarb['EPA Region'] == epa_region]
                    prevalence_carb, b_carb, c_carb, pop_carb = self.get_numbers(temp_carb, of=what)
                    prevalence_noncarb, b_noncarb, c_noncarb, pop_noncarb = self.get_numbers(temp_noncarb, of=what)
                    plt.title("EPA Region {}".format(epa_region))

                #plt.xlim(0, None)
                x_pos = [2, 4]
                plt.bar(x_pos, [prevalence_carb, prevalence_noncarb])
                plt.errorbar(x_pos[0], prevalence_carb, yerr=prevalence_carb - c_carb, color='r')
                plt.errorbar(x_pos[1], prevalence_noncarb, yerr=prevalence_noncarb - c_noncarb, color='r')
                plt.ylabel("Number of cases")
                plt.xticks(x_pos, ['CARB States', 'Non-CARB States'])
                carb_per = "{:.2f}%".format((prevalence_carb*100)/pop_carb)
                noncarb_per = "{:.2f}%".format((prevalence_noncarb*100)/pop_noncarb)
                ax.text(x_pos[0]-0.25, prevalence_carb/3, carb_per, size=12, color='w')
                ax.text(x_pos[1]-0.25, prevalence_noncarb/3, noncarb_per, size=12, color='w')
                # plt.bar([2, 6, 10, 14], [prevalence_carb, incidence_carb, prevalence_noncarb, incidence_noncarb])
                # plt.errorbar(2, prevalence_carb, yerr=prevalence_carb - c_carb)
                # plt.errorbar(6, incidence_carb, yerr=incidence_carb - z_carb)
                # plt.errorbar(10, prevalence_noncarb, yerr=prevalence_noncarb - c_noncarb)
                # plt.errorbar(14, incidence_noncarb, yerr=incidence_noncarb - z_noncarb)
                flag += 1
        plt.tight_layout()
        super_title = self.get_super_title(ofwhat=what)
        plt.suptitle(super_title, fontsize=22, y=1.05)
        fname = "{}/{}.png".format(OUTPUT_IMAGE, super_title.replace(" ", "_"))
        plt.savefig(fname, bbox_inches='tight')
        print("Written Image: {}".format(fname))


if __name__ == "__main__":
    obj = RegionWisePlot('ASTHMA', '2017', 'ADULT')
    obj.plot(what='prevalence')

    obj = RegionWisePlot('ASTHMA', '2017', 'ADULT')
    obj.plot(what='incidence')

    obj = RegionWisePlot('ASTHMA', '2017', 'CHILD')
    obj.plot( what='prevalence')

    obj = RegionWisePlot('ASTHMA', '2017', 'CHILD')
    obj.plot( what='incidence')


