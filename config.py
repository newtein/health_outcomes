CONFIG = {
    "analysis_years": ["2016", "2017", "2018", "2019", "2020"],
    "epa_regions": [1, 3, 8, 9, 10],
    "disease": 'ASTHMA',
    "BRFSS": {
        "2008": 'CDBRFS08.XPT',
        "2009": 'CDBRFS09.XPT',
        "2010": 'CDBRFS10.XPT',
        "2011": 'LLCP2011.XPT',
        "2012": 'LLCP2012.XPT',
        "2013": 'LLCP2013.XPT',
        "2014": 'LLCP2014.XPT',
        "2015": 'LLCP2015.XPT',
        "2016": 'LLCP2016.XPT',
        "2017": 'LLCP2017.XPT',
        "2018": 'LLCP2018.XPT',
        "2019": 'LLCP2019.XPT',
        "2020": 'LLCP2020.XPT'
    },
    "ACBS": {
        "2008": {
            "CHILD": "ACBS_2008_CHILD_PUBLIC.sas7bdat"
        },
        "2009": {
            "CHILD": "acbs_2009_child_public.sas7bdat"
        },
        "2010": {
            "CHILD": "acbs_2010_child_public.sas7bdat"
        },
        "2011": {
            "CHILD": "acbs_2011_child_public.sas7bdat"
        },
        "2012": {
            "CHILD": "acbs_2012_child_public_llcp.sas7bdat"
        },
        "2013": {
            "CHILD": "acbs_2013_child_public_llcp.sas7bdat"
        },
        "2014": {
            "CHILD": "ACBS_2014_CHILD_PUBLIC_LLCP.sas7bdat"
        },
        "2015": {
            "CHILD": "ACBS_2015_CHILD_PUBLIC_LLCP.sas7bdat"
        },
        "2016" :{
            "ADULT": "acbs_2016_adult_public_llcp.sas7bdat",
            "CHILD": "acbs_2016_child_public_llcp.sas7bdat"
        },
        "2017": {
            "ADULT": "ACBS_2017_ADULT_PUBLIC_LLCP.sas7bdat",
            "CHILD": "ACBS_2017_CHILD_PUBLIC_LLCP.sas7bdat"
        },
        "2018": {
            "ADULT": "acbs_2018_adult_public_llcp.sas7bdat",
            "CHILD": "acbs_2018_child_public_llcp.sas7bdat"
        },
        "2019": {
            "CHILD": "acbs_2019_child_public_llcp.sas7bdat"
        },
    },
    "CENSUS": {
        "age_sex": "sc-est_2010_2021_agesex-civ.csv"
    },
    "ASTHMA": {
        "2016": {
            "ADULT": {
                "GLOBAL": 8.9,
                "GLOBAL_HIGH": 9.1,
                "GLOBAL_LOW": 8.7,
                "SRC": "https://www.cdc.gov/asthma/brfss/2016/tableC1.htm",
                "Prevalence": "current_adult_prevalance_rate.xlsx",
            },
            "CHILD": {
                "GLOBAL": 8.1,
                "GLOBAL_HIGH": 8.4,
                "GLOBAL_LOW": 7.7,
                "SRC": "https://www.cdc.gov/asthma/brfss/2016/child/tableC1.htm",
                "Prevalence": "current_child_prevalance_rate.xlsx",
            }

        },
        "2017": {
            "ADULT": {
                "GLOBAL": 9.1,
                "GLOBAL_HIGH": 9.2,
                "GLOBAL_LOW": 8.9,
                "SRC": "https://www.cdc.gov/asthma/brfss/2017/tableC1.htm",
                "Prevalence": "current_adult_prevalance_rate.xlsx",
            },
            "CHILD": {
                "GLOBAL": 7.9,
                "GLOBAL_HIGH": 8.4,
                "GLOBAL_LOW": 7.5,
                "SRC": "https://www.cdc.gov/asthma/brfss/2017/child/tableC1.htm",
                "Prevalence": "current_child_prevalance_rate.xlsx",
            }

        },
        "2018": {
            "ADULT": {
                "GLOBAL": 9.2,
                "GLOBAL_HIGH": 9.4,
                "GLOBAL_LOW": 9.1,
                "SRC": "https://www.cdc.gov/asthma/brfss/2018/tableC1.html",
                "Prevalence": "current_adult_prevalance_rate.xlsx",
            },
            "CHILD": {
                "GLOBAL": 7.2,
                "GLOBAL_HIGH": 7.6,
                "GLOBAL_LOW": 6.7,
                "SRC": "https://www.cdc.gov/asthma/brfss/2018/child/tableC1.html",
                "Prevalence": "current_child_prevalance_rate.xlsx",
            }

        }
    },
    "POVERTY": {
        "HOUSEHOLD_DATA": {
            "SRC": "https://www.federalregister.gov/documents/2017/01/31/2017-02076/annual-update-of-the-hhs-poverty-guidelines",
            "DATA": {
                'Persons in family/household': 'Poverty guideline',
                "1": 12060,
                "2": 16240,
                "3": 20420,
                "4": 24600,
                "5": 28780,
                "6": 32960,
                "7": 37140,
                "8": 41320,
                "+8": 4180
            },
            "AK": {
                'Persons in family/household': 'Poverty guideline',
                "1": 15060,
                "2": 20290,
                "3": 25520,
                "4": 30750,
                "5": 35980,
                "6": 41210,
                "7": 46440,
                "8": 51670,
                "+8": 5230
            },
            "HW": {
                'Persons in family/household': 'Poverty guideline',
                "1": 13860,
                "2": 18670,
                "3": 23480,
                "4": 28290,
                "5": 33100,
                "6": 37910,
                "7": 42720,
                "8": 47530,
                "+8": 4810
            }
        },
        "INCOME_INDEX": {
            "SRC": "https://www.cdc.gov/brfss/annual_data/2016/pdf/codebook16_llcp.pdf",
            "DATA": {
                "1": 9999,
                "2": 14999,
                "3": 19999,
                "4": 24999,
                "5": 34999,
                "6": 49999,
                "7": 74999,
                "8": 10e10
            }
        }
    },
    "TRAP_GLOBAL": {
        "value": "0.176",
        "src": "https://www.sciencedirect.com/science/article/pii/S1047279720303446?via%3Dihub#tbls5"
    }

}