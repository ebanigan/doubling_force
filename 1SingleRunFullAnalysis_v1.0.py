##################################RUN CONTROLS################################
run = "2019-09-12_R1-2"
runSave= "n"
inputStyle = "File"
projectInfoFile = "Test" + ".csv"
#################################PLOT CONTROLS################################
calShowPlot = "y" 
pullShowRawPlot,pullShowJumpRejPlot = 2*["y"]
pullShowSDPlot,pullShowSDOutPlot,pullShowFitPlot = 3*["y"]
invert, manualLimits = "n", ("n",(0,3),(0,100))
xSAreaShowPlot = "y"
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
#################################MANUAL INPUTS################################
if inputStyle == "Manual":
    runCondition = "Strain_Treatment"
    cals = 6
    calPipette = 72.5
    calEventTimes = [20,40,60,80]
    calGap = 2.5
    calRejMan = []
    calAutoAgree = "y"
    calManual = ["n","Value"]
    pulls = 6
    pullRejMan = []
    pullAutoAgree = "y"
    pullRejJump = ["y",0.1]
    pullRejHys = ["y",9.0,"y"]
    pullRejRValue = ["y",0.9,"y"]
    l0Source = "ChrIsolated (Px)"
    l0all = [10]
    l0Camera = ["Andor",60,1.5]
    xSAreaCamera = ["Andor",60,1.5]
    xSAreaSource = ["FWHM_A",1]
    xSAreaShowPlot = "y"
###########################PULLS DATA FROM WORKSHEET##########################
elif inputStyle == "File":
    ietRun = 0
    with open(projectInfoFile, newline='') as csvfile:
        projectData = list(csv.reader(csvfile))
    if not os.path.exists(projectInfoFile):
        sys.exit ("Please add "+ projectInfoFile + " to current folder")
    while not projectData[ietRun][0] == run:
        ietRun = ietRun + 1
    runCondition = str(projectData[ietRun][1])
    cals = int(projectData[ietRun][2])
    calRejMan = list(map(int,(projectData[ietRun][3]).split(',')))
    calPipette = float(projectData[ietRun][4])
    calGap = float(projectData[ietRun][5])
    calEventTimes =  list(map(int,(projectData[ietRun][6]).split(',')))
    calAutoAgree = str(projectData[ietRun][7])
    calManual = list(map(str,(projectData[ietRun][8]).split(',')))
    pulls = int(projectData[ietRun][9])
    pullRejMan = list(map(int,(projectData[ietRun][10]).split(',')))
    pullRejJump= ((projectData[ietRun][11]).split(','))
    pullRejRValue = ((projectData[ietRun][12]).split(','))
    pullRejHys = (projectData[ietRun][13]).split(',')
    pullAutoAgree = str(projectData[ietRun][14])
    l0Camera = ((projectData[ietRun][15]).split(','))
    l0Source = str(projectData[ietRun][16])
    l0all = list(map(float,(projectData[ietRun][17]).split(',')))
    xSAreaCamera = ((projectData[ietRun][18]).split(','))
    xSAreaSource = ((projectData[ietRun][19]).split(','))   
else:
    sys.exit("Please choose File or Manual for data input")
####################QUIRK OF CURRENT SCRIPT,FIX IF POSSIBLE###################
runName = run
if calRejMan == [0]:
    calRejMan = []
if pullRejMan == [0]:
    pullRejMan = []
###############################CALIBRATION SCRIPT#############################
if calManual[0] == "y":
    ForcePipette,ForcePipetteSterr,calN,cals,calsAllUncut,ForcePipette_all = (
            float(calManual[1]),"Manual input",1,1,np.zeros((5,1)),np.zeros((1,5)))
else:
    exec(open(__location__ +calExe).read())
    if (calQuality == qualityParameters[2][0]) or (calN < qualityN["N"]):
        runName = runName + "_" + qualityParameters[2][0] + "Cals"   
######################STRETCH-DEFLECTION ANALYSIS SCRIPT######################
exec(open(__location__ +strDefExe).read())  
###################L0 & CROSS SECTIONAL AREA ANALYSIS SCRIPT##################
exec(open(__location__ +fwhmExe).read())  
#ITERATES OVER DIFFERENT RAW PULL DATA PROBLEMS TO GET GOOD FINAL DATA AGREEMENT
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
             AxSArea, AllStrDef[-2,1], AllStrDef[-2,2],
             pullN, AStrDefSterr*pullN**0.5/AStrDef, runCondition, "", "", "")
AAData[0:15,2] = ("", "+/-","+/-","+/-","+/-","+/-","+/-","+/-","+/-",
               "Cals N", "Rejected Cals", "Rejected Pulls","", "", "")
AAData[0:15,3] = ("", AStrDefSterr*AForcePipette*Al0/AxSArea, AStrDefSterr*AForcePipette*Al0,
             AStrDefSterr*AForcePipette, AForcePipetteSterr,l0stErr,
             xSAreaSErr, str(abs(float(AllStrDef[-1,1]))), str(abs(float(AllStrDef[-1,2]))),
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
        np.savetxt(__location__+"/"+savedDataFolder+"/"+runName,AAData,fmt='%s', 
               delimiter= ',' , newline='\n')