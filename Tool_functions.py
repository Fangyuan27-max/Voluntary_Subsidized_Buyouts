import pandas as pd
import copy
import Class_Gov
from Gov_wo_opt import ResRun_WO_Optimization

## For mode 2, select one fixed subsidy percentagte from the percentage list that minimize the objective value of fixed subsidy plan
def selecting_percentage(perlist, resList, calLength,decLength, totalLength, disMethodGov, disRateGov, disAlphaGov):
    objectivelist = []
    result_table = {}
    for per in perlist:
        result_table[per] = {}

        Gov = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)
        resList_copy = copy.deepcopy(resList)

        Gov, resList_computed = ResRun_WO_Optimization(Gov, resList_copy, per, calLength, decLength, totalLength)

        result_table[per]['Objective_value_self'] = Gov.objective_wo_subsidy
        result_table[per]['Objective_value_fix'] = Gov.objective_fixed_subsidy

        objectivelist.append(Gov.objective_fixed_subsidy)
    result = pd.DataFrame(result_table)
    selected_per = perlist[objectivelist.index(min(objectivelist))]
    return result, selected_per

