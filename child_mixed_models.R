library("GLMMadaptive")

args <- commandArgs(trailingOnly = TRUE)
fname = args[1]

p = unlist(strsplit(fname, "/"))
wfname = paste(p[0], "/", p[1], "/", p[2], "/", p[3], "/RESULTS_", p[4], sep="")
wfname = substring(wfname, 2)

print(wfname)
data <- read.csv(fname)

fixed = ASTHMA  ~ ZEV_MANDATES + GENDER +  DENSITY + POVERTY + RACE  
random = ~ 1 | STATE
keeps <- c("ASTHMA", "ZEV_MANDATES",  "GENDER","RACE", "POVERTY","DENSITY", "STATE")

data <- data[keeps]
print(fixed)
print(random)

data$GENDER = as.factor(data$GENDER)
data$RACE = as.factor(data$RACE)
#data$STATE = as.factor(data$STATE)

model <- mixed_model(fixed=fixed, random=random, data = data, family = binomial(), penalized=TRUE) 

sink(wfname)
s = summary(model)
odds = exp(coef(model))
print(s)
print(odds)
sink()
print(s)
print(odds)

