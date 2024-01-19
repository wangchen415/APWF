# from cgitb import reset
# from importlib.resources import path
'''
ssh junli@192.168.1.208
conda activate py39plus
nohup python wc_SWAT2.py >/dev/null 2>&1 &
ps aux|grep wc_SWAT2.py
ps -ef | grep wc_SWAT2.py | awk '{ print $2 }'
ps -ef | grep wc_SWAT2.py | awk '{ print $2 }' | xargs
ps -ef | grep wc_SWAT2.py | awk '{ print $2 }' | xargs kill -9
'''
# from math import factorial
# from cv2 import split
import multiprocessing
import glob
import os
import re
import shutil
import subprocess
import datetime
import json
import math
import pandas as pd
import numpy as np
from numpy import append
from numpy import hsplit
from pip import main
from wc_global import *
from wc_mgt import HRU_MGT
from wc_sol import HRU_SOL
from wc_hru import HRU_HRU
from wc_gw import HRU_GW
from wc_rte import HRU_RTE
from wc_bsn import HRU_BSN
from wc_sub import HRU_SUB
from wc_plant import HRU_PLANT



#############
class SOL(object):
    ext='sol'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_SOL()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'[0-9]*.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            sol=self.obj.read(templatefile)
            #print(rule)
            #############
            #{'fullname': 'r__SOL_AWC(1).sol________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subbsn': '1'}
            for r in rule:
                #filtering hru
                #hydrogrp
                if r['hydrogrp'] is not None:
                    if re.match(str(r['hydrogrp']),sol[2]['Soil Hydrologic Group']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #soltext
                if r['soltext'] is not None:
                    if re.match(str(r['soltext']),sol[2]['Soil Name']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #landuse
                if r['landuse'] is not None:
                    if re.match(str(r['landuse']),sol[2]['Luse']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #subbsn
                if r['subbsn'] is not None:
                    tmp=re.findall('([0-9\-\,]*)?',r['subbsn'])
                    if tmp[0]=='':
                        subbsn=None
                    else:
                        subbsn=[]
                    for num in tmp[0].split(','):
                        if num.isdigit():
                            subbsn.append(int(num))
                        else:
                            lb,ub=num.split('-')
                            for i in range(int(lb),int(ub)+1):
                                subbsn.append(i)
                    if subbsn is not None and int(sol[2]['Subbasin']) not in subbsn:
                        flag = False
                    else:
                        flag = True
                #Slope
                if r['slope'] is not None:
                    if re.match(str(r['slope']),sol[2]['Slope']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #
                #extracting soil layers and soil varibles
                if flag:  
                    tmp=re.findall('([A-Z_]+)(\(([0-9\-\,]*)\))?',r['parname'])
                    varname=tmp[0][0]
                    if tmp[0][2]=='':
                        layers=None
                        if varname=='SOL_ALB':
                            soilvalue=sol[3]['Soil Albedo (Moist)'][0]
                        soillayers=None
                    else:
                        layers=[]
                        for num in tmp[0][2].split(','):
                            if num.isdigit():
                                layers.append(int(num))
                            else:
                                lb,ub=num.split('-')
                                for i in range(int(lb),int(ub)+1):
                                    layers.append(i)  
                        soilvalue=None               
                        # #modifing
                        # [['Depth                [mm]', ['330.00', '900.00', '1100.00']], ['Bulk Density Moist [g/cc]', ['1.44', '1.50', '1.62']], ['Ave. AW Incl. Rock Frag', ['0.13', '0.12', '0.08']], ['Ksat. (est.)      [mm/hr]', ['2.29', '1.57', '38.54']], ['Organic Carbon [weight %]', ['1.69', '0.41', '0.16']], ['Clay           [weight %]', ['38.00', '38.00', '11.00']], ['Silt           [weight %]', ['25.00', '20.00', '20.00']], ['Sand           [weight %]', ['37.00', '42.00', '69.00']], ['Rock Fragments   [vol. %]', ['0.00', '0.00', '0.00']], ['Soil Albedo (Moist)', ['0.01', '0.10', '0.17']], ['Erosion K', ['0.28', '0.34', '0.40']], ['Salinity (EC, Form 5)', ['0.00', '0.00', '0.0']], ['Soil pH', ['0.00', '0.00', '0.00']], ['Soil CACO3', ['0.00', '0.00', '0.00']]]
                        #
                        #modifing soil varibles
                        if varname=='SOL_AWC':
                            soillayers=sol[3]['Ave. AW Incl. Rock Frag']
                        elif varname=='SOL_K':
                            soillayers=sol[3]['Ksat. (est.)      [mm/hr]']
                        elif varname=='SOL_BD':
                            soillayers=sol[3]['Bulk Density Moist [g/cc]']
                        # soillayers=None

                    #
                    if soillayers is not None:
                        for i in range(len(soillayers)):
                            if layers is None or i+1 in layers:
                                if r['x']=='r':
                                    #factor=1+sim[r['fullname']]
                                    factor=1+r['parval']
                                    soillayers[i]=round(float(soillayers[i])*factor,2) 
                                elif r['x']=='v':
                                    #factor=sim[r['fullname']]
                                    factor=r['parval']
                                    soillayers[i]=round(factor,2)
                                elif r['x']=='a':
                                    #factor=sim[r['fullname']]
                                    factor=r['parval']
                                    soillayers[i]=round(float(soillayers[i])+factor,2) 
                    if soilvalue is not None:
                        if r['x']=='r':
                                factor=1+r['parval']
                                soilvalue =round(float(soilvalue)*factor,2)
                        elif r['x']=='r':
                                factor=r['parval']
                                soilvalue =round(factor,2)
                        elif r['x']=='a':
                                factor=r['parval']
                                soilvalue =round(float(soilvalue)+factor,2)

                #
                #save to disk
                if flag:
                    self.obj.write(sol,outfile)
    #
    def run(self):
        self.modifyTemplates()


class HRU(object):
    ext='hru'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_HRU()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'[0-9]*.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            hru=self.obj.read(templatefile)
            #print(rule)
            #############
            #{'fullname': 'r__SOL_AWC(1).sol________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subbsn': '1'}
            for r in rule:
                #filtering hru
                #soltext
                if r['soltext'] is not None:
                    if re.match(str(r['soltext']),hru[2]['Soil']) :
                        pass
                    else:
                        flag=False
                else:
                    pass
                #landuse
                if r['landuse'] is not None:
                    if re.match(str(r['landuse']),hru[2]['FRST']) :
                        pass
                    else:
                        flag=False
                else:
                    pass
                #subbsn
                if r['subbsn'] is not None:
                    tmp=re.findall('([0-9\-\,]*)?',r['subbsn'])
                    if tmp[0]=='':
                        subbsn=None
                    else:
                        subbsn=[]
                    for num in tmp[0].split(','):
                        if num.isdigit():
                            subbsn.append(int(num))
                        else:
                            lb,ub=num.split('-')
                            for i in range(int(lb),int(ub)+1):
                                subbsn.append(i)
                    if subbsn is not None and int(hru[2]['Subbasin']) not in subbsn:
                        flag = False
                    else:
                        flag = True
                #Slope
                if r['slope'] is not None:
                    if re.match(str(r['slope']),hru[2]['Slope']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #               
                #modifing hru varibles
                if flag:
                    try:
                        hru_tmp=hru[2][r['parname']] 
                    except Exception as e:
                        print('%s parameter does not exist'%(str(r['parname'])))
                        pass
                    if r['parname']=='LAT_TTIME':
                        dig=3
                    elif r['parname']=='ESCO':
                        dig=3          
                    elif r['parname']=='HRU_SLP':
                        dig=3 
                    elif r['parname']=='OV_N':
                        dig=3
                    elif r['parname']=='SLSUBBSN':
                        dig=3  
                    elif r['parname']=='SLSOIL':
                        dig=3
                    elif r['parname']=='EPCO':
                        dig=3
                    elif r['parname']=='LAT_SED':
                        dig=3
                    elif r['parname']=='CANMX':
                        dig=3
                    else:
                        hru_tmp=None
                    #
                    if hru_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            hru[2][r['parname']]=round(float(hru[2][r['parname']])*factor,dig)                   
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            hru[2][r['parname']]=round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            hru[2][r['parname']]=round(float(hru[2][r['parname']])+factor,dig) 
                #
                #save to disk
                if flag: 
                    self.obj.write(hru,outfile)
    #
    def run(self):
        self.modifyTemplates()

    
class RTE(object):
    ext='rte'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_RTE()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'[0-9]*.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            rte=self.obj.read(templatefile)
            #print(rule)
            #############
            #{'fullname': 'r__SOL_AWC(1).sol________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subbsn': '1'}
            for r in rule:
                #filtering rte
                #subbsn
                if r['subbsn'] is not None:
                    tmp=re.findall('([0-9\-\,]*)?',r['subbsn'])
                    # print(tmp)
                    if tmp[0]=='':
                        subbsn=None
                    else:
                        subbsn=[]
                    for num in tmp[0].split(','):
                        if num.isdigit():
                            subbsn.append(int(num))
                        else:
                            lb,ub=num.split('-')
                            for i in range(int(lb),int(ub)+1):
                                subbsn.append(i)
                    # print(subbsn)
                    if subbsn is not None and int(rte[2]['Subbasin']) not in subbsn:
                        # for i in range(len(subbsn)):        
                        #     # if not re.match('%05d[0-9]{4}\.sol'%(int(r['subbsn'])),filename) :
                        #     if re.match(str(subbsn[i]),rte[2][0][1]) :
                        #         pass:
                            flag = False
                    else:
                        flag = True        
                    #modifing rte varibles
                if flag:
                    try:
                        rte_tmp=rte[2][r['parname']] 
                    except Exception as e:
                        print('%s parameter does not exist'%(str(r['parname'])))
                        pass
                    if r['parname']=='CH_L2':
                        dig=3  
                    elif r['parname']=='CH_W2':
                        dig=3
                    elif r['parname']=='CH_S2':
                        dig=3          
                    elif r['parname']=='CH_N2':
                        dig=3          
                    elif r['parname']=='CH_K2':
                        dig=3 
                    elif r['parname']=='ALPHA_BNK':
                        dig=3 
                    elif r['parname']=='PRF':
                        dig=3 
                    else:
                        rte_tmp=None
                    #
                    if rte_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            rte[2][r['parname']] =round(float(rte[2][r['parname']])*factor,dig)                   
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            rte[2][r['parname']] =round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            rte[2][r['parname']] =round(float(rte[2][r['parname']])+factor,dig) 
                #
                #save to disk
                if flag: 
                    self.obj.write(rte,outfile)
    #
    def run(self):
        self.modifyTemplates()

class GW(object):
    ext='gw'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_GW()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'[0-9]*.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            gw=self.obj.read(templatefile)
            #############
            #{'fullname': 'r__SOL_AWC(1).sol________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subbsn': '1'}
            for r in rule:
                #filtering gw
                #soltext
                if r['soltext'] is not None:
                    if re.match(str(r['soltext']),gw[2]['Soil']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #landuse
                if r['landuse'] is not None:
                    if re.match(str(r['landuse']),gw[2]['FRST']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #subbsn
                if r['subbsn'] is not None:
                    tmp=re.findall('([0-9\-\,]*)?',r['subbsn'])
                    if tmp[0]=='':
                        subbsn=None
                    else:
                        subbsn=[]
                    for num in tmp[0].split(','):
                        if num.isdigit():
                            subbsn.append(int(num))
                        else:
                            lb,ub=num.split('-')
                            for i in range(int(lb),int(ub)+1):
                                subbsn.append(i)
                    if subbsn is not None and int(gw[2]['Subbasin']) not in subbsn:
                        flag = False
                    else:
                        flag=True
                #Slope
                if r['slope'] is not None:
                    if re.match(str(r['slope']),gw[2]['Slope']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #
                if flag:               
                    #modifing gw varibles
                    try:
                        gw_tmp=gw[2][r['parname']] 
                    except Exception as e:
                        print('%s parameter does not exist'%(str(r['parname'])))
                        pass
                    if r['parname']=='GWQMN':
                        dig=4          
                    elif r['parname']=='GW_REVAP':
                        dig=4  
                    elif r['parname']=='REVAPMN':
                        dig=4  
                    elif r['parname']=='GW_DELAY':
                        dig=4  
                    elif r['parname']=='ALPHA_BF':
                        dig=4  
                    elif r['parname']=='RCHRG_DP':
                        dig=4  
                    elif r['parname']=='GW_SPYLD':
                        dig=4  
                    elif r['parname']=='SHALLST_N':
                        dig=4  
                    else:
                        gw_tmp=None
                    #
                    if gw_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            gw[2][r['parname']] =round(float(gw[2][r['parname']] )*factor,dig) 
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            gw[2][r['parname']] =round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            gw[2][r['parname']] =round(float(gw[2][r['parname']] )+factor,dig) 
                #
                #save to disk
                if flag:
                    self.obj.write(gw,outfile)
    #
    def run(self):
        self.modifyTemplates()
##########################


class MGT(object):
    ext='mgt'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_MGT()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'[0-9]*.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            mgt=self.obj.read(templatefile)
            #print(rule)
            #############
            #{'fullname': 'r__CN2.mgt________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subbsn': '1'}
            for r in rule:
                #filtering mgt
                #soltext
                if r['soltext'] is not None:
                    if re.match(str(r['soltext']),mgt[2]['Soil']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #landuse
                if r['landuse'] is not None:
                    if re.match(str(r['landuse']),mgt[2]['Luse']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #subbsn
                if r['subbsn'] is not None:
                    tmp=re.findall('([0-9\-\,]*)?',r['subbsn'])
                    if tmp[0]=='':
                        subbsn=None
                    else:
                        subbsn=[]
                    for num in tmp[0].split(','):
                        if num.isdigit():
                            subbsn.append(int(num))
                        else:
                            lb,ub=num.split('-')
                            for i in range(int(lb),int(ub)+1):
                                subbsn.append(i)
                    if subbsn is not None and int(mgt[2]['Subbasin']) not in subbsn:
                        flag = False
                    else:
                        flag = True
                #Slope
                if r['slope'] is not None:
                    if re.match(str(r['slope']),mgt[2]['Slope']) :
                        pass
                    else:
                        flag = False
                else:
                    pass
                #
                if flag:                
                    #modifing mgt varibles
                    try:
                        mgt_tmp=mgt[2][r['parname']] 
                    except Exception as e:
                        print('%s parameter does not exist'%(str(r['parname'])))
                        pass
                    if r['parname']=='CN2':
                        dig=2         
                    else:
                        mgt_tmp=None
                    #
                    if mgt_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            mgt[2][r['parname']]=round(float(mgt[2][r['parname']])*factor,dig) 
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            mgt[2][r['parname']]=round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            mgt[2][r['parname']]=round(float(mgt[2][r['parname']])+factor,dig) 
                #
                #save to disk
                if flag: 
                    self.obj.write(mgt,outfile)
    #
    def run(self):
        self.modifyTemplates()

#########################
class BSN(object):
    ext='bsn'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_BSN()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'basins.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            bsn=self.obj.read(templatefile)
            #############
            #{'fullname': 'r__CN2.bsn________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subbsn': '1'}
            for r in rule:
                if flag:      
                    # print(r)          
                    #modifing bsn varibles
                    try:
                        bsn_tmp=bsn[2][r['parname']] 
                    except Exception as e:
                        print('%s parameter does not exist'%(str(r['parname'])))
                        pass
                    if r['parname']=='SFTMP':
                        dig=3
                    elif r['parname']=='SMTMP':
                        dig=3
                    elif r['parname']=='SMFMX':
                        dig=3
                    elif r['parname']=='SMFMN':
                        dig=3
                    elif r['parname']=='TIMP':
                        dig=3
                    elif r['parname']=='SNOCOVMX':
                        dig=3
                    elif r['parname']=='SNO50COV':
                        dig=3 
                    elif r['parname']=='SURLAG':
                        dig=3
                    elif r['parname']=='ADJ_PKR':
                        dig=3    
                    elif r['parname']=='PRF_BSN':
                        dig=3    
                    elif r['parname']=='SPCON':
                        dig=4
                    elif r['parname']=='SPEXP':
                        dig=3  
                    elif r['parname']=='FFCB':
                        dig=3
                    else:
                        bsn_tmp=None
                    #
                    if bsn_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            bsn[2][r['parname']] =round(float(bsn[2][r['parname']] )*factor,dig) 
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            bsn[2][r['parname']]=round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            bsn[2][r['parname']] =round(float(bsn[2][r['parname']] )+factor,dig) 
                #
                #save to disk
            if flag: 
                self.obj.write(bsn,outfile)
                # print(sub)
    #
    def run(self):
        self.modifyTemplates()

########################
class SUB(object):
    ext='sub'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_SUB()
    #
    def modifyTemplates(self):
        rule=self.solution[self.ext]
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'[0-9]*.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            sub=self.obj.read(templatefile)
            #############
            #{'fullname': 'r__CN2.sub________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subsub': '1'}
            for r in rule:
                #subbsn
                if r['subbsn'] is not None:
                    tmp=re.findall('([0-9\-\,]*)?',r['subbsn'])
                    if tmp[0]=='':
                        subbsn=None
                    else:
                        subbsn=[]
                    for num in tmp[0].split(','):
                        if num.isdigit():
                            subbsn.append(int(num))
                        else:
                            lb,ub=num.split('-')
                            for i in range(int(lb),int(ub)+1):
                                subbsn.append(i)
                    if subbsn is not None and int(sub[1]['Subbasin']) not in subbsn:
                        # for i in range(len(subbsn)):        
                        #     # if not re.match('%05d[0-9]{4}\.sol'%(int(r['subbsn'])),filename) :
                        #     if re.match(str(subbsn[i]),rte[2][0][1]) :
                        #         pass:
                            flag = False
                    else:
                        flag = True 
                else:
                    pass
                if flag:                
                    #modifing sub varibles
                    try:
                        sub_tmp=sub[1][r['parname']] 
                    except Exception as e:
                        print('%s parameter does not exist'%(str(r['parname'])))
                        pass
                    if r['parname']=='PLAPS':
                        dig=3
                    elif r['parname']=='TLAPS':
                        dig=3
                    elif r['parname']=='SNO_SUB':
                        dig=3
                    elif r['parname']=='CH_L1':
                        dig=3
                    elif r['parname']=='CH_S1':
                        dig=3
                    elif r['parname']=='CH_W1':
                        dig=3
                    elif r['parname']=='CH_K1':
                        dig=3 
                    elif r['parname']=='CH_N1':
                        dig=3
                    elif r['parname']=='CO2':
                        dig=3      
                    else:
                        sub_tmp=None
                    #
                    if sub_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            sub[1][r['parname']]=round(float(sub[1][r['parname']])*factor,dig) 
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            sub[1][r['parname']]=round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            sub[1][r['parname']]=round(float(sub[1][r['parname']])+factor,dig) 
                #
                #save to disk
                if flag: 
                    self.obj.write(sub,outfile)
    #
    def run(self):
        self.modifyTemplates()

class plant(object):
    ext='dat'
    #
    def __init__(self,solution,templatefilepath,outfilepath):
        self.solution=solution
        self.templatefilepath=templatefilepath
        self.outfilepath=outfilepath
        self.obj=HRU_PLANT()
    #
    def modifyTemplates(self):
        rule=self.solution['dat']
        # print(rule)
        #path = r'E:\文件\FileStorage\File\2022-01\simulated_TxtInOut\TxtInOutCopy' 
        templatefilelist=glob.glob(os.path.join(self.templatefilepath,'plant.%s'%(self.ext)))
        self.modifyTemplate(rule,templatefilelist)
    #
    def modifyTemplate(self,rule,templatefilelist):
        for templatefile in templatefilelist:
            flag=True
            outfile=os.path.join(self.outfilepath,os.path.split(templatefile)[1])
            plant=self.obj.readFile(templatefile)
            #print(rule)
            #############
            #{'fullname': 'r__CN2.plant________1', 'x': 'r', 'parname': 'SOL_AWC(1)', 'ext': 'sol', 'hydrogrp': None, 'soltext': None, 'landuse': None, 'subplant': '1'}
            for r in rule:
                if flag:
                    icnum=int(re.findall('[A-Za-z_0-9]*\{+([0-9]*)\}+',r['parname'])[0])
                    parname=re.findall('([A-Za-z_0-9]*)\{+[0-9]*\}+',r['parname'])[0]
                    # print(parname)
                    plant_tmp=plant[icnum][parname]
                    #modifing plant varibles
                    if parname=='GSI':
                        dig=4
                    elif parname=='VPDFR':
                        dig=2
                    elif parname=='BIO_E':
                        dig=2
                    elif parname=='HVSTI':
                        dig=2
                    elif parname=='BLAI':
                        dig=2
                    elif parname=='DLAI':
                        dig=2
                    elif parname=='CHTMX':
                        dig=2 
                    elif parname=='T_BASE':
                        dig=2
                    elif parname=='ALAI_MIN':
                        dig=3    
                    elif parname=='EXT_COEF':
                        dig=3    
                    elif parname=='LAIMX1':
                        dig=2
                    elif parname=='LAIMX2':
                        dig=2  
                    elif parname=='FRGMAX':
                        dig=3  
                    else:
                        plant_tmp=None
                    #
                    if plant_tmp is not None:
                        if r['x']=='r':
                            #factor=1+sim[r['fullname']]
                            factor=1+r['parval']
                            plant[icnum][parname]=round(float(plant[icnum][parname])*factor,dig) 
                        elif r['x']=='v':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            plant[icnum][parname]=round(factor,dig)
                        elif r['x']=='a':
                            #factor=sim[r['fullname']]
                            factor=r['parval']
                            plant[icnum][parname]=round(float(plant[icnum][parname])+factor,dig) 
                #
                #save to disk
            # print(plant)
            if flag: 
                self.obj.writeFile(outfile,plant)
    #
    def run(self):
        self.modifyTemplates()

class SWATCUPRule():
    #
    # re.findall('([rva]{1})__([A-Z0-9_]+)\.([a-z]+).*',q.name[0])
    # b='SOL_AWC(1).sol'
    # a="r__SOL_AWC(1).sol________1"
    # a.split("__")
    # x__<parname>.<ext>__<hydrogrp>__<soltext>__<landuse>__<subbsn>__<slope>
    def parseRule_(self,name):
        rule={}
        com=['x','parname','ext','hydrogrp','soltext','landuse','subbsn','slope']
        val=name.split("__")
        #
        rule['fullname']=name
        rule[com[0]]=val[0]
        res=re.findall('([0-9a-zA-Z_\.\(\)\{\},-]+)\.([a-z]+)',val[1])
        rule[com[1]]=res[0][0]
        rule[com[2]]=res[0][1]
        #
        # for i in range(2,len(com)):
        #     rule[com[i+1]]=None
        #
        for i in range(2,len(val)):
            rule[com[i+1]]=None if len(val[i])==0 else val[i]
            if i==len(val):
                break
        if len(com)>len(val)+1:
            for j in range(len(com)-len(val)-1):
                rule[com[-1+j]]=None
        #
        return rule
    #
    def parseRule(self,simulation):
        rule={}
        for fullname in simulation.keys():
            r=self.parseRule_(fullname)
            r['parval']=simulation[fullname]
            if rule.get(r['ext'],None):
                rule[r['ext']].append(r)
            else:
                rule[r['ext']]=[r]
        return rule
    #
    def simulate(self,i,simulation,swatpath,templatefilepath):
        if not os.path.exists(swatpath):
            os.makedirs(swatpath)
        solution=self.parseRule(simulation)
        # print(i,solution,swatpath,templatefilepath)
        print(i,'transforming...')
        try:
            solobject=SOL(solution,templatefilepath,swatpath)
            solobject.run()
        except Exception as e:
            print('no replace SOL')
            pass
        try:
            hruobject=HRU(solution,templatefilepath,swatpath)
            hruobject.run()
        except Exception as e:
            print('no replace HRU')
            pass
        try:
            gwobject=GW(solution,templatefilepath,swatpath)
            gwobject.run()
        except Exception as e:
            print('no replace GW')
            pass  
        try:
            mgtobject=MGT(solution,templatefilepath,swatpath)
            mgtobject.run()
        except Exception as e:
            print('no replace MGT')
            pass  
        try:
            rteobject=RTE(solution,templatefilepath,swatpath)
            rteobject.run()
        except Exception as e:
            print('no replace RTE')
            pass
        try:
            bsnobject=BSN(solution,templatefilepath,swatpath)
            bsnobject.run()
        except Exception as e:
            print('no replace BSN')
            pass
        try:
            subobject=SUB(solution,templatefilepath,swatpath)
            subobject.run()
        except Exception as e:
            print('no replace SUB')
            pass
        # try:
        plantobject=plant(solution,templatefilepath,swatpath)
        plantobject.run()
        # except Exception as e:
        #     print('no replace plant.dat')
        #     pass

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    exogfile=os.path.join(LHS_path,'LHS_exog_1.csv')
    csv=pd.read_csv(exogfile,index_col=0)
    simulations=csv.to_dict(orient ='records')
    print(simulations)
    i=0
    swatpath=r'/home/junli/wangchen/swat/cache/swat_cache4565125215'
    templatefilepath=templatefile_path
    SWATCUPRule().simulate(i,simulations[i],swatpath,templatefilepath)