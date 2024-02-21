import pandas as pd
import copy
import Class_Gov
from Gov_wo_opt import ResRun_WO_Optimization

## For mode 2, select one fixed subsidy percentagte from the percentage list that minimize the objective value of fixed subsidy plan
def selecting_percentage(perlist, resList, calLength, disMethodGov, disRateGov, disAlphaGov):
    objectivelist = []
    result_table = {}
    for per in perlist:
        result_table[per] = {}

        Gov = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)
        resList_copy = copy.deepcopy(resList)

        Gov, resList_computed = ResRun_WO_Optimization(Gov, resList_copy, per, calLength)

        result_table[per]['Objective_value_self'] = Gov.objective_wo_subsidy
        result_table[per]['Objective_value_wo_replacement'] = Gov.objective_fixed_subsidy
        result_table[per]['Objective_value_w_replacement'] = Gov.obj_fixed_subsidy_replacement

        objectivelist.append(Gov.objective_fixed_subsidy)
    result = pd.DataFrame(result_table)
    selected_per = perlist[objectivelist.index(min(objectivelist))]
    return result, selected_per

