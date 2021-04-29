##################################RUN CONTROLS################################
projectInfoFile = "Test" + ".csv"
runSave, projectSave = "y","y"
#################################PLOT CONTROLS#################################
calShowPlot = "n" 
pullShowRawPlot,pullShowJumpRejPlot = 2*["n"]
pullShowSDPlot,pullShowSDOutPlot,pullShowFitPlot = 3*["n"]
invert, manualLimits = "n", ("n",(0,3),(0,100))
xSAreaShowPlot = "n"
###############################FUNCTION IMPORTS###############################
import csv
import numpy as np
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import sys
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__flocation__ = __location__ +"/RawData/"
exec(open(__location__ +"/4DataLabelProperties.py").read())
###########IETERATES OVER THE MULTIPLE RUNS AS DICTATED BY MAIN FILE###########
ietRun = 0
with open(projectInfoFile, newline='') as csvfile:
    projectData = np.matrix(list(csv.reader(csvfile)))
AAAProjectData = np.zeros((16,len(projectData))).astype(str)
AAAProjectData[:] = ("")
runParameters = projectData [0]
while  ietRun < len(projectData[:])-1-list(np.array(projectData[:,0])).count([""]):
    ietRun = ietRun+1
###########################PULLS DATA FROM WORKSHEET###########################
    run = str(projectData[ietRun,0])    
    runCondition = str(projectData[ietRun,1])
    cals = int(projectData[ietRun,2])
    calRejMan = list(map(int,(projectData[ietRun,3]).split(',')))
    calPipette = float(projectData[ietRun,4])
    calGap = float(projectData[ietRun,5])
    calEventTimes =  list(map(int,(projectData[ietRun,6]).split(',')))
    calAutoAgree = str(projectData[ietRun,7])
    calManual = list(map(str,(projectData[ietRun,8]).split(',')))
    pulls = int(projectData[ietRun,9])
    pullRejMan = list(map(int,(projectData[ietRun,10]).split(',')))
    pullRejJump= ((projectData[ietRun,11]).split(','))
    pullRejRValue = ((projectData[ietRun,12]).split(','))
    pullRejHys = (projectData[ietRun,13]).split(',')
    pullAutoAgree = str(projectData[ietRun,14])
    l0Camera = ((projectData[ietRun,15]).split(','))
    l0Source = str(projectData[ietRun,16])
    l0all = list(map(float,(projectData[ietRun,17]).split(',')))
    xSAreaCamera = ((projectData[ietRun,18]).split(','))
    xSAreaSource = ((projectData[ietRun,19]).split(','))
    runName = run
####################QUIRK OF CURRENT SCRIPT,FIX IF POSSIBLE####################
    if calRejMan == [0]:
        calRejMan = []
    if pullRejMan == [0]:
        pullRejMan = []
###############################CALIBRATION SCRIPT##############################
    if calManual[0] == "y":
        ForcePipette,ForcePipetteSterr,calN,cals,calsAllUncut,ForcePipette_all = (
                float(calManual[1]),"Manual input",1,1,np.zeros((5,1)),np.zeros((1,5)))
    else:
        exec(open(__location__ +calExe).read())
        if (calQuality == qualityParameters[2][0]) or (calN < qualityN["N"]):
            runName = runName + "_" + qualityParameters[2][0] + "Cals"   
######################STRETCH-DEFLECTION ANALYSIS SCRIPT#######################
    exec(open(__location__ +strDefExe).read())  
###################L0 & CROSS SECTIONAL AREA ANALYSIS SCRIPT###################
    exec(open(__location__ +fwhmExe).read())  
#IETERATES OVER DIFFERENT RAW PULL DATA PROBLEMS TO GET GOOD FINAL DATA AGREEMENT
    if pullQuality == qualityParameters[2][0]:
        runName = runName + "_noisy"
    if pullRejRValue[2] == "y":
        pullRejRValue[0] = "n"
        exec(open(__location__ +strDefExe).read())
    if pullQuality == qualityParameters[2][0]:
        runName = runName.strip("_noisy")
        runName = runName + "_hyst"
        pullRejRValue[0] = "y"
        if pullRejHys[2] == "y":
            pullRejHys[0] = "n"
            exec(open(__location__ +strDefExe).read())
            if pullQuality ==qualityParameters[2][0] and pullRejRValue[2] == "y":
                runName = runName + "_noisy"
                pullRejRValue[0] = "n"
                exec(open(__location__ +strDefExe).read())
    if pullQuality == qualityParameters[2][0] or pullN < qualityN["N"]:
                    runName = runName + "_" + qualityParameters[2][0] + "Pull"     
    print ("")
    #######################FILLS OUT FORM FOR ANALYSIS SHEET######################
    AAData = np.zeros ((18+len(AllForcePipetteUncut)+len(AllStrDefUncut)+len(
        AllStrDef),1+len(AllForcePipetteUncut[0])+len(AllForcePipette[0]))).astype(str)
    AAData[:,:] = ("")
    #####################FILLS IN THE LABELS AND COMBINES DATA####################
    AAData[0:15,0] = ("Run name", "Young's Modulus (Pa)", "Doubling Force (pN)",
                 "Spring const (pN/um)", "F Pipette (pN/um)","Initial Length(um)",
                 "Area(Cross sect)(um^2)", "F pipette max(um)", "Stretch max (um)",
                 "Pulls N", "StrDef Sigma/avg", "Run Condition", "", "", "")
    AAData[0:15,1] = (runName, AStrDef*AForcePipette*Al0/AxSArea, AStrDef*AForcePipette*Al0,
                 AStrDef*AForcePipette, AForcePipette,Al0,
                 AxSArea, str(abs(float(AllStrDef[-1,1]))), str(abs(float(AllStrDef[-1,2]))),
                 pullN, AStrDefSterr*pullN**0.5/AStrDef, runCondition, "", "", "")
    AAData[0:15,2] = ("", "+/-","+/-","+/-","+/-","+/-","+/-","+/-","+/-",
                   "Cals N", "Rejected Cals", "Rejected Pulls","", "", "")
    AAData[0:15,3] = ("", AStrDefSterr*AForcePipette*Al0/AxSArea, AStrDefSterr*AForcePipette*Al0,
                 AStrDefSterr*AForcePipette, AForcePipetteSterr,l0stErr,
                 xSAreaSErr, AllStrDef[-1,1], AllStrDef[-1,2],
                 calN, str(calRej), str(pullRej), "", "", "")
    AAData[0:15,4] = ("")
    ############################FILLS IN THE INPUT DATA###########################
    AAData[0,5:9] = ("Cals (#)","BadCals (Run#)",	"Pulls (#)", "BadPulls (Run#)")
    AAData[1,5:9] = (str(cals),str(calRejMan),str(pulls),str(pullRejMan))
    AAData[2,5:10] = ("Cal Pipette (pN/um)","Timing gap (sec)","Cal: Ta,Tb,Tc,Td (sec)"
                     ,"autoCalAgree (y/n)","FPmanual [y/n,value]")
    AAData[3,5:10] = (str(calPipette),str(calGap),str(calEventTimes),
                      str(calAutoAgree),str(calManual))
    AAData[4,5:9] = ("jump reject [y/n, value]","rValueReject (y/n,Value,autoallow)",
                     "hysteresisReject (y/n,Value,autoallow)",	"autoPullAgree (y/n)")
    AAData[5,5:9] = (str(pullRejJump),str(pullRejRValue),
                      str(pullRejHys),str(pullAutoAgree))
    AAData[6,5:10] = ("L0 camera(Name, mag, pullout)",	"L0 Source (Pulls-ChrGrabTwo-ChrIsolated-Manual)",	
                      "L0 collection (Px)","Area camera(Name, mag, pullout)",	
                      "Area Source ((FWHM-FWHM Multi-Manual),Value)")
    AAData[7,5:10] =(str(l0Camera),str(l0Source),
                     str(l0all),str(xSAreaCamera),
                     str(xSAreaSource))
    #########################FILLS IN THE CALIBRATION DATA########################
    AAData[15:15+len(AllForcePipetteUncut),0:len(AllForcePipetteUncut[0])] = (
        AllForcePipetteUncut)
    AAData[15:15+len(AllForcePipette),len(AllForcePipetteUncut[0])+1:1+
           len(AllForcePipetteUncut[0])+len(AllForcePipette[0])] = AllForcePipette
    #####################FILLS IN THE STRETCH-DEFLECTION DATA#####################
    AAData[16+len(AllForcePipetteUncut):16+len(AllForcePipetteUncut)+
           len(AllStrDef),0:len(AllStrDef[0])] = AllStrDef
    AAData[16+len(AllForcePipetteUncut)+len(AllStrDef):16+len(AllForcePipetteUncut)+
           len(AllStrDefUncut)+len(AllStrDef),0:len(AllStrDefUncut[0])] = AllStrDefUncut
    runName = runName + ".csv"
    if runSave == "y":
        if not os.path.exists (__location__ + "/"+ savedDataFolder+"/"):
            sys.exit("Please add "+ savedDataFolder + " folder to current folder")
        else:
            np.savetxt(__location__+"/"+savedDataFolder+"/"+runName,AAData,
                       fmt='%s', delimiter= ',' , newline='\n')
    AAAProjectData[0:15,0] = AAData[0:15,0] 
    AAAProjectData[0:15,ietRun] = AAData[0:15,1]
    if projectSave == "y":
        if not os.path.exists (__location__ + "/"+ savedDataFolder+"/"):
                sys.exit("Please add "+ savedDataFolder + " folder to current folder")
        else:
            np.savetxt(__location__+"/"+projectInfoFile.strip(".csv")+"_Analyzed.csv",
                       AAAProjectData,fmt='%s',delimiter= ',' , newline='\n')