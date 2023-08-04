def ResRun_WO_Optimization(gov, resList, subPercent, calLength, decLength, totalLength):
    ## separate the calculation of self-relocation and fixed-subsidy relocation
    # self-relocation
    for res in resList:
        for year in range(calLength):
            # check if the resident has moved out
            if res.selfMoveFlag:
                break
            if not res.selfMoveFlag and res.FutureLoss[year] >= res.replacementcost + res.relocationcost:
                res.selfMoveFlag = 1
                res.selfMoveYear = year

    # fixed-subsidy relocation
    for res in resList:
        for year in range(calLength):
            # check if the resident has moved out
            if res.motiMoveFlag:
                break
            if not res.motiMoveFlag and res.FutureLoss[year] + res.replacementcost*subPercent >= res.replacementcost + res.relocationcost:
                # check the b/c of such a relocation, compare the EAD reduction with the total cost
                cost = res.replacementcost*subPercent + res.replacementcost + res.relocationcost
                # exponential discounting - discount the ead reduction using government's discount rate
                if gov.disMethod == "Exponential":
                    if res.selfMoveYear < calLength:
                        EAD_reduction_gov = sum(
                            [res.ead[i] / (1 + gov.disRate) ** (i - year) for i in range(year, res.selfMoveYear)])
                    else:
                        EAD_reduction_gov = sum([res.ead[i] / (1 + gov.disRate) ** (i - year) for i in range(year, year + decLength)])

                # hyperbolic discounting
                elif gov.disMethod == 'Hyperbolic':
                    if res.selfMoveYear < calLength:
                        EAD_reduction_gov = sum([res.ead[i] / (1 + gov.alpha * (i - year)) for i in range(year, res.selfMoveYear)])
                    else:
                        EAD_reduction_gov = sum([res.ead[i] / (1 + gov.alpha * (i - year)) for i in range(year, year + decLength)])

                if EAD_reduction_gov >= cost:
                    res.motiMoveFlag = 1
                    res.motiMoveYear = year
                # if b/c is less than 1, the moti_year is the same as the self_relocation unless there is a year in the future that moti_year is earlier than self_relocation year
                else:
                    res.motiMoveYear = res.selfMoveYear
                    res.motiMoveFlag = 0

    gov.discountedPastLoss(resList, totalLength)

    gov.calculating_objective_WO_optimization(subPercent, resList, calLength, totalLength)

    return gov, resList































