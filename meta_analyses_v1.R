library(lme4)
library(nlme)


fname = "C:/Users/harsh/OneDrive - University of Toronto/Projects/Environmental Discrimination/output_files/for_R_ambient_model_filter.csv"
data = read.csv(fname)

data$state_code = factor(data$state_code)
formula = "incidences_trap ~ ev_sales + nonev_sales + year_fixed + (1|EPA_Region/state_code)"
model <- lmer(formula, data=data)
summary(model)

#model2 <- lme(incidences_trap ~ ev_sales + nonev_sales + year_fixed, random=~1|EPA_Region/state_code,data=data)
#anova(m1)
#summary(ml)