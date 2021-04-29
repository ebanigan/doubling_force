#############################FILE AND LABEL CHECKS############################
if not os.path.exists (__flocation__):
    sys.exit("Please add "+ rawDataFolder + " folder to current folder")
if ietPullSuffix1 == "alphabet":
    pullFiles = alphabet
elif ietPullSuffix1 == "numbers":
    pullFiles = numbers
else: 
    sys.exit ("Please indicate how pull suffixes are labeled and increased")
if not (os.path.exists(__flocation__ + run + "_"+ietPullSuffix1[0]+ietPullSuffix2)):
    sys.exit ("Please add pull files to "+ rawDataFolder + " folder as " + 
              run + "_"+ ietPullSuffix2 + " starting with " + ietPullSuffix1[0]+
              ietPullSuffix2)
########################LABEL AND INFORMATION CREATION########################
AllStrDefUncut = (np.zeros((pulls+3, 8))).astype(str)
pullsHyst,pullsNoisy, pullRej = [],[], pullRejMan
pullFilesUsed = [run + "_" + s + ietPullSuffix2 for s in pullFiles]
AllStrDefUncut[0, :] = ["Pull number Uncut","Force pipette max", "Stiff pipette max",
        "Out Slope (no_units)", "R Value (Out)","Ret Slope (no_units)",
        "Hysteresis angle (deg)","Sigma from average"]
AllStrDefUncut[-2,6] = qualityParameters[2][0]
ietPull = 0
if not pullDataCamera[0] == "NA":
    pullMag =  cameraInfo[pullDataCamera[0]]/(
        float(pullDataCamera[1])*float(pullDataCamera[2]))
else:
    pullMag = 1    
##########################PULL ITERATION FROM FILES###########################
while ietPull < pulls:
    ietPull,fig = ietPull+1,fig+1
    if ietPull < pulls+1:
        if not os.path.exists(__flocation__+pullFilesUsed[ietPull-1]):
            sys.exit ("please add " +pullFilesUsed[ietPull-1] + " to RawData File,"+ 
                      " edit the number of pulls, or change pull suffixes")
        pullRaw = np.asarray(pd.read_table(__flocation__+pullFilesUsed[ietPull-1],sep="\t"))
        pullP1XRaw = pullRaw[:,columnLocations["pullP1X"]]*pullMag
        pullP2XRaw = pullRaw[:,columnLocations["pullP2X"]]*pullMag
        if pullRejJump[0] == "y":
            pullP1Jump = np.zeros(len(pullP1XRaw)-1)
            for i in range(0,len(pullP1XRaw)-1):
               pullP1Jump[i] = abs(pullP1XRaw[i+1]-pullP1XRaw[i])
            pullP1Jump = np.where(pullP1Jump >= float(pullRejJump[1]))
            pullP1X = np.delete(pullP1XRaw,pullP1Jump,None)
            pullP2X = np.delete(pullP2XRaw,pullP1Jump,None)
            pullP2Jump = np.zeros(len(pullP2X)-1)
            for i in range(0,len(pullP2X)-1):
               pullP2Jump[i] = abs(pullP2X[i+1]-pullP2X[i])
            pullP2Jump = np.where(pullP2Jump >= float(pullRejJump[1]))
            pullP1X = np.delete(pullP1X,pullP2Jump,None)
            pullP2X = np.delete(pullP2X,pullP2Jump,None)
        else:
            pullP1X, pullP2X = pullP1XRaw, pullP2XRaw
        if max(pullP1X) - min(pullP1X) > max(pullP2X) - min(pullP2X):
            pullSP,pullDef = pullP1X,pullP2X
        else: 
            pullSP,pullDef = pullP2X,pullP1X
        pullStr = pullSP-pullDef
        pullMax = np.where(abs(pullSP) == np.max(abs(pullSP)))
        pullRet = np.arange(min(pullMax[0]), len(pullStr),1)
        pullOutStr = np.delete(pullStr,pullRet,None)
        pullOutDef = np.delete(pullDef,pullRet,None)
        pullOutSD = (len(pullOutStr)*(sum(pullOutStr*pullOutDef))-sum(
                pullOutStr)*sum(pullOutDef))/(len(pullOutStr)*sum(
                pullOutStr**2)-sum(pullOutStr)**2)
        pullOutRV = (len(pullOutStr)*(sum(pullOutStr*pullOutDef))-sum(
                pullOutStr)*sum(pullOutDef))/((len(pullOutStr)*sum(
                pullOutStr**2)-sum(pullOutStr)**2)*(len(pullOutDef)*sum(
                pullOutDef**2)-sum(pullOutDef)**2))**0.5
        pullRetStr = pullStr[pullRet]
        pullRetDef = pullDef[pullRet]
        pullRetSD = (len(pullRetStr)*(sum(pullRetStr*pullRetDef))-sum(
                pullRetStr)*sum(pullRetDef))/(len(pullRetStr)*sum(
                pullRetStr**2)-sum(pullRetStr)**2)
        pullHystAngle = (180/3.1415)*np.arctan(abs(pullRetSD-pullOutSD)/(
                1+pullRetSD*pullOutSD))
###############################PLOTS PULL GRAPHS##############################
        if pullShowRawPlot == "y" or pullShowJumpRejPlot == "y":
            plt.figure(fig)
            plt.title(pullFilesUsed[ietPull-1]+" Stretch-Deflection")
        if pullShowRawPlot == "y":
            plt.plot(pullP1XRaw,pullP2XRaw)
        if pullShowJumpRejPlot == "y":
            plt.plot(pullP1X,pullP2X)
        if pullShowSDPlot == "y" or pullShowSDOutPlot == "y" or pullShowFitPlot == "y":
            fig = fig +1
            plt.figure(fig)
            plt.title(pullFilesUsed[ietPull-1]+" Force-Extension")
        if pullShowSDPlot == "y":
            plt.plot(pullStr,pullDef, color="Orange")
        if pullShowSDOutPlot == "y":
            plt.plot(pullOutStr,pullOutDef, color="Black")
        if pullShowFitPlot == "y":
            plt.plot(pullOutStr,pullOutStr*pullOutSD,color="Black")
            plt.plot(pullOutStr,pullOutStr*pullRetSD,color="Orange")
########################CONSOLIDATES PULL INSTANCE DATA#######################
        AllStrDefUncut[ietPull,:] = [ietPull,pullDef[pullRet[0]],
             pullSP[pullRet[0]],pullOutSD,pullOutRV,pullRetSD,pullHystAngle,""]
    if pullOutSD < 0 and not ietPull in pullRej:
        pullRej = pullRej + [ietPull]
    if abs(pullHystAngle) > float(pullRejHys[1]):
            pullsHyst = pullsHyst + [ietPull]
            if pullRejHys[0] == "y"and not ietPull in pullRej:
                pullRej = pullRej + [ietPull]
    if float(pullRejRValue[1]) > pullOutRV:
        pullsNoisy = pullsNoisy + [ietPull]
        if pullRejRValue[0] == "y" and not ietPull in pullRej:
            pullRej = pullRej + [ietPull]
#######################CONSOLIDATES AND ANALYZES PULLS########################
pullN = ietPull
AllStrDefUncut [1:-2,7] = (abs(AllStrDefUncut[1:-2,3].astype(float) - 
        np.mean(AllStrDefUncut[1:-2,3].astype(float)))/
        np.std(AllStrDefUncut[1:-2,3].astype(float)))
AllStrDefUncut[-2,:] = ("Average",np.mean((AllStrDefUncut[1:-2,1]).astype(float)),
        np.mean((AllStrDefUncut[1:-2,2]).astype(float)),
        np.mean((AllStrDefUncut[1:-2,3]).astype(float)),"N","Noisy Pulls",
        "Pulls with hysteresis","Outlier Detected?")
AllStrDefUncut[-1,:] = ("Standard Error",(np.std((AllStrDefUncut[1:-2,1]).astype(
        float))/pullN**0.5),np.std((AllStrDefUncut[1:-2,2]).astype(float))/
        pullN**0.5,np.std((AllStrDefUncut[1:-2,3]).astype(float))/pullN**0.5,
        pullN,str(pullsNoisy),str(pullsHyst),"")
AllStrDef = AllStrDefUncut
pullN = pullN-len(pullRej)
AllStrDef [-2,(1,2,3)] = (np.mean((AllStrDef[1:-2,1]).astype(float)),
          np.mean((AllStrDef[1:-2,2]).astype(float)),
          np.mean((AllStrDef[1:-2,3]).astype(float)))
AllStrDef [-1,(1,2,3,4)] = ((
        np.std((AllStrDef[1:-2,1]).astype(float))/pullN**0.5),
        (np.std((AllStrDef[1:-2,2]).astype(float))/pullN**0.5),
        (np.std((AllStrDef[1:-2,3]).astype(float))/pullN**0.5),pullN)
AllStrDef [1:-2,7] = (abs(AllStrDef [1:-2,3].astype(float) - 
        np.mean(AllStrDef [1:-2,3].astype(float)))/
        np.std(AllStrDef [1:-2,3].astype(float)))
AStrDef = float(AllStrDef[-2,3])
AStrDefSterr = float(AllStrDef[-1,3])
#############CALCULATES DATA QUALITY AND ATTEMPTS TO MAKE IT GOOD#############
if pullAutoAgree == "y":
    while AStrDefSterr/AStrDef > qualityParameters[1][0] and (
            pullN > qualityN["N"]):
        pullOutlier = (np.where((AllStrDef[:,7]) == (max(AllStrDef[1:-2,7].astype(float))).astype(str)))
        pullRej = pullRej + [np.where(AllStrDefUncut[1:,3].astype(float)==AllStrDef[[pullOutlier[0][0]],3].astype(float)[0])[0][0]+1]
        AllStrDef = np.delete(AllStrDef,pullOutlier,axis=0)
        pullN = pullN - 1
        AllStrDef [-2,(1,2,3)] = (np.mean((AllStrDef[1:-2,1]).astype(float)),
          np.mean((AllStrDef[1:-2,2]).astype(float)),
          np.mean((AllStrDef[1:-2,3]).astype(float)))
        AllStrDef [-1,(1,2,3,4)] = ((
                np.std((AllStrDef[1:-2,1]).astype(float))/pullN**0.5),
                (np.std((AllStrDef[1:-2,2]).astype(float))/pullN**0.5),
                (np.std((AllStrDef[1:-2,3]).astype(float))/pullN**0.5),pullN)
        AllStrDef [1:-2,7] = (abs(AllStrDef [1:-2,3].astype(float) - 
                np.mean(AllStrDef [1:-2,3].astype(float)))/
                np.std(AllStrDef [1:-2,3].astype(float)))
        AStrDef = float(AllStrDef[-2,3])
        AStrDefSterr = float(AllStrDef[-1,3])
if pullN >=qualityN["N"] and any(AStrDefSterr/AStrDef < (
        np.asarray(qualityParameters[1][:]))):
    pullQuality =  qualityParameters[0][max(np.where(AStrDefSterr/
            AStrDef<(np.asarray(qualityParameters[1][:])))[0])]
else:
    pullQuality = qualityParameters[2][0]
AllStrDef[0,0] = "All Pulls Used" 
########################PRINTS CALIBRATION INFORMATION########################
print (runName + " Stretch-Deflection equal to " + str(round(AStrDef,4)))
print ("Pulls were of " + pullQuality + " quality")
if len(pullsHyst) == 0:
    print ("No Runs had hysteresis")
else:
    print ("Pulls " + str(pullsHyst[:]) + " had hysteresis")
if not pullRejHys[0] == "y":
    print (" but accepting pulls with hysteresis")
if len(pullsNoisy) == 0:
    print ("No Runs had high noise")
else:
    print ("Pulls " + str(pullsNoisy[:]) + " had high noise")
if not pullRejRValue[0] == "y":
    print (" but accepting noisy pulls")
if len (pullRej) == 0:
    print ("No Pulls were rejected")
else:
    print ("Pulls " + str(pullRej) + " were rejected")