import pandas as pd

def relocation_num_year(gov, resList, calLength):
    relocation_num = {}
    relocation_num['Year'] = []
    relocation_num['Self_relocation'] = []
    relocation_num['Moti_relocation'] = []
    relocation_num['Opt_moti_relocation'] = []
    for i in range(calLength):
        relocation_num[i] = {}
        count_self = 0
        count_moti = 0
        count_opt_moti = 0
        for res in resList:
            if res.selfMoveYear == i:
                count_self += 1
            else:
                count_self += 0

            if res.motiMoveYear == i:
                count_moti += 1
            else:
                count_moti += 0

            if res.optmotiMoveYear == i:
                count_opt_moti += 1
            else:
                count_opt_moti += 0

        # store the relocation number to the object - gov for later quick cheking (if needed)
        gov.selfRelocationNum.append(count_self)
        gov.motiRelocationNum.append(count_moti)
        gov.optMotiRelocationNum.append(count_opt_moti)

        relocation_num['Year'].append(i)
        relocation_num['Self_relocation'].append(count_self)
        relocation_num['Moti_relocation'].append(count_moti)
        relocation_num['Opt_moti_relocation'].append(count_opt_moti)
    relocation_num = pd.DataFrame(relocation_num, columns=['Year', 'Self_relocation', 'Moti_relocation', 'Opt_moti_relocation'])
    return relocation_num


def adoption_rate_year(gov, resList, calLength):
    resnum = len(resList)
    adoption_rate = {}
    adoption_rate["Year"] = []
    adoption_rate['Self_Move_Adopt'] = []
    adoption_rate['Fixmoti_Move_Adopt'] = []
    adoption_rate['Opt_Subsidy_Move_Adopt'] = []
    for i in range(calLength):
        adoption_rate['Year'].append(i)
        adoption_rate['Self_Move_Adopt'].append(sum(gov.selfRelocationNum[:i+1]) / resnum)
        adoption_rate['Fixmoti_Move_Adopt'].append(sum(gov.motiRelocationNum[:i+1]) / resnum)
        adoption_rate['Opt_Subsidy_Move_Adopt'].append(sum(gov.optMotiRelocationNum[:i+1]) / resnum)
    adoption_rate_table = pd.DataFrame(adoption_rate)
    return adoption_rate_table


def discount(value, dr, length):
    return value / (1 + dr) ** length


# Exponential discounting
def EAD_Discounting_Cost(gov, resList, calLength, decLength, totalLength):
    benefit_cost_year = {}
    benefit_cost_year['Year'] = []
    benefit_cost_year['Original_EAD'] = []
    benefit_cost_year['Self_EAD'] = []
    benefit_cost_year['Self_Subsidy'] = []
    benefit_cost_year['Self_TC'] = []
    benefit_cost_year['Moti_EAD'] = []
    benefit_cost_year['Moti_Subsidy'] = []
    benefit_cost_year['Moti_TC'] = []
    benefit_cost_year['Opt_Moti_EAD'] = []
    benefit_cost_year['Opt_Moti_Subsidy'] = []
    benefit_cost_year['Opt_Moti_TC'] = []
    benefit_cost_year['EAD_Reduction_SR_NoRelocation'] = []
    benefit_cost_year['EAD_Reduction_FS_SR'] = []
    benefit_cost_year['EAD_Reduction_OS_SR'] = []

    for i in range(totalLength):
        benefit_cost_year['Year'].append(i)
        Original_EAD = 0
        Self_EAD, Self_Subsidy, Self_TC = 0, 0, 0
        Moti_EAD, Moti_Subsidy, Moti_TC = 0, 0, 0
        Opt_Moti_EAD, Opt_Moti_Subsidy, Opt_Moti_TC = 0, 0, 0
        EAD_Reduction_SR_NoRelocation, EAD_Reduction_FS_SR, EAD_Reduction_OS_SR = 0, 0, 0

        # obtain the original ead value of all residents
        for res in resList:
            Original_EAD += res.ead[i] / ((1 + gov.disRate) ** i)

        if i < calLength:
            for res in resList:
               ## calculate the benefit and cost of self-move
                # for a given year, if the resident does not relocate, its EAD contributes to the EAD loss that gov bears this year
                if i < res.selfMoveYear:
                    Self_EAD += res.ead[i] / ((1 + gov.disRate) ** i)
                else:
                    Self_EAD += 0
                # compared with "No Relocation", the EAD reduction is the sum of NPV(in year 0) of EAD from the self-relocation year to the year 50.
                if i == res.selfMoveYear:
                    EAD_Reduction_SR_NoRelocation += sum([discount(res.ead[j], gov.disRate, j) for j in range(i, i + decLength)])
                    Self_TC += res.relocationcost / ((1 + gov.disRate) ** i)
                # since under the self-move mode, the government will not provide any subsidy but bear the flood loss, the subsidy and totalcost will be 0

                ## calculate the benefit and cost of fixed-subsidy percentage relocation
                # EAD follows the same logic as in the self-relocation
                if i < res.motiMoveYear:
                    Moti_EAD += res.ead[i] / ((1 + gov.disRate) ** i)
                else:
                    Moti_EAD += 0

                # calculate the ead reduction and cost
                if i == res.motiMoveYear:
                    # if the resident will relocate in any year before year 21, the EAD reduction is the sum of npv of ead between motivated_year and self_year, else
                    # the reduction is between the motivated relocation year and year 50
                    if res.selfMoveYear < calLength:
                        EAD_Reduction_FS_SR += sum([res.ead[j] / (1 + gov.disRate) ** j for j in range(i, res.selfMoveYear)])
                    else:
                        EAD_Reduction_FS_SR += sum([res.ead[j] / (1 + gov.disRate) ** j for j in range(i, i + decLength)])

                    # a relocation subsidy occurs only when the fixed-relocation-year is strictly earlier than the self-relocation year
                    if res.motiMoveYear < res.selfMoveYear:
                        Moti_Subsidy += res.replacementcost * gov.subPercent / ((1 + gov.disRate) ** i)
                        # old
                        # Moti_TC += res.replacementcost * gov.subPercent/((1 + gov.disRate) ** i)
                        # new
                        Moti_TC += (res.replacementcost * gov.subPercent + res.relocationcost)/((1 + gov.disRate) ** i)
                        # Moti_TC += (res.replacementcost * gov.subPercent + res.replacementcost + res.relocationcost) / ((1 + gov.disRate) ** i)

                ## calculate the benefit and cost of individually optimized subsidized relocation, calculation follows a similar logic as the fixed-subsidy
                if i < res.optmotiMoveYear:
                    Opt_Moti_EAD += res.ead[i] / ((1 + gov.disRate) ** i)
                else:
                    Opt_Moti_EAD += 0

                # calculate the ead reduction and cost
                if i == res.optmotiMoveYear and res.optmotiMoveYear < res.selfMoveYear:
                    if res.selfMoveYear < calLength:
                        EAD_Reduction_OS_SR += sum([discount(res.ead[j], gov.disRate, j) for j in range(i, res.selfMoveYear)])
                    else:
                        EAD_Reduction_OS_SR += sum([discount(res.ead[j], gov.disRate, j) for j in range(i, i + decLength)])

                    # a relocation subsidy occurs only when the optimal-relocation-year is strictly earlier than the self-relocation year
                    if res.optmotiMoveYear < res.selfMoveYear:
                        Opt_Moti_Subsidy += res.Subsidyneeded[i] / ((1 + gov.disRate) ** i)
                        #old
                        # Opt_Moti_TC += res.Subsidyneeded[i] / ((1 + gov.disRate) ** i)
                        # new
                        Opt_Moti_TC += (res.Subsidyneeded[i] + res.relocationcost) / ((1 + gov.disRate) ** i)
        else:
            for res in resList:
                ## calculate the benefit and cost of self-move
                if i < res.selfMoveYear:
                    Self_EAD += res.ead[i] / ((1 + gov.disRate) ** i)
                else:
                    Self_EAD += 0
                # since under the self-move mode, the government will not provide any subsidy but bear the flood loss, the subsidy and totalcost will be 0
                ## calculate the benefit and cost of fixed-subsidy percentage relocation
                if i < res.motiMoveYear:
                    Moti_EAD += res.ead[i] / ((1 + gov.disRate) ** i)
                else:
                    Moti_EAD += 0

                if i < res.optmotiMoveYear:
                    Opt_Moti_EAD += res.ead[i] / ((1 + gov.disRate) ** i)
                else:
                    Opt_Moti_EAD += 0

        benefit_cost_year['EAD_Reduction_SR_NoRelocation'].append(EAD_Reduction_SR_NoRelocation)
        benefit_cost_year['Original_EAD'].append(Original_EAD)
        benefit_cost_year['Self_EAD'].append(Self_EAD)
        benefit_cost_year['Self_Subsidy'].append(Self_Subsidy)
        benefit_cost_year['Self_TC'].append(Self_TC)
        benefit_cost_year['Moti_EAD'].append(Moti_EAD)
        benefit_cost_year['Moti_Subsidy'].append(Moti_Subsidy)
        benefit_cost_year['Moti_TC'].append(Moti_TC)
        benefit_cost_year['Opt_Moti_EAD'].append(Opt_Moti_EAD)
        benefit_cost_year['Opt_Moti_Subsidy'].append(Opt_Moti_Subsidy)
        benefit_cost_year['Opt_Moti_TC'].append(Opt_Moti_TC)
        benefit_cost_year['EAD_Reduction_FS_SR'].append(EAD_Reduction_FS_SR)
        benefit_cost_year['EAD_Reduction_OS_SR'].append(EAD_Reduction_OS_SR)

    benefit_cost_result = pd.DataFrame(benefit_cost_year)
    return benefit_cost_result

def Relocation_Outcome(resList, selected_per, landscape):
    resident_outcome = []
    for res in resList:
        res_info = {}
        res_info['structure_id'] = res.idx
        res_info['RC1'] = res.replacementcost
        res_info['RC2'] = res.relocationcost
        res_info['mhi'] = res.mhi_ratio
        res_info['self_year'] = res.selfMoveYear
        res_info['fixed_year'] = res.motiMoveYear
        res_info['optimal_year'] = res.optmotiMoveYear
        res_info['fixed_flag'] = (1 if res.motiMoveFlag == 1 else 0)
        res_info['fixed_subsidy'] = (res.replacementcost * selected_per if res.motiMoveFlag == 1 else 0)
        res_info['optimal_flag'] = (1 if res.optimotiFlag == 1 else 0)
        res_info['optimal_subsidy'] = (res.Subsidyneeded[res.optmotiMoveYear] if res.optimotiFlag == 1 else 0)

        resident_outcome.append(res_info)
    resident_outcome = pd.DataFrame(resident_outcome)
    return resident_outcome
def analysis_mhi(gov, resList, mhi_list, mode, subPercent, calLength):
    mhi_result = {}
    for mhi in mhi_list:
        mhi_result[mhi] = {}
        mhi_result[mhi]['Total_Relocation_Num'] = 0
        mhi_result[mhi]['Total_Subsidy_Amount'] = 0
        mhi_result[mhi]['Total_Cost'] = 0

        mhi_result[mhi]['Relocation_Year'] = []
        mhi_result[mhi]['Percent_Relocation'] = 0
        mhi_result[mhi]['Avg_Subsidy_Amount'] = 0
        mhi_result[mhi]['Avg_TC'] = 0

    if mode == 'Opt':
        for mhi in mhi_list:
            mhi_number = 0
            motivated_relocation_num = 0
            for res in resList:
                if res.mhi_ratio == mhi:
                    mhi_number += 1
                    if res.optmotiMoveYear < calLength:
                        mhi_result[mhi]['Total_Relocation_Num'] += 1
                        mhi_result[mhi]['Relocation_Year'].append(res.optmotiMoveYear)
                        if res.optimotiFlag == True:
                            motivated_relocation_num += 1
                            mhi_result[mhi]['Total_Subsidy_Amount'] += res.Subsidyneeded[res.optmotiMoveYear]/(1 + gov.disRate)**res.optmotiMoveYear
                            mhi_result[mhi]['Total_Cost'] += (res.Subsidyneeded[res.optmotiMoveYear] + res.relocationcost) / (1 + gov.disRate) ** res.optmotiMoveYear
                            # mhi_result[mhi]['Total_Cost'] += (res.Subsidyneeded[res.optmotiMoveYear] + res.replacementcost + res.relocationcost)/(1 + gov.disRate)**res.optmotiMoveYear
            mhi_result[mhi]['Percent_Relocation'] = mhi_result[mhi]['Total_Relocation_Num'] / (mhi_number+1)
            mhi_result[mhi]['Avg_Subsidy_Amount'] = mhi_result[mhi]['Total_Subsidy_Amount'] / (motivated_relocation_num + 1)
            mhi_result[mhi]['Avg_TC'] = mhi_result[mhi]['Total_Cost'] / (motivated_relocation_num + 1)

    elif mode == 'Fix':
        for mhi in mhi_list:
            mhi_number = 0
            motivated_relocation_num = 0
            for res in resList:
                if res.mhi_ratio == mhi:
                    mhi_number += 1
                    if res.motiMoveYear < calLength:
                        mhi_result[mhi]['Total_Relocation_Num'] += 1
                        mhi_result[mhi]['Relocation_Year'].append(res.motiMoveYear)
                        if res.motiMoveFlag == True:
                            motivated_relocation_num += 1
                            mhi_result[mhi]['Total_Subsidy_Amount'] += res.replacementcost * subPercent/(1 + gov.disRate)**res.motiMoveYear
                            mhi_result[mhi]['Total_Cost'] += (res.replacementcost * subPercent + res.relocationcost) / (1 + gov.disRate) ** res.optmotiMoveYear
                            # mhi_result[mhi]['Total_Cost'] += (res.replacementcost * (1 + subPercent) + res.relocationcost)/(1 + gov.disRate)**res.motiMoveYear

            mhi_result[mhi]['Percent_Relocation'] = mhi_result[mhi]['Total_Relocation_Num'] / (mhi_number+1)
            mhi_result[mhi]['Avg_Subsidy_Amount'] = mhi_result[mhi]['Total_Subsidy_Amount'] / (motivated_relocation_num + 1)
            mhi_result[mhi]['Avg_TC'] = mhi_result[mhi]['Total_Cost'] / (motivated_relocation_num + 1)
    else:
        for mhi in mhi_list:
            mhi_number = 0
            for res in resList:
                if res.mhi_ratio == mhi:
                    mhi_number += 1
                    if res.selfMoveFlag == 1:
                        mhi_result[mhi]['Total_Relocation_Num'] += 1
                        mhi_result[mhi]['Total_Subsidy_Amount'] += 0
                        mhi_result[mhi]['Total_Cost'] += res.relocationcost/(1 + gov.disRate)**res.selfMoveYear
                        mhi_result[mhi]['Relocation_Year'].append(res.motiMoveYear)

            mhi_result[mhi]['Percent_Relocation'] = mhi_result[mhi]['Total_Relocation_Num'] / (mhi_number+1)
            mhi_result[mhi]['Avg_Subsidy_Amount'] = 0
            mhi_result[mhi]['Avg_TC'] = mhi_result[mhi]['Total_Cost'] / (mhi_result[mhi]['Total_Relocation_Num'] + 1)

    mhi_result_output = pd.DataFrame(mhi_result).T
    return mhi_result_output

