import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

base_dir = './The result output/'
num_file_path = 'Relocation_num_each_year.csv'
adoption_rate_path = 'Adoption_rate.csv'
bcr_path = 'benefit_cost_result.csv'

Relocation_num = pd.read_csv(base_dir + num_file_path)
Adoption_rate = pd.read_csv(base_dir + adoption_rate_path)
Benefit_cost = pd.read_csv(base_dir + bcr_path)

# A function to plot the bar chart of the number of relocation every year
def Bar_relocation(Relocation_num):
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
    x1 = list(np.arange(0, 55, time_interval))
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

Bar_relocation(Relocation_num)

# A function to plot the stack line chart of the adoption rate
def Line_adoption(Adoption):
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
    x1 = np.arange(0, 55, 5)
    plt.xticks(x1)
    plt.xlim(0,50)
    plt.show()

Line_adoption(Adoption_rate)


# A function to plot the EAD(bar chart) and benefit/cost ratio(line chart) simultaneously
def Bar_EAD_Line_BC(Benefit_cost):
    x = Benefit_cost['Year']
    x1 = np.arange(0, 55, 5)
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
    ax1.legend(bbox_to_anchor=(0.60, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x2, BC_fix_moti, marker = 'o', color='#D47828')
    ax2.plot(x2 + bar_width, BC_opt_moti, marker = 'o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every five years')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every five years")
    plt.show()
Bar_EAD_Line_BC(Benefit_cost)



