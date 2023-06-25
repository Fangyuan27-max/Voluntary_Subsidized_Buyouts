import copy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

base_dir = './The result output/'
num_file_path_30 = 'Relocation_num_each_year_30.csv'
adoption_rate_path_30 = 'Adoption_rate_30.csv'
bcr_path_30 = 'benefit_cost_result_30.csv'

Relocation_num_30 = pd.read_csv(base_dir + num_file_path_30)
Adoption_rate_30 = pd.read_csv(base_dir + adoption_rate_path_30)
Benefit_cost_30 = pd.read_csv(base_dir + bcr_path_30)

num_file_path_50 = 'Relocation_num_each_year_50.csv'
adoption_rate_path_50 = 'Adoption_rate_50.csv'
bcr_path_50 = 'benefit_cost_result_50.csv'

Relocation_num_50 = pd.read_csv(base_dir + num_file_path_50)
Adoption_rate_50 = pd.read_csv(base_dir + adoption_rate_path_50)
Benefit_cost_50 = pd.read_csv(base_dir + bcr_path_50)

mhi_result_path = 'mhi_result.csv'
mhi_result = pd.read_csv(base_dir + mhi_result_path)

# A function to plot the bar chart of the number of relocation every year
def Bar_relocation(Relocation_num, calLength):
    x = Relocation_num['Year']
    y1 = Relocation_num['Self_relocation']
    y2 = Relocation_num['Moti_relocation']
    y3 = Relocation_num['Opt_moti_relocation']

    # plot the relocation by year, however, the results is too dense and have a sharp contrast
    # bar_width = 1 / 4
    # plt.figure()
    # plt.bar(x, y1, width=bar_width, label="Self_Relo")
    # plt.bar(x + bar_width, y2, width=bar_width, label="Fixed_Subsidy_Relo")
    # plt.bar(x + 2 * bar_width, y3, width=bar_width, label='Opt_Subsidy_Relo')
    # plt.xlabel('Year')
    # plt.ylabel('The number of relocation')
    # plt.title('The relocation number each year under three relocation modes')
    # plt.legend()
    # plt.xticks(x + bar_width, x)
    # plt.show()

    # aggregated the relocation number to a 5-year or 10-year time period
    time_interval = 5
    x1 = list(np.arange(0, calLength + 5, time_interval))
    y1_agg = []
    y2_agg = []
    y3_agg = []
    for i in np.arange(len(x1)-1):
        y1_agg.append(Relocation_num[(Relocation_num['Year'] >= x1[i])&(Relocation_num['Year'] < x1[i+1])]['Self_relocation'].sum())
        y2_agg.append(Relocation_num[(Relocation_num['Year'] >= x1[i])&(Relocation_num['Year'] < x1[i + 1])]['Moti_relocation'].sum())
        y3_agg.append(Relocation_num[(Relocation_num['Year'] >= x1[i])&(Relocation_num['Year'] < x1[i + 1])]['Opt_moti_relocation'].sum())

    # plot the relocation by year, however, the results is too dense and have a sharp contrast
    bar_width = 5 / 4
    x2 = np.array(x1[1:])
    plt.figure()

    plt.bar(x2 - bar_width, np.array(y1_agg), width=bar_width, label="Self_Relo", color = '#D3E2B7')
    plt.bar(x2, np.array(y2_agg), width=bar_width, label="Fixed_Subsidy_Relo", color = '#F7C97E')
    plt.bar(x2 + bar_width, np.array(y3_agg), width=bar_width, label='Opt_Subsidy_Relo', color = '#ECA8A9')

    plt.xlabel('Year')
    plt.ylabel('The number of relocation')
    plt.title('The relocation number each year under three relocation modes')
    plt.legend()
    plt.xticks(x2)
    plt.show()

# Bar_relocation(Relocation_num_30, 30)
# Bar_relocation(Relocation_num_50, 50)

# A function to plot the stack line chart of the adoption rate
def Line_adoption(Adoption, calLength):
    x = Adoption['Year']
    y1 = Adoption['Self_Move_Adopt']
    y2 = Adoption['Fixmoti_Move_Adopt']
    y3 = Adoption['Opt_Subsidy_Move_Adopt']

    # plot the cumulative adoption rate
    plt.figure()

    plt.stackplot(x, y1, y2, y3, labels = ["Self_Relo", "Fixed_Subsidy_Relo", 'Opt_Subsidy_Relo'],
                  colors=['#D3E2B7', '#F7C97E', '#ECA8A9'])

    # plt.plot(x, y1, width=bar_width, label="Self_Relo")
    # plt.plot(x , y2, width=bar_width, label="Fixed_Subsidy_Relo")
    # plt.plot(x, y3, width=bar_width, label='Opt_Subsidy_Relo')
    plt.xlabel('Year')
    plt.ylabel('The accumulated adoption rate')
    plt.title('The accumulative relocation rate under three relocation modes')
    plt.legend(loc = 'upper left')
    x1 = np.arange(0, calLength+5, 5)
    plt.xticks(x1)
    plt.xlim(0, calLength)
    plt.show()

# Line_adoption(Adoption_rate_30, 30)
# Line_adoption(Adoption_rate_50, 50)

# A function to plot the EAD(bar chart) and benefit/cost ratio(line chart) simultaneously
def Bar_EAD_Line_BC_WO_Discounting(Benefit_cost, calLength):
    x = Benefit_cost['Year']
    x1 = np.arange(0, calLength+5, 5)
    x2 = x1[1:]

    self_EAD = []
    fixmoti_EAD = []
    optmoti_EAD = []

    fixmoti_TC = []
    optmoti_TC = []

    # aggregate the flood loss, and total cost
    for i in range(len(x1)-1):
        self_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Self_EAD'].sum())
        fixmoti_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Moti_EAD'].sum())
        optmoti_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Opt_Moti_EAD'].sum())

        fixmoti_TC.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Moti_TC'].sum())
        optmoti_TC.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Opt_Moti_TC'].sum())

    BC_fix_moti = []
    BC_opt_moti = []
    # calculate the benefit/cost ratio
    for i in range(len(x1)-1):
        BC_fix_moti.append(min((self_EAD[i] - fixmoti_EAD[i])/fixmoti_TC[i], 5))
        BC_opt_moti.append(min((self_EAD[i] - optmoti_EAD[i])/optmoti_TC[i], 5))

    fig, ax1 = plt.subplots()
    bar_width = 5/4
    ax1.bar(x2 - bar_width, self_EAD, width=bar_width, label="Self_Relo", color='#D3E2B7')
    ax1.bar(x2, fixmoti_EAD, width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    ax1.bar(x2 + bar_width, optmoti_EAD, width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')
    ax1.set_ylabel('EAD every five years')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x2)
    ax1.set_ylim(0, 8e9)
    ax1.legend(bbox_to_anchor=(0.60, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x2, BC_fix_moti, marker = 'o', color='#D47828')
    ax2.plot(x2 + bar_width, BC_opt_moti, marker = 'o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every five years')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every five years")
    plt.show()
# Bar_EAD_Line_BC_WO_Discounting(Benefit_cost_30, 30)
# Bar_EAD_Line_BC_WO_Discounting(Benefit_cost_50, 50)

def discount_value(value, year, rate):
    return value / (1 + rate) ** year
def Bar_EAD_Line_BC_Discounting(Benefit_cost, DG, calLength):
    # step 1: discounted to year 0
    Benefit_cost = copy.deepcopy(Benefit_cost)
    column_list = list(Benefit_cost.columns)[2:]
    for column in column_list:
        Benefit_cost[column] = Benefit_cost.apply(lambda row: discount_value(row[column], row['Year'], DG), axis=1)

    x = Benefit_cost['Year']
    x1 = np.arange(0, calLength+5, 5)
    x2 = x1[1:]

    self_EAD = []
    fixmoti_EAD = []
    optmoti_EAD = []

    fixmoti_TC = []
    optmoti_TC = []

    # aggregate the flood loss, and total cost
    for i in range(len(x1)-1):
        self_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Self_EAD'].sum())
        fixmoti_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Moti_EAD'].sum())
        optmoti_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Opt_Moti_EAD'].sum())

        fixmoti_TC.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Moti_TC'].sum())
        optmoti_TC.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Opt_Moti_TC'].sum())

    BC_fix_moti = []
    BC_opt_moti = []
    # calculate the benefit/cost ratio
    for i in range(len(x1)-1):
        BC_fix_moti.append(min((self_EAD[i] - fixmoti_EAD[i])/fixmoti_TC[i], 5))
        BC_opt_moti.append(min((self_EAD[i] - optmoti_EAD[i])/optmoti_TC[i], 5))

    fig, ax1 = plt.subplots()
    bar_width = 5/4
    ax1.bar(x2 - bar_width, self_EAD, width=bar_width, label="Self_Relo", color='#D3E2B7')
    ax1.bar(x2, fixmoti_EAD, width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    ax1.bar(x2 + bar_width, optmoti_EAD, width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')
    ax1.set_ylabel('EAD every five years')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x2)
    ax1.set_ylim(0, 8e9)
    ax1.legend(bbox_to_anchor=(0.60, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x2, BC_fix_moti, marker = 'o', color='#D47828')
    ax2.plot(x2 + bar_width, BC_opt_moti, marker = 'o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every five years')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every five years_Discounted")
    plt.show()

# Bar_EAD_Line_BC_Discounting(Benefit_cost_30, 0.05, 30)
#
# Bar_EAD_Line_BC_Discounting(Benefit_cost_50, 0.05, 50)


# a function to display the variable vs mhi_ratio; the variable that can be used include
#         mhi_result[mhi]['Total_Relocation_Num'] = 0
#         mhi_result[mhi]['Total_Subsidy_Amount'] = 0
#         mhi_result[mhi]['Total_Cost'] = 0
#
#         mhi_result[mhi]['Relocation_Year'] = []
#         mhi_result[mhi]['Percent_Relocation'] = 0
#         mhi_result[mhi]['Avg_Subsidy_Amount'] = 0
#         mhi_result[mhi]['Avg_TC'] = 0
def mhi_analysis_visualization(mhi_result, column_name):
    mhi_list = list(mhi_result.iloc[:, 0])
    # print(mhi_list)
    x = np.arange(1, len(mhi_list)+1, 1)
    value_list = mhi_result[column_name]

    plt.figure()
    bar_width = 1/2
    plt.bar(x, value_list, width=bar_width, color='#ECA8A9')

    plt.xlabel('Mhi_Ratio')
    plt.ylabel(column_name)
    plt.title(column_name + ' VS MHI_Ratio')
    plt.xticks(x, mhi_list)

    for i, value in enumerate(value_list):
        if column_name == 'Percent_Relocation':
            plt.text(i+1, value, str('%0.2f'%value), ha='center', va='bottom')
        else:
            plt.text(i + 1, value, str('%0.2e' % value), ha='center', va='bottom')
    plt.show()

# mhi_analysis_visualization(mhi_result, 'Total_Relocation_Num')
# mhi_analysis_visualization(mhi_result, 'Total_Subsidy_Amount')
# mhi_analysis_visualization(mhi_result, 'Total_Cost')
# mhi_analysis_visualization(mhi_result, 'Percent_Relocation')
# mhi_analysis_visualization(mhi_result, 'Avg_Subsidy_Amount')
# mhi_analysis_visualization(mhi_result, 'Avg_TC')

def Relocation_year_each_mhi(mhi_result, colname, calLength):
    mhi_list = list(mhi_result.iloc[:, 0])
    for mhi in mhi_list:
        figtitle = 'Relocation Num Each Year for Mhi_ratio' + str(mhi)
        relocation_year = list(mhi_result[mhi_result.iloc[:, 0] == mhi][colname])[0]
        decision_year = np.arange(0, calLength, 1)
        year_count = []
        for year in decision_year:
            year_count.append(relocation_year.count(str(year)))

        plt.bar(decision_year, year_count)
        plt.xlabel('Year')
        plt.ylabel('Relocation Num')

        plt.title(figtitle)

        # for i, count in enumerate(year_count):
        #     plt.text(i, count, str(count), ha = 'center', va = 'bottom')
        plt.show()

Relocation_year_each_mhi(mhi_result, 'Relocation_Year', 30)

def Relocation_year_Aggregate(mhi_result, colname, calLength):
    mhi_list = list(mhi_result.iloc[:, 0])
    decision_year = np.arange(0, calLength, 1)
    relocation_result = {}
    figtitle = 'Relocation Num Each Year for Mhi_Ratio Groups'
    for year in decision_year:
        relocation_result[year] = {}
        relocation_result[year]['Year'] = year
        for mhi in mhi_list:
            relocation_year = list(mhi_result[mhi_result.iloc[:, 0] == mhi][colname])[0]
            relocation_result[year][mhi] = relocation_year.count(str(year))
    result = pd.DataFrame(relocation_result).T

    time_interval = 5
    x1 = list(np.arange(0, calLength + 5, time_interval))

    list_collection = {}
    for mhi in mhi_list:
        listname = str(mhi) + '_agg'
        list_collection[listname] = []

    for mhi in mhi_list:
        listname = str(mhi) + '_agg'
        for i in np.arange(len(x1) - 1):
            list_collection[listname].append(result[(result['Year'] >= x1[i]) & (result['Year'] < x1[i + 1])][mhi].sum())

    # plot the relocation by year, however, the results is too dense and have a sharp contrast
    bar_width = 5 / 6
    x2 = np.array(x1[1:])
    plt.figure()
    count = 0
    for mhi in mhi_list:
        count += 1
        listname = str(mhi) + '_agg'
        plt.bar(x2 + (count - 3)*bar_width, np.array(list_collection[listname]), width=bar_width, label = str(mhi))

    plt.xlabel('Year')
    plt.ylabel('Relocation Num')
    plt.title(figtitle)
    plt.legend()
    plt.show()

Relocation_year_Aggregate(mhi_result, 'Relocation_Year', 30)

