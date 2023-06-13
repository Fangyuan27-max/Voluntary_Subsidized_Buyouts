import time
import numpy as np
import pandas as pd
import Class_Gov, Class_Res
from Objects_Creater_Res import CreateRes
from Gov_wo_opt import ResRun_WO_Optimization, WO_optimization_Tuning
from Gov_w_opt import Run_W_Optimization

if __name__ == '__main__':
    # create residents
    resident_info = pd.read_csv("Res_info.csv")
    ead_info = pd.read_csv('ead_list.csv')
    ead_info = ead_info.drop(columns = ['landscape_scenario_id'])
    colname = 'structure_id'

    disMethod = 'Exponential'
    resDisRate = 0.18
    resAlpha = 0.05
    calLength = 51
    relocationcost = 5

    starttime1 = time.time()
    resList = CreateRes(resident_info, ead_info, colname, disMethod, resDisRate, resAlpha, calLength)
    endtime1 = time.time()
    print("Time used to create the resident list,", endtime1 - starttime1)

    #create government
    disMethodGov = 'Exponential'
    disRateGov = 0.05
    disAlphaGov = 0.1
    Gov1 = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)

    # run a sample model without optimization
    subPercent = 0.5
    starttime2 = time.time()
    resList = ResRun_WO_Optimization(resList, relocationcost, subPercent, calLength)
    endtime2 = time.time()
    print("Time used to create the resident list,", endtime2 - starttime2)

    # display the result of the run without optimization
    # Gov1.relocation_num_year(resList, calLength)
    # print(Gov1.selfRelocationNum)
    # print(Gov1.motiRelocationNum)

    # run with optimization
    starttime3 = time.time()
    Gov2 = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)
    government = Run_W_Optimization(Gov2, resList, calLength)
    endtime3 = time.time()
    print("Time used to create the resident list,", endtime3 - starttime3)
    # print(Gov2.Subsidyyear) # results show that all three residents in the experiment relocate in year o with subsidy support from the government

    # # check the amount of subsidy offered
    # for res in resList:
    #     relocationyear = Gov2.Subsidyyear[res.idx]
    #     subsidyamount = res.Subsidyneeded[relocationyear]
    #     print(subsidyamount)
    #
    # print("government past loss and total expense:\n")
    # for res in resList:
    #     print(Gov2.pastloss[res.idx])
    #     print(Gov2.NPVlossSubsidy[res.idx])

