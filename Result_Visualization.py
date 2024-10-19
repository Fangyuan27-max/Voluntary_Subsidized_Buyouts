import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

landscape = 7
data_path = './Results' + str(landscape) + '/'
num_file_path = data_path + 'Relocation_num_each_year_' + str(landscape) +'_gov3_res12.csv'
adoption_rate_path = data_path + 'Adoption_rate_' + str(landscape) + '_gov3_res12.csv'
EAD_Cost_Discounting_path = data_path + 'EADReduction_Cost_' + str(landscape) +'_gov3_res12.csv'
Relocation_outcome_path = data_path + 'Relocation_Outcome_Landscape'+ str(landscape) +'.csv'

Relocation_num = pd.read_csv(num_file_path)
Adoption_rate = pd.read_csv(adoption_rate_path)
EAD_Cost_Discounting = pd.read_csv(EAD_Cost_Discounting_path)
Relocation_Outcome = pd.read_csv(Relocation_outcome_path)

mhi_result_self_path = data_path + 'mhi_result_self_' + str(landscape) + '_gov3_res12.csv'
mhi_result_fix_path = data_path + 'mhi_result_fix_' + str(landscape) + '_gov3_res12.csv'
mhi_result_opt_path = data_path + 'mhi_result_opt_' + str(landscape) + '_gov3_res12.csv'

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
    plt.ylim(0, 4e4)
    plt.show()

# Bar_relocation(Relocation_num, 20)

# Showing the Accumulative relocation number
# the first step is to learn the relocation components in each year, the total number, self-relocation num, and motivated num

def Construct_Cumulative_Num(Relocation_Outcome):
    # unify the flag
    Relocation_Outcome.replace({True: 1, 'False': 0, '0': 0, '1': 1}, inplace=True)
    # print(Relocation_Outcome['fixed_flag'].unique())
    yearlist = list(np.arange(0, 20, 1))
    Fixed_Self = []
    Fixed_Motivated = []
    Optimal_Self = []
    Optimal_Motivated = []
    for year in yearlist:
        # obtain the fixed data
        Fixed_df = Relocation_Outcome[Relocation_Outcome['fixed_year'] == year]
        Fixed_Self.append(Fixed_df[Fixed_df['fixed_flag'] == 0].shape[0])
        Fixed_Motivated.append(Fixed_df[Fixed_df['fixed_flag'] == 1].shape[0])
        # obtain the optimal data
        Optimal_df = Relocation_Outcome[Relocation_Outcome['optimal_year'] == year]
        Optimal_Self.append(Optimal_df[Optimal_df['optimal_flag'] == 0].shape[0])
        Optimal_Motivated.append(Optimal_df[Optimal_df['optimal_flag'] == 1].shape[0])
    return Fixed_Self, Fixed_Motivated, Optimal_Self, Optimal_Motivated

# Define Colors
colors = {
    'darkblue': '#004488',
    'lightblue': '#47abd8',
    'darkred' : '#BB5566',
    'lightred': '#febdbb'
}

def Cumulative_Relocation_num(Self, Motivated, yearlist, label1, label2, color1, color2, title):
    # make
    x = yearlist
    y1 = np.array(Self)
    y2 = np.array(Motivated)
    y3 = y1 + y2

    self_relocation = y1.cumsum()
    motivated_relocation = y3.cumsum()

    bar_width = 0.2  # the width of the bars
    width = 0.22

    # Bar Plot - every year
    fig = plt.plot()
    # fig, ax = plt.subplots(figsize=(10, 6))

    # plot the accumulated relocation number

    plt.plot(x, self_relocation, label = label1, color=colors[color1], marker = 'o')
    plt.plot(x, motivated_relocation, label=label2, color=colors[color2], marker = 'D')

    # Labeling, Legend etc.
    plt.xlabel('Years')
    plt.ylabel('Cumulative Relocation')
    plt.title(title)
    plt.xticks([h for h in x])  # Center the x-ticks between the two bars
    plt.legend(loc='upper left')

    # Display Plot
    plt.xlim(left = 0)
    plt.ylim(0, 50000)
    plt.tight_layout()
    plt.show()


yearlist = list(np.arange(0, 20, 1))
Fixed_Self, Fixed_Motivated, Optimal_Self, Optimal_Motivated = Construct_Cumulative_Num(Relocation_Outcome)
# print(Fixed_Self, Fixed_Motivated, Optimal_Self, Optimal_Motivated)
# Cumulative_Relocation_num(Fixed_Self, Fixed_Motivated, yearlist, "Self-Relocations (Fixed Subsidy)", "Total-Relocations (Fixed Subsidy)",
#                           'yellow', 'darkblue', "Accumulated Relocation of Fixed Subsidy Plan, Higher Scenario")
# Cumulative_Relocation_num(Optimal_Self, Optimal_Motivated, yearlist, "Self-Relocations (Optimal Subsidy)", "Total-Relocations (Optimal Subsidy)",
#                           'yellow', 'darkred', "Accumulated Relocation of Optimal Subsidy Plan, Higher Scenario")

def Cumulative_Relocation_In_One_Figure(Fixed_Self, Fixed_Motivated, Optimal_Self, Optimal_Motivated,yearlist, label1, label2, label3, label4, color1, color2,color3, color4, title):
    x = yearlist
    y1 = np.array(Fixed_Self)
    y2 = np.array(Fixed_Motivated)
    y3 = np.array(Optimal_Self)
    y4 = np.array(Optimal_Motivated)

    y5 = y1 + y2
    y6 = y3 + y4

    fixed_self_relocation = y1.cumsum()
    fixed_motivated_relocation = y5.cumsum()

    opt_self_relocation = y3.cumsum()
    opt_motivated_relocation = y6.cumsum()

    # Bar Plot - every year
    # fig = plt.plot()
    plt.figure(figsize = (8, 6))
    # fig, ax = plt.subplots(figsize=(10, 6))

    # plot the accumulated relocation number

    plt.plot(x, fixed_self_relocation, label=label1, color=colors[color1], marker='P')
    plt.plot(x, fixed_motivated_relocation, label=label2, color=colors[color2], marker='P')
    plt.plot(x, opt_self_relocation, label=label3, color=colors[color3], marker='o')
    plt.plot(x, opt_motivated_relocation, label=label4, color=colors[color4], marker='o')

    # Labeling, Legend etc.
    plt.xlabel('Year', fontsize = 24)
    plt.ylabel('Cumulative Relocations', fontsize = 24)
    plt.title(title, fontsize = 30)
    plt.xticks([h for h in x], fontsize = 18)  # Center the x-ticks between the two bars
    plt.yticks(fontsize = 18)
    plt.legend(loc='upper left',fontsize = 14, handlelength=1)

    plt.tick_params(axis='both',  # Apply to both x and y axes
                    which='both',  # Apply to both major and minor ticks
                    direction='in',  # 'in' for ticks pointing inwards
                    bottom=True,  # Apply changes to the bottom axis
                    top=False,  # Apply changes to the top axis
                    left=True,  # Apply changes to the left axis
                    right=False)

    # Display Plot
    plt.xlim(left=0)
    plt.ylim(0, 60000)
    plt.tight_layout()

    plt.show()

# Cumulative_Relocation_In_One_Figure(Fixed_Self, Fixed_Motivated, Optimal_Self, Optimal_Motivated,yearlist,
#                                     "Self Relocations | Fixed Subsidy", "Total Relocations | Fixed Subsidy", "Self Relocations | Optimal Subsidy",
#                                     "Total Relocations | Optimal Subsidy",'lightblue', 'darkblue','lightred', 'darkred', 'Lower Scenario')

# A function to plot the stack line chart of the adoption rate
def Line_adoption(Adoption, calLength):
    x = Adoption['Year']
    y1 = Adoption['Self_Move_Adopt']
    y2 = Adoption['Fixmoti_Move_Adopt']
    y3 = Adoption['Opt_Subsidy_Move_Adopt']

    # plot the cumulative adoption rate
    plt.figure()

    # plt.plot(x, y1, y2, y3, labels = ["Self_Relo", "Fixed_Subsidy_Relo", 'Opt_Subsidy_Relo'],
    #               colors=['#D3E2B7', '#F7C97E', '#ECA8A9'])

    plt.plot(x, y1, label="Self_Relo", color = '#D3E2B7')
    plt.plot(x , y2, label="Fixed_Subsidy_Relo", color = '#F7C97E')
    plt.plot(x, y3, label='Opt_Subsidy_Relo', color = '#ECA8A9')
    plt.xlabel('Year')
    plt.ylabel('The accumulated adoption rate')
    plt.title('The accumulative relocation rate under three relocation modes')
    plt.legend(loc = 'upper left')
    x1 = np.arange(0, calLength+5, 5)
    plt.xticks(x1)
    plt.xlim(0, calLength)
    plt.ylim(0, 0.15)
    plt.show()

# Line_adoption(Adoption_rate, 19)

# A function to plot the EAD(bar chart) and benefit/cost ratio(line chart) simultaneously
def Bar_EAD_Line_BC(Benefit_cost, calLength):
    x = Benefit_cost['Year']
    x1 = np.arange(0, calLength+5, 5)
    x2 = x1[1:]

    self_EAD = []
    fixmoti_EAD = []
    optmoti_EAD = []

    fixmoti_TC = []
    optmoti_TC = []
    
    fixed_reduced_EAD = []
    opt_reduced_EAD = []

    # aggregate the flood loss, and total cost
    for i in range(len(x1)-1):
        self_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Self_EAD'].sum())
        fixmoti_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Moti_EAD'].sum())
        optmoti_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Opt_Moti_EAD'].sum())

        fixmoti_TC.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Moti_TC'].sum())
        optmoti_TC.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['Opt_Moti_TC'].sum())

        fixed_reduced_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['EAD_Reduction_FS_SR'].sum())
        opt_reduced_EAD.append(Benefit_cost[(Benefit_cost['Year'] >= x1[i])&(Benefit_cost['Year'] < x1[i+1])]['EAD_Reduction_OS_SR'].sum())

    BC_fix_moti = []
    BC_opt_moti = []
    # calculate the benefit/cost ratio
    for i in range(len(x1)-1):
        BC_fix_moti.append(min(fixed_reduced_EAD[i]/(1+fixmoti_TC[i]), 5))
        BC_opt_moti.append(min(opt_reduced_EAD[i]/(1+optmoti_TC[i]), 5))

    fig, ax1 = plt.subplots()
    bar_width = 5/4
    ax1.bar(x2 - bar_width, self_EAD, width=bar_width, label="Self_Relo", color='#D3E2B7')
    ax1.bar(x2, fixmoti_EAD, width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    ax1.bar(x2 + bar_width, optmoti_EAD, width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')
    ax1.set_ylabel('EAD every five years')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x2, ['0-4','5-9','10-14','15-19'])
    ax1.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x2, BC_fix_moti, marker = 'o', color='#D47828')
    ax2.plot(x2 + bar_width, BC_opt_moti, marker = 'o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every five years')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every five years")
    plt.show()

# Bar_EAD_Line_BC(EAD_Cost_Discounting, 20)

def Bar_EAD_Line_BC_Each_Year(Benefit_cost):
    x = Benefit_cost['Year']
    x1 = np.arange(0, 20, 1)

    BC_fix_moti = []
    BC_opt_moti = []
    # calculate the benefit/cost ratio
    for i in range(len(x)):
        BC_fix_moti.append(min(Benefit_cost.loc[i, 'EAD_Reduction_FS_SR']/ (Benefit_cost.loc[i,'Moti_TC']+1), 5))
        BC_opt_moti.append(min(Benefit_cost.loc[i, 'EAD_Reduction_OS_SR']/ (Benefit_cost.loc[i,'Opt_Moti_TC']+1), 5))

    fig, ax1 = plt.subplots()
    bar_width = 1 / 4
    ax1.bar(x - bar_width, Benefit_cost['Self_EAD'], width=bar_width, label="Self_Relo", color='#D3E2B7')
    ax1.bar(x, Benefit_cost['Moti_EAD'], width=bar_width, label="Fixed_Subsidy_Relo", color='#F7C97E')
    ax1.bar(x + bar_width, Benefit_cost['Opt_Moti_EAD'], width=bar_width, label='Opt_Subsidy_Relo', color='#ECA8A9')
    ax1.set_ylabel('EAD every year')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x)
    plt.xticks(x, rotation = 300)
    tick_spacing = 5
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.legend(bbox_to_anchor=(0.60, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(x1, BC_fix_moti[0:20], marker='o', color='#D47828')
    ax2.plot(x1 + bar_width, BC_opt_moti[0:20], marker='o', color='#BF6070')
    ax2.set_ylabel('Benefit/Cost every year')
    ax2.set_ylim(0, 6)

    plt.title("EAD and Benefit/Cost every year")
    plt.show()

# Bar_EAD_Line_BC_Each_Year(EAD_Cost_Discounting)

# This function shows the perceived EAD difference between Subsidized plan and self-relocation
def Relative_EAD_Difference_Each_Year_Line(Benefit_cost, title):
    x = Benefit_cost['Year']
    x1 = np.arange(0, 51, 1)
    Self_EAD = Benefit_cost['Self_EAD'].tolist()
    Fixed_EAD = Benefit_cost['Moti_EAD'].tolist()
    Optimal_EAD = Benefit_cost['Opt_Moti_EAD'].tolist()
    Fixed_difference = [Self_EAD[i] - Fixed_EAD[i] for i in np.arange(0, 51, 1)]
    # transform the unit to billions
    Fixed_difference = [Fixed_difference[i]/1e9 for i in np.arange(0, 51, 1)]

    Optimal_difference = [Self_EAD[i] - Optimal_EAD[i] for i in np.arange(0, 51, 1)]
    Optimal_difference = [Optimal_difference[i] / 1e9 for i in np.arange(0, 51, 1)]

    # get the difference of self-relocation and fixed-relocation, as well as the difference between
    fig, ax1 = plt.subplots(figsize=(8,6))

    ax1.plot(x1, Fixed_difference, linewidth=2, label="Fixed Subsidy", color='#004488')
    ax1.plot(x1, Optimal_difference, linewidth=2, label='Optimal Subsidy', color='#994455')
    ax1.set_ylabel('Yearly EAD Reduction (in billions)', fontsize = 22)
    # ax1.set_xlabel('Year')
    ax1.set_xticks(x)
    plt.xticks(x, rotation = 300, fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlabel('Year', fontsize = 24)
    tick_spacing = 5
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper right', fontsize = 18, handlelength = 1)

    plt.title(title, fontsize = 30)
    plt.ylim(0, 1.0)
    plt.tight_layout()
    plt.tick_params(axis='both',  # Apply to both x and y axes
                    which='both',  # Apply to both major and minor ticks
                    direction='in',  # 'in' for ticks pointing inwards
                    bottom=True,  # Apply changes to the bottom axis
                    top=False,  # Apply changes to the top axis
                    left=True,  # Apply changes to the left axis
                    right=False)

    plt.show()

# Relative_EAD_Difference_Each_Year_Line(EAD_Cost_Discounting,'')

# This function visualizes the Absolute EAD difference
def Absolute_EAD_Difference_Each_Year_Line(Benefit_cost, title):
    x = Benefit_cost['Year']
    x1 = np.arange(0, 51, 1)
    Self_EAD = Benefit_cost['Original_EAD'].tolist()
    Fixed_EAD = Benefit_cost['Moti_EAD'].tolist()
    Optimal_EAD = Benefit_cost['Opt_Moti_EAD'].tolist()
    Fixed_difference = [Self_EAD[i] - Fixed_EAD[i] for i in np.arange(0, 51, 1)]
    Optimal_difference = [Self_EAD[i] - Optimal_EAD[i] for i in np.arange(0, 51, 1)]

    # get the difference of self-relocation and fixed-relocation, as well as the difference between
    fig, ax1 = plt.subplots()
    ax1.plot(x1, Fixed_difference, linewidth=2, label="Fixed_Subsidy_Relo", color='#004488')
    ax1.plot(x1, Optimal_difference, linewidth=2, label='Opt_Subsidy_Relo', color='#994455')
    ax1.set_ylabel('EAD Difference - Subsidized VS No Relocation')
    ax1.set_xlabel('Year')
    ax1.set_xticks(x)
    plt.xticks(x, rotation = 300)
    tick_spacing = 5
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper right')

    plt.title(title)
    plt.ylim(1e9, 2.75e9)
    plt.show()

# Absolute_EAD_Difference_Each_Year_Line(EAD_Cost_Discounting, 'Government Perceived Absolute EAD Difference Every Year')

def Accumulated_EAD_Reduction_Subsidy(Benefit_cost):
    # x = Benefit_cost['Year']
    x1 = np.arange(0, 21, 1)
    Fixed_subsidy = Benefit_cost['Moti_Subsidy'].tolist()
    Fixed_EAD_Reduction = Benefit_cost['EAD_Reduction_FS_SR'].tolist()
    Optimal_subsidy = Benefit_cost['Opt_Moti_Subsidy'].tolist()
    Optimal_EAD_Reduction = Benefit_cost['EAD_Reduction_OS_SR'].tolist()

    Accumulated_Fix_Subsidy = [sum(Fixed_subsidy[i] for i in range(0, j)) for j in range(len(Fixed_subsidy))]
    Accumulated_Fix_EADR = [sum(Fixed_EAD_Reduction[i] for i in range(0, j)) for j in range(len(Fixed_EAD_Reduction))]
    Accumulated_Opt_Subsidy = [sum(Optimal_subsidy[i] for i in range(0, j)) for j in range(len(Optimal_subsidy))]
    Accumulated_Opt_EADR = [sum(Optimal_EAD_Reduction[i] for i in range(0, j)) for j in range(len(Optimal_EAD_Reduction))]

    # get the difference of self-relocation and fixed-relocation, as well as the difference between
    fig, ax1 = plt.subplots()
    ax1.plot(Accumulated_Fix_Subsidy, Accumulated_Fix_EADR, linewidth=2, label="Fixed_Subsidy_Relo", color='#004488')
    ax1.plot(Accumulated_Opt_Subsidy, Accumulated_Opt_EADR, linewidth=2, label='Opt_Subsidy_Relo', color='#994455')
    ax1.set_ylabel('Accumulated EAD Reduction')
    ax1.set_xlabel('Accumulated Subsidy')

    plt.title("Accumulated EAD Reduction VS Accumulated Subsidy")
    plt.ylim(0, 1.6e10)
    plt.legend()
    plt.show()

# Accumulated_EAD_Reduction_Subsidy(EAD_Cost_Discounting)

def EAD_Reduction_Cost(Benefit_cost, calLength):
    x = np.arange(calLength)

    bar_width = 1 / 3
    fig, ax1 = plt.subplots()
    ax1.bar(x, list(Benefit_cost['EAD_Reduction_FS_SR'].values)[0:calLength], width=bar_width, label="EAD_Reduction", color='#FA7F6F')
    ax1.set_ylabel('EAD Reduction Each Year')
    ax1.set_xlabel('Year')
    ax1.set_ylim(0,1.5e10)
    ax1.set_xticks(x)
    plt.xticks(x, rotation = 300)
    tick_spacing = 5
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.bar(x + bar_width, list(Benefit_cost['Moti_TC'].values)[0:calLength], width=bar_width, label="Cost", color = '#8ECFC9')
    ax2.set_ylabel('Cost Each Year')
    ax2.set_ylim(0,1.5e10)
    ax2.legend(bbox_to_anchor=(0.85, 0.9), loc='upper right')

    plt.title("EAD Reduction VS Relocation Cost for Fixed Subsidy")
    plt.show()

    fig2, ax3 = plt.subplots()
    ax3.bar(x, list(Benefit_cost['EAD_Reduction_OS_SR'].values)[0:calLength], width=bar_width, label="EAD_Reduction",
            color='#FA7F6F')
    ax3.set_ylabel('EAD Reduction Each Year')
    ax3.set_xlabel('Year')
    ax3.set_ylim(0, 1.5e10)
    ax3.set_xticks(x)
    plt.xticks(x, rotation=300)
    tick_spacing = 5
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax3.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

    ax4 = ax3.twinx()
    ax4.bar(x + bar_width, list(Benefit_cost['Opt_Moti_TC'].values)[0:calLength], width=bar_width, label="Cost",
            color='#8ECFC9')
    ax4.set_ylabel('Cost Each Year')
    ax4.set_ylim(0, 1.5e10)
    ax4.legend(bbox_to_anchor=(0.85, 0.9), loc='upper right')
    plt.title("EAD Reduction VS Relocation Cost for Optimal Subsidy")
    plt.show()
# EAD_Reduction_Cost(EAD_Cost_Discounting, 21)

def Aggregated_EAD_Reduction_Cost(Benefit_cost, calLength):
    x = np.arange(0, calLength-1, 5)

    fixed_ead_reduction = []
    fixed_cost = []
    optimal_ead_reduction = []
    optimal_cost = []

    for i in x:
        fixed_ead_reduction.append(sum(list(Benefit_cost[Benefit_cost['Year'].isin([i+j for j in range(0, 5)])]['EAD_Reduction_FS_SR'].values)))
        fixed_cost.append(sum(list(Benefit_cost[Benefit_cost['Year'].isin([i+j for j in range(0, 5)])]['Moti_TC'].values)))
        optimal_ead_reduction.append(sum(list(Benefit_cost[Benefit_cost['Year'].isin([i+j for j in range(0, 5)])]['EAD_Reduction_OS_SR'].values)))
        optimal_cost.append(sum(list(Benefit_cost[Benefit_cost['Year'].isin([i+j for j in range(0, 5)])]['Opt_Moti_TC'].values)))

    bar_width = 1 / 3
    fig, ax1 = plt.subplots()
    ax1.bar(x, fixed_ead_reduction, width=bar_width, label="EAD_Reduction", color='#FA7F6F')
    ax1.set_ylabel('EAD Reduction Every Five Years')
    ax1.set_xlabel('Year')
    ax1.set_ylim(0,1.5e10)
    ax1.set_xticks(x, ['0-4', '5-9', '10-14', '15-19'])
    plt.xticks(x)
    ax1.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

    ax2 = ax1.twinx()
    ax2.bar(x + bar_width, fixed_cost, width=bar_width, label="Cost", color = '#8ECFC9')
    ax2.set_ylabel('Cost Every Five Years')
    ax2.set_ylim(0, 1.5e10)
    ax2.legend(bbox_to_anchor=(0.85, 0.9), loc='upper right')

    plt.title("EAD Reduction VS Relocation Cost for Fixed Subsidy")
    plt.show()

    fig2, ax3 = plt.subplots()
    ax3.bar(x, optimal_ead_reduction, width=bar_width, label="EAD_Reduction",
            color='#FA7F6F')
    ax3.set_ylabel('EAD Reduction Every Five Years')
    ax3.set_xlabel('Year')
    ax3.set_ylim(0, 1.5e10)
    ax3.set_xticks(x, ['0-4', '5-9', '10-14', '15-19'])
    plt.xticks(x)
    ax3.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

    ax4 = ax3.twinx()
    ax4.bar(x + bar_width, optimal_cost, width=bar_width, label="Cost",
            color='#8ECFC9')
    ax4.set_ylabel('Cost Every Five Years')
    ax4.set_ylim(0, 1.5e10)
    ax4.legend(bbox_to_anchor=(0.85, 0.9), loc='upper right')
    plt.title("EAD Reduction VS Relocation Cost for Optimal Subsidy")
    plt.show()

# Aggregated_EAD_Reduction_Cost(EAD_Cost_Discounting, 21)

## a function to represent the optimal subsidy amount as a percentage of the replacement cost
def subsidy_percentage(Optimal_Residents):
    Optimal_Residents['Percentage'] = Optimal_Residents['Opt_Subsidy']/Optimal_Residents['Replacement_cost']
    Optimal_Residents['Percentage'].hist(grid=False, color = '#ECA8A9')
    plt.title("Frequency of subsidy percentage")
    plt.xlabel("Subsidy amount/Replacement cost")
    plt.ylabel('Frequency')
    plt.ylim(0, 3000)
    plt.show()

# subsidy_percentage(Optimal_Relocation_Residents)

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
    x = np.arange(1, len(mhi_list)+1, 1)
    value_list = mhi_result[column_name]

    plt.figure()
    bar_width = 1/2
    plt.bar(x, value_list, width=bar_width, color='#ECA8A9')

    plt.xlabel('Mhi_Ratio')
    plt.ylabel(column_name)
    plt.title(column_name + ' VS MHI_Ratio')
    plt.xticks(x, mhi_list)

    if column_name == 'Total_Relocation_Num':
        plt.ylim(0, 30000)
    elif column_name == 'Percent_Relocation':
        plt.ylim(0, 0.12)
    elif column_name == 'Total_Subsidy_Amount':
        plt.ylim(0, 4e9)
    elif column_name == 'Total_Cost':
        plt.ylim(0, 4e9)
    elif column_name == 'Avg_Subsidy_Amount':
        plt.ylim(0, 4e5)
    elif column_name == 'Avg_TC':
        plt.ylim(0, 4e5)

    for i, value in enumerate(value_list):
        plt.text(i+1, value, str('%0.2e'%value), ha = 'center', va = 'bottom')
    plt.show()

# mhi_analysis_visualization(mhi_result_opt, 'Total_Relocation_Num')
# mhi_analysis_visualization(mhi_result_opt, 'Percent_Relocation')
# mhi_analysis_visualization(mhi_result_opt, 'Total_Subsidy_Amount')
# # mhi_analysis_visualization(mhi_result_opt, 'Total_Cost')
# mhi_analysis_visualization(mhi_result_opt, 'Avg_Subsidy_Amount')
# # mhi_analysis_visualization(mhi_result_opt, 'Avg_TC')

def Relocation_year_each_mhi(mhi_result, colname, calLength):
    mhi_list = list(mhi_result.iloc[:, 0])
    print(mhi_list)

    for mhi in mhi_list:
        figtitle = 'Relocation Num Each Year for Mhi_ratio' + str(mhi)
        relocation_year = list(mhi_result[mhi_result.iloc[:, 0] == mhi][colname])[0]
        decision_year = np.arange(0, calLength, 1)
        year_count = []
        for year in decision_year:
            year_count.append(relocation_year.count(str(year)))

        plt.bar(decision_year, year_count)
        plt.xlabel('Year')
        plt.ylabel('Relocation_num')
        plt.title(figtitle)
        plt.show()

# Relocation_year_each_mhi(mhi_result_opt, 'Relocation_Year', 21)

def Relocation_year_Aggregate(mhi_result, colname, calLength):
    mhi_list = list(mhi_result.iloc[:, 0])
    decision_year = np.arange(0, calLength, 1)
    relocation_result = {}
    figtitle = 'Relocation Num Every Five Years for Mhi_Ratio Groups'
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
    plt.ylim(0, 20000)
    plt.xlabel('Year')
    plt.ylabel('Relocation Num')
    plt.title(figtitle)

    plt.legend()
    plt.show()

# Relocation_year_Aggregate(mhi_result_self, 'Relocation_Year', 30)
def EAD_Reduction_Calculation(row, subsidymode):
    self_year = int(row['self_year'])
    motivated_year = int(row[subsidymode])
    if self_year < 21:
        EAD_list = [row[f'ead_fwoa_year{i:02}'] for i in range(motivated_year, self_year + 1)]
        EAD_Reduction = sum([EAD_list[i]/1.03**(i+motivated_year) for i in range(len(EAD_list))])
    else:
        EAD_list = [row[f'ead_fwoa_year{i:02}'] for i in range(motivated_year, motivated_year + 31)]
        EAD_Reduction = sum([EAD_list[i] / 1.03 ** (i + motivated_year) for i in range(len(EAD_list))])
    return EAD_Reduction

def Accumulated_EADReduction_Accumulated_Subsidy(Relocation_Outcome, EAD, gov_dr):
    # For the Fixed Subsidy Plan
    fixed_residents = Relocation_Outcome[Relocation_Outcome['fixed_flag'] == 1]
    fixed_residents['discounted_fixed_subsidy'] = fixed_residents['fixed_subsidy']/(1 + gov_dr)**fixed_residents['fixed_year']
    fixed_residents = fixed_residents.merge(EAD, on = 'structure_id', how = 'left')
    fixed_residents['EAD_Reduction'] = fixed_residents.apply(EAD_Reduction_Calculation, axis=1, subsidymode = 'fixed_year')
    fixed_residents['BCR_Fix'] = fixed_residents['EAD_Reduction']/fixed_residents['discounted_fixed_subsidy']

    fixed_residents.sort_values(by='BCR_Fix')

    fixed_discounted_subsidy = np.array(fixed_residents['discounted_fixed_subsidy'].tolist())
    EAD_reduction_fixed = np.array(fixed_residents['EAD_Reduction'].tolist())
    accumulated_fixed_subsidy = fixed_discounted_subsidy.cumsum()
    accumulated_fixed_ead_reduction = EAD_reduction_fixed.cumsum()
    plt.plot(accumulated_fixed_subsidy, accumulated_fixed_ead_reduction, label = 'Fixed')
    # plt.show()
    # print(fixed_discounted_subsidy[0:10])
    # print(EAD_reduction_fixed[0:10])

    # For the Optimal Subsidy Plan
    optimal_residents = Relocation_Outcome[Relocation_Outcome['optimal_flag'] == 1]
    optimal_residents['discounted_optimal_subsidy'] = optimal_residents['optimal_subsidy'] / (1 + gov_dr) ** optimal_residents['optimal_year']
    optimal_residents = optimal_residents.merge(EAD, on='structure_id', how='left')
    optimal_residents['EAD_Reduction'] = optimal_residents.apply(EAD_Reduction_Calculation, axis=1, subsidymode='optimal_year')

    optimal_residents['BCR_Opt'] = optimal_residents['EAD_Reduction'] / optimal_residents['discounted_optimal_subsidy']

    optimal_residents.sort_values(by='BCR_Opt')

    optimal_discounted_subsidy = np.array(optimal_residents['discounted_optimal_subsidy'].tolist())
    EAD_reduction_optimal = np.array(optimal_residents['EAD_Reduction'].tolist())

    accumulated_optimal_subsidy = optimal_discounted_subsidy.cumsum()
    accumulated_optimal_ead_reduction = EAD_reduction_optimal.cumsum()
    plt.plot(accumulated_optimal_subsidy, accumulated_optimal_ead_reduction, label = 'Optimal')
    plt.legend()
    plt.show()
    # print(optimal_discounted_subsidy[0:10])
    # print(EAD_reduction_optimal[0:10])

# EAD = pd.read_csv('./EAD_Data/landscape7_fragility1.0_pumping0.5.csv')
#     # For the Optimal Subsidy Plan
# Accumulated_EADReduction_Accumulated_Subsidy(Relocation_Outcome, EAD, 0.03)

def Accumulated_BCR_Accumulated_Cost(Relocation_Outcome_Data, EAD, gov_dr, title, cutoff_value):
    Relocation_Outcome = Relocation_Outcome_Data
    # For the Fixed Subsidy Plan
    fixed_residents = Relocation_Outcome[Relocation_Outcome['fixed_flag'] == 1]
    fixed_residents['discounted_fixed_subsidy'] = fixed_residents['fixed_subsidy'] / (1 + gov_dr) ** fixed_residents['fixed_year']
    fixed_residents = fixed_residents.merge(EAD, on='structure_id', how='left')
    fixed_residents['EAD_Reduction'] = fixed_residents.apply(EAD_Reduction_Calculation, axis=1,subsidymode='fixed_year')

    fixed_residents['BCR_Fix'] = fixed_residents['EAD_Reduction']/fixed_residents['discounted_fixed_subsidy']

    # fixed_residents = fixed_residents[fixed_residents['BCR_Fix'] <= cutoff_value]
    fixed_residents = fixed_residents.sort_values(by = 'BCR_Fix', ascending = False)
    # fixed_residents = fixed_residents.sort_values(by='discounted_fixed_subsidy', ascending=False)
    # sort files by 'Subsidy' and 'EAD_Reduction'
    # fixed_residents = fixed_residents.sort_values(by = ['discounted_fixed_subsidy', 'EAD_Reduction'], ascending = [True, False])

    fixed_discounted_subsidy = np.array(fixed_residents['discounted_fixed_subsidy'].tolist())
    EAD_reduction_fixed = np.array(fixed_residents['EAD_Reduction'].tolist())
    accumulated_fixed_subsidy = fixed_discounted_subsidy.cumsum()/1e6
    accumulated_fixed_ead_reduction = EAD_reduction_fixed.cumsum()/1e6
    BCR_fixed = accumulated_fixed_ead_reduction/accumulated_fixed_subsidy

    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(accumulated_fixed_subsidy, BCR_fixed, color = colors['darkblue'], label = 'Fixed Subsidy')
    # plt.show()
    # print(fixed_discounted_subsidy[0:10])
    # print(EAD_reduction_fixed[0:10])

    # For the Optimal Subsidy Plan
    optimal_residents = Relocation_Outcome[Relocation_Outcome['optimal_flag'] == 1]
    optimal_residents['discounted_optimal_subsidy'] = optimal_residents['optimal_subsidy'] / (1 + gov_dr) ** optimal_residents['optimal_year']
    optimal_residents = optimal_residents.merge(EAD, on='structure_id', how='left')
    optimal_residents['EAD_Reduction'] = optimal_residents.apply(EAD_Reduction_Calculation, axis=1,
                                                                 subsidymode='optimal_year')
    optimal_residents['BCR_Opt'] = optimal_residents['EAD_Reduction']/optimal_residents['discounted_optimal_subsidy']
    # optimal_residents = optimal_residents[optimal_residents['BCR_Opt'] <= cutoff_value]
    optimal_residents = optimal_residents.sort_values(by = 'BCR_Opt', ascending = False)
    # optimal_residents = optimal_residents.sort_values(by='discounted_optimal_subsidy', ascending=False)

    #sort files by 'Subsidy' and 'EAD_Reduction'
    # optimal_residents = optimal_residents.sort_values(by=['discounted_optimal_subsidy', 'EAD_Reduction'],
    #                                               ascending=[True, False])

    optimal_discounted_subsidy = np.array(optimal_residents['discounted_optimal_subsidy'].tolist())
    EAD_reduction_optimal = np.array(optimal_residents['EAD_Reduction'].tolist())

    accumulated_optimal_subsidy = optimal_discounted_subsidy.cumsum()/1e6
    accumulated_optimal_ead_reduction = EAD_reduction_optimal.cumsum()/1e6
    BCR_optimal = accumulated_optimal_ead_reduction/accumulated_optimal_subsidy
    ax1.plot(accumulated_optimal_subsidy, BCR_optimal, color = colors['darkred'],label = 'Optimal Subsidy')

    # plt.ylim(1.0, 3.5)
    plt.xlim(left = 0, right = 1000)
    plt.ylim(0, cutoff_value)
    plt.ylabel('Cumulative BCR', fontsize=24)
    plt.xlabel('Cumulative Subsidy, in millions', fontsize=24)
    plt.title(title, fontsize=30)
    plt.legend(fontsize = 18, handlelength = 1)
    plt.tick_params(axis='both',  # Apply to both x and y axes
                    which='both',  # Apply to both major and minor ticks
                    direction='in',  # 'in' for ticks pointing inwards
                    bottom=True,  # Apply changes to the bottom axis
                    top=False,  # Apply changes to the top axis
                    left=True,  # Apply changes to the left axis
                    right=False,
                    labelsize = 18)
    plt.show()
    # print(optimal_discounted_subsidy[0:10])
    # print(EAD_reduction_optimal[0:10])
EAD_filename = './EAD_Data/landscape' + str(landscape) + '_fragility1.0_pumping0.5.csv'
EAD = pd.read_csv(EAD_filename)
Accumulated_BCR_Accumulated_Cost(Relocation_Outcome, EAD, 0.03, 'Lower Scenario', 50)