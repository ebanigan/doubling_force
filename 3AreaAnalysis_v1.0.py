#############################FILE AND LABEL CHECKS############################
if not l0Camera[0] in dict.keys(cameraInfo) and not l0Source == "Manual":
        sys.exit ("Camera not found for L0 measurement; please enter proper " +
                  "camera name, enter results manually (in microns), or "+
                  "update dictionary " + str(cameraInfo))
if not xSAreaCamera[0] in dict.keys(cameraInfo):
    sys.exit ("Camera not found for Area measurement; please enter proper " +
              "camera name or update dictionary"+str(cameraInfo))
############################ANALYZES L0 INFORMATION########################### 
if not l0Source == "Manual":
    l0 = [l * cameraInfo[l0Camera[0]]/(float(l0Camera[1])*float(l0Camera[2])
         ) for l in l0all[:]]
else:
    l0 = l0all
Al0, l0stdDev, l0stErr = np.mean(l0), np.std(l0),np.std(l0)/len(l0)
################DETERMINES HOW TO ANALYZE CROSS-SECTIONAL AREA################
xSAreaRes = cameraInfo[xSAreaCamera[0]]/(float(xSAreaCamera[1])*float(xSAreaCamera[2]))
if xSAreaSource[0] == "Manual":
    AxSArea = xSAreaSource[1]
elif xSAreaSource[0] == 'Manual (Px)':
    xSArea = [3.1415*0.25*(xSAreaRes*float(xSAreaSource[1:][0]))**2]
elif int(xSAreaSource[1]) == 1:
    if os.path.exists(__flocation__ + run + "_"+ xSAreaSource[0]+ietFWHMSuffix2):
        fwhmFiles = [run + "_"+ xSAreaSource[0]+ietFWHMSuffix2,0]
    else:
        sys.exit ("Please manually enter cross sectional area (um^2) with area"+
            " source = Manual or add " + run + "_"+ xSAreaSource[0]+
             ietFWHMSuffix2 + " to "+ rawDataFolder + " folder, or change area"+
            " source information")
else:
     if ietFWHMSuffix1 == "alphabet":
         fwhmFiles = alphabet
         fwhmFiles = [run + "_" + xSAreaSource[0] + s + ietFWHMSuffix2 for s 
                      in fwhmFiles]
     elif ietFWHMSuffix1 == "numbers":
        fwhmFiles = numbers
        fwhmFiles = [run + "_" + xSAreaSource[0] + s + ietFWHMSuffix2 for s 
                      in fwhmFiles]
     else: 
        sys.exit ("Please indicate how fwhm suffixes are labeled and "+
                  " increased, or change the Area Source information")
ietFWHM, fig = 0, fig+1         
###########CALCULATES DIAMETER FROM FULL-WIDTH AT HALF-MAXIMUM TRACE##########
while ietFWHM < int(xSAreaSource[1]) and not xSAreaSource[0] == "Manual" and not (
                 xSAreaSource[0] ==  "Manual (Px)"):
    ietFWHM,fig = ietFWHM+1, fig+1
    if ietFWHM < int(xSAreaSource[1]) + 1:
        if not os.path.exists(__flocation__+fwhmFiles[ietFWHM-1]):
            sys.exit ("please add " +fwhmFiles[ietFWHM-1] + " to RawData File,"+ 
                      " edit the number of FWHM files, or change fwhm suffixes")
        fwhmRaw =  np.asarray(pd.read_table(__flocation__+fwhmFiles[ietFWHM-1],sep="\,"))  
        fwhmRaw = fwhmRaw[:,columnLocations["FWHM"]]
        fwhmRaw = fwhmRaw - min(fwhmRaw)
        fwhmFront = fwhmRaw[0:int(np.where(fwhmRaw == 0)[0][0])+1]
        fwhmBack = fwhmRaw[int(np.where(fwhmRaw == 0)[0][0]):(len(fwhmRaw)-1)]
        fwhmFMid, fwhmBMid = max(fwhmFront)/2, max(fwhmBack)/2
        fwhmFPx = len(fwhmFront)-(np.where(min(abs(fwhmFront-(fwhmFMid)))==(
            abs(fwhmFront-fwhmFMid)))[0][0])
        fwhmBPx = np.where(min(abs(fwhmBack-fwhmBMid))==(
            abs(fwhmBack-fwhmBMid)))[0][0]
        fwhmPx = fwhmFPx + fwhmBPx
        fwhmtoFMid = len(fwhmFront) - fwhmFPx
        if (fwhmFront[fwhmtoFMid]-fwhmFMid)<0:
            fwhmPx = fwhmPx + 0.5
        if (fwhmBack[fwhmBPx]-fwhmBMid)<0:
            fwhmPx = fwhmPx + 0.5
        fwhmI = float(max(fwhmFront)+max(fwhmBack))/2
        xSArea = np.zeros(int(xSAreaSource[1]))
#######################PLOTS CROSS-SECTIONAL AREA GRAPHS######################
        if xSAreaShowPlot == "y":
            plt.figure(fig)
            plt.title(run+"_FWHM_"+xSAreaCamera[0][0])
            plt.plot(fwhmRaw)
            plt.plot(range(((fwhmtoFMid)),((fwhmtoFMid))+len(fwhmRaw[(fwhmtoFMid):
               len(fwhmFront)+fwhmBPx])),fwhmRaw[(fwhmtoFMid):len(fwhmFront)+fwhmBPx])
        xSArea[ietFWHM-1] = 3.1415*0.25*(xSAreaRes*fwhmPx)**2
if not xSAreaSource[0] == "Manual":    
    AxSArea = np.mean(xSArea[:])
    xSAreaSErr = np.std(xSArea[:])/len(xSArea)**0.5