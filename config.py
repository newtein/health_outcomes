CONFIG = {
    "BRFSS": {
        "2017": 'LLCP2017.XPT'
    },
    "ACBS": {
        "2017": {
            "ADULT": "ACBS_2017_ADULT_PUBLIC_LLCP.sas7bdat",
            "CHILD": "ACBS_2017_CHILD_PUBLIC_LLCP.sas7bdat"
        }
    },
    "CENSUS": {
        "age_sex": "sc-est2019-agesex-civ.csv"
    },
    "ASTHMA": {
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

        }
    }
}