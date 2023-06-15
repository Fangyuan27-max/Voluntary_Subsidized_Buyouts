import Class_Res

def CreateRes(resident_info, ead_info, colname, startcol,  disMethod, disRate, alpha, calLength):
    # Instantiate residents
    res_list = []
    for index, res in resident_info.iterrows():
        if index == 0:
            continue

        eadlist = ead_info.loc[ead_info[colname] == res[colname]].values.tolist()[0][startcol:]

        resident = Class_Res.resident(res[colname], round(res['replacement_cost'],1), round(res['relocation_cost'],1), eadlist, disMethod, disRate, alpha)
        resident.expectedFutureLoss(calLength)

        # calculate the expected future loss and determine when to relocate for every resident
        res_list.append(resident)
    return res_list










