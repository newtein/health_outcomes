MANDATORY_BRFSS_COLUMNS = ["_STATE", "FMONTH", "IDATE", "IMONTH", "IDAY", "IYEAR",
                     "LADULT", "CADULT",
                    "DISPCODE", "NUMADULT", "NUMMEN", "NUMWOMEN", "CSTATE1",
                    "HHADULT", "HLTHPLN1", "MEDCOST", "ASTHMA3", "ASTHNOW",
                    "CHCCOPD1", "EDUCA", "RENTHOM1", "EMPLOY1", "INCOME2",
                    "SMOKE100", "SMOKDAY2", "STOPSMK2", "LASTSMK2", "USENOW3",
                    "ECIGARET", "ECIGNOW",
                    "MEDICARE", "NOCOV121",
                    "LSTCOVRG", "MEDBILL1",
                    "CASTHDX2", "CASTHNO2", "_CHISPNC", "_CRACE1",
                    "_CPRACE", "_HCVU651", "_LTASTH1", "_CASTHM1", "_ASTHMS1",
                    "_PRACE1", "_MRACE1", "_RACEG21", "_CHLDCNT", "_INCOMG",
                    "_SMOKER3", "_RFSMOK3", "_LLCPWT2", "_CLLCPWT"]

OUTPUT_FILE = 'output_files'
OUTPUT_IMAGE = 'output_images'
US_CENSUS_DIR = "us_census"
TRAP_INCIDENCE = 'data/TRAP/khreis_2021.xlsx'
CENSUS_DATA_PATH = US_CENSUS_DIR+"/2010_2019_population.csv"

# California, Connecticut, Maine, Maryland, Massachusetts, New Jersey, New York, Oregon, Rhode Island, Vermont
ZEV_STATES = [6, 9, 23, 24,25, 34, 36, 41, 44, 50]
# CARB = [6, 8, 41, 9, 23, 24,25, 34, 36, 44, 50]

# Arizona (lev repeled), Colarado (zev MY 2022), Delaware (nz), District Of Columbia (nz), Minnesota,
# New Mexico (lev repealed), Pennsylvania (nz), Washington (nz)
# 4 CARB states don't have ZEV mandates
# 2 states AZ and NM has LEV repealed
# Colarado and Manisota has ZEV, but model year are well-beyound (2022).
EXCLUDE_STATES = [4, 8, 10, 11, 27, 35, 42, 53]

## Odds Ratio
DATA_ODDS_RATIO_MODULE = "odds_ratio_module/data"

COLUMNS_FOR_ODD_RATIO = ["SMOKE100", "_STATE", "ASTHMA3", "ASTHNOW", "_AGEG5YR", "SEX", "_RACE_G1",
"INCOME2", "_INCOMG", "EDUCA", "_EDUCAG", "_BMI5", "_BMI5CAT", "CHILDREN", "NUMADULT", "HHADULT", "_CHLDCNT", "_LLCPWT2"]


COLUMNS_FOR_ODD_RATIO_FOR_CHILD = ["_STATE", "CASTHDX2", "CASTHNO2", "RCSGENDR", "_CPRACE",
"INCOME2", "_INCOMG", "CHILDREN", "NUMADULT", "HHADULT", "_CHLDCNT", "_CLLCPWT"]

RENAME  = {
    "SEX1": "SEX",
    "SOMKE100": "SMOKE100",
}

# MODELING_COLUMNS = ["TAILPIPE", "_AGEG5YR", "SEX", "_RACE_G1", 'POVERTY', 'POPEST2017_CIV', "_EDUCAG", "_BMI5CAT",
#                     "ASTHMA"]
#
# MODELING_COLUMNS_FOR_CHILD = ["TAILPIPE", "RCSGENDR", "_CPRACE", 'POVERTY', 'POPEST2017_CIV', "ASTHMA"]


# MODELING_COLUMNS = ["NONCARB", "_AGEG5YR", "SEX", "_RACE_G1", 'POVERTY', 'DENSITY', "_EDUCAG", "_BMI5CAT",
#                     "ASTHMA"]

MODELING_COLUMNS = ["NONCARB", "_AGEG5YR", "SEX", "_RACE_G1", 'POVERTY', 'DENSITY', "_EDUCAG", "_BMI5CAT",
                    "ASTHMA", "_LLCPWT2"]

MODELING_COLUMNS_FOR_CHILD = ["NONCARB", "RCSGENDR"  ,"_CPRACE", 'POVERTY', 'DENSITY', "ASTHMA"]





