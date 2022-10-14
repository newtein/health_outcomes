library(lme4)

fname = "C:/Users/harsh/OneDrive - University of Toronto/Projects/Environmental Discrimination/output_files/for_R.csv"
data = read.csv(fname)

data$state_code = factor(data$state_code)
formula = "incidence_trap ~ ev_sales_log + nonev_sales_log + ZEV_Mandates + year_fixed + (1|state_code)"
model <- lmer(formula, data=data)
summary(model)