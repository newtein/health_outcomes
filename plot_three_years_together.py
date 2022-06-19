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
import matplotlib
import math
from matplotlib.lines import Line2D



class RegionWisePlotThreeYears:
    def __init__(self, disease, years, pop_type):
        self.years = years
        self.disease = disease
        self.pop_type = pop_type
        self.fnames = self.get_fnames()
        dfs = [pd.read_csv(fname) for fname in self.fnames]
        self.dfs_carb, self.dfs_noncarb = [], []
        self.cmap = plt.get_cmap("Paired")
        for index in range(len(dfs)):
            dfs[index] = dfs[index][~dfs[index]['STATE'].isin(EXCLUDE_STATES)]
            self.dfs_carb.append(dfs[index][dfs[index]['STATE'].isin(CARB)])
            self.dfs_noncarb.append(dfs[index][~dfs[index]['STATE'].isin(CARB)])

    def get_fnames(self):
        s = ["{}/{}.csv".format(OUTPUT_FILE, "{}_{}_{}".format(self.disease, year, self.pop_type)) for year in self.years]
        return s

    def get_rows_and_cols_for_counties(self):
        cols = 3
        rows = 4
        return rows, cols

    def get_annot(self, int):
        return "{})".format(chr(97 + int))

    def get_numbers(self, df, index, of='prevalence'):
        if of == "prevalence":
            a, b, c = df[
                ['prevalence_cases', 'prevalence_cases_high', 'prevalence_cases_low']].sum().tolist()
        else:
            a, b, c = df[
                ['trap_incidence_cases', 'trap_incidence_cases_high', 'trap_incidence_cases_low']].sum().tolist()
            # a, b, c = df[
            #     ['incidence_cases', 'incidence_cases_high', 'incidence_cases_low']].sum().tolist()
            # a, b, c = trap_a*100/a, trap_b*100/b, trap_c*100/c
        pop = df['POPEST{}_CIV'.format(self.years[index])].sum()
        return a, b, c, pop

    def get_numbers_from_dfs(self, dfs, of):
        a, b, c, pop = [], [], [], []
        for index, df in enumerate(dfs):
            ta, tb, tc, tpop = self.get_numbers(df, index, of=of)
            a.append(ta)
            b.append(tb)
            c.append(tc)
            pop.append(tpop)
        return a, b, c, pop

    def get_super_title(self, ofwhat):
        s = "Annual {} {} in {} ({}-{})"
        d = self.disease.lower()
        ofw = ofwhat
        if ofw != 'prevalence':
            ofw = ofw + " due to TRAP"
        pop_type = "Adults" if self.pop_type == "ADULT" else "Children"
        s = s.format(d, ofw, pop_type.lower(), min(self.years), max(self.years))
        return s

    def get_bar_annote(self, x):
        if len(str(x)) == 2:
            return 0.05
        return 0

    def plot(self, what='prevalence'):
        sns.set_style("ticks")
        rows, cols = self.get_rows_and_cols_for_counties()
        posCord = [(i, j) for i in range(0, rows) for j in range(0, cols)]
        plt.close()
        plt.figure(figsize=(11, 9), dpi=600)
        gs = gridspec.GridSpec(rows, cols)
        carb_regions = self.dfs_carb[0]['EPA Region'].unique().tolist()
        noncarb_regions = self.dfs_noncarb[0]['EPA Region'].unique().tolist()
        flag = 0
        file_headers = ["Region", ""]
        for index, epa_region in enumerate([0,1,2,3,4,5,6,7,8,9,10]):
            ax = plt.subplot(gs[posCord[flag][0], posCord[flag][1]])
            ax.text(-0.09, 1.05, self.get_annot(flag), transform=ax.transAxes, size=15, color='black')
            # if epa_region == 0 or (epa_region in carb_regions and epa_region in noncarb_regions):
            if epa_region == 0:
                prevalences_carb, bs_carb, cs_carb, pops_carb = self.get_numbers_from_dfs(self.dfs_carb, what)
                prevalences_noncarb, bs_noncarb, cs_noncarb, pops_noncarb = self.get_numbers_from_dfs(self.dfs_noncarb, what)
                plt.title("US")
                carb_labels = ['2016', '2017', '\n\nCARB States', '2018']
                noncarb_labels = ['2016', '2017', '\n\nNon-CARB States', '2018']
            elif epa_region in carb_regions and epa_region in noncarb_regions:
                n = range(len(self.dfs_carb))
                temps_carb = [self.dfs_carb[index][self.dfs_carb[index]['EPA Region'] == epa_region] for index in n]
                temps_noncarb = [self.dfs_noncarb[index][self.dfs_noncarb[index]['EPA Region'] == epa_region] for index in n]
                prevalences_carb, bs_carb, cs_carb, pops_carb = self.get_numbers_from_dfs(temps_carb, what)
                prevalences_noncarb, bs_noncarb, cs_noncarb, pops_noncarb = self.get_numbers_from_dfs(temps_noncarb, what)
                plt.title("EPA Region {}".format(epa_region))
                carb_labels = ['2016', '2017', '\n\nCARB States', '2018']
                noncarb_labels = ['2016', '2017', '\n\nNon-CARB States', '2018']
            elif epa_region in carb_regions and epa_region not in noncarb_regions:
                n = range(len(self.dfs_carb))
                nan_list = [np.nan for index in n]
                temps_carb = [self.dfs_carb[index][self.dfs_carb[index]['EPA Region'] == epa_region] for index in n]
                temps_noncarb = nan_list
                prevalences_carb, bs_carb, cs_carb, pops_carb = self.get_numbers_from_dfs(temps_carb, what)
                prevalences_noncarb, bs_noncarb, cs_noncarb, pops_noncarb = nan_list, nan_list, nan_list, nan_list
                plt.title("EPA Region {}".format(epa_region))
                carb_labels = ['2016', '2017', '\n\nCARB States', '2018']
                noncarb_labels = ['']*4
            elif epa_region not in carb_regions and epa_region in noncarb_regions:
                n = range(len(self.dfs_noncarb))
                nan_list = [np.nan for index in n]
                temps_carb = nan_list
                temps_noncarb = [self.dfs_noncarb[index][self.dfs_noncarb[index]['EPA Region'] == epa_region] for index
                                 in n]
                prevalences_carb, bs_carb, cs_carb, pops_carb = nan_list, nan_list, nan_list, nan_list
                prevalences_noncarb, bs_noncarb, cs_noncarb, pops_noncarb = self.get_numbers_from_dfs(temps_noncarb,
                                                                                                      what)
                plt.title("EPA Region {}".format(epa_region))
                carb_labels = ['']*4
                noncarb_labels = ['2016', '2017', '\n\nNon-CARB States', '2018']


                #plt.xlim(0, None)
            write_row = [epa_region, ]
            x_pos = [2, 4, 6, 9, 11, 13]
            plt.bar(x_pos, prevalences_carb + prevalences_noncarb, width=1.5, color=self.cmap(0))
            idx = 0
            for prevalence_carb, c_carb in zip(prevalences_carb, cs_carb):
                plt.errorbar(x_pos[idx], prevalence_carb, yerr=prevalence_carb - c_carb, color='r')
                idx += 1
            for prevalence_noncarb, c_noncarb in zip(prevalences_noncarb, cs_noncarb):
                plt.errorbar(x_pos[idx], prevalence_noncarb, yerr=prevalence_noncarb - c_noncarb, color='r')
                idx += 1
            if index%3 == 0:
                plt.ylabel("Number of cases", fontsize=10)
            combined_x_ticks = sorted(x_pos+[4.1, 11.1])
            xt_labels = carb_labels + noncarb_labels
            plt.xticks(combined_x_ticks, xt_labels, fontsize=10)
            #plt.xticks([4, 11], ['CARB States', 'Non-CARB States'])
            idx = 0
            # ax2 = ax.twinx()
            # ax2.scatter(x_pos, pops_carb + pops_noncarb, color=self.cmap(1), marker='^', s=8, label='Population trend')
            # ax2.set_ylabel("Population", fontsize=12)
            a, b = [], []
            bar_annote_size = 8
            for prevalence_carb, pop_carb in zip(prevalences_carb, pops_carb):

                # if (what=='prevalence') and (not pd.isna(prevalence_carb)):
                #     carb_per = int(round((prevalence_carb * 100) / pop_carb))
                #     alignment = self.get_bar_annote(carb_per)
                #     ax.text(x_pos[idx]-alignment, prevalence_carb/3, carb_per, size=10, color='k', alpha=0.8)
                # else:
                #     carb_per = round((prevalence_carb * 1000) / pop_carb)
                #     alignment = self.get_bar_annote(carb_per)
                #     ax.text(x_pos[idx] - alignment, prevalence_carb / 3, carb_per, size=10, color='k', alpha=0.8)
                a.append(x_pos[idx])
                b.append(pop_carb)
                idx += 1
            k_plot_style = {"color": self.cmap(1),
                            "linewidth": 0.5,
                            "linestyle": '--'}
            # ax2.plot(a, b, **k_plot_style)
            a, b = [], []
            for prevalence_noncarb, pop_noncarb in zip(prevalences_noncarb, pops_noncarb):
                # if (what=='prevalence') and (not pd.isna(prevalence_noncarb)):
                #     noncarb_per = int(round((prevalence_noncarb * 100) / pop_noncarb))
                #     alignment = self.get_bar_annote(noncarb_per)
                #     ax.text(x_pos[idx]-alignment, prevalence_noncarb/3, noncarb_per, size=10, color='k', alpha=0.8)
                # else:
                #     noncarb_per = round((prevalence_noncarb * 1000) / pop_noncarb)
                #     alignment = self.get_bar_annote(noncarb_per)
                #     ax.text(x_pos[idx] - alignment, prevalence_noncarb / 3, noncarb_per, size=10, color='k',
                #             alpha=0.8)
                #
                # print(prevalence_noncarb, pop_noncarb, (prevalence_noncarb * 1000) / pop_noncarb)
                a.append(x_pos[idx])
                b.append(pop_noncarb)
                idx += 1
            if index == 2:
                custom_lines = [Line2D([0], [0], color='r', lw=2)]
                ax.legend(custom_lines, ['95% conf.'], loc='upper right')
                #plt.legend(loc='upper right', prop={'size': 11})
            # ax2.plot(a, b, **k_plot_style)
            ax.tick_params(axis=u'x', which=u'both', length=0)
            ax.spines['top'].set_visible(False)
            # ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            # ax.spines['left'].set_visible(False)
            ax.get_yaxis().set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            # ax2.spines['top'].set_visible(False)
            # ax2.spines['right'].set_visible(False)
            # ax2.spines['bottom'].set_visible(False)
            # ax2.spines['left'].set_visible(False)
            # ax2.get_yaxis().set_major_formatter(
            #     matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

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
    obj = RegionWisePlotThreeYears('ASTHMA', ['2016', '2017', '2018'], 'ADULT')
    obj.plot(what='incidence')

    # obj = RegionWisePlot('ASTHMA', '2017', 'ADULT')
    # obj.plot(what='incidence')
    #
    # obj = RegionWisePlot('ASTHMA', '2017', 'CHILD')
    # obj.plot( what='prevalence')
    #
    # obj = RegionWisePlot('ASTHMA', '2017', 'CHILD')
    # obj.plot( what='incidence')


