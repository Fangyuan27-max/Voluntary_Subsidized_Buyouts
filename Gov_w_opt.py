import pandas as pd
import numpy as np
import Class_Gov
import Class_Res

def Run_W_Optimization(government, resList, calLength):
    # the subsidy needed to motivate relocation every year is calculated when creating residents
    # for each resident, government will select the year in which the NPV of past loss and subsidy is minimal
    # the first step is to calculate the past loss for government
    government.discountedPastLoss(resList, calLength)

    if government.disMethod == "Exponential":
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                NPVsum.append(government.pastloss[res.idx][year] + res.Subsidyneeded[year]/(1+government.disRate)**year)
            government.NPVlossSubsidy[res.idx] = NPVsum
            government.Subsidyyear[res.idx] = government.NPVlossSubsidy[res.idx].index(min(government.NPVlossSubsidy[res.idx]))

    elif government.disMethod == 'Hyperbolic':
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                NPVsum.append(government.pastloss[res.idx][year] + res.Subsidyneeded[year] / (1 + government.alpha * year))
            government.NPVlossSubsidy[res.idx] = NPVsum
            government.Subsidyyear[res.idx] = government.NPVlossSubsidy[res.idx].index(min(government.NPVlossSubsidy[res.idx]))
    else:
        print("The discounting method should be either Exponential or Hyperbolic")

    return government







