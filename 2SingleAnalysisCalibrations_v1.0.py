#################################DATA INPUTS##################################
run = "2019-09-20_R2-2"
cals = 6
calPipette = 72.5
calEventTimes = [20,40,60,80]
calGap = 2.5
calStepFactor = 1000
calRejMan = []
calAutoAgree = "y"
calShowPlot = "y"
runName = run
###############################FUNCTION IMPORTS###############################
import csv
import numpy as np
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import sys
calManual = "n"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__flocation__ = __location__ +"/RawData/"
exec(open(__location__ +"/4DataLabelProperties.py").read())  
exec(open(__location__ +calExe).read())