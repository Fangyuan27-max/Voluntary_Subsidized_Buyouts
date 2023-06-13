class government:

    def __init__(self, disMethod, disRate, alpha):
        self.disMethod = disMethod
        self.disRate = disRate
        self.alpha = alpha

        # record the past loss for each resident at each year
        self.pastloss = {}
        self.NPVlossSubsidy = {}
        self.Subsidyyear = {}

        # lists to record the number of relocation each year
        self.selfRelocationNum = []
        self.motiRelocationNum = []
        # lists to record the subsidy cost and total buyout each year
        self.subsidycost = []
        self.totalcost = []

        self.totalobjective = []

    def discountedPastLoss(self, residents, calLength):
        for resident in residents:
            self.pastloss[resident.idx] = {}
            for i in range(calLength):
                discountedLoss = 0
                if self.disMethod == "Exponential":
                    for j in range(0, i):
                        discountedLoss += resident.ead[j] / (1 + self.disRate) ** (j - i)
                elif self.disMethod == 'Hyperbolic':
                    for j in range(0, i):
                        discountedLoss += resident.ead[j] / (1 + self.alpha * j)
                else:
                    print("Please enter a valid discounting method!")
                self.pastloss[resident.idx][i] = discountedLoss

    def relocation_num_year(self, resList, calLength):
        for i in range(calLength):
            count_self = 0
            count_moti = 0
            for res in resList:
                if res.selfMoveYear == i:
                    count_self += 1
                else:
                    count_self += 0

                if res.motiMoveYear == i:
                    count_moti += 1
                else:
                    count_moti += 0
            self.selfRelocationNum.append(count_self)
            self.motiRelocationNum.append(count_moti)





