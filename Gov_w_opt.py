def Run_W_Optimization(gov, resList, calLength, decLength):
    # the subsidy needed to motivate relocation every year is calculated when creating residents
    # for each resident, government will select the year in which the NPV of past loss and subsidy is minimal
    # the first step is to calculate the past loss for government

    if gov.disMethod == "Exponential":
        for res in resList:
            NPVsum = []
            for year in range(calLength):
                # original version
                # NPVsum.append(gov.pastloss[res.idx][year] + res.Subsidyneeded[year] / (1 + gov.disRate) ** year)
                # new version
                NPVsum.append(gov.pastloss[res.idx][year] + (res.Subsidyneeded[year] + res.relocationcost)/ (1 + gov.disRate) ** year)
                # NPVsum.append(gov.pastloss[res.idx][year] + (res.Subsidyneeded[year]+res.replacementcost + res.relocationcost)/(1+gov.disRate)**year)
            gov.NPVlossSubsidy[res.idx] = NPVsum

            moveYear_Optimize = gov.NPVlossSubsidy[res.idx].index(min(gov.NPVlossSubsidy[res.idx]))
            # check if the relocation satisfies the condition that B/C are greater than 1
            # if the minimum occurs at the 20th year, it might not be a global minimum and we assume the resident will not conduct motivated move
            if moveYear_Optimize == calLength - 1:
                res.optmotiMoveYear = 100
            else:
                # old version
                # cost = res.Subsidyneeded[moveYear_Optimize]
                # new version
                cost = round((res.Subsidyneeded[moveYear_Optimize] + res.relocationcost)/1e4, 1)
                # cost = res.replacementcost + res.relocationcost + res.Subsidyneeded[moveYear_Optimize]
                if res.selfMoveYear < calLength:
                    EAD_reduction = sum(
                        [res.ead[i] / (1 + gov.disRate) ** (i - moveYear_Optimize) for i in range(moveYear_Optimize, res.selfMoveYear)])
                else:
                    EAD_reduction = sum([res.ead[i] / (1 + gov.disRate) ** (i - moveYear_Optimize) for i in range(moveYear_Optimize, moveYear_Optimize + decLength)])

                EAD_reduction = round(EAD_reduction/1e4, 1)
                if EAD_reduction >= cost and not (moveYear_Optimize == res.selfMoveYear) and res.Subsidyneeded[moveYear_Optimize] != 0:
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
                NPVsum.append(gov.pastloss[res.idx][year] + (res.Subsidyneeded[year]+res.replacementcost + res.relocationcost) / (1 + gov.alpha * year))
            gov.NPVlossSubsidy[res.idx] = NPVsum

            moveYear_Optimize = gov.NPVlossSubsidy[res.idx].index(min(gov.NPVlossSubsidy[res.idx]))
            if moveYear_Optimize == calLength - 1:
                res.optmotiMoveYear = 100
            else:
                cost = res.replacementcost + res.relocationcost + res.Subsidyneeded[moveYear_Optimize]
                if res.selfMoveYear <= 30:
                    EAD_reduction = sum(
                        [res.ead[i] / (1 + gov.alpha * (i-moveYear_Optimize)) for i in range(moveYear_Optimize, res.selfMoveYear)])
                else:
                    EAD_reduction = sum([res.ead[i] / (1 + gov.disRate) ** (i - moveYear_Optimize) for i in range(moveYear_Optimize + decLength)])

                if EAD_reduction >= cost:
                    res.optmotiMoveYear = moveYear_Optimize
                    res.optimotiFlag = 1
                else:
                    res.optmotiMoveYear = res.selfMoveYear

            gov.Subsidyyear[res.idx] = res.optmotiMoveYear

    else:
        print("The discounting method should be either Exponential or Hyperbolic")

    return gov















