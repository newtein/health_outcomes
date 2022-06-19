import matplotlib.pyplot as plt
from constants import *
import seaborn as sns
from logistic_oe import OddsRatio
import matplotlib.gridspec as gridspec
import csv


class plt_error_bar:
    def __init__(self, column='NONCARB'):
        self.column = column
        self.results_adult, self.accuracy_adult = OddsRatio(pop_type='ADULT').get_results()
        self.results_child, self.accuracy_child = OddsRatio(pop_type='CHILD').get_results()
        self.cmap = plt.get_cmap("Paired")

    def get_param(self, results):
        epa_regions = sorted(results)
        x_ticks = ["US" if epa_region == 0 else "EPA Region {}".format(epa_region) for epa_region in epa_regions]
        x = [i for i in range(len(epa_regions))]
        y = [results.get(epa_region).loc[self.column]['Odds Ratio'] for epa_region in epa_regions]
        y1 = [results.get(epa_region).loc[self.column]['5%'] for epa_region in epa_regions]
        y2 = [results.get(epa_region).loc[self.column]['95%'] for epa_region in epa_regions]
        error = [i - j for i, j in zip(y2, y)]
        return epa_regions, x, y, error, x_ticks

    def f2(self, x):
        if x:
            return "{:.2f}".format(x)
        else:
            return None

    def execute(self):
        plt.close()
        sns.set_style("ticks")
        epa_regions_adult, x_adult, y_adult, error_adult, x_ticks_adult = self.get_param(self.results_adult)

        rows, cols = 2, 1
        posCord = [(i, j) for i in range(0, rows) for j in range(0, cols)]
        plt.close()
        plt.figure(figsize=(5, 5), dpi=600)
        gs = gridspec.GridSpec(rows, cols)
        ax = plt.subplot(gs[posCord[0][0], posCord[0][1]])
        ax.text(-0.09, 1.05, 'a)', transform=ax.transAxes, size=15, color='black')
        plt.scatter(x_adult, y_adult, marker='o', s=15, color=self.cmap(0))
        for i, j in zip(x_adult, y_adult):
            ax.text(i + 0.05, j, "{:.2f}".format(j), size=9, color='k', alpha=0.6)
        for i, j, e in zip(x_adult, y_adult, error_adult):
            plt.errorbar(i, j, yerr=e, color=self.cmap(1), elinewidth=1)
        plt.hlines(1, min(x_adult), max(x_adult), linestyles='--', linewidth=0.4, color='r')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis=u'x', which=u'both', length=0)
        plt.ylabel("Odds Ratio (95% CI)")
        plt.xticks(x_adult, [i.replace("EPA ", "EPA \n") for i in x_ticks_adult])
        plt.title("Adults", size=12)


        epa_regions_child, x_child, y_child, error_child, x_ticks_child = self.get_param(self.results_child)
        ax = plt.subplot(gs[posCord[1][0], posCord[1][1]])
        ax.text(-0.09, 1.05, 'b)', transform=ax.transAxes, size=15, color='black')
        plt.scatter(x_child, y_child, marker='o', s=15, color=self.cmap(0))
        for i, j in zip(x_child, y_child):
            ax.text(i+0.05, j, "{:.2f}".format(j), size=9, color='k',alpha=0.6)

        for i, j, e in zip(x_child, y_child, error_child):
            plt.errorbar(i, j, yerr=e, color=self.cmap(1), elinewidth=1)
        plt.hlines(1, min(x_child), max(x_child), linestyles='--', linewidth=0.4, color='r')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis=u'x', which=u'both', length=0)
        plt.ylabel("Odds Ratio (95% CI)")
        plt.xticks(x_child, [i.replace("EPA ", "EPA \n") for i in x_ticks_child])
        plt.title("Children", size=12)

        fw = "{}/{}_{}.png".format(OUTPUT_IMAGE, "Odds_ratio", self.column)
        plt.tight_layout()
        if self.column == 'NONCARB':
            s = "a lack of ZEV and LEV mandates"
        else:
            s = 'poverty'
        epa_regions = sorted(set(epa_regions_adult+epa_regions_child))
        wfile = "{}/{}_{}.csv".format(DATA_ODDS_RATIO_MODULE, "Odds_ratio", self.column)
        fpointer = open(wfile, "w", newline='')
        writer = csv.writer(fpointer)
        headers = ["EPA Regions", "Adults", "Accuracy Adult", "Children", "Accuracy Child"]
        writer.writerow(headers)
        for epa_region in epa_regions:
            try:
                value_lookup = self.results_adult.get(epa_region, {}).loc[self.column]
            except:
                value_lookup = {}
            value_adult = "{} ({}-{})".format(self.f2(value_lookup.get('Odds Ratio')), self.f2(value_lookup.get('5%')),
                                              self.f2(value_lookup.get('95%')))
            try:
                value_lookup = self.results_child.get(epa_region, {}).loc[self.column]
            except:
                value_lookup = {}
            value_child = "{} ({}-{})".format(self.f2(value_lookup.get('Odds Ratio')), self.f2(value_lookup.get('5%')),
                                              self.f2(value_lookup.get('95%')))
            row = [epa_region, value_adult, self.accuracy_adult.get(epa_region), value_child,
                   self.accuracy_child.get(epa_region)]
            writer.writerow(row)
        fpointer.close()
        #plt.suptitle("Association between {} and current asthma prevalence".format(s), fontsize=22, y=1.05)
        plt.savefig(fw, bbox_inches='tight')
        print("Figure written")


if __name__ == "__main__":
    obj = plt_error_bar(column='NONCARB')
    obj.execute()
    # obj = plt_error_bar(column='POVERTY')
    # obj.execute()

