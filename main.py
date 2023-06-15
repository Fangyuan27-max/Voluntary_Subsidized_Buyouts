import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Class_Gov, Class_Res
from Objects_Creater_Res import CreateRes
from Gov_wo_opt import ResRun_WO_Optimization
from Gov_w_opt import Run_W_Optimization
from Result_Analysis_Functions import relocation_num_year, adoption_rate_year, benefit_cost, subsidy_count_year

if __name__ == '__main__':
    # create residents
    # structure_id = pd.read_csv('structure_id.csv')
    # resident_info = pd.read_csv("cost_replacement_relocation.csv")
    # resident_info.drop_duplicates(keep='first', inplace=True)
    # ead_info = pd.read_csv('EAD_g500_interpolated.csv')
    # ead_info = ead_info.drop(columns=['landscape_scenario_id'])
    # ead_info = ead_info.drop_duplicates('structure_id')
    colname = 'structure_id'
    startcol = 3
    #
    # #    print(structure_id.shape)
    # #    print(resident_info.shape)
    # #    print(ead_info.shape)
    #
    # merged_df = structure_id.merge(resident_info, on='structure_id', how='inner')
    # #    print(merged_df.shape)
    # #    print(merged_df.columns)
    # merged_df1 = merged_df.merge(ead_info, on='structure_id', how='inner', validate='1:1')
    # #    print(merged_df1.shape)
    #
    # resident_info = merged_df1[['structure_id', 'replacement_cost', 'relocation_cost']]
    # ead_info = merged_df1.drop(['replacement_cost', 'relocation_cost'], axis=1)
    # #    print(ead_info.columns)

    ## The sample information
    resident_info = pd.read_csv('sample_resident.csv')
    ead_info = pd.read_csv('sample_eadlist.csv')

    disMethod = 'Exponential'
    resDisRate = 0.12
    resAlpha = 0.05
    calLength = 51
    relocationcost = 5

    print("Start simulation")
    starttime1 = time.time()
    resList = CreateRes(resident_info, ead_info, colname, startcol, disMethod, resDisRate, resAlpha, calLength)
    endtime1 = time.time()
    print("Time used to create the resident list,", endtime1 - starttime1)

    # create government
    disMethodGov = 'Exponential'
    disRateGov = 0.05
    disAlphaGov = 0.1
    Gov1 = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)

    # run a sample model without optimization
    subPercent = 0.5
    starttime2 = time.time()
    resList = ResRun_WO_Optimization(resList, subPercent, calLength)
    endtime2 = time.time()
    print("Time used to run simulation without optimization,", endtime2 - starttime2)

    # run with optimization
    starttime3 = time.time()
    Gov2 = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)
    government = Run_W_Optimization(Gov2, resList, calLength)
    endtime3 = time.time()
    print("Time used to run simulation optimization,", endtime3 - starttime3)

    relocation_num_year(Gov2, resList, calLength)

    print(Gov2.selfRelocationNum)
    print(Gov2.motiRelocationNum)
    print(Gov2.optMotiRelocationNum)

    for res in resList:
        print('id:', res.idx, "self_move:", res.selfMoveYear, "moti_move:", res.motiMoveYear, "opt_moti_move:", res.optmotiMoveYear)

    # table = adoption_rate_year(Gov2, calLength)
    # print(table)
    # result = subsidy_count_year(Gov2, resList, calLength)
    # print(result)
    benefit_cost_result = benefit_cost(Gov2, resList, calLength)
    # print(benefit_cost_result)
    benefit_cost_result.to_csv('benefit_cost_result.csv')
    # print(result)
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

