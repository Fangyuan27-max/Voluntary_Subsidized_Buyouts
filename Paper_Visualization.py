import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch

# Function to obtain the number of relocation each year
def Construct_Cumulative_Num(Relocation_Outcome):
    # unify the flag
    Relocation_Outcome.replace({True: 1, 'False': 0, '0': 0, '1': 1}, inplace=True)
    # print(Relocation_Outcome['fixed_flag'].unique())
    yearlist = list(np.arange(0, 21, 1))
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

landscape_lsit = [7, 8]
Relocation_result = {}
for landscape in landscape_lsit:
    Relocation_result[landscape] = {}
    data_path = './Results' + str(landscape) + '/'
    num_file_path = data_path + 'Relocation_num_each_year_' + str(landscape) +'_gov3_res12.csv'
    EAD_Cost_Discounting_path = data_path + 'EADReduction_Cost_' + str(landscape) +'_gov3_res12.csv'
    Relocation_outcome_path = data_path + 'Relocation_Outcome_Landscape'+ str(landscape) +'.csv'

    Relocation_result[landscape]['Relocation_Num'] = pd.read_csv(num_file_path)
    Relocation_result[landscape]['EAD_Cost_Discounting'] = pd.read_csv(EAD_Cost_Discounting_path)
    Relocation_result[landscape]['Relocation_Outcome'] = pd.read_csv(Relocation_outcome_path)

    # get the number of relocation
    Fixed_Self, Fixed_Motivated, Optimal_Self, Optimal_Motivated = Construct_Cumulative_Num(Relocation_result[landscape]['Relocation_Outcome'])
    Relocation_result[landscape]['Fixed_Self'] = Fixed_Self
    Relocation_result[landscape]['Fixed_Motivated'] = Fixed_Motivated
    Relocation_result[landscape]['Optimal_Self'] = Optimal_Self
    Relocation_result[landscape]['Optimal_Motivated'] = Optimal_Motivated

colors = {
    'darkblue': '#004488',
    'lightblue': '#47abd8',
    'darkred' : '#BB5566',
    'lightred': '#febdbb'
}

# Figure 2 is a summary plot of relocation outcome
def figure2(Relocation_outcome):

    fig, axs = plt.subplots(2,2, figsize = (7,7), dpi=300)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)

    # data
    yearlist1 = list(np.arange(0, 21, 1))
    yearlist2 = np.arange(0, 51, 1)

    # labels

    # First subplot
    x = yearlist1
    y1 = np.array(Relocation_outcome[7]['Fixed_Self'])
    y2 = np.array(Relocation_outcome[7]['Fixed_Motivated'])
    y3 = np.array(Relocation_outcome[7]['Optimal_Self'])
    y4 = np.array(Relocation_outcome[7]['Optimal_Motivated'])

    y5 = y1 + y2
    y6 = y3 + y4

    fixed_self_relocation = y1.cumsum()
    fixed_motivated_relocation = y5.cumsum()

    opt_self_relocation = y3.cumsum()
    opt_motivated_relocation = y6.cumsum()

    axs[0, 0].plot(x, fixed_self_relocation, label="Self Relocations | Fixed Subsidy", color=colors['lightblue'], marker='o', markersize = 3)
    axs[0, 0].plot(x, fixed_motivated_relocation, label="Total Relocations | Fixed Subsidy", color=colors['darkblue'], marker='o', markersize = 3)
    axs[0, 0].plot(x, opt_self_relocation, label="Self Relocations | Optimal Subsidy", color=colors['lightred'], marker='o', markersize = 3)
    axs[0, 0].plot(x, opt_motivated_relocation, label="Total Relocations | Optimal Subsidy", color=colors['darkred'], marker='o', markersize = 3)

    axs[0, 0].set_xlabel('Year', fontsize=10)
    axs[0, 0].set_ylabel('Cumulative Relocations', fontsize=10)
    axs[0, 0].set_title("Lower Scenario", fontsize=12)
    axs[0, 0].set_ylim(0, 71000)
    axs[0, 0].set_xlim(-1, 21)
    tick_spacing = 2
    axs[0, 0].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axs[0, 0].tick_params(axis='both', which='major', direction='in', bottom=True, top=False, left=True, right=False,
                          labelsize=8)

    x = yearlist1
    y1 = np.array(Relocation_outcome[8]['Fixed_Self'])
    y2 = np.array(Relocation_outcome[8]['Fixed_Motivated'])
    y3 = np.array(Relocation_outcome[8]['Optimal_Self'])
    y4 = np.array(Relocation_outcome[8]['Optimal_Motivated'])

    y5 = y1 + y2
    y6 = y3 + y4

    fixed_self_relocation = y1.cumsum()
    fixed_motivated_relocation = y5.cumsum()

    opt_self_relocation = y3.cumsum()
    opt_motivated_relocation = y6.cumsum()

    axs[0, 1].plot(x, fixed_self_relocation, label="Self Relocations | Fixed Subsidy", color=colors['lightblue'], marker='o', markersize = 3)
    axs[0, 1].plot(x, fixed_motivated_relocation, label="Total Relocations | Fixed Subsidy", color=colors['darkblue'], marker='o', markersize = 3)
    axs[0, 1].plot(x, opt_self_relocation, label="Self Relocations | Optimal Subsidy", color=colors['lightred'], marker='o', markersize = 3)
    axs[0, 1].plot(x, opt_motivated_relocation, label="Total Relocations | Optimal Subsidy", color=colors['darkred'], marker='o', markersize = 3)

    axs[0, 1].set_xlabel('Year', fontsize=10)
    # axs[0, 1].set_ylabel('Cumulative Relocations', fontsize=24)
    axs[0, 1].set_title("Higher Scenario", fontsize=12)
    axs[0, 1].set_ylim(0, 71000)
    axs[0, 1].set_xlim(-1, 21)
    tick_spacing = 2
    axs[0, 1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axs[0, 1].tick_params(axis='both', which='major', direction='in', bottom=True, top=False, left=True, right=False,
                          labelsize=8)
    # # set the angel of label of the first two figures to be 45
    # for ax in axs[0, :]:
    #     for label in ax.get_xticklabels():
    #         label.set_rotation(45)
    # third plot
    x1 = yearlist2
    Self_EAD = Relocation_outcome[7]['EAD_Cost_Discounting']['Self_EAD'].tolist()
    Fixed_EAD = Relocation_outcome[7]['EAD_Cost_Discounting']['Moti_EAD'].tolist()
    Optimal_EAD = Relocation_outcome[7]['EAD_Cost_Discounting']['Opt_Moti_EAD'].tolist()
    Fixed_difference = [Self_EAD[i] - Fixed_EAD[i] for i in np.arange(0, 51, 1)]
    # transform the unit to billions
    Fixed_difference = [Fixed_difference[i] / 1e9 for i in np.arange(0, 51, 1)]

    Optimal_difference = [Self_EAD[i] - Optimal_EAD[i] for i in np.arange(0, 51, 1)]
    Optimal_difference = [Optimal_difference[i] / 1e9 for i in np.arange(0, 51, 1)]

    axs[1, 0].plot(x1, Fixed_difference, linewidth=2, label="Fixed Subsidy", color='#004488')
    axs[1, 0].plot(x1, Optimal_difference, linewidth=2, label='Optimal Subsidy', color='#994455')
    axs[1, 0].set_ylabel('Yearly EAD Reduction, in Billions (USD 2020)', fontsize=10)
    axs[1, 0].set_xlabel('Year', fontsize=10)
    axs[1, 0].set_ylim(0, 1.0)
    axs[1, 0].set_xticks(x1)
    tick_spacing = 5
    axs[1, 0].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axs[1, 0].tick_params(axis='both', which='major', direction='in', bottom=True, top=False, left=True, right=False, labelsize=8)

    # the fourth figure
    x1 = yearlist2
    Self_EAD = Relocation_outcome[8]['EAD_Cost_Discounting']['Self_EAD'].tolist()
    Fixed_EAD = Relocation_outcome[8]['EAD_Cost_Discounting']['Moti_EAD'].tolist()
    Optimal_EAD = Relocation_outcome[8]['EAD_Cost_Discounting']['Opt_Moti_EAD'].tolist()
    Fixed_difference = [Self_EAD[i] - Fixed_EAD[i] for i in np.arange(0, 51, 1)]
    # transform the unit to billions
    Fixed_difference = [Fixed_difference[i] / 1e9 for i in np.arange(0, 51, 1)]

    Optimal_difference = [Self_EAD[i] - Optimal_EAD[i] for i in np.arange(0, 51, 1)]
    Optimal_difference = [Optimal_difference[i] / 1e9 for i in np.arange(0, 51, 1)]

    axs[1, 1].plot(x1, Fixed_difference, linewidth=2, label="Fixed Subsidy", color='#004488')
    axs[1, 1].plot(x1, Optimal_difference, linewidth=2, label='Optimal Subsidy', color='#994455')
    # axs[1, 1].set_ylabel('Yearly EAD Reduction (in billions)', fontsize=22)
    axs[1, 1].set_xlabel('Year', fontsize=10)
    axs[1, 1].set_ylim(0, 1.0)
    axs[1, 1].set_xticks(x1)
    tick_spacing = 5
    axs[1, 1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axs[1, 1].tick_params(axis='both', which='major', direction='in', bottom=True, top=False, left=True, right=False, labelsize=8)

    # legend for fig 1 and fig 2
    handles1, labels1 = axs[0, 0].get_legend_handles_labels()
    handles2, labels2 = axs[0, 1].get_legend_handles_labels()
    combined_handles_labels_1 = {label: handle for handle, label in zip(handles1, labels1)}
    combined_handles_labels_2 = {label: handle for handle, label in zip(handles2, labels2)}
    combined_handles_labels = {**combined_handles_labels_1, **combined_handles_labels_2}

    fig.legend(combined_handles_labels.values(), combined_handles_labels.keys(), loc='lower center',
               bbox_to_anchor=(0.525, 0.45), ncol=2, fontsize = 8)

    # legend for fig 3 and fig 4
    handles3, labels3 = axs[1, 0].get_legend_handles_labels()
    handles4, labels4 = axs[1, 1].get_legend_handles_labels()
    combined_handles_labels_3 = {label: handle for handle, label in zip(handles3, labels3)}
    combined_handles_labels_4 = {label: handle for handle, label in zip(handles4, labels4)}
    combined_handles_labels = {**combined_handles_labels_3, **combined_handles_labels_4}
    fig.legend(combined_handles_labels.values(), combined_handles_labels.keys(), loc='upper center',
               bbox_to_anchor=(0.525, 0.06), ncol=2, fontsize = 8)

    # plt.subplots_adjust(top = 1, bottom = 0.1)
    # Display the figure
    axs[0, 0].text(0.1, 1.1, '(A)', transform=axs[0, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[0, 1].text(0.1, 1.1, '(B)', transform=axs[0, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[1, 0].text(0.1, 1.1, '(C)', transform=axs[1, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[1, 1].text(0.1, 1.1, '(D)', transform=axs[1, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    plt.show()
    fig.savefig("Figure2.tiff", format='tiff', dpi=300)

# figure2(Relocation_result)

# figure 3: flood risk reduction vs subsidy input, single figure
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

# figure 3 alternative 1: cumulative BCR VS cumulative subsidy
def figure3(Relocation_outcome7, Relocation_outcome8, EAD7, EAD8, sorting_metirc, gov_dr, cutoff_value):

    fig, axs = plt.subplots(1, 2, figsize=(8, 4), dpi=300)
    plt.subplots_adjust(wspace=0.2, hspace = 0.1)

    outcome_7 = Relocation_outcome7
    # result for landscape 7
    fixed_residents = outcome_7[outcome_7['fixed_flag'] == 1]
    fixed_residents['Subsidy'] = fixed_residents['fixed_subsidy'] / (1 + gov_dr) ** fixed_residents[
        'fixed_year']
    fixed_residents = fixed_residents.merge(EAD7, on='structure_id', how='left')
    fixed_residents['EAD_Reduction'] = fixed_residents.apply(EAD_Reduction_Calculation, axis=1,
                                                             subsidymode='fixed_year')
    fixed_residents['BCR'] = fixed_residents['EAD_Reduction'] / fixed_residents['Subsidy']
    fixed_residents = fixed_residents.sort_values(by=sorting_metirc, ascending=False)

    fixed_discounted_subsidy = np.array(fixed_residents['Subsidy'].tolist())
    EAD_reduction_fixed = np.array(fixed_residents['EAD_Reduction'].tolist())
    accumulated_fixed_subsidy = fixed_discounted_subsidy.cumsum() / 1e9
    accumulated_fixed_ead_reduction = EAD_reduction_fixed.cumsum() / 1e9
    BCR_fixed = accumulated_fixed_ead_reduction / accumulated_fixed_subsidy
    axs[0].plot(accumulated_fixed_subsidy, BCR_fixed, label = 'Fixed Subsidy', linewidth=5, color = '#004488')

    optimal_residents = outcome_7[outcome_7['optimal_flag'] == 1]
    optimal_residents['Subsidy'] = optimal_residents['optimal_subsidy'] / (1 + gov_dr) ** \
                                                      optimal_residents['optimal_year']
    optimal_residents = optimal_residents.merge(EAD7, on='structure_id', how='left')
    optimal_residents['EAD_Reduction'] = optimal_residents.apply(EAD_Reduction_Calculation, axis=1,
                                                                 subsidymode='optimal_year')
    optimal_residents['BCR'] = optimal_residents['EAD_Reduction'] / optimal_residents['Subsidy']
    optimal_residents = optimal_residents.sort_values(by=sorting_metirc,ascending=False)
    optimal_discounted_subsidy = np.array(optimal_residents['Subsidy'].tolist())
    EAD_reduction_optimal = np.array(optimal_residents['EAD_Reduction'].tolist())

    accumulated_optimal_subsidy = optimal_discounted_subsidy.cumsum() / 1e9
    accumulated_optimal_ead_reduction = EAD_reduction_optimal.cumsum() / 1e9
    BCR_optimal = accumulated_optimal_ead_reduction / accumulated_optimal_subsidy

    axs[0].plot(accumulated_optimal_subsidy, BCR_optimal, label = 'Optimal Subsidy', linewidth=5, color = '#994455')
    axs[0].set_xlabel('Cumulative Subsidy, in Billions (USD 2020)', fontsize = 10)
    axs[0].set_ylabel('Cumulative Benefit-Cost Ratio', fontsize = 10)
    axs[0].set_ylim(0, cutoff_value)
    # axs[0].set_xlim(0, 1000)
    axs[0].set_title('Lower Scenario', fontsize = 12)
    axs[0].tick_params(axis='both', which='major', direction='in', bottom=True, top=False, left=True, right=False,
                          labelsize=10)
    axs[0].legend(fontsize = 10, loc = 'upper right')

    # result for landscape 8
    outcome_8 = Relocation_outcome8
    # result for landscape 7
    fixed_residents = outcome_8[outcome_8['fixed_flag'] == 1]
    fixed_residents['Subsidy'] = fixed_residents['fixed_subsidy'] / (1 + gov_dr) ** fixed_residents[
        'fixed_year']
    fixed_residents = fixed_residents.merge(EAD8, on='structure_id', how='left')
    fixed_residents['EAD_Reduction'] = fixed_residents.apply(EAD_Reduction_Calculation, axis=1,
                                                             subsidymode='fixed_year')
    fixed_residents['BCR'] = fixed_residents['EAD_Reduction'] / fixed_residents['Subsidy']
    fixed_residents = fixed_residents.sort_values(by=sorting_metirc, ascending=False)

    fixed_discounted_subsidy = np.array(fixed_residents['Subsidy'].tolist())
    EAD_reduction_fixed = np.array(fixed_residents['EAD_Reduction'].tolist())
    accumulated_fixed_subsidy = fixed_discounted_subsidy.cumsum() / 1e9
    accumulated_fixed_ead_reduction = EAD_reduction_fixed.cumsum() / 1e9
    BCR_fixed = accumulated_fixed_ead_reduction / accumulated_fixed_subsidy
    axs[1].plot(accumulated_fixed_subsidy, BCR_fixed, label='Fixed Subsidy', linewidth=5, color='#004488')

    optimal_residents = outcome_8[outcome_8['optimal_flag'] == 1]
    optimal_residents['Subsidy'] = optimal_residents['optimal_subsidy'] / (1 + gov_dr) ** \
                                   optimal_residents['optimal_year']
    optimal_residents = optimal_residents.merge(EAD8, on='structure_id', how='left')
    optimal_residents['EAD_Reduction'] = optimal_residents.apply(EAD_Reduction_Calculation, axis=1,
                                                                 subsidymode='optimal_year')
    optimal_residents['BCR'] = optimal_residents['EAD_Reduction'] / optimal_residents['Subsidy']
    optimal_residents = optimal_residents.sort_values(by=sorting_metirc, ascending=False)
    optimal_discounted_subsidy = np.array(optimal_residents['Subsidy'].tolist())
    EAD_reduction_optimal = np.array(optimal_residents['EAD_Reduction'].tolist())

    accumulated_optimal_subsidy = optimal_discounted_subsidy.cumsum() / 1e9
    accumulated_optimal_ead_reduction = EAD_reduction_optimal.cumsum() / 1e9
    BCR_optimal = accumulated_optimal_ead_reduction / accumulated_optimal_subsidy

    axs[1].plot(accumulated_optimal_subsidy, BCR_optimal, label='Optimal Subsidy', linewidth=5, color='#994455')
    axs[1].set_xlabel('Cumulative Subsidy, in Billions (USD 2020)', fontsize=10)
    axs[1].set_ylabel('Cumulative Benefit-Cost Ratio', fontsize=10)
    axs[1].set_ylim(0, cutoff_value)
    # axs[1].set_xlim(0, 1000)
    axs[1].set_title('Higher Scenario', fontsize=12)
    axs[1].tick_params(axis='both', which='major', direction='in', bottom=True, top=False, left=True, right=False,
                          labelsize=10)
    axs[1].legend(fontsize = 10, loc='upper right')

    axs[0].text(0.1, 1.07, '(A)', transform=axs[0].transAxes, fontsize=10, fontweight='bold', va='top',
                   ha='right')
    axs[1].text(0.1, 1.07, '(B)', transform=axs[1].transAxes, fontsize=10, fontweight='bold', va='top',
                   ha='right')
    plt.tight_layout()
    plt.show()
    fig.savefig("Figure3.tiff", format = "tiff", dpi=300)

# EAD7 = pd.read_csv('./EAD_Data/landscape7_fragility1.0_pumping0.5.csv')
# EAD8 = pd.read_csv('./EAD_Data/landscape8_fragility1.0_pumping0.5.csv')
# Relocation_result7 = pd.read_csv('./Results7/Relocation_Outcome_Landscape7.csv')
# Relocation_result8 = pd.read_csv('./Results8/Relocation_Outcome_Landscape8.csv')
# figure3(Relocation_result7, Relocation_result8, EAD7, EAD8, 'BCR', 0.03, 20)

# Equity Implication of the
# exploratory_table7 = pd.read_csv('./ExploratoryData/3_Exploratory_Table7.csv')
# exploratory_table8 = pd.read_csv('./ExploratoryData/3_Exploratory_Table8.csv')
# census_data = pd.read_csv('./ExploratoryData/census_data.csv')

def EAD_Calculation(row, mode):
    # self_year = int(row['self_year'])
    relocation_year = min(50, int(row[mode]))

    EAD_list = [row[f'ead_fwoa_year{i:02}'] for i in range(0, relocation_year)]
    EAD = sum([EAD_list[i]/1.03**i for i in range(len(EAD_list))])
    return EAD

def Subsidy_Calculation(row, mode_year, mode_amount):
    relocation_year = int(row[mode_year])
    if relocation_year > 20:
        subsidy = 0
    else:
        subsidy = row[mode_amount]/1.03**relocation_year
    return subsidy

def figure4and5_table_EASD(Data, EAD, census_data):
    NewData = Data.loc[:, ['structure_id', 'block_id', 'self_year','fixed_year','optimal_year','fixed_flag','fixed_subsidy','optimal_flag','optimal_subsidy']]
    NewData['block_group'] = NewData['block_id'].astype(str).str[:12]

    census_data['Block_Group'] = census_data['GEO_ID'].astype(str).str[-12:]

    Table = NewData.merge(census_data, left_on = 'block_group', right_on = 'Block_Group')

    Table = Table.merge(EAD, on = 'structure_id')

    Table['self_easd'] = Table.apply(EASD_Calculation, axis = 1, mode = 'self_year')
    Table['fixed_easd'] = Table.apply(EASD_Calculation, axis=1, mode='fixed_year')
    Table['optimal_easd'] = Table.apply(EASD_Calculation, axis=1, mode='optimal_year')

    category_names = ['White', 'Black', 'Asia / Pacific Islander', 'Native American', 'Other / Multi-Racial', 'PIR 0 to 0.5', 'PIR 0.5 to 1', 'PIR 1 to 2', 'PIR 2 and above']
    category_list = ['pop_white', 'pop_black', 'pop_asian_pacific', 'pop_native', 'pop_other_multi', 'pir_under_pt5', 'pir_pt5_pt99', 'pir_1_1pt99','pir_2_plus']
    Result = {}
    for i in range(len(category_list)):
        Result[category_names[i]] = {}
        Result[category_names[i]]['self_easd'] = (Table['self_easd']*Table[category_list[i]]).sum(axis = 0)
        Result[category_names[i]]['fixed_easd'] = (Table['fixed_easd'] * Table[category_list[i]]).sum(axis = 0)
        Result[category_names[i]]['optimal_easd'] = (Table['optimal_easd'] * Table[category_list[i]]).sum(axis = 0)
    Result = pd.DataFrame(Result)
    return Result

# Result7 = figure4and5_table_EASD(exploratory_table7, EASD7, census_data)
# Result7.to_csv('EquityDataEASD7.csv')
# Result8 = figure4and5_table_EASD(exploratory_table8, EASD8, census_data)
# Result8.to_csv('EquityDataEASD8.csv')

def figure4and5_table_loss(Data, EAD, census_data):
    NewData = Data.loc[:, ['structure_id', 'block_id', 'self_year','fixed_year','optimal_year','fixed_flag','fixed_subsidy','optimal_flag','optimal_subsidy']]
    NewData['block_group'] = NewData['block_id'].astype(str).str[:12]

    census_data['Block_Group'] = census_data['GEO_ID'].astype(str).str[-12:]

    Table = NewData.merge(census_data, left_on = 'block_group', right_on = 'Block_Group')

    Table = Table.merge(EAD, on = 'structure_id')

    Table['self_loss'] = Table.apply(EAD_Calculation, axis = 1, mode = 'self_year')
    Table['fixed_loss'] = Table.apply(EAD_Calculation, axis=1, mode='fixed_year')
    Table['optimal_loss'] = Table.apply(EAD_Calculation, axis=1, mode='optimal_year')
    Table['fixed_subsidy'] = Table.apply(Subsidy_Calculation, axis = 1, mode_year = 'fixed_year', mode_amount = 'fixed_subsidy')
    Table['optimal_subsidy'] = Table.apply(Subsidy_Calculation, axis = 1, mode_year = 'optimal_year', mode_amount = 'optimal_subsidy')

    category_names = ['White', 'Black', 'Asia / Pacific Islander', 'Native American', 'Other / Multi-Racial', 'PIR 0 to 0.5', 'PIR 0.5 to 1', 'PIR 1 to 2', 'PIR 2 and above']
    category_list = ['pop_white', 'pop_black', 'pop_asian_pacific', 'pop_native', 'pop_other_multi', 'pir_under_pt5', 'pir_pt5_pt99', 'pir_1_1pt99','pir_2_plus']
    Result = {}
    for i in range(len(category_list)):
        Result[category_names[i]] = {}
        Result[category_names[i]]['self_loss'] = (Table['self_loss']*Table[category_list[i]]).sum(axis = 0)
        Result[category_names[i]]['fixed_loss'] = (Table['fixed_loss'] * Table[category_list[i]]).sum(axis = 0)
        Result[category_names[i]]['optimal_loss'] = (Table['optimal_loss'] * Table[category_list[i]]).sum(axis = 0)
        Result[category_names[i]]['fixed_subsidy'] = (Table['fixed_subsidy'] * Table[category_list[i]]).sum(axis = 0)
        Result[category_names[i]]['optimal_subsidy'] = (Table['optimal_subsidy'] * Table[category_list[i]]).sum(axis = 0)
    Result = pd.DataFrame(Result)
    return Result


# Result7 = figure4and5_table_loss(exploratory_table7, EAD7, census_data)
# Result7.to_csv('EquityData7.csv')
# Result8 = figure4and5_table_loss(exploratory_table8, EAD8, census_data)
# Result8.to_csv('EquityData8.csv')

EquityData7 = pd.read_csv('EquityData7.csv', index_col=None)
EquityData8 = pd.read_csv('EquityData8.csv', index_col=None)

def divide_by_billion(x):
    return x/1e9 if isinstance(x, (int, float)) else x
def figure4(Data7, Data8):
    Data7 = Data7.T.iloc[1:, :]
    Data7.columns = ['self_loss', 'fixed_loss', 'optimal_loss', 'fixed_subsidy', 'optimal_subsidy']
    Data8 = Data8.T.iloc[1:, :]
    Data8.columns = ['self_loss', 'fixed_loss', 'optimal_loss', 'fixed_subsidy', 'optimal_subsidy']
    Data7['fixed_reduction'] = Data7['self_loss'] - Data7['fixed_loss']
    Data7['optimal_reduction'] = Data7['self_loss'] - Data7['optimal_loss']
    Data8['fixed_reduction'] = Data8['self_loss'] - Data8['fixed_loss']
    Data8['optimal_reduction'] = Data8['self_loss'] - Data8['optimal_loss']
    data7 = Data7.applymap(divide_by_billion)
    data8 = Data8.applymap(divide_by_billion)

    race_list = ['White', 'Black', 'Asia / Pacific Islander', 'Native American', 'Other / Multi-Racial']
    income_list = ['PIR 0 to 0.5', 'PIR 0.5 to 1', 'PIR 1 to 2', 'PIR 2 and above']

    fig, axs = plt.subplots(2, 2, figsize=(7, 7), dpi=300)
    plt.subplots_adjust(wspace=0.2, hspace=0.49)
    barWidth = 0.5
    racecolors = ['#f58925', '#5ba44c', '#23719e', '#019b98', '#de4c4e']
    x = [1.5,2.5,4,5]
    for i in range(len(x)):
        if x[i] == 1.5:
            y = data7.loc[race_list, 'fixed_reduction']
        elif x[i] == 2.5:
            y = data7.loc[race_list, 'fixed_subsidy']
        elif x[i] == 4:
            y = data7.loc[race_list, 'optimal_reduction']
        else:
            y = data7.loc[race_list, 'optimal_subsidy']
        for j in range(len(race_list)):
            if x[i] == 1.5 or x[i] == 4:
                axs[0,0].bar(x[i], y[j], bottom = sum(y[:j]), color = racecolors[j], label = race_list[j], width=0.8)
            else:
                axs[0, 0].bar(x[i], y[j], bottom=sum(y[:j]), color=racecolors[j], label=race_list[j], width=0.8, hatch = '//')
    axs[0,0].set_ylim(0, 30)
    axs[0,0].set_ylabel("Monetary Value, in Billions (USD 2020)", fontsize=10)
    axs[0,0].set_title('Lower Scenario', fontsize = 14)
    axs[0,0].set_xticks([2, 4.5], ['Fixed Subsidy', 'Optimal Subsidy'])

    for i in range(len(x)):
        if x[i] == 1.5:
            y = data8.loc[race_list, 'fixed_reduction']
        elif x[i] == 2.5:
            y = data8.loc[race_list, 'fixed_subsidy']
        elif x[i] == 4:
            y = data8.loc[race_list, 'optimal_reduction']
        else:
            y = data8.loc[race_list, 'optimal_subsidy']

        for j in range(len(race_list)):
            if x[i] == 1.5 or x[i] == 4:
                axs[0,1].bar(x[i], y[j], bottom = sum(y[:j]), color = racecolors[j], label = race_list[j], width=0.8)
            else:
                axs[0, 1].bar(x[i], y[j], bottom=sum(y[:j]), color=racecolors[j], width=0.8, hatch = '//')

    axs[0, 1].set_ylim(0, 30)
    axs[0, 1].set_title('Higher Scenario', fontsize=14)
    axs[0, 1].set_xticks([2, 4.5], ['Fixed Subsidy', 'Optimal Subsidy'])

    incomecolors = ["#7d807d", '#c2c7c9', "#f58825", "#23719e"]
    for i in range(len(x)):
        if x[i] == 1.5:
            y = data7.loc[income_list, 'fixed_reduction']
        elif x[i] == 2.5:
            y = data7.loc[income_list, 'fixed_subsidy']
        elif x[i] == 4:
            y = data7.loc[income_list, 'optimal_reduction']
        else:
            y = data7.loc[income_list, 'optimal_subsidy']
        for j in range(len(income_list)):
            if x[i] == 1.5 or x[i] == 4:
                axs[1,0].bar(x[i], y[j], bottom = sum(y[:j]), color = incomecolors[j], label = income_list[j], width=0.8)
            else:
                axs[1, 0].bar(x[i], y[j], bottom=sum(y[:j]), color=incomecolors[j], width=0.8, hatch = '//')

    axs[1, 0].set_ylim(0, 30)
    axs[1, 0].set_ylabel("Monetary Value, in Billions (USD 2020)", fontsize=10)
    axs[1, 0].set_xticks([2, 4.5], ['Fixed Subsidy', 'Optimal Subsidy'])

    for i in range(len(x)):
        if x[i] == 1.5:
            y = data8.loc[income_list, 'fixed_reduction']
        elif x[i] == 2.5:
            y = data8.loc[income_list, 'fixed_subsidy']
        elif x[i] == 4:
            y = data8.loc[income_list, 'optimal_reduction']
        else:
            y = data8.loc[income_list, 'optimal_subsidy']
        for j in range(len(income_list)):
            if x[i] == 1.5 or x[i] == 4:
                axs[1, 1].bar(x[i], y[j], bottom=sum(y[:j]), color=incomecolors[j], label=income_list[j], width=0.8)
            else:
                axs[1,1].bar(x[i], y[j], bottom = sum(y[:j]), color = incomecolors[j], width=0.8, hatch='//')

    axs[1, 1].set_ylim(0, 30)
    axs[1, 1].set_xticks([2, 4.5], ['Fixed Subsidy', 'Optimal Subsidy'])

    # legend for fig 1 and fig 2
    handles1, labels1 = axs[0, 0].get_legend_handles_labels()
    handles2, labels2 = axs[0, 1].get_legend_handles_labels()
    combined_handles_labels_1 = {label: handle for handle, label in zip(handles1, labels1)}
    combined_handles_labels_2 = {label: handle for handle, label in zip(handles2, labels2)}
    combined_handles_labels = {**combined_handles_labels_1, **combined_handles_labels_2}

    fig.legend(combined_handles_labels.values(), combined_handles_labels.keys(), loc='upper left',
               bbox_to_anchor=(0.12, 0.54), ncol=2, fontsize=8)

    legend_handles = [
        Patch(facecolor='grey', edgecolor='black', hatch=None, label='Flood Risks Reduction'),
        Patch(facecolor='grey', edgecolor='black', hatch='//', label='Subsidy Cost')
    ]
    fig.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(0.6, 0.53), ncol=1, fontsize=8 )

    # legend for fig 3 and fig 4
    handles3, labels3 = axs[1, 0].get_legend_handles_labels()
    handles4, labels4 = axs[1, 1].get_legend_handles_labels()
    combined_handles_labels_3 = {label: handle for handle, label in zip(handles3, labels3)}
    combined_handles_labels_4 = {label: handle for handle, label in zip(handles4, labels4)}
    combined_handles_labels = {**combined_handles_labels_3, **combined_handles_labels_4}
    fig.legend(combined_handles_labels.values(), combined_handles_labels.keys(), loc='lower left',
               bbox_to_anchor=(0.12, 0.013), ncol=2, fontsize=8)
    fig.legend(handles=legend_handles, loc='lower left', bbox_to_anchor=(0.6, 0.013), ncol=1, fontsize=8)

    axs[0, 0].text(0.1, 1.1, '(A)', transform=axs[0, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[0, 1].text(0.1, 1.1, '(B)', transform=axs[0, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[1, 0].text(0.1, 1.1, '(C)', transform=axs[1, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[1, 1].text(0.1, 1.1, '(D)', transform=axs[1, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')

    plt.show()
    fig.savefig('Figure4.tiff', format = 'tiff', dpi=300)
# figure4(EquityData7, EquityData8)

def figure5(Table, mode):
    fig, axs = plt.subplots(2, 4, figsize = (8, 5), dpi = 300)
    plt.subplots_adjust(wspace=0.3, hspace=0.4)

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j].tick_params(direction='in')

    # The population info
    race_list = ['White', 'Black', 'Asia / Pacific Islander', 'Native American', 'Other / Multi-Racial']
    racecolors = ['#f58925', '#5ba44c', '#23719e', '#019b98', '#de4c4e']
    racevalues = [Table[i].sum() for i in race_list]
    axs[0,0].pie(racevalues, colors=racecolors, autopct=None, startangle=90)
    axs[0,0].set_title('Population', fontsize = 8)

    income_list = ['PIR 0 to 0.5', 'PIR 0.5 to 1', 'PIR 1 to 2', 'PIR 2 and above']
    incomecolors = ["#7d807d", '#c2c7c9', "#f58825", "#23719e"]
    incomevalues = [Table[i].sum() for i in income_list]
    axs[1,0].pie(incomevalues, colors=incomecolors, autopct=None, startangle=90)
    axs[1, 0].set_title('Population', fontsize = 8)

    # Average EAD
    if mode == 'optimal':
        loss_column = 'optimal_loss'
    else:
        loss_column = 'fixed_loss'

    avg_risk_before = []
    avg_risk_after = []
    for race in race_list:
        avg_risk_before.append((Table['self_loss']*Table[race]).sum()/Table[race].sum())
        avg_risk_after.append((Table[loss_column] * Table[race]).sum() / Table[race].sum())
    xvalue1 = [1,4,7,10,13]
    xvalue2 = [2,5,8,11,14]
    tick_value = [1.5, 4.5, 7.5, 10.5, 13.5]
    for k in range(len(race_list)):
        axs[0,1].bar(xvalue1[k], avg_risk_before[k], color=racecolors[k], width=0.8)
        axs[0,1].bar(xvalue2[k], avg_risk_after[k], color=racecolors[k], width=0.8, hatch='//')
    axs[0,1].set_xticks([])
    axs[0,1].set_ylabel('Amount, in 1,000 (USD 2020)', fontsize = 8)
    axs[0,1].set_yticks(list(np.arange(0, 110000, 10000)), list(np.arange(0,110, 10)), fontsize = 8)
    axs[0,1].set_title('Average Flood Risks', fontsize = 8)

    avg_risk_before = []
    avg_risk_after = []
    for income in income_list:
        avg_risk_before.append((Table['self_loss'] * Table[income]).sum() / Table[income].sum())
        avg_risk_after.append((Table[loss_column] * Table[income]).sum() / Table[income].sum())
    xvalue1 = [1, 4, 7, 10]
    xvalue2 = [2, 5, 8, 11]
    tick_value = [1.5, 4.5, 7.5, 10.5]
    for k in range(len(income_list)):
        axs[1, 1].bar(xvalue1[k], avg_risk_before[k], color=incomecolors[k], width=0.8)
        axs[1, 1].bar(xvalue2[ k], avg_risk_after[k], color=incomecolors[k], width=0.8, hatch='//')
    axs[1,1].set_xticks([])
    axs[1,1].set_ylabel('Amount, in 1,000 (USD 2020)', fontsize = 8)
    axs[1, 1].set_yticks(list(np.arange(0, 110000, 10000)), list(np.arange(0, 110, 10)), fontsize=8)
    axs[1, 1].set_title('Average Flood Risks', fontsize=8)

    # The average structure damage

    if mode == 'optimal':
        easd_column = 'optimal_easd'
    else:
        easd_column = 'fixed_easd'

    avg_damage_before = []
    avg_damage_after = []
    for race in race_list:
        avg_damage_before.append((Table['self_easd'] * Table[race]).sum() / Table[race].sum())
        avg_damage_after.append((Table[easd_column] * Table[race]).sum() / Table[race].sum())
    xvalue1 = [1, 4, 7, 10, 13]
    xvalue2 = [2, 5, 8, 11, 14]
    tick_value = [1.5, 4.5, 7.5, 10.5, 13.5]
    for k in range(len(race_list)):
        axs[0, 2].bar(xvalue1[k], avg_damage_before[k], color=racecolors[k], width=0.8)
        axs[0, 2].bar(xvalue2[k], avg_damage_after[k], color=racecolors[k], width=0.8, hatch='//')
    axs[0, 2].set_xticks([])
    axs[0, 2].set_ylabel('Structural Damage', fontsize=8)
    axs[0, 2].set_yticks(list(np.arange(0, 0.6, 0.1)), [0, 0.1, 0.2, 0.3, 0.4, 0.5], fontsize=6)
    axs[0, 2].set_title('Average Structural Damage', fontsize=8)

    avg_damage_before = []
    avg_damage_after = []
    for income in income_list:
        avg_damage_before.append((Table['self_easd'] * Table[income]).sum() / Table[income].sum())
        avg_damage_after.append((Table[easd_column] * Table[income]).sum() / Table[income].sum())
    xvalue1 = [1, 4, 7, 10]
    xvalue2 = [2, 5, 8, 11]
    tick_value = [1.5, 4.5, 7.5, 10.5]
    for k in range(len(income_list)):
        axs[1, 2].bar(xvalue1[k], avg_damage_before[k], color=incomecolors[k], width=0.8)
        axs[1, 2].bar(xvalue2[k], avg_damage_after[k], color=incomecolors[k], width=0.8, hatch='//')
    axs[1, 2].set_xticks([])
    axs[1, 2].set_ylabel('Structural Damage', fontsize=8)
    axs[1, 2].set_yticks(list(np.arange(0, 0.6, 0.1)), [0, 0.1, 0.2, 0.3, 0.4, 0.5], fontsize=6)
    axs[1, 2].set_title('Average Structural Damage', fontsize=8)

    # Average Subsidy
    if mode == 'optimal':
        subsidy_column = 'optimal_subsidy'
    else:
        subsidy_column = 'fixed_subsidy'

    avg_subsidy = []
    for race in race_list:
        avg_subsidy.append((Table[subsidy_column] * Table[race]).sum() / Table[race].sum())
    xvalue1 = [1, 4, 7, 10, 13]
    for k in range(len(race_list)):
        axs[0, 3].bar(xvalue1[k], avg_subsidy[k], color=racecolors[k], width=0.8)
    axs[0, 3].set_xticks([])
    axs[0, 3].set_ylabel('Amount, in 10,000 (USD 2020)', fontsize=8)
    axs[0, 3].set_yticks(list(np.arange(0, 21000, 10000)), [0,1,2], fontsize=8)
    axs[0, 3].set_title('Average Subsidy', fontsize=8)

    avg_subsidy = []
    for income in income_list:
        avg_subsidy.append((Table[subsidy_column] * Table[income]).sum() / Table[income].sum())
    xvalue1 = [1, 4, 7, 10]
    for k in range(len(income_list)):
        axs[1, 3].bar(xvalue1[k], avg_subsidy[k], color=incomecolors[k], width=0.8)
    axs[1, 3].set_xticks([])
    axs[1, 3].set_ylabel('Amount, in 10,000 (USD 2020)', fontsize=8)
    axs[1, 3].set_yticks(list(np.arange(0, 21000, 10000)), [0,1,2], fontsize=8)
    axs[1, 3].set_title('Average Subsidy', fontsize=8)

    # get the legend
    newracelist = ['White', 'Black', 'Asia/Pacific', 'Native American', 'Other/Multi']
    race_legend = []
    for i in range(len(race_list)):
        race_legend.append(Patch(facecolor=racecolors[i], edgecolor='black', hatch=None, label = newracelist[i]))
    income_legend = []
    for i in range(len(income_list)):
        income_legend.append(Patch(facecolor=incomecolors[i], edgecolor='black', hatch=None, label=income_list[i]))

    if mode == 'optimal':
        name_mode = 'Optimal Subsidy'
    else:
        name_mode = 'Fixed Subsidy'

    mode_legend = [
        Patch(facecolor='gray', edgecolor='black', hatch=None, label='Self-Relocation'),
        Patch(facecolor='gray', edgecolor='black', hatch='//', label=name_mode)
    ]

    fig.legend(handles=race_legend, loc='upper left', bbox_to_anchor=(0, 0.8), ncol=1, fontsize=6)
    fig.legend(handles=mode_legend, loc='upper left', bbox_to_anchor=(0, 0.65), ncol=1, fontsize=6)
    fig.legend(handles=income_legend, loc='upper left', bbox_to_anchor=(0, 0.4), ncol=1, fontsize=6)
    fig.legend(handles=mode_legend, loc='upper left', bbox_to_anchor=(0, 0.25), ncol=1, fontsize=6)

    axs[0, 0].text(0.2, 1.1, '(A)', transform=axs[0, 0].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[0, 1].text(0, 1.12, '(B)', transform=axs[0, 1].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[0, 2].text(-0.1, 1.12, '(C)', transform=axs[0, 2].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[0, 3].text(0.12, 1.12, '(D)', transform=axs[0, 3].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[1, 0].text(0.2, 1.1, '(E)', transform=axs[1, 0].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[1, 1].text(0, 1.12, '(F)', transform=axs[1, 1].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[1, 2].text(-0.1, 1.12, '(G)', transform=axs[1, 2].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')
    axs[1, 3].text(0.12, 1.12, '(H)', transform=axs[1, 3].transAxes, fontsize=12, fontweight='bold', va='top',
                   ha='right')

    # plt.tight_layout()
    plt.show()
    fig.savefig('Figure5.tiff', format='tiff', dpi=300)
    ##
Table = pd.read_csv('./Table8.csv')
figure5(Table, 'optimal')


# Geo7 = pd.read_csv('./ExploratoryData/GeoVisual_Landscape7.csv')
# Geo8 = pd.read_csv('./ExploratoryData/GeoVisual_Landscape8.csv')
# EASD7 = pd.read_csv('./EAD_Data/landscape7_fragility1.0_pumping0.5_EASD.csv')
# EASD8 = pd.read_csv('./EAD_Data/landscape8_fragility1.0_pumping0.5_EASD.csv')

## get the average RC1 of each county
# Result1 = Geo7.groupby('parish_name')['RC1'].mean()
# Result2 = Geo7.groupby('parish_name')['structure_id'].count()

def EASD_Calculation(row, mode):
    relocation_year = min(50, int(row[mode]))

    EASD_list = [row[f'easd_fwoa_year{i:02}'] for i in range(0, relocation_year)]
    EASD = sum([EASD_list[i] for i in range(len(EASD_list))])
    return EASD

def Discounted_EASD(row, mode):
    relocation_year = min(50, int(row[mode]))
    EASD_list = [row[f'easd_fwoa_year{i:02}'] for i in range(0, relocation_year)]
    EASD_Discounted = sum([EASD_list[i]/1.03 ** i for i in range(len(EASD_list))])
    return EASD_Discounted

def figure6table(GEO_Result, EASD):
    Data = GEO_Result.loc[:, ['structure_id', 'parish_name', 'Discounted_Self_Loss', 'Discounted_Fixed_Subsidy', 'Discounted_Optimal_Subsidy',\
                              'self_year', 'fixed_year', 'optimal_year','fixed_flag','optimal_flag']]
    data = Data.merge(EASD, on = 'structure_id')

    data['self_easd'] = data.apply(EASD_Calculation, axis=1, mode='self_year')
    data['self_easd_discounted'] = data.apply(Discounted_EASD, axis=1, mode='self_year')

    aggregated_df = data.groupby('parish_name').agg({
        'structure_id': 'count',
        'Discounted_Self_Loss': 'sum',
        'self_easd': 'sum',
        'self_easd_discounted': 'sum',

        'Discounted_Fixed_Subsidy': 'sum',
        'Discounted_Optimal_Subsidy': 'sum',

        'fixed_flag': 'sum',
        'optimal_flag': 'sum'
    })
    aggregated_df.columns = ['Structure_Count', 'Self_Loss', 'Self_EASD', 'Self_EASD_Discounted', 'Fixed_Subsidy',\
                             'Optimal_Subsidy', 'Fixed_Count', 'Optimal_Count']
    
    aggregated_df['Avg_Self_Loss'] = aggregated_df['Self_Loss']/aggregated_df['Structure_Count']
    aggregated_df['Avg_Self_EASD'] = aggregated_df['Self_EASD']/aggregated_df['Structure_Count']
    aggregated_df['Avg_Self_EASD_Discounted'] = aggregated_df['Self_EASD_Discounted'] / aggregated_df['Structure_Count']
    
    aggregated_df['Avg_Fixed'] = aggregated_df['Fixed_Subsidy']/aggregated_df['Structure_Count']
    aggregated_df['Avg_Optimal'] = aggregated_df['Optimal_Subsidy'] / aggregated_df['Structure_Count']
    
    aggregated_df['Avg_Fixed_Relo'] = aggregated_df['Fixed_Subsidy']/aggregated_df['Fixed_Count']
    aggregated_df['Avg_Optimal_Relo'] = aggregated_df['Optimal_Subsidy'] / aggregated_df['Optimal_Count']
    result = pd.DataFrame(aggregated_df.loc[:, ['Avg_Self_Loss', 'Avg_Self_EASD','Avg_Self_EASD_Discounted', 'Avg_Fixed', 'Avg_Optimal', 'Avg_Fixed_Relo', 'Avg_Optimal_Relo']])
    return result

# Geo_df7 = figure6table(Geo7, EASD7)
# Geo_df7.to_csv('Geo7df.csv')
# Geo_df8 = figure6table(Geo8, EASD7)
# Geo_df8.to_csv('Geo8df.csv')


def figure6(df7, df8):
    colors = {
        'darkblue': '#004488',
        'darkred': '#BB5566'
    }
    df7.set_index('parish_name', inplace=True)
    df8.set_index('parish_name', inplace=True)

    df7.sort_values(by='Avg_Self_Loss', ascending=False, inplace=True)
    df8.sort_values(by='Avg_Self_Loss', ascending=False, inplace=True)

    # sort the dataframe by their avg_self_loss
    fig, axs = plt.subplots(3, 2, figsize=(7, 10), dpi=300)

    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    # figure set 1 - average subsidy vs average loss
    coefficients1 = np.polyfit(df7['Avg_Self_Loss'], df7['Avg_Fixed'], 1)
    polynomial1 = np.poly1d(coefficients1)
    x_fit1 = np.linspace(min(df7['Avg_Self_Loss'])-10000, max(df7['Avg_Self_Loss'])+10000, 1000)
    y_fit1 = polynomial1(x_fit1)
    axs[0, 0].scatter(df7['Avg_Self_Loss'], df7['Avg_Fixed'], color=colors['darkblue'], label='Fixed Subsidy')
    axs[0, 0].plot(x_fit1, y_fit1, color=colors['darkblue'], linewidth = 2)

    coefficients2 = np.polyfit(df7['Avg_Self_Loss'], df7['Avg_Optimal'], 1)
    polynomial2 = np.poly1d(coefficients2)
    x_fit2 = np.linspace(min(df7['Avg_Self_Loss']) - 10000, max(df7['Avg_Self_Loss']) + 10000, 1000)
    y_fit2 = polynomial2(x_fit2)
    axs[0, 0].scatter(df7['Avg_Self_Loss'], df7['Avg_Optimal'], color=colors['darkred'], label='Optimal Subsidy')
    axs[0, 0].plot(x_fit2, y_fit2, color=colors['darkred'], linewidth = 2)
    axs[0, 0].text(df7.loc['St. Martin', 'Avg_Self_Loss']-10000, df7.loc['St. Martin', 'Avg_Fixed']+1000, 'St Martin', fontsize = 8, color = 'black')
    axs[0, 0].text(df7.loc['Lafayette', 'Avg_Self_Loss']+2000, df7.loc['Lafayette', 'Avg_Fixed'] - 500,
                   'Lafayette', fontsize=8, color='black')
    axs[0, 0].set_title('Lower Scenario', fontsize=12)
    axs[0, 0].set_xlabel('Average Flood Loss, in 10,000 (USD 2020)',  fontsize = 8)
    axs[0, 0].set_ylabel('Subsidy Per Household, in 1,000 (USD 2020)',  fontsize = 8)
    axs[0, 0].set_xlim(50000, 131000)
    axs[0, 0].set_xticks(np.arange(50000, 131000, 10000), np.arange(5, 14, 1))
    axs[0, 0].set_ylim(5000, 31000)
    axs[0, 0].set_yticks(np.arange(5000, 31000, 5000), np.arange(5, 31, 5))

    coefficients3 = np.polyfit(df8['Avg_Self_Loss'], df8['Avg_Fixed'], 1)
    polynomial3 = np.poly1d(coefficients3)
    x_fit3 = np.linspace(min(df8['Avg_Self_Loss']) - 10000, max(df8['Avg_Self_Loss']) + 10000, 1000)
    y_fit3 = polynomial3(x_fit3)
    axs[0, 1].scatter(df8['Avg_Self_Loss'], df8['Avg_Fixed'].values, color=colors['darkblue'], label='Fixed Subsidy')
    axs[0, 1].plot(x_fit3, y_fit3, color=colors['darkblue'], linewidth = 2)

    coefficients4 = np.polyfit(df8['Avg_Self_Loss'], df8['Avg_Optimal'], 1)
    polynomial4 = np.poly1d(coefficients4)
    x_fit4 = np.linspace(min(df8['Avg_Self_Loss']) - 10000, max(df8['Avg_Self_Loss']) + 10000, 1000)
    y_fit4 = polynomial4(x_fit4)
    axs[0, 1].scatter(df8['Avg_Self_Loss'], df8['Avg_Optimal'].values, color=colors['darkred'],
                   label='Optimal Subsidy')
    axs[0, 1].plot(x_fit4, y_fit4, color=colors['darkred'], linewidth=2)
    axs[0, 1].text(df8.loc['Lafayette', 'Avg_Self_Loss']-12000, df8.loc['Lafayette', 'Avg_Optimal']-3000, 'Lafayette',\
                   fontsize=8, color = 'Black')
    axs[0, 1].set_title('Higher Scenario', fontsize=12)
    axs[0, 1].set_xlabel('Average Flood Loss, in 10,000 (USD 2020)', fontsize = 8)
    axs[0, 1].set_xlim(50000, 131000)
    axs[0, 1].set_xticks(np.arange(50000, 131000, 10000), np.arange(5, 14, 1))
    axs[0, 1].set_ylim(5000, 31000)
    axs[0, 1].set_yticks(np.arange(5000, 31000, 5000), np.arange(5, 31, 5))

    coefficients5 = np.polyfit(df7['Avg_Self_Loss'], df7['Avg_Fixed_Relo'], 1)
    polynomial5 = np.poly1d(coefficients5)
    x_fit5 = np.linspace(min(df7['Avg_Self_Loss']) - 10000, max(df7['Avg_Self_Loss']) + 10000, 1000)
    y_fit5 = polynomial5(x_fit5)
    axs[1, 0].scatter(df7['Avg_Self_Loss'], df7['Avg_Fixed_Relo'], color=colors['darkblue'], label='Fixed Subsidy')
    axs[1, 0].plot(x_fit5, y_fit5, color = colors['darkblue'], linewidth=2)

    coefficients6 = np.polyfit(df7['Avg_Self_Loss'], df7['Avg_Optimal_Relo'], 1)
    polynomial6 = np.poly1d(coefficients6)
    x_fit6 = np.linspace(min(df7['Avg_Self_Loss']) - 10000, max(df7['Avg_Self_Loss']) + 10000, 1000)
    y_fit6 = polynomial6(x_fit6)
    axs[1, 0].scatter(df7['Avg_Self_Loss'], df7['Avg_Optimal_Relo'], color=colors['darkred'], label='Optimal Subsidy')
    axs[1, 0].plot(x_fit6, y_fit6, color=colors['darkred'], linewidth=2)
    axs[1, 0].text(df7.loc['Lafayette','Avg_Self_Loss'] - 20000, df7.loc['Lafayette', 'Avg_Fixed_Relo']-5000, 'Lafayette', fontsize=8, color='black')
    axs[1, 0].text(df7.loc['Iberville', 'Avg_Self_Loss'] - 6000, df7.loc['Iberville', 'Avg_Optimal_Relo'] + 35000, \
                   'Iberville', fontsize=8, color='black')
    axs[1, 0].text(df7.loc['St. Martin', 'Avg_Self_Loss'] - 2000, df7.loc['St. Martin', 'Avg_Optimal_Relo'] + 10000, 'St Martin', fontsize=8, color='black')
    axs[1, 0].set_xlabel('Average Flood Loss, in 10,000 (USD 2020)', fontsize=8)
    axs[1, 0].set_ylabel('Subsidy Per Relocation, in 10,000 (USD 2020)', fontsize=8)
    axs[1, 0].set_xlim(50000, 131000)
    axs[1, 0].set_xticks(np.arange(50000, 131000, 10000), np.arange(5, 14, 1))
    axs[1, 0].set_ylim(50000, 360000)
    axs[1, 0].set_yticks(np.arange(50000, 361000, 50000), np.arange(5, 37, 5))

    coefficients7 = np.polyfit(df8['Avg_Self_Loss'], df8['Avg_Fixed_Relo'], 1)
    polynomial7 = np.poly1d(coefficients7)
    x_fit7 = np.linspace(min(df8['Avg_Self_Loss']) - 10000, max(df8['Avg_Self_Loss']) + 10000, 1000)
    y_fit7 = polynomial7(x_fit7)
    axs[1, 1].scatter(df8['Avg_Self_Loss'], df8['Avg_Fixed_Relo'].values, color=colors['darkblue'], label='Fixed Subsidy')
    axs[1, 1].plot(x_fit7, y_fit7, color=colors['darkblue'], linewidth=2)

    coefficients8 = np.polyfit(df8['Avg_Self_Loss'], df8['Avg_Optimal_Relo'], 1)
    polynomial8 = np.poly1d(coefficients8)
    x_fit8 = np.linspace(min(df8['Avg_Self_Loss']) - 10000, max(df8['Avg_Optimal_Relo']) + 10000, 1000)
    y_fit8 = polynomial8(x_fit8)
    axs[1, 1].scatter(df8['Avg_Self_Loss'], df8['Avg_Optimal_Relo'].values, color=colors['darkred'],
                   label='Optimal Subsidy')
    axs[1, 1].plot(x_fit8, y_fit8, color=colors['darkred'], linewidth=2)
    axs[1, 1].text(df8.loc['Iberville', 'Avg_Self_Loss'] - 12000, df8.loc['Iberville', 'Avg_Optimal_Relo']  + 20000, \
                   'Iberville', fontsize = 8, color='black')
    axs[1, 1].set_xlabel('Average Flood Loss, in 10,000 (USD 2020)', fontsize=8)
    axs[1, 1].set_xlim(50000, 131000)
    axs[1, 1].set_xticks(np.arange(50000, 131000, 10000), np.arange(5, 14, 1))
    axs[1, 1].set_ylim(50000, 360000)
    axs[1, 1].set_yticks(np.arange(50000, 361000, 50000), np.arange(5, 37, 5))

    axs[2, 0].scatter(df7['Avg_Self_Loss'], df7['Avg_Self_EASD'], color='gray', label='Fixed Subsidy')
    axs[2, 0].text(df7.loc['Iberville', 'Avg_Self_Loss']-5000, df7.loc['Iberville', 'Avg_Self_EASD'] + 0.015, 'Iberville', fontsize=8,\
                   color = 'black')
    axs[2, 0].text(df7.loc['St. Martin', 'Avg_Self_Loss'] - 10000, df7.loc['St. Martin', 'Avg_Self_EASD']+0.015,
                   'St Martin', fontsize=8, color='black')
    axs[2, 0].text(df7.loc['Lafayette', 'Avg_Self_Loss'] - 10000, df7.loc['Lafayette', 'Avg_Self_EASD'] -0.02,
                   'Lafayette', fontsize=8, color='black')
    axs[2, 0].set_xlabel('Average Flood Loss, in 10,000 (USD 2020)', fontsize=8)
    axs[2, 0].set_ylabel('Average Structural Damage (FWOA)', fontsize = 8)
    axs[2, 0].set_xlim(50000, 131000)
    axs[2, 0].set_xticks(np.arange(50000, 131000, 10000), np.arange(5, 14, 1))
    axs[2, 0].set_yticks([0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6])

    axs[2, 1].scatter(df8['Avg_Self_Loss'], df8['Avg_Self_EASD'].values, color='gray', label='Fixed Subsidy')
    axs[2, 1].text(df8.loc['Iberville', 'Avg_Self_Loss']-5000, df8.loc['Iberville', 'Avg_Self_EASD'] + 0.015, 'Iberville', fontsize=8,\
                   color = 'black')
    axs[2, 1].text(df8.loc['St. Martin', 'Avg_Self_Loss'] - 10000, df8.loc['St. Martin', 'Avg_Self_EASD'] + 0.015,
                   'St Martin', fontsize=8, color='black')
    axs[2, 1].text(df8.loc['Lafayette', 'Avg_Self_Loss'] - 12000, df7.loc['Lafayette', 'Avg_Self_EASD'] - 0.02,
                   'Lafayette', fontsize=8, color='black')
    axs[2, 1].set_xlabel('Average Flood Loss, in 10,000 (USD 2020)', fontsize=8)
    axs[2, 1].set_xlim(50000, 131000)
    axs[2, 1].set_xticks(np.arange(50000, 131000, 10000), np.arange(5, 14, 1))
    axs[2, 1].set_yticks([0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6])

    # legend for fig 1 and fig 2
    handles1, labels1 = axs[0, 0].get_legend_handles_labels()
    handles2, labels2 = axs[0, 1].get_legend_handles_labels()
    combined_handles_labels_1 = {label: handle for handle, label in zip(handles1, labels1)}
    combined_handles_labels_2 = {label: handle for handle, label in zip(handles2, labels2)}
    combined_handles_labels = {**combined_handles_labels_1, **combined_handles_labels_2}

    fig.legend(combined_handles_labels.values(), combined_handles_labels.keys(), loc='upper center',
               bbox_to_anchor=(0.5, 0.05), ncol=2, fontsize=8)

    # Add panel labels
    axs[0, 0].text(0.1, 1.1, '(A)', transform=axs[0, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[0, 1].text(0.1, 1.1, '(B)', transform=axs[0, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[1, 0].text(0.1, 1.1, '(C)', transform=axs[1, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[1, 1].text(0.1, 1.1, '(D)', transform=axs[1, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[2, 0].text(0.1, 1.1, '(E)', transform=axs[2, 0].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')
    axs[2, 1].text(0.1, 1.1, '(F)', transform=axs[2, 1].transAxes, fontsize=14, fontweight='bold', va='top',
                   ha='right')


    # legend_handles = [
    #     Patch(facecolor='grey', edgecolor='black', hatch=None, label='Flood Risks Reduction'),
    #     Patch(facecolor='grey', edgecolor='black', hatch='//', label='Subsidy Cost')
    # ]
    # fig.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(0.6, 0.53), ncol=1, fontsize=8 )

    # # legend for fig 3 and fig 4
    # handles3, labels3 = axs[1, 0].get_legend_handles_labels()
    # handles4, labels4 = axs[1, 1].get_legend_handles_labels()
    # combined_handles_labels_3 = {label: handle for handle, label in zip(handles3, labels3)}
    # combined_handles_labels_4 = {label: handle for handle, label in zip(handles4, labels4)}
    # combined_handles_labels = {**combined_handles_labels_3, **combined_handles_labels_4}
    # fig.legend(combined_handles_labels.values(), combined_handles_labels.keys(), loc='lower left',
    #            bbox_to_anchor=(0.12, 0.013), ncol=2, fontsize=8)
    # fig.legend(handles=legend_handles, loc='lower left', bbox_to_anchor=(0.6, 0.013), ncol=1, fontsize=8)

    plt.show()
    fig.savefig('Figure6.tiff', format = 'tiff', dpi=300)

Geo7df = pd.read_csv('./Geo7df.csv')
Geo8df = pd.read_csv('./Geo8df.csv')

# figure6(Geo7df, Geo8df)




