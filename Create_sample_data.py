import numpy as np
import pandas as pd
import random

# eadlist_1 = {1: [1] + list(np.arange(0.5,1,0.5/30)),
#              2: [2] + list(np.arange(1,1.5,0.5/30)),
#              3: [3] + list(np.arange(0.5,2,1.5/30))}
# eadlist_2 = pd.DataFrame(eadlist_1)
# eadlist = eadlist_2.T
#
# keys = ['id'] + [f"EAD{i}" for i in range(1,31)]
# eadlist.columns = keys
# eadlist.set_index('id', inplace=True)
# print(eadlist)
#
# eadlist.to_csv('ead_list.csv')

keys = ['idx', 'replacementcost', 'relocationcost']
reslist1 = {1: [1,5,5],
           2: [2,10,5],
           3: [3,7,5]}
reslist2 = pd.DataFrame(reslist1)
reslist = reslist2.T
reslist.columns = keys
reslist.to_csv('Res_info.csv')

# multipleresident = {}
# for i in range(500000):
#     multipleresident[i] = [i+1] + [10,20,1.5,2005,5,1,47906,100,1]
# multipleresident2 = pd.DataFrame(multipleresident).T
# multipleresident2.columns = keys
# multipleresident2.to_csv('moresample.csv')
#
# multi_ead = {}
# for i in range(500000):
#     multi_ead[i] = [i+1] + [random.randint(1, 10) for _ in range(30)]
# eadlist_2 = pd.DataFrame(multi_ead)
# eadlist = eadlist_2.T
#
# keys = ['id'] + [f"EAD{i}" for i in range(1,31)]
# eadlist.columns = keys
# eadlist.set_index('id', inplace=True)
# # print(eadlist)
#
# eadlist.to_csv('multi_ead.csv')