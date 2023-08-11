class government:
    def __init__(self, disMethod, disRate, alpha):
        self.disMethod = disMethod
        self.disRate = disRate
        self.alpha = alpha

        self.subPercent = 0.5

        # record the past loss for each resident at each year
        self.pastloss = {}
        self.NPVlossSubsidy = {}
        self.Subsidyyear = {}

        # lists to record the number of relocation each year
        self.selfRelocationNum = []
        self.motiRelocationNum = []
        self.optMotiRelocationNum = []

        # lists to record the objective of three different mode
        self.objective_wo_subsidy = 0
        self.objective_fixed_subsidy = 0
        self.objective_optimize_individually = 0

    # A function to calculate the discounted
    def discountedPastLoss(self, residents, totalLength):
        for resident in residents:
            self.pastloss[resident.idx] = {}
            for i in range(totalLength):
                discountedLoss = 0
                if self.disMethod == "Exponential":
                    for j in range(0, i):
                        discountedLoss += resident.ead[j] / (1 + self.disRate) ** j
                elif self.disMethod == 'Hyperbolic':
                    for j in range(0, i):
                        discountedLoss += resident.ead[j] / (1 + self.alpha * j)
                else:
                    print("Please enter a valid discounting method!")
                self.pastloss[resident.idx][i] = discountedLoss

    def calculating_objective_WO_Optimization(self, subPercent, residents, calLength, totalLength):
        for res in residents:
            if res.selfMoveYear < calLength:
                self.objective_wo_subsidy += self.pastloss[res.idx][res.selfMoveYear]
            else:
                self.objective_wo_subsidy += self.pastloss[res.idx][totalLength - 1]

            if res.motiMoveYear < calLength and res.motiMoveYear == res.selfMoveYear:
                self.objective_fixed_subsidy += self.pastloss[res.idx][res.selfMoveYear]
            elif res.motiMoveYear < calLength and res.motiMoveYear < res.selfMoveYear:
                self.objective_fixed_subsidy += self.pastloss[res.idx][res.motiMoveYear] + subPercent * res.replacementcost /((1 + self.disRate)**res.motiMoveYear)
            else:
                self.objective_fixed_subsidy += self.pastloss[res.idx][totalLength - 1]

    def calculating_objective_W_Optimization(self, residents, calLength, totalLength):
        for res in residents:
            if res.optmotiMoveYear < calLength and res.optmotiMoveYear == res.selfMoveYear:
                self.objective_optimize_individually += self.pastloss[res.idx][res.selfMoveYear]
            elif res.optmotiMoveYear < calLength and res.optmotiMoveYear < res.selfMoveYear:
                self.objective_optimize_individually += self.pastloss[res.idx][res.optmotiMoveYear] + res.Subsidyneeded[res.optmotiMoveYear] /((1 + self.disRate)**res.optmotiMoveYear)
            else:
                self.objective_optimize_individually += self.pastloss[res.idx][totalLength - 1]




