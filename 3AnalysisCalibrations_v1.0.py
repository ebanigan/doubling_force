#############################FILE AND LABEL CHECKS############################
if not os.path.exists (__flocation__):
    sys.exit("Please add "+ rawDataFolder + " folder to current folder")
if ietCalSuffix1 == "alphabet":
    calFiles = alphabet
elif ietCalSuffix1 == "numbers":
    calFiles = numbers
else: 
    sys.exit ("Please indicate how calibration suffixes are labeled  and increased")
if not (os.path.exists(__flocation__ + run + "_"+ietCalSuffix1[0]+ietCalSuffix2
                       ) or calManual[0] == "y"):
    sys.exit ("Please manually enter force pipette stiffness or add calibration "+
              "files to " + rawDataFolder + " folder as " + run + "_"+ietCalSuffix2+
               " starting with " + ietCalSuffix1[0]+ietCalSuffix2)
########################LABEL AND INFORMATION CREATION########################
calFiles = [run + "_" + s + ietCalSuffix2 for s in calFiles]
AllForcePipette = np.zeros((cals+1, 5)).astype(str)
AllForcePipette[0,0:5]=("Calibration Values Used","Sigma from average",
                        "x0Sigma","x1Sigma","x2Sigma")
calGapF = calGap * calStepFactor
calEventTimesF = [i * calStepFactor for i in calEventTimes]
ietCals = -1
#######################CALIBRATION ITERATION FROM FILES#######################
while ietCals <= cals:
    ietCals, fig = ietCals+1, fig + 1
    if cals >= ietCals + 1: 
        if not os.path.exists(__flocation__+calFiles[ietCals]):
            sys.exit ("please add " +calFiles[ietCals] + " to RawData File or edit "+
                      "number of calibration instances")
        calRaw = np.asmatrix(pd.read_table(__flocation__+calFiles[ietCals],sep = "\t"))
        calPosAll = calRaw[:,columnLocations["calX"]]
        calTime = calRaw[:,columnLocations["calTime"]]
        calT0 = calRaw[0]
        calT0,calT1,calT2,calT3,calT4,calT5 = (
              np.where(calTime>calT0)[0][0],
              np.where(calT0+calTime>(calEventTimesF[0]-calGapF))[0][0],
              np.where(calT0+calTime>(calEventTimesF[1]+calGapF))[0][0],
              np.where(calT0+calTime>(calEventTimesF[2]-calGapF))[0][0], 
              np.where(calT0+calTime>(calEventTimesF[2]+calGapF))[0][0],
              np.where(calT0+calTime>calEventTimesF[3]-calGapF)[0][0])
        calX0All, calX1All, calX2All = (
            np.arange(calT0,calT1,1),
            np.arange(calT2,calT3,1),
            np.arange(calT4,calT5,1))
        calX0All,calX1All,calX2All = (
            calPosAll[[calX0All]],
            calPosAll[[calX1All]],
            calPosAll[[calX2All]])
        calX0 = np.mean(calX0All)
        calX1, calX2 = np.mean(calX1All)-calX0, np.mean(calX2All)-calX0
        if calShowPlot == "y":
            plt.figure(fig)
            plt.title(str(calFiles[ietCals]))
            plt.plot(calPosAll),plt.plot(calX0All),plt.plot(calX1All),
            plt.plot(calX2All)
        forcePipStr = calPipette * (calX2-calX1)/(calX1)
####################CONSOLIDATES CALIBRATION INSTANCE DATA####################
        AllForcePipette[ietCals+1,(0,2,3,4)] = (forcePipStr,
                         np.std(calX0All),
                         np.std(calX1All),
                         np.std(calX2All))
####################CONSOLIDATES AND ANALYZES CALIBRATION#####################
AllForcePipetteUncut = AllForcePipette
AllForcePipetteUncut [1:,1] = (abs(AllForcePipetteUncut[1:,0].astype(float) - 
        np.mean(AllForcePipetteUncut[1:,0].astype(float)))/
        np.std(AllForcePipetteUncut[1:,0].astype(float)))
AllForcePipette = np.delete(AllForcePipette,calRejMan,axis=0)
calN = len(AllForcePipette)-1
AForcePipette = np.mean((AllForcePipette[1:calN+1,0]).astype(float))
AForcePipetteSterr = np.std(AllForcePipette[1:calN+1,0].astype(float))/(
        np.size(AllForcePipette[1:calN+1,0])**0.5)
AllForcePipette[1:,1] = (abs(AllForcePipette[1:,0].astype(float) - 
        np.mean(AllForcePipette[1:,0].astype(float)))/
        np.std(AllForcePipette[1:,0].astype(float)))
calRej = calRejMan
AllForcePipetteUncut[0,0] = "All Calibrations Uncut"
#############CALCULATES DATA QUALITY AND ATTEMPTS TO MAKE IT GOOD#############
if calAutoAgree == "y":
    while AForcePipetteSterr/AForcePipette > qualityParameters[1][0] and (
            calN > qualityN["N"]):
        calOutlier = (np.where((AllForcePipette[:,1]) == (max(AllForcePipette[
                    1:,1].astype(float))).astype(str)))
        calRej = calRej + [np.where(AllForcePipetteUncut[1:,0].astype(
                float)==AllForcePipette[[calOutlier[0][0]],0].astype(float)[0])[0][0]+1]
        AllForcePipette = np.delete(AllForcePipette,calOutlier,axis=0)
        calN = calN - 1
        AForcePipette = np.mean((AllForcePipette[1:,0]).astype(float))
        AForcePipetteSterr = (np.std(AllForcePipette[1:,0].astype(float))/(
                np.size(AllForcePipette[1:,0])**0.5))
        AllForcePipette[1:,1] = ((abs(AllForcePipette[1:,0].astype(float)-
               AForcePipette.astype(float)))/
               np.std(AllForcePipette[1:,0].astype(float)))
if calN >= qualityN["N"] and any(AForcePipetteSterr/AForcePipette < (
        np.asarray(qualityParameters[1][:]))):
    calQuality =  qualityParameters[0][max(np.where(AForcePipetteSterr/
            AForcePipette<(np.asarray(qualityParameters[1][:])))[0])]
else:
    calQuality = qualityParameters[2][0]
########################PRINTS CALIBRATION INFORMATION########################
print (runName + " Force Pipette equal to " + str(round(AForcePipette,2)))
print ("Calibrations were of " + calQuality + " quality")
if len (calRej) == 0:
    print ("No Calibrations were rejected")
else:
    print ("Calibrations " + str(calRej) + " were rejected")