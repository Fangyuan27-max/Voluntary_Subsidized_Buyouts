import Class_Res

def CreateRes(resident_info, ead_info, colname, startcol,  disMethod, disRate, alpha, inflaRate, calLength, decLength):
    # Instantiate residents
    res_list = []
    for index, res in resident_info.iterrows():
        if index == 0:
            continue

        eadlist = ead_info.loc[ead_info[colname] == res[colname]].values.tolist()[0][startcol:]

        replacement_cost = int(res['replacement_cost'])
        relocation_cost = int(res['relocation_cost'])

        resident = Class_Res.resident(res[colname], replacement_cost, relocation_cost, eadlist, disMethod, disRate, alpha, inflaRate, res['mhi_ratio'])
        resident.expectedFutureLoss(calLength, decLength)

        # calculate the expected future loss and determine when to relocate for every resident
        res_list.append(resident)
    return res_list










