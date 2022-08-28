import os

refresh = 1
syear = 2015
eyear = 2020
fname = "df_AFv2_EPA0_CHILD.csv"
filepath = "odds_ratio_module/data/{}/{}"
rfilepath = "odds_ratio_module/data/{}/{}"
python_path = "~/projects/'Environmental Discrimination'/"
model_type = "glm"

for year in range(syear, eyear + 1):
    s = year
    y = "{}".format(s)
    pathexists = filepath.format(y, fname)
    if model_type == "mixed":
        rscript = "Rscript child_mixed_models.R {}".format(rfilepath.format(y, fname))
    elif model_type == "glm":
        rscript = "Rscript child_glm.R {}".format(rfilepath.format(y, fname))
    if not os.path.exists(pathexists) or refresh:
        python_cmd = "python logistic_oe_each_zev_old.py {}".format(s)
        print("Executing: ", python_cmd)
        os.system(python_cmd)
        print("Done")
    print(pathexists, "\nExists:", os.path.exists(pathexists))
    wfname = filepath.format(s, "RESULTS_{}".format(fname))
    if not os.path.exists(wfname) or refresh:
        print("Executing: ", rscript)
        #os.system(rscript)
        print("Done.")

    print("Completed: {}".format(y))



