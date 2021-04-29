#################################DATA INPUTS##################################
run = "2019-09-20_R1-2"
l0Source = "ChrIsolated (Px)"
l0all = [1]
xSAreaCamera = l0Camera = ["Andor",60,1.5]
xSAreaSource = ["FWHM_A",1]
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
exec(open(__location__ +fwhmExe).read()) 