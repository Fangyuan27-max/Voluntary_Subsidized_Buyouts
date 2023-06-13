class resident: #around 44 residents in total

    ## The first version is a complete version, containing all resident information, but for the sample run, I would use a simple version to define the class
    # def __init__(self, idx, lat, lon, alt, valYear, stories, zipCode, squareFeet, replacementcost, relocationcost, eadlist, disMethod, disRate, alpha):
    #     self.idx = idx
    #     self.lat = lat
    #     self.lon = lon
    #     self.alt = alt
    #     self.valYear = valYear
    #     self.stories = stories
    #     self.squareFeet = squareFeet # In Coastal Louisiana, we do not the value of squarefeet, stories, as well as market value to calculate the flood loss
    #     self.zipCode = zipCode
    #     self.replacementcost = replacementcost
    #     self.relocationcost = relocationcost
    #     self.ead = eadlist
    #     self.disMethod = disMethod
    #     self.disRate = disRate
    #     self.alpha = alpha
    #
    #     self.selfMoveYear = 200
    #     self.motiMoveYear = 150
    #     self.selfMoveFlag = False
    #     self.motiMoveFlag = False
    #     self.freeRiderFlag = False
    #
    #     self.movedOutFlag = False
    #     self.notAffected = False
    #
    #     self.FutureLoss = []
    #     self.Subsidyneeded = []

    ## This version will only contain necessary information
    def __init__(self, idx, replacementcost, relocationcost, eadlist, disMethod, disRate, alpha):
        self.idx = idx
        self.replacementcost = replacementcost
        self.relocationcost = relocationcost
        self.ead = eadlist
        self.disMethod = disMethod
        self.disRate = disRate
        self.alpha = alpha

        self.selfMoveYear = 200
        self.motiMoveYear = 150
        self.optmotiMoveYear = 100

        self.selfMoveFlag = False
        self.motiMoveFlag = False

        self.freeRiderFlag = False

        self.movedOutFlag = False

        self.FutureLoss = []
        self.Subsidyneeded = []

    def expectedFutureLoss(self, calLength):
        for i in range(calLength):
            expectedLoss = 0
            if self.disMethod == "Exponential":
                for j in range(i, calLength):
                    expectedLoss += self.ead[j] / (1 + self.disRate) ** (j - i)
            elif self.disMethod == 'Hyperbolic':
                for j in range(i, calLength):
                    expectedLoss += self.ead[j] / (1 + self.alpha * (j - i))
            else:
                print("Please enter a valid discounting method!")
            self.FutureLoss.append(expectedLoss)

            self.Subsidyneeded.append(max(0, (self.relocationcost + self.replacementcost - expectedLoss)))




