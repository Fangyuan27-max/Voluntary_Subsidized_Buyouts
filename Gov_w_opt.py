def Run_W_Optimization(government, resList, calLength):
    # the subsidy needed to motivate relocation every year is calculated when creating residents
    # for each resident, government will select the year in which the NPV of past loss and subsidy is minimal
    # the first step is to calculate the past loss for government

    if government.disMethod == "Exponential":
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                NPVsum.append(government.pastloss[res.idx][year] + (res.Subsidyneeded[year]+res.replacementcost + res.relocationcost)/(1+government.disRate)**year)
            government.NPVlossSubsidy[res.idx] = NPVsum

            moveYear_Optimize = government.NPVlossSubsidy[res.idx].index(min(government.NPVlossSubsidy[res.idx]))
            if moveYear_Optimize == calLength - 1:
                res.optmotiMoveYear = 100
            else:
                res.optmotiMoveYear = moveYear_Optimize
                res.optimotiFlag = 1
            government.Subsidyyear[res.idx] = res.optmotiMoveYear


    elif government.disMethod == 'Hyperbolic':
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                NPVsum.append(government.pastloss[res.idx][year] + (res.Subsidyneeded[year]+res.replacementcost + res.relocationcost) / (1 + government.alpha * year))
            government.NPVlossSubsidy[res.idx] = NPVsum

            moveYear_Optimize = government.NPVlossSubsidy[res.idx].index(min(government.NPVlossSubsidy[res.idx]))
            if moveYear_Optimize == calLength - 1:
                res.optmotiMoveYear = 100
            else:
                res.optmotiMoveYear = moveYear_Optimize
                res.optimotiFlag = 1
            government.Subsidyyear[res.idx] = res.optmotiMoveYear

    else:
        print("The discounting method should be either Exponential or Hyperbolic")

    government.calculating_objective_W_optimization(resList, calLength)
    return government















