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

        gov.selfRelocationNum.append(count_self)
        gov.motiRelocationNum.append(count_moti)
        gov.optMotiRelocationNum.append(count_opt_moti)

        relocation_num['Year'].append(i)
        relocation_num['Self_relocation'].append(count_self)
        relocation_num['Moti_relocation'].append(count_moti)
        relocation_num['Opt_moti_relocation'].append(count_opt_moti)
    relocation_num = pd.DataFrame(relocation_num, columns = ['Year','Self_relocation', 'Moti_relocation','Opt_moti_relocation'])
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
        adoption_rate['Self_Move_Adopt'].append(sum(gov.selfRelocationNum[:i])/resnum)
        adoption_rate['Fixmoti_Move_Adopt'].append(sum(gov.motiRelocationNum[:i])/resnum)
        adoption_rate['Opt_Subsidy_Move_Adopt'].append(sum(gov.optMotiRelocationNum[:i])/resnum)
    adoption_rate_table = pd.DataFrame(adoption_rate)
    return adoption_rate_table

def benefit_cost(gov, resList, calLength):
    benefit_cost_year = {}
    benefit_cost_year['Year'] = []
    benefit_cost_year['Self_EAD'] = []
    benefit_cost_year['Self_Subsidy'] = []
    benefit_cost_year['Self_TC'] = []
    benefit_cost_year['Moti_EAD'] = []
    benefit_cost_year['Moti_Subsidy'] = []
    benefit_cost_year['Moti_TC'] = []
    benefit_cost_year['Opt_Moti_EAD'] = []
    benefit_cost_year['Opt_Moti_Subsidy'] = []
    benefit_cost_year['Opt_Moti_TC'] = []
    for i in range(calLength):
        benefit_cost_year['Year'].append(i)
        Self_EAD, Self_Subsidy, Self_TC = 0, 0, 0
        Moti_EAD, Moti_Subsidy, Moti_TC = 0, 0, 0
        Opt_Moti_EAD, Opt_Moti_Subsidy, Opt_Moti_TC = 0, 0, 0
        for res in resList:
            ## calculate the benefit and cost of self-move
            if i < res.selfMoveYear:
                Self_EAD += res.ead[i]/((1 + gov.disRate) ** i)
            else:
                Self_EAD += 0
            # since under the self-move mode, the government will not provide any subsidy but bear the flood loss, the subsidy and totalcost will be 0
            ## calculate the benefit and cost of fixed-subsidy percentage relocation
            if i < res.motiMoveYear:
                Moti_EAD += res.ead[i]/((1 + gov.disRate) ** i)
            else:
                Moti_EAD += 0
            if i == res.motiMoveYear:
                Moti_Subsidy += res.replacementcost * gov.subPercent/((1 + gov.disRate) ** i)
                Moti_TC += (res.replacementcost * gov.subPercent + res.replacementcost + res.relocationcost)/((1 + gov.disRate) ** i)
            ## calculate the benefit and cost of individually optimized subsidized relocation
            if i < res.optmotiMoveYear:
                Opt_Moti_EAD += res.ead[i]/((1 + gov.disRate) ** i)
            else:
                Opt_Moti_EAD += 0
            if i == res.optmotiMoveYear:
                Opt_Moti_Subsidy += res.Subsidyneeded[i]/((1 + res.disRate) ** i)
                Opt_Moti_TC += (res.Subsidyneeded[i] + res.replacementcost + res.relocationcost)/((1 + gov.disRate) ** i)
        benefit_cost_year['Self_EAD'].append(Self_EAD)
        benefit_cost_year['Self_Subsidy'].append(Self_Subsidy)
        benefit_cost_year['Self_TC'].append(Self_TC)
        benefit_cost_year['Moti_EAD'].append(Moti_EAD)
        benefit_cost_year['Moti_Subsidy'].append(Moti_Subsidy)
        benefit_cost_year['Moti_TC'].append(Moti_TC)
        benefit_cost_year['Opt_Moti_EAD'].append(Opt_Moti_EAD)
        benefit_cost_year['Opt_Moti_Subsidy'].append(Opt_Moti_Subsidy)
        benefit_cost_year['Opt_Moti_TC'].append(Opt_Moti_TC)
    benefit_cost_result = pd.DataFrame(benefit_cost_year)
    return benefit_cost_result


def analysis_mhi(resList, mhi_list, mode, subPercent, calLength):
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
            for res in resList:
                if res.mhi_ratio == mhi:
                    mhi_number += 1
                    if res.optimotiFlag == 1:
                        mhi_result[mhi]['Total_Relocation_Num'] += 1
                        mhi_result[mhi]['Total_Subsidy_Amount'] += res.Subsidyneeded[res.optmotiMoveYear]
                        mhi_result[mhi]['Total_Cost'] += res.Subsidyneeded[res.optmotiMoveYear] + res.replacementcost + res.relocationcost
                        mhi_result[mhi]['Relocation_Year'].append(res.optmotiMoveYear)

            mhi_result[mhi]['Percent_relocation'] = mhi_result[mhi]['Total_Relocation_Num']/(mhi_number+1)
            mhi_result[mhi]['Avg_Subsidy_Amount'] = mhi_result[mhi]['Total_Subsidy_Amount']/mhi_result[mhi]['Total_Relocation_Num']
            mhi_result[mhi]['Avg_TC'] = mhi_result[mhi]['Total_Cost']/mhi_result[mhi]['Total_Relocation_Num']

    elif mode == 'Fix':
        for mhi in mhi_list:
            mhi_number = 0
            for res in resList:
                if res.mhi_ratio == mhi:
                    mhi_number += 1
                    if res.motiMoveFlag == 1:
                        mhi_result[mhi]['Total_Relocation_Num'] += 1
                        mhi_result[mhi]['Total_Subsidy_Amount'] += res.replacementcost * subPercent
                        mhi_result[mhi]['Total_Cost'] += res.replacementcost * (1 + subPercent) + res.relocationcost
                        mhi_result[mhi]['Relocation_Year'].append(res.motiMoveYear)

            mhi_result[mhi]['Percent_relocation'] = mhi_result[mhi]['Total_Relocation_Num']/(mhi_number+1)
            mhi_result[mhi]['Avg_Subsidy_Amount'] = mhi_result[mhi]['Total_Subsidy_Amount']/mhi_result[mhi]['Total_Relocation_Num']
            mhi_result[mhi]['Avg_TC'] = mhi_result[mhi]['Total_Cost']/mhi_result[mhi]['Total_Relocation_Num']

    mhi_result_output = pd.DataFrame(mhi_result).T
    return mhi_result_output


