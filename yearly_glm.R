library("mgcv")
library("fastDummies")

print("lib import: 1/4") 
fname = "df_ZDEPA Region 0 Odds Ratio CHILD.csv"
wfname = "mgcv_original_model_with_dummy"

print(wfname)
df <- read.csv(fname)
print("data import: 2/4")

# data_year = subset(data, YEAR == 3)
# fixed = ASTHMA  ~ ZEV_MANDATES + GENDER + RACE + POVERTY + s(DENSITY)
fixed = ASTHMA  ~ ZEV_MANDATES +  POVERTY + s(DENSITY) + GENDER_1 + GENDER_2+ GENDER_9 + RACE_1+ RACE_2+ RACE_3+ RACE_4+ RACE_5+ RACE_6+ RACE_7+ RACE_77+ RACE_99

for (year in 1:5) {
data <- subset(df, df$YEAR == year)
keeps <- c("ASTHMA", "ZEV_MANDATES", "GENDER",  "RACE",   "POVERTY", "DENSITY")
data <- data[keeps]
data <- dummy_cols(data, select_columns = c('GENDER', 'RACE'),remove_selected_columns = TRUE)
print(fixed)
model <- gam(formula=fixed, data = data, family = binomial("logit"))
print("model trained: 3/4")
wf = paste(wfname, year, ".txt")
sink(wf)
print(summary(model))
sink()
print("written: 4/4")
}
