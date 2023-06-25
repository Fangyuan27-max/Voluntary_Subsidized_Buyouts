import numpy as np
import pandas as pd

mhi_result = {}
mhi_list = [0.5, 0.85, 1.25, 2, 999]

for mhi in mhi_list:
    mhi_result[mhi] = {}
    mhi_result[mhi]['Total_Relocation_Num'] = np.random.randint(10, 100)
    mhi_result[mhi]['Total_Subsidy_Amount'] = np.random.randint(10, 100)
    mhi_result[mhi]['Total_Cost'] = np.random.randint(10, 100)

    mhi_result[mhi]['Relocation_Year'] = np.random.uniform(0, 15, 20)
    mhi_result[mhi]['Percent_Relocation'] = np.random.randint(10, 100)
    mhi_result[mhi]['Avg_Subsidy_Amount'] = np.random.randint(10, 100)
    mhi_result[mhi]['Avg_TC'] = np.random.randint(10, 100)
mhi_result = pd.DataFrame(mhi_result).T
mhi_result.to_csv('mhi_result.csv')