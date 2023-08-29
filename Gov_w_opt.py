def Run_W_Optimization(gov, resList, calLength, decLength, totalLength):
    # the subsidy needed to motivate relocation every year is calculated when creating residents
    # for each resident, government will select the year in which the NPV of past loss and subsidy is minimal
    # the first step is to calculate the past loss for government

    if gov.disMethod == "Exponential":
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                NPVsum.append(gov.pastloss[res.idx][year] + (res.Subsidyneeded[year])/(1+gov.disRate)**year)
            gov.NPVlossSubsidy[res.idx] = NPVsum

            moveYear_Optimize = gov.NPVlossSubsidy[res.idx].index(min(gov.NPVlossSubsidy[res.idx]))
            # check if the relocation satisfies the condition that B/C are greater than 1
            if moveYear_Optimize == calLength - 1:
                res.optmotiMoveYear = 100
            else:
                cost = res.Subsidyneeded[moveYear_Optimize]
                if res.selfMoveYear < calLength:
                    EAD_reduction = sum(
                        [res.ead[i] / (1 + gov.disRate) ** (i - moveYear_Optimize) for i in range(moveYear_Optimize, res.selfMoveYear)])
                else:
                    EAD_reduction = sum([res.ead[i] / (1 + gov.disRate) ** (i - moveYear_Optimize) for i in range(moveYear_Optimize, moveYear_Optimize + decLength)])

                if EAD_reduction >= cost:
                    res.optmotiMoveYear = moveYear_Optimize
                    res.optimotiFlag = 1
                else:
                    res.optmotiMoveYear = res.selfMoveYear
                    res.optimotiFlag = 0
            gov.Subsidyyear[res.idx] = res.optmotiMoveYear


    elif gov.disMethod == 'Hyperbolic':
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                NPVsum.append(gov.pastloss[res.idx][year] + (res.Subsidyneeded[year]) / (1 + gov.alpha * year))
            gov.NPVlossSubsidy[res.idx] = NPVsum

            moveYear_Optimize = gov.NPVlossSubsidy[res.idx].index(min(gov.NPVlossSubsidy[res.idx]))
            if moveYear_Optimize == calLength - 1:
                res.optmotiMoveYear = 100
            else:
                cost = res.Subsidyneeded[moveYear_Optimize]
                if res.selfMoveYear <= 30:
                    EAD_reduction = sum(
                        [res.ead[i] / (1 + gov.alpha * (i-moveYear_Optimize)) for i in range(moveYear_Optimize, res.selfMoveYear)])
                else:
                    EAD_reduction = sum([res.ead[i] / (1 + gov.disRate) ** (i - moveYear_Optimize) for i in range(moveYear_Optimize + decLength)])

                if EAD_reduction >= cost and not (moveYear_Optimize == res.selfMoveYear):
                    res.optmotiMoveYear = moveYear_Optimize
                    res.optimotiFlag = 1
                else:
                    res.optmotiMoveYear = res.selfMoveYear

            gov.Subsidyyear[res.idx] = res.optmotiMoveYear

    else:
        print("The discounting method should be either Exponential or Hyperbolic")

    gov.calculating_objective_W_Optimization(resList, calLength, totalLength)

    return gov





























