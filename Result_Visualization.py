import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

num_file_path = 'Relocation_num_each_year.csv'
adoption_rate_path = 'Adoption_rate.csv'
EAD_Cost_WO_Discounting_path = 'EAD_Cost.csv'
EAD_Cost_Discounting_path = 'EAD_Cost_Discounting.csv'

Relocation_num = pd.read_csv(num_file_path)
Adoption_rate = pd.read_csv(adoption_rate_path)
EAD_Cost_WO_Discounting = pd.read_csv(EAD_Cost_WO_Discounting_path)
EAD_Cost_Discounting = pd.read_csv(EAD_Cost_Discounting_path)

mhi_result_self_path = 'mhi_result_self.csv'
mhi_result_fix_path = 'mhi_result_fix.csv'
mhi_result_opt_path = 'mhi_result_opt.csv'

mhi_result_self = pd.read_csv(mhi_result_self_path)
mhi_result_fix = pd.read_csv(mhi_result_fix_path)
mhi_result_opt = pd.read_csv(mhi_result_opt_path)


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
    for i in np.arange(len(x1) - 1):
        y1_agg.append(Relocation_num[(Relocation_num['Year'] >= x1[i]) & (Relocation_num['Year'] < x1[i + 1])][
                          'Self_relocation'].sum())
        y2_agg.append(Relocation_num[(Relocation_num['Year'] >= x1[i]) & (Relocation_num['Year'] < x1[i + 1])][
                          'Moti_relocation'].sum())
        y3_agg.append(Relocation_num[(Relocation_num['Year'] >= x1[i]) & (Relocation_num['Year'] < x1[i + 1])][
                          'Opt_moti_relocation'].sum())

    # plot the relocation by year, however, the results is too dense and have a sharp contrast
    bar_width = 5 / 4
    x2 = np.array(x1[1:])
    plt.figure()

    plt.bar(x2 - bar_width, np.array(y1_agg), width=bar_width, label="Self_Relo", color='#D3E2B7')
    plt.bar(x2, np.array(y2_agg), width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    plt.bar(x2 + bar_width, np.array(y3_agg), width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')

    plt.xlabel('Year')
    plt.ylabel('The number of relocation')
    plt.title('The relocation number each year under three relocation modes')
    plt.legend()
    plt.xticks(x2)
    plt.show()


# Bar_relocation(Relocation_num, 30)

# A function to plot the stack line chart of the adoption rate
def Line_adoption(Adoption, calLength):
    x = Adoption['Year']
    y1 = Adoption['Self_Move_Adopt']
    y2 = Adoption['Fixmoti_Move_Adopt']
    y3 = Adoption['Opt_Subsidy_Move_Adopt']

    # plot the cumulative adoption rate
    plt.figure()

    plt.stackplot(x, y1, y2, y3, labels=["Self_Relo", "Fixed_Subsidy_Relo", 'Opt_Subsidy_Relo'],
                  colors=['#D3E2B7', '#F7C97E', '#ECA8A9'])

    # plt.plot(x, y1, width=bar_width, label="Self_Relo")
    # plt.plot(x , y2, width=bar_width, label="Fixed_Subsidy_Relo")
    # plt.plot(x, y3, width=bar_width, label='Opt_Subsidy_Relo')
    plt.xlabel('Year')
    plt.ylabel('The accumulated adoption rate')
    plt.title('The accumulative relocation rate under three relocation modes')
    plt.legend(loc='upper left')
    x1 = np.arange(0, calLength + 5, 5)
    plt.xticks(x1)
    plt.xlim(0, calLength)
    plt.show()


# Line_adoption(Adoption_rate, 30)
def discount(value, dr, length):
    return value / (1 + dr) ** length


# A function to plot the EAD(bar chart) and benefit/cost ratio(line chart) simultaneously
def Bar_EAD_Line_BC(Benefit_cost, calLength):
    x = Benefit_cost['Year']
    x1 = np.arange(0, calLength + 5, 5)
    x2 = x1[1:]

    self_EAD = []
    fixmoti_EAD = []
    optmoti_EAD = []

    fixmoti_TC = []
    optmoti_TC = []

    fixed_reduced_EAD = []
    opt_reduced_EAD = []
    # aggregate the flood loss, and total cost
    for i in range(len(x1) - 1):
        self_EAD.append(
            Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])]['Self_EAD'].sum())
        fixmoti_EAD.append(
            Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])]['Moti_EAD'].sum())
        optmoti_EAD.append(
            Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])]['Opt_Moti_EAD'].sum())

        fixmoti_TC.append(
            Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])]['Moti_TC'].sum())
        optmoti_TC.append(
            Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])]['Opt_Moti_TC'].sum())

        fixed_reduced_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])][
                                     'EAD_Reduction_FS'].sum())
        opt_reduced_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i]) & (Benefit_cost['Year'] < x1[i + 1])][
                                   'EAD_Reduction_OS'].sum())

    BC_fix_moti = []
    BC_opt_moti = []
    # calculate the benefit/cost ratio
    for i in range(len(x1) - 1):
        BC_fix_moti.append(min(fixed_reduced_EAD[i] / fixmoti_TC[i], 5))
        BC_opt_moti.append(min(opt_reduced_EAD[i] / optmoti_TC[i], 5))

    fig, ax1 = plt.subplots()
    bar_width = 5 / 4
    ax1.bar(x2 - bar_width, self_EAD, width=bar_width, label="Self_Relo", color='#D3E2B7')
    ax1.bar(x2, fixmoti_EAD, width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    ax1.bar(x2 + bar_width, optmoti_EAD, width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')
    ax1.set_ylabel('EAD every five years')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x2)
    ax1.legend(bbox_to_anchor=(0.60, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x2, BC_fix_moti, marker='o', color='#D47828')
    ax2.plot(x2 + bar_width, BC_opt_moti, marker='o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every five years')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every five years")
    plt.show()


# Bar_EAD_Line_BC(EAD_Cost_WO_Discounting, 30)
# Bar_EAD_Line_BC(EAD_Cost_Discounting, 30)


def Bar_EAD_Line_BC_Each_Year(Benefit_cost):
    x = Benefit_cost['Year']

    BC_fix_moti = []
    BC_opt_moti = []
    # calculate the benefit/cost ratio
    for i in range(len(x)):
        BC_fix_moti.append(min(Benefit_cost.loc[i, 'EAD_Reduction_FS'] / Benefit_cost.loc[i, 'Moti_TC'], 5))
        BC_opt_moti.append(min(Benefit_cost.loc[i, 'EAD_Reduction_OS'] / Benefit_cost.loc[i, 'Opt_Moti_TC'], 5))

    fig, ax1 = plt.subplots()
    bar_width = 1 / 4
    ax1.bar(x - bar_width, Benefit_cost['Self_EAD'], width=bar_width, label="Self_Relo", color='#D3E2B7')
    ax1.bar(x, Benefit_cost['Moti_EAD'], width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    ax1.bar(x + bar_width, Benefit_cost['Opt_Moti_EAD'], width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')
    ax1.set_ylabel('EAD every year')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x)
    plt.xticks(x, rotation=300)
    tick_spacing = 5
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.legend(bbox_to_anchor=(0.60, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x, BC_fix_moti, marker='o', color='#D47828')
    ax2.plot(x + bar_width, BC_opt_moti, marker='o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every year')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every year")
    plt.show()


Bar_EAD_Line_BC_Each_Year(EAD_Cost_WO_Discounting)
Bar_EAD_Line_BC_Each_Year(EAD_Cost_Discounting)


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
    x = np.arange(1, len(mhi_list) + 1, 1)
    value_list = mhi_result[column_name]

    plt.figure()
    bar_width = 1 / 2
    plt.bar(x, value_list, width=bar_width, color='#ECA8A9')

    plt.xlabel('Mhi_Ratio')
    plt.ylabel(column_name)
    plt.title(column_name + ' VS MHI_Ratio')
    plt.xticks(x, mhi_list)

    if column_name == 'Total_Relocation_Num':
        plt.ylim(0, 65000)
    elif column_name == 'Percent_Relocation':
        plt.ylim(0, 0.30)
    elif column_name == 'Total_Subsidy_Amount':
        plt.ylim(0, 2.5e10)
    elif column_name == 'Total_Cost':
        plt.ylim(0, 6.5e10)
    elif column_name == 'Avg_Subsidy_Amount':
        plt.ylim(0, 6e5)
    elif column_name == 'Avg_TC':
        plt.ylim(0, 2e6)

    for i, value in enumerate(value_list):
        plt.text(i + 1, value, str('%0.2e' % value), ha='center', va='bottom')
    plt.show()


# mhi_analysis_visualization(mhi_result_self, 'Total_Relocation_Num')
# mhi_analysis_visualization(mhi_result_self, 'Percent_Relocation')
# mhi_analysis_visualization(mhi_result_self, 'Total_Subsidy_Amount')
# mhi_analysis_visualization(mhi_result_self, 'Total_Cost')
# mhi_analysis_visualization(mhi_result_self, 'Avg_Subsidy_Amount')
# mhi_analysis_visualization(mhi_result_self, 'Avg_TC')

# def Relocation_year_each_mhi(mhi_result, colname, calLength):
#     mhi_list = list(mhi_result.iloc[:, 0])
#     print(mhi_list)
#
#     for mhi in mhi_list:
#         figtitle = 'Relocation Num Each Year for Mhi_ratio' + str(mhi)
#         relocation_year = list(mhi_result[mhi_result.iloc[:, 0] == mhi][colname])[0]
#         decision_year = np.arange(0, calLength, 1)
#         year_count = []
#         for year in decision_year:
#             year_count.append(relocation_year.count(str(year)))
#
#         plt.bar(decision_year, year_count)
#         plt.xlabel('Year')
#         plt.ylabel('Relocation_num')
#         plt.title(figtitle)
#         plt.show()
#
# Relocation_year_each_mhi(mhi_result_opt, 'Relocation_Year', 31)

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
            list_collection[listname].append(
                result[(result['Year'] >= x1[i]) & (result['Year'] < x1[i + 1])][mhi].sum())

    # plot the relocation by year, however, the results is too dense and have a sharp contrast
    bar_width = 5 / 6
    x2 = np.array(x1[1:])
    plt.figure()
    count = 0
    for mhi in mhi_list:
        count += 1
        listname = str(mhi) + '_agg'
        plt.bar(x2 + (count - 3) * bar_width, np.array(list_collection[listname]), width=bar_width, label=str(mhi))
    plt.ylim(0, 75000)
    plt.xlabel('Year')
    plt.ylabel('Relocation Num')
    plt.title(figtitle)

    plt.legend()
    plt.show()

# Relocation_year_Aggregate(mhi_result_self, 'Relocation_Year', 30)