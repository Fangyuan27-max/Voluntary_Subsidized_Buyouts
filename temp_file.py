# import numpy as np
# import pandas as pd
# import random
#
# mhi_result = {}
# mhi_list = [0.5, 0.85, 1.25, 2, 999]
#
# for mhi in mhi_list:
#     mhi_result[mhi] = {}
#     mhi_result[mhi]['Total_Relocation_Num'] = np.random.randint(10, 100)
#     mhi_result[mhi]['Total_Subsidy_Amount'] = np.random.randint(10, 100)
#     mhi_result[mhi]['Total_Cost'] = np.random.randint(10, 100)
#
#     mhi_result[mhi]['Relocation_Year'] = [random.randint(0,30) for _ in range(20)]
#     mhi_result[mhi]['Percent_Relocation'] = np.random.randint(10, 100)
#     mhi_result[mhi]['Avg_Subsidy_Amount'] = np.random.randint(10, 100)
#     mhi_result[mhi]['Avg_TC'] = np.random.randint(10, 100)
# mhi_result = pd.DataFrame(mhi_result).T
# mhi_result.to_csv('mhi_result.csv')

import matplotlib.pyplot as plt
import pandas as pd

# Sample categorical data
data = ['Category A', 'Category B', 'Category A', 'Category C', 'Category A', 'Category B', 'Category B']

# Convert data to pandas Series
series = pd.Series(data)

# Count the occurrences of each category
category_counts = series.value_counts()

# Plot the counts
plt.bar(category_counts.index, category_counts.values)
plt.xlabel('Categories')
plt.ylabel('Count')
plt.title('Count of Categorical Variables')

# Annotate the plot with the count values
for i, count in enumerate(category_counts.values):
    plt.text(i, count, str(count), ha='center', va='bottom')

plt.show()