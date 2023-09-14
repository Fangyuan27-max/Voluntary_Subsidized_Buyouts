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
        self.obj_fixed_subsidy_replacement = 0

        self.objective_optimize_individually = 0
        self.obj_optimal_subsidy_replacement = 0

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









