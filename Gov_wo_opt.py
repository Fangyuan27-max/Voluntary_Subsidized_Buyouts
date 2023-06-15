import Class_Gov
import copy

def ResRun_WO_Optimization(resList, subPercent, calLength):
    for res in resList:
        for year in range(calLength):
            # check if the resident has moved out
            if res.selfMoveFlag and res.motiMoveFlag:
                break
            # check the self relocation
            if not res.selfMoveFlag and res.FutureLoss[year] >= res.replacementcost * (1 + res.inflaRate) ** year + res.relocationcost * (1 + res.inflaRate) ** year:
                res.selfMoveFlag = 1
                res.selfMoveYear = year
            # check the motivated relocation
            if not res.motiMoveFlag and res.FutureLoss[year] + res.replacementcost*subPercent * (1 + res.inflaRate) ** year >= res.replacementcost * (1 + res.inflaRate) ** year + \
                    res.relocationcost * (1 + res.inflaRate) ** year:
                res.motiMoveFlag = 1
                res.motiMoveYear = year
    return resList

def WO_optimization_Tuning(disMethod, disRate, govAlpha, calLength, resList,relcostList, perList):
    # instantiate government
    Gov = Class_Gov(disMethod, disRate, govAlpha)
    # run simulation for each combination of parameters and select the one accoring to requirement
    for relocationcost in relcostList:
        for percent in perList:
            resListcopy = copy.deepcopy(resList)
            resListcopy = ResRun_WO_Optimization(resListcopy, relocationcost, percent, calLength)
            Gov.relocation_num_year(resListcopy, calLength)















