class resident: #around 44 residents in total
    def __init__(self, idx, replacementcost, relocationcost, eadlist, disMethod, disRate, alpha, inflaRate, mhi_ratio):
        self.idx = idx
        self.replacementcost = replacementcost
        self.relocationcost = relocationcost
        self.ead = eadlist
        self.disMethod = disMethod
        self.disRate = disRate
        self.alpha = alpha
        self.inflaRate = inflaRate
        self.mhi_ratio = mhi_ratio

        self.selfMoveYear = 200
        self.motiMoveYear = 150
        self.optmotiMoveYear = 100

        self.selfMoveFlag = False
        self.motiMoveFlag = False
        self.optimotiFlag = False

        self.freeRiderFlag = False

        self.movedOutFlag = False

        self.FutureLoss = []
        self.Subsidyneeded = []

    def expectedFutureLoss(self, calLength, decLength):
        for i in range(calLength):
            expectedLoss = 0
            if self.disMethod == "Exponential":
                for j in range(decLength):
                    expectedLoss += self.ead[i + j] / (1 + self.disRate) ** j
            elif self.disMethod == 'Hyperbolic':
                for j in range(decLength):
                    expectedLoss += self.ead[i + j] / (1 + self.alpha * j)
            else:
                print("Please enter a valid discounting method!")
            self.FutureLoss.append(expectedLoss)

            self.Subsidyneeded.append(max(0, (self.relocationcost + self.replacementcost - expectedLoss)))



