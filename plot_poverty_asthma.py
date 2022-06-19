import matplotlib.pyplot as plt
from poverty_asthma_module import PovertyModule
import matplotlib.gridspec as gridspec
import pandas as pd
from constants import *
import matplotlib.patches as mpatches
import csv
from config import CONFIG


class PlotBar:
    def __init__(self):
        self.pop_type = 'ADULT'
        obj = PovertyModule(self.pop_type)
        self.carb_data, self.noncarb_data = obj.get_data()
        self.cmap = plt.get_cmap("Paired")
        # self.carb_weighted_data, self.noncarb_weighted_data = obj.get_weighted_data()

    def filter_null(self, r):
        return [i for i in r if not pd.isna(r.get(i).get('POVERTY%'))]

    def get_common_epa_regions(self):
        carb_regions = self.filter_null(self.carb_data)
        noncarb_regions = self.filter_null(self.noncarb_data)
        return sorted(list(set(carb_regions).intersection(noncarb_regions)))

    def get_one(self, x):
        return "{:.1f}".format(x)

    def execute(self):
        # rows, cols = 2, 1
        # posCord = [(i, j) for i in range(0, rows) for j in range(0, cols)]
        plt.close()
        plt.figure(figsize=(8, 4), dpi=600)
        ax = plt.gca()
        # gs = gridspec.GridSpec(rows, cols)
        # ax = plt.subplot(gs[posCord[0][0], posCord[0][1]])
        epa_regions = [0] + CONFIG.get("epa_regions")
        flag = 0
        x_list, x_ticks = [], []
        labels = ["US" if i==0 else "EPA\nRegion {}".format(i) for i in epa_regions]
        headers = ["Region", "CARB Poverty%", "Non CARB Poverty%", "CARB Poverty+Asthma%", "Non CARB Poverty+Asthma%"]
        file_w = "{}/poverty_asthma_module.csv".format(OUTPUT_FILE)
        pointer_f = open(file_w, "w", newline='')
        writer = csv.writer(pointer_f)
        writer.writerow(headers)
        for index, epa_region in enumerate(epa_regions):
            carb_poverty = self.carb_data.get(epa_region)['POVERTY%']
            carb_poverty_with_asth = self.carb_data.get(epa_region)['POVERTYASTHMA%']

            noncarb_poverty = self.noncarb_data.get(epa_region)['POVERTY%']
            noncarb_poverty_with_asth = self.noncarb_data.get(epa_region)['POVERTYASTHMA%']
            width = 0.6
            alingnment = width/2
            x1, x2 = flag, flag+1
            x_list.append(x1)
            avg = (x1 + x2) / 2
            x_list.append(avg)
            x_list.append(x2)
            x_ticks.append("CARB")
            x_ticks.append("\n\n\n{}".format(labels[index]))
            x_ticks.append("Non\nCARB")
            plt.bar([x1, x2], [carb_poverty, noncarb_poverty], color=self.cmap(0), width=width)
            plt.bar([x1, x2], [carb_poverty_with_asth, noncarb_poverty_with_asth], color=self.cmap(1), width=width)
            ax.text(x1-alingnment, carb_poverty_with_asth, "{:.1f}%".format(carb_poverty_with_asth*100/carb_poverty), size=7, color='k', alpha=0.6)
            ax.text(x2-alingnment, noncarb_poverty_with_asth, "{:.1f}%".format(noncarb_poverty_with_asth*100/noncarb_poverty), size=7, color='k', alpha=0.6)
            row = [epa_region, self.get_one(carb_poverty), self.get_one(noncarb_poverty),
                   self.get_one(carb_poverty_with_asth), self.get_one(noncarb_poverty_with_asth)]
            writer.writerow(row)
            flag += 2.5
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(x_list, x_ticks, fontsize=9)
        ax.tick_params(axis=u'x', which=u'both', length=0)
        red_patch = mpatches.Patch(color=self.cmap(0), label='Poverty')
        blue_patch = mpatches.Patch(color=self.cmap(1), label='Poverty and Asthma')
        plt.legend(handles=[red_patch, blue_patch])
        plt.ylabel("Percentage")

        # ax = plt.subplot(gs[posCord[1][0], posCord[1][1]])
        # epa_regions = self.get_common_epa_regions()
        # x_list, x_ticks = [], []
        # labels = ["US" if i==0 else "EPA\nRegion {}".format(i) for i in epa_regions]
        # flag = 0
        # for index, epa_region in enumerate(epa_regions):
        #     carb_poverty = self.carb_weighted_data.get(epa_region)['POVERTY%']
        #     carb_poverty_with_asth = self.carb_weighted_data.get(epa_region)['POVERTYASTHMA%']
        #
        #     noncarb_poverty = self.noncarb_weighted_data.get(epa_region)['POVERTY%']
        #     noncarb_poverty_with_asth = self.noncarb_weighted_data.get(epa_region)['POVERTYASTHMA%']
        #     x1, x2 = flag, flag + 1
        #     x_list.append(x1)
        #     avg = (x1+x2)/2
        #     x_list.append(avg)
        #     x_list.append(x2)
        #     x_ticks.append("CARB\nStates")
        #     x_ticks.append("\n\n\n{}".format(labels[index]))
        #     x_ticks.append("Non-CARB\nStates")
        #     plt.bar([x1, x2], [carb_poverty, noncarb_poverty], color='b')
        #     plt.bar([x1, x2], [carb_poverty_with_asth, noncarb_poverty_with_asth], color='g')
        #     flag += 2
        #
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        # plt.xticks(x_list, x_ticks)
        # plt.tight_layout()
        # plt.legend(loc='upper right', prop={'size': 11})
        fw = "{}/poverty_asthma.png".format(OUTPUT_IMAGE)
        plt.savefig(fw, bbox_inches='tight')


if __name__ == "__main__":
    obj = PlotBar()
    obj.execute()