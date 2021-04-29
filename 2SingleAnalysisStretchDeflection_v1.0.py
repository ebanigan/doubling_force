#################################DATA INPUTS##################################
run = "2019-09-20_R1-2"
pulls = 6
pullRejMan = []
pullAutoAgree = "y"
pullRejJump = ["y",0.1]
pullRejHys = ["y",9.0,"y"]
pullRejRValue = ["y",0.9,"y"]
#################################PLOT CONTROLS################################
pullShowRawPlot, pullShowJumpRejPlot = 2*["y"] #"n", "n" #"y", "y"
pullShowSDPlot, pullShowSDOutPlot, pullShowFitPlot =3*["y"]#"n", "n", "n" #"y", "y", "y"
runName = run
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
exec(open(__location__ +strDefExe).read())  