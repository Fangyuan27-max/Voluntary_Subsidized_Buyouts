import time
import numpy as np
import pandas as pd
import Class_Gov, Class_Res
from Objects_Creater_Res import CreateRes
from Gov_wo_opt import ResRun_WO_Optimization
from Gov_w_opt import Run_W_Optimization
from Result_Analysis_Functions import relocation_num_year, adoption_rate_year, EAD_Discounting_Cost,analysis_mhi, Relocated_Residents
from Tool_functions import selecting_percentage

## Perform simulation for three different mode:
# 1. self-relocation without subsidy
# 2. relocation with subsidy, but the subsidy is a fixed amount of replacement cost and the government does not optimize for each resident over the years
# 3. relocation with subsidy, and the government optimize for each resident when to offer the subsidy

if __name__ == '__main__':
    ## Data input
    #cost_replacement_relocation.csv is a file generated based on Dr. Johnson's code, it has three columns: structure_id, replacement cost, and relocation cost(calculated according to Master Plan File - F1)
    resident_info = pd.read_csv("cost_replacement_relocation.csv")
    resident_info.drop_duplicates(keep='first', inplace=True)
    # EAD_g500_interpolated.csv contains the EAD data for each structure
    ead_info = pd.read_csv('EAD_g500_interpolated.csv')
    ead_info = ead_info.drop(columns=['landscape_scenario_id'])
    ead_info = ead_info.drop_duplicates('structure_id')
    # merging the structure data and ead data together and obtain the inputs for later functions (creating residents)
    merged_df = resident_info.merge(ead_info, on='structure_id', how='inner', validate = '1:1')

    resident_info = merged_df[['structure_id', 'replacement_cost', 'relocation_cost', 'mhi_ratio']]
    ead_info = merged_df.drop(['replacement_cost', 'relocation_cost', 'mhi_ratio'], axis=1)

    # Define the key of ead_info, and from which column the ead starts
    colname = 'structure_id'
    startcol = 1

    ## Government parameters and creating government objects
    disMethodGov = 'Exponential'
    disRateGov = 0.05
    disAlphaGov = 0.1

    # Parameters of residents, where InflaRate is used to calculate the replacement and relocation costs in different years
    disMethod = 'Exponential'
    resDisRate = 0.12
    resAlpha = 0.05
    resInflaRate = 0.02

    calLength = 21
    decLength = 31
    totalLength = 51

    ## Instantiate residents and choose the near-optimal subsidy percentage
    print("Start simulation")
    starttime1 = time.time()
    resList = CreateRes(resident_info, ead_info, colname, startcol, disMethod, resDisRate, resAlpha, resInflaRate, calLength, decLength)
    endtime1 = time.time()
    print("Time used to create the resident list,", endtime1 - starttime1)

    # select the percentage for fixed subsidy without optimization, given that we are not able to judge the
    # perlist = list(np.arange(0.1, 0.61, 0.1))
    # result, selected_per = selecting_percentage(perlist, resList, calLength, decLength, totalLength, disMethodGov, disRateGov, disAlphaGov)
    # print("The selected fixed percentage:", selected_per)

    # # simualtion for 1 and 2
    selected_per = 0.5 # the final selected percentage
    subPercent = selected_per
    Gov = Class_Gov.government(disMethodGov, disRateGov, disAlphaGov)
    starttime2 = time.time()
    Gov, resList = ResRun_WO_Optimization(Gov, resList, subPercent, calLength, decLength, totalLength)
    endtime2 = time.time()
    print("Time used to run simulation without optimization,", endtime2 - starttime2)

    # simulation for 3
    starttime3 = time.time()
    Gov = Run_W_Optimization(Gov, resList, calLength, decLength, totalLength)
    endtime3 = time.time()
    print("Time used to run simulation optimization,", endtime3 - starttime3)

    # save the resident and government info for future investigation
    # np.save('Resident.npy', resList)
    # np.save('Government.npy', Gov)

    # ## Result analysis and visualization parts
    # The relocation number in each year for three modes
    relocation_num = relocation_num_year(Gov, resList, calLength)
    relocation_num.to_csv("Relocation_num_each_year.csv")

    # The relocation adoption rate of the three modes
    adoption_rate = adoption_rate_year(Gov, resList, calLength)
    adoption_rate.to_csv("Adoption_rate.csv")

    # EAD Reduction VS Cost
    EADReduction_Cost_Dis = EAD_Discounting_Cost(Gov, resList, calLength, decLength, totalLength)
    EADReduction_Cost_Dis.to_csv('EADReduction_Cost.csv')

    # Relocated residents for three modes; for self-relocation, the csv contains all self-relocated residents, for fixed_motivated/optimal_motivated,
    # residents relocated is the union of self_relocated csv and motivated_relocated csv
    Self_relocation_DF, Fixed_relocation_DF, Optimal_relocation_DF = Relocated_Residents(resList)
    Self_relocation_DF.to_csv("Self_Relocated_Residents.csv")
    Fixed_relocation_DF.to_csv("Fixed_Relocated_Residents.csv")
    Optimal_relocation_DF.to_csv("Optimal_Relocated_residents.csv")

    mode1 = 'Opt'
    mhi_list = [0.5, 0.85, 1.25, 2, 999]
    mhi_result = analysis_mhi(Gov, resList, mhi_list, mode1, subPercent, calLength)
    mhi_result.to_csv('mhi_result_opt.csv')

    mode2 = 'Fix'
    mhi_list = [0.5, 0.85, 1.25, 2, 999]
    mhi_result = analysis_mhi(Gov, resList, mhi_list, mode2, subPercent, calLength)
    mhi_result.to_csv('mhi_result_fix.csv')

    mode3 = 'Self'
    mhi_list = [0.5, 0.85, 1.25, 2, 999]
    mhi_result = analysis_mhi(Gov, resList, mhi_list, mode3, subPercent, calLength)
    mhi_result.to_csv('mhi_result_self.csv')