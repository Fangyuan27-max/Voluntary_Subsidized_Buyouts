import pandas as pd
import numpy as np
import time
import Class_Res

def CreateRes(resident_info, ead_info, colname, disMethod, disRate, alpha, calLength):
    # Instantiate residents
    res_list = []
    for index, res in resident_info.iterrows():
        eadlist = ead_info.loc[ead_info[colname] == res['idx']].values.tolist()[0][1:]

        resident = Class_Res.resident(res['idx'], res['replacementcost'], res['relocationcost'], eadlist, disMethod, disRate, alpha)
        resident.expectedFutureLoss(calLength)

        # calculate the expected future loss and determine when to relocate for every resident
        res_list.append(resident)
    return res_list





