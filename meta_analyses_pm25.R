library(lme4)

fname = "C:/Users/harsh/OneDrive - University of Toronto/Projects/Environmental Discrimination/output_files/for_R_filter_by_per_v2.csv"
data = read.csv(fname)

data$state_code = factor(data$state_code)
formula = "incidence_trap ~ ev_sales + nonev_sales + year_fixed + (1|state_code)"
model <- lmer(formula, data=data)
summary(model)
