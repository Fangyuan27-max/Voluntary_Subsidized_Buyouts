def ResRun_WO_Optimization(gov, resList, subPercent, calLength):
    for res in resList:
        for year in range(calLength):
            # check if the resident has moved out
            if res.selfMoveFlag and res.motiMoveFlag:
                break
            # check the self relocation
            if not res.selfMoveFlag and res.FutureLoss[year] >= res.replacementcost + res.relocationcost:
                res.selfMoveFlag = 1
                res.selfMoveYear = year
            # check the motivated relocation
            if not res.motiMoveFlag and res.FutureLoss[year] + res.replacementcost*subPercent >= res.replacementcost + res.relocationcost:
                res.motiMoveFlag = 1
                res.motiMoveYear = year

    gov.discountedPastLoss(resList, calLength)

    gov.calculating_objective_WO_optimization(subPercent, resList, calLength)

    return gov, resList















