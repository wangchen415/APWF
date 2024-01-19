import warnings
warnings.filterwarnings("ignore")
import glob
import os
import re
import subprocess
import datetime
import math
import pandas as pd
import numpy as np
from numpy import append
from numpy import hsplit
from pip import main
from model_evaluation import triple_collocation as tc
from wc_global import *
from wc_simulation import *
from wc_SimET import *
from wc_Simflow import *
from wc_SimSW import *
from wc_ObvET import *
from wc_Obvflow import *
from wc_ObvSW import *
from multiprocessing import Pool

##############

#Qm pandas 观测值 ；Qs pandas 模拟值
def r2(Qm,Qs):
    Qm=Qm.astype(np.float64)
    Qs=Qs.astype(np.float64)
    try:
        r_square=(sum((Qm-(sum(Qm)/len(Qm)))*(Qs-(sum(Qs)/len(Qs))))**2)/(sum((Qm-(sum(Qm)/len(Qm)))**2)*sum((Qs-(sum(Qs)/len(Qs)))**2))
    except:
        r_square=0
    return r_square

def Nes(Qm,Qs):
    Qm=Qm.astype(np.float64)
    Qs=Qs.astype(np.float64)
    try:
        nes=1-((sum((Qm-Qs)**2))/(sum((Qm-(sum(Qm)/len(Qm)))**2)))
    except:
        nes=0
    return nes

def PBIAS(Qm,Qs):
    Qm=Qm.astype(np.float64)
    Qs=Qs.astype(np.float64)
    try:
        pbias=100*((sum((Qm-Qs)))/(sum(Qm)))
    except:
        pbias=0
    return pbias

def KGE(Qm,Qs):
    Qm=Qm.astype(np.float64).dropna()
    Qs=Qs.astype(np.float64).dropna()
    try:
        r = ((Qm - (sum(Qm)/len(Qm))) * (Qs - (sum(Qs)/len(Qs)))).sum() / (math.sqrt(((Qm - (sum(Qm)/len(Qm))) ** 2).sum() * ((Qs - (sum(Qs)/len(Qs))) ** 2).sum()))
        kge = 1 - math.sqrt((r - 1) ** 2 + ((np.nanstd(Qs) / np.nanstd(Qm)) - 1) ** 2 + (((sum(Qs)/len(Qs)) / (sum(Qm)/len(Qm))) - 1) ** 2)
        # print(kge)
    except:
        kge=0
    return kge

def process_file(args):
    filename, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date, weight = args
    r_square={}
    nes={}
    pbias={}
    kge={}

    if modle.split('-')[0]=='flow':
        if modle.split('-')[-1]=='Mon':
            simflow=SimFlow(filename,rchdict,begin_date,end_date,modle).getflow_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            simflow=SimFlow(filename,rchdict,begin_date,end_date,modle).getflow_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            simflow=SimFlow(filename,rchdict,begin_date,end_date,modle).getflow_days(begin_date2,end_date2)
        for k,df  in simflow.items():
            merged=pd.merge(obv[k], simflow[k],left_on=obv[k]['DAY'],right_on=simflow[k]['DAY'],suffixes=("_m", "_s"))
            r_square['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=r2(merged['FLOW_OUT_m'],merged['FLOW_OUT_s'])
            nes['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=Nes(merged['FLOW_OUT_m'],merged['FLOW_OUT_s'])
            pbias['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=PBIAS(merged['FLOW_OUT_m'],merged['FLOW_OUT_s'])
            kge['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=KGE(merged['FLOW_OUT_m'],merged['FLOW_OUT_s'])
            # r_square_dict = pd.Series(r_square).rename('r_square')
            # nes_dict = pd.Series(nes).rename('nes')
            # pbias_dict = pd.Series(pbias).rename('pbias')
            # kge_dict = pd.Series(kge).rename('kge')
            # all =pd.concat([r_square_dict, nes_dict,pbias_dict,kge_dict], axis = 1)
            r_square_flow = {}
            for key, value in r_square.items():
                first_char = key.split('-')[0]
                if first_char in r_square_flow:
                    r_square_flow[first_char] += value*weig
                else:
                    r_square_flow[first_char] = value*weig
            nes_flow = {}
            for key, value in nes.items():
                first_char = key.split('-')[0]
                if first_char in nes_flow:
                    nes_flow[first_char] += value*weig
                else:
                    nes_flow[first_char] = value*weig
            #
            pbias_flow = {}
            for key, value in pbias.items():
                first_char = key.split('-')[0]
                if first_char in pbias_flow:
                    pbias_flow[first_char] += value*weig
                else:
                    pbias_flow[first_char] = value*weig
            #
            kge_flow = {}
            for key, value in kge.items():
                first_char = key.split('-')[0]
                if first_char in kge_flow:
                    kge_flow[first_char] += value*weig
                else:
                    kge_flow[first_char] = value*weig
        r_square,nes,pbias,kge=r_square_flow,nes_flow,pbias_flow,kge_flow
    elif modle.split('-')[0]=='ET':
        if modle.split('-')[-1]=='Mon':
            simET=SimET(filename,subdict,begin_date,end_date,modle).getet_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            simET=SimET(filename,subdict,begin_date,end_date,modle).getet_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            simET=SimET(filename,subdict,begin_date,end_date,modle).getet_days(begin_date2,end_date2)
        for k,df  in simET.items():
            merged=pd.merge(obv[k], simET[k],left_on=obv[k]['DAY'],right_on=simET[k]['DAY'],suffixes=("_m", "_s"))
            r_square['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=r2(merged['ET_m'],merged['ET_s'])
            nes['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=Nes(merged['ET_m'],merged['ET_s'])
            pbias['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=PBIAS(merged['ET_m'],merged['ET_s'])
            kge['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=KGE(merged['ET_m'],merged['ET_s'])
            # r_square_dict = pd.Series(r_square).rename('r_square')
            # nes_dict = pd.Series(nes).rename('nes')
            # pbias_dict = pd.Series(pbias).rename('pbias')
            # kge_dict = pd.Series(kge).rename('kge')
            # all =pd.concat([r_square_dict, nes_dict,pbias_dict,kge_dict], axis = 1)
            r_square_ET = {}
            for key, value in r_square.items():
                first_char = key.split('-')[0]
                if first_char in r_square_ET:
                    r_square_ET[first_char] += value*weig
                else:
                    r_square_ET[first_char] = value*weig
            nes_ET = {}
            for key, value in nes.items():
                first_char = key.split('-')[0]
                if first_char in nes_ET:
                    nes_ET[first_char] += value*weig
                else:
                    nes_ET[first_char] = value*weig
            #
            pbias_ET = {}
            for key, value in pbias.items():
                first_char = key.split('-')[0]
                if first_char in pbias_ET:
                    pbias_ET[first_char] += value*weig
                else:
                    pbias_ET[first_char] = value*weig
            #
            kge_ET = {}
            for key, value in kge.items():
                first_char = key.split('-')[0]
                if first_char in kge_ET:
                    kge_ET[first_char] += value*weig
                else:
                    kge_ET[first_char] = value*weig
        r_square,nes,pbias,kge=r_square_ET,nes_ET,pbias_ET,kge_ET
    elif modle.split('-')[0]=='SW':
        if modle.split('-')[-1]=='Mon':
            simsw=SimSW(filename,subdict,begin_date,end_date,modle).getsw_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            simsw=SimSW(filename,subdict,begin_date,end_date,modle).getsw_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            simsw=SimSW(filename,subdict,begin_date,end_date,modle).getsw_days(begin_date2,end_date2)
        r_square={}
        nes={}
        pbias={}
        kge={}
        for (i,df),(j,df2) in zip(simsw.items(),obv.items()):
            merged=pd.merge(obv[i], simsw[i], left_index=True,right_index=True)
            for k,n in zip(df2.columns,range(len(df2.columns))):
                r_square['%d-%s-%s'%(int(os.path.split(filename)[-1][7:10]),i,n+1)]=r2(merged['Layer%s_x'%str(n+1)],merged['Layer%s_y'%str(n+2)])
                nes['%d-%s-%s'%(int(os.path.split(filename)[-1][7:10]),i,n+1)]=Nes(merged['Layer%s_x'%str(n+1)],merged['Layer%s_y'%str(n+2)])
                pbias['%d-%s-%s'%(int(os.path.split(filename)[-1][7:10]),i,n+1)]=PBIAS(merged['Layer%s_x'%str(n+1)],merged['Layer%s_y'%str(n+2)])
                kge['%d-%s-%s'%(int(os.path.split(filename)[-1][7:10]),i,n+1)]=KGE(merged['Layer%s_x'%str(n+1)],merged['Layer%s_y'%str(n+2)])
            r_square_SW = {}
            for key, value in r_square.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in r_square_SW:
                    r_square_SW['%s-%s'%(first_char,layer_char)] += value*weig
                else:
                    r_square_SW['%s-%s'%(first_char,layer_char)] = value*weig
            filtered_values = [v for k, v in r_square_SW.items() if k.startswith('%s-'%first_char)]
            r_square_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
            nes_SW = {}
            for key, value in nes.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in nes_SW:
                    nes_SW['%s-%s'%(first_char,layer_char)] += value*weig
                else:
                    nes_SW['%s-%s'%(first_char,layer_char)] = value*weig
            filtered_values = [v for k, v in nes_SW.items() if k.startswith('%s-'%first_char)]
            nes_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
            pbias_SW = {}
            for key, value in pbias.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in pbias_SW:
                    pbias_SW['%s-%s'%(first_char,layer_char)] += value*weig
                else:
                    pbias_SW['%s-%s'%(first_char,layer_char)] = value*weig
            filtered_values = [v for k, v in pbias_SW.items() if k.startswith('%s-'%first_char)]
            pbias_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
            kge_SW = {}
            for key, value in kge.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in kge_SW:
                    kge_SW['%s-%s'%(first_char,layer_char)] += value*weig
                else:
                    kge_SW['%s-%s'%(first_char,layer_char)] = value*weig
            filtered_values = [v for k, v in kge_SW.items() if k.startswith('%s-'%first_char)]
            kge_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
        r_square,nes,pbias,kge=r_square_SW,nes_SW,pbias_SW,kge_SW
    elif modle.split('-')[0]=='flow&ET':
        r_square={}
        nes={}
        pbias={}
        kge={}
        r_square_F={}
        r_square_E={}
        nes_F={}
        nes_E={}
        pbias_F={}
        pbias_E={}
        kge_F={}
        kge_E={}
        if modle.split('-')[-1]=='Mon':
            simflow=SimFlow(filename['flow'],rchdict,begin_date,end_date,modle).getflow_month(begin_date2,end_date2)
            simET=SimET(filename['ET'],subdict,begin_date,end_date,modle).getet_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            simflow=SimFlow(filename['flow'],rchdict,begin_date,end_date,modle).getflow_8days(begin_date2,end_date2)
            simET=SimET(filename['ET'],subdict,begin_date,end_date,modle).getet_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            simflow=SimFlow(filename['flow'],rchdict,begin_date,end_date,modle).getflow_days(begin_date2,end_date2)
            simET=SimET(filename['ET'],subdict,begin_date,end_date,modle).getet_days(begin_date2,end_date2)
        for (k,df) in simflow.items():
            merged_flow=pd.merge(obv['flow'][k], simflow[k],left_on=obv['flow'][k]['DAY'],right_on=simflow[k]['DAY'],suffixes=("_m", "_s"))
            #
            r_square_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=r2(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            nes_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=Nes(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            pbias_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=PBIAS(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            kge_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=KGE(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            #                    
            r_square_flow = {}
            for key, value in r_square_F.items():
                first_char = key.split('-')[0]
                if first_char in r_square_flow:
                    r_square_flow[first_char] += value*weig['flow']
                else:
                    r_square_flow[first_char] = value*weig['flow']
            nes_flow = {}
            for key, value in nes_F.items():
                first_char = key.split('-')[0]
                if first_char in nes_flow:
                    nes_flow[first_char] += value*weig['flow']
                else:
                    nes_flow[first_char] = value*weig['flow']
            #
            pbias_flow = {}
            for key, value in pbias_F.items():
                first_char = key.split('-')[0]
                if first_char in pbias_flow:
                    pbias_flow[first_char] += value*weig['flow']
                else:
                    pbias_flow[first_char] = value*weig['flow']
            #
            kge_flow = {}
            for key, value in kge_F.items():
                first_char = key.split('-')[0]
                if first_char in kge_flow:
                    kge_flow[first_char] += value*weig['flow']
                else:
                    kge_flow[first_char] = value*weig['flow']
        for k,df  in simET.items():
            merged_ET=pd.merge(obv['ET'][k], simET[k],left_on=obv['ET'][k]['DAY'],right_on=simET[k]['DAY'],suffixes=("_m", "_s"))
            #
            r_square_E['%d-%s'%(int(os.path.split(filename['ET'])[-1][7:10]),k)]=r2(merged_ET['ET_m'],merged_ET['ET_s'])
            nes_E['%d-%s'%(int(os.path.split(filename['ET'])[-1][7:10]),k)]=Nes(merged_ET['ET_m'],merged_ET['ET_s'])
            pbias_E['%d-%s'%(int(os.path.split(filename['ET'])[-1][7:10]),k)]=PBIAS(merged_ET['ET_m'],merged_ET['ET_s'])
            kge_E['%d-%s'%(int(os.path.split(filename['ET'])[-1][7:10]),k)]=KGE(merged_ET['ET_m'],merged_ET['ET_s'])
            r_square_ET = {}
            for key, value in r_square_E.items():
                first_char = key.split('-')[0]
                if first_char in r_square_ET:
                    r_square_ET[first_char] += value*weig['ET']
                else:
                    r_square_ET[first_char] = value*weig['ET']
            nes_ET = {}
            for key, value in nes_E.items():
                first_char = key.split('-')[0]
                if first_char in nes_ET:
                    nes_ET[first_char] += value*weig['ET']
                else:
                    nes_ET[first_char] = value*weig['ET']
            #
            pbias_ET = {}
            for key, value in pbias_E.items():
                first_char = key.split('-')[0]
                if first_char in pbias_ET:
                    pbias_ET[first_char] += value*weig['ET']
                else:
                    pbias_ET[first_char] = value*weig['ET']
            #
            kge_ET = {}
            for key, value in kge_E.items():
                first_char = key.split('-')[0]
                if first_char in kge_ET:
                    kge_ET[first_char] += value*weig['ET']
                else:
                    kge_ET[first_char] = value*weig['ET']
        for i,j,k in zip(r_square_flow.keys(),r_square_flow.values(),r_square_ET.values()):
            r_square[i]=j*weight['flow']+k*weight['ET']
        for i,j,k in zip(nes_flow.keys(),nes_flow.values(),nes_ET.values()):
            nes[i]=j*weight['flow']+k*weight['ET']
        for i,j,k in zip(pbias_flow.keys(),pbias_flow.values(),pbias_ET.values()):
            pbias[i]=j*weight['flow']+k*weight['ET']
        for i,j,k in zip(kge_flow.keys(),kge_flow.values(),kge_ET.values()):
            kge[i]=j*weight['flow']+k*weight['ET']
    #
    elif modle.split('-')[0]=='flow&SW':
        r_square_F={}
        r_square_S={}
        nes_F={}
        nes_S={}
        pbias_F={}
        pbias_S={}
        kge_F={}
        kge_S={}
        if modle.split('-')[-1]=='Mon':
            simflow=SimFlow(filename['flow'],rchdict,begin_date,end_date,modle).getflow_month(begin_date2,end_date2)
            simsw=SimSW(filename['SW'],subdict,begin_date,end_date,modle).getsw_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            simflow=SimFlow(filename['flow'],rchdict,begin_date,end_date,modle).getflow_8days(begin_date2,end_date2)
            simsw=SimSW(filename['SW'],subdict,begin_date,end_date,modle).getsw_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            simflow=SimFlow(filename['flow'],rchdict,begin_date,end_date,modle).getflow_days(begin_date2,end_date2)
            simsw=SimSW(filename['SW'],subdict,begin_date,end_date,modle).getsw_days(begin_date2,end_date2)
        for (k,df) in simflow.items():
            merged_flow=pd.merge(obv['flow'][k], simflow[k],left_on=obv['flow'][k]['DAY'],right_on=simflow[k]['DAY'],suffixes=("_m", "_s"))
            #
            r_square_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=r2(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            nes_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=Nes(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            pbias_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=PBIAS(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            kge_F['%d-%s'%(int(os.path.split(filename['flow'])[-1][7:10]),k)]=KGE(merged_flow['FLOW_OUT_m'],merged_flow['FLOW_OUT_s'])
            #                    
            r_square_flow = {}
            for key, value in r_square_F.items():
                first_char = key.split('-')[0]
                if first_char in r_square_flow:
                    r_square_flow[first_char] += value*weig['flow']
                else:
                    r_square_flow[first_char] = value*weig['flow']
            nes_flow = {}
            for key, value in nes_F.items():
                first_char = key.split('-')[0]
                if first_char in nes_flow:
                    nes_flow[first_char] += value*weig['flow']
                else:
                    nes_flow[first_char] = value*weig['flow']
            #
            pbias_flow = {}
            for key, value in pbias_F.items():
                first_char = key.split('-')[0]
                if first_char in pbias_flow:
                    pbias_flow[first_char] += value*weig['flow']
                else:
                    pbias_flow[first_char] = value*weig['flow']
            #
            kge_flow = {}
            for key, value in kge_F.items():
                first_char = key.split('-')[0]
                if first_char in kge_flow:
                    kge_flow[first_char] += value*weig['flow']
                else:
                    kge_flow[first_char] = value*weig['flow']
        for (i,df),(j,df2) in zip(simsw.items(),obv['SW'].items()):
            merged_SW=pd.merge(obv['SW'][i], simsw[i], left_index=True,right_index=True)
            for k,n in zip(df2.columns,range(len(df2.columns))):
                r_square_S['%d-%s-%s'%(int(os.path.split(filename['SW'])[-1][7:10]),i,n+1)]=r2(merged_SW['Layer%s_x'%str(n+1)],merged_SW['Layer%s_y'%str(n+2)])
                nes_S['%d-%s-%s'%(int(os.path.split(filename['SW'])[-1][7:10]),i,n+1)]=Nes(merged_SW['Layer%s_x'%str(n+1)],merged_SW['Layer%s_y'%str(n+2)])
                pbias_S['%d-%s-%s'%(int(os.path.split(filename['SW'])[-1][7:10]),i,n+1)]=PBIAS(merged_SW['Layer%s_x'%str(n+1)],merged_SW['Layer%s_y'%str(n+2)])
                kge_S['%d-%s-%s'%(int(os.path.split(filename['SW'])[-1][7:10]),i,n+1)]=KGE(merged_SW['Layer%s_x'%str(n+1)],merged_SW['Layer%s_y'%str(n+2)])
            r_square_SW = {}
            for key, value in r_square_S.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in r_square_SW:
                    r_square_SW['%s-%s'%(first_char,layer_char)] += value*weig['SW']
                else:
                    r_square_SW['%s-%s'%(first_char,layer_char)] = value*weig['SW']
            filtered_values = [v for ks, v in r_square_SW.items() if ks.startswith('%s-'%first_char)]
            r_square_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
            nes_SW = {}
            for key, value in nes_S.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in nes_SW:
                    nes_SW['%s-%s'%(first_char,layer_char)] += value*weig['SW']
                else:
                    nes_SW['%s-%s'%(first_char,layer_char)] = value*weig['SW']
            filtered_values = [v for ks, v in nes_SW.items() if ks.startswith('%s-'%first_char)]
            nes_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
            pbias_SW = {}
            for key, value in pbias_S.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in pbias_SW:
                    pbias_SW['%s-%s'%(first_char,layer_char)] += value*weig['SW']
                else:
                    pbias_SW['%s-%s'%(first_char,layer_char)] = value*weig['SW']
            filtered_values = [v for ks, v in pbias_SW.items() if ks.startswith('%s-'%first_char)]
            pbias_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
            kge_SW = {}
            for key, value in kge_S.items():
                first_char = key.split('-')[0]
                layer_char = key.split('-')[-1]
                if '%s-%s'%(first_char,layer_char) in kge_SW:
                    kge_SW['%s-%s'%(first_char,layer_char)] += value*weig['SW']
                else:
                    kge_SW['%s-%s'%(first_char,layer_char)] = value*weig['SW']
            filtered_values = [v for ks, v in kge_SW.items() if ks.startswith('%s-'%first_char)]
            kge_SW[first_char]= sum(filtered_values) / len(filtered_values) if filtered_values else None
        for i,j in zip(r_square_flow.keys(),r_square_flow.values()):
            r_square[i]=j*weight['flow']+r_square_SW[i]*weight['SW']
        for i,j in zip(nes_flow.keys(),nes_flow.values()):
            nes[i]=j*weight['flow']+nes_SW[i]*weight['SW']
        for i,j in zip(pbias_flow.keys(),pbias_flow.values()):
            pbias[i]=j*weight['flow']+pbias_SW[i]*weight['SW']
        for i,j in zip(kge_flow.keys(),kge_flow.values()):
            kge[i]=j*weight['flow']+kge_SW[i]*weight['SW']
    elif modle.split('-')[0]=='TC':
        if modle.split('-')[-1]=='Mon':
            simET=SimET(filename,subdict,begin_date,end_date,modle).getet_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            simET=SimET(filename,subdict,begin_date,end_date,modle).getet_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            simET=SimET(filename,subdict,begin_date,end_date,modle).getet_days(begin_date2,end_date2)
        for k,df  in simET.items():
            x=simET[k]['ET'].to_numpy().astype(np.float32)
            y=obv[0][k]['ET'].to_numpy().astype(np.float32)
            z=obv[1][k]['ET'].to_numpy().astype(np.float32)
            q_hat = tc.covariance_matrix(x, y, z)
            stderr, rho, snr_db, sensitivity = tc.etc(q_hat)
            # print(rho**2)
            r_square['%d-%s'%(int(os.path.split(filename)[-1][7:10]),k)]=rho[0]**2
            # r_square[int(os.path.split(filename)[-1][7:10])]={'simluation':rho[0]**2,'%s'%(os.path.split(ETfile_1)[-1].split('_')[-1].split('.')[0]):rho[1]**2,'%s'%(os.path.split(ETfile_2)[-1].split('_')[-1].split('.')[0]):rho[2]**2}
            # r_square[int(os.path.split(filename)[-1][7:10])]={'simluation':rho**2[0],'%s'%(os.path.split(ETfile_1)[-1].split('_')[-1].split('.')[0]):rho**2[1],'%s'%(os.path.split(ETfile_2)[-1].split('_')[-1].split('.')[0]):rho**2[1]}
            r_square_ET = {}
            for key, value in r_square.items():
                first_char = key.split('-')[0]
                if first_char in r_square_ET:
                    r_square_ET[first_char] += value*weig
                else:
                    r_square_ET[first_char] = value*weig
            nes_ET = {}
            # for key, value in nes.items():
            #     first_char = key.split('-')[0]
            #     if first_char in nes_ET:
            #         nes_ET[first_char] += value*weig
            #     else:
            #         nes_ET[first_char] = value*weig
            #
            pbias_ET = {}
            # for key, value in pbias.items():
            #     first_char = key.split('-')[0]
            #     if first_char in pbias_ET:
            #         pbias_ET[first_char] += value*weig
            #     else:
            #         pbias_ET[first_char] = value*weig
            #
            kge_ET = {}
            # for key, value in kge.items():
            #     first_char = key.split('-')[0]
            #     if first_char in kge_ET:
            #         kge_ET[first_char] += value*weig
            #     else:
            #         kge_ET[first_char] = value*weig
        r_square,nes,pbias,kge=r_square_ET,nes_ET,pbias_ET,kge_ET
    return {"r_square": r_square, "nes": nes, "pbias": pbias, "kge": kge}

def evaluate_model(modle, begin_date, end_date, begin_date2, end_date2, pro_num=50, obvdir={}, simdir={}, rchdict=None, subdict=None, weight=None):
    if modle.split('-')[0]=='flow':
        filelist=glob.glob(os.path.join(simdir['flow'],'output_???.rch'))
        filelist.sort()
        if modle.split('-')[-1]=='Mon':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_8day(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_day(begin_date2,end_date2)
        obv=obvflow
        weig=1/len(obv)
        args_list = [(filename, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date,weight) for filename in filelist]
        with Pool(processes=pro_num) as pool:  # 并行进程的数量，根据CPU核心数量来设置
            results = pool.map(process_file, args_list)
    elif modle.split('-')[0]=='ET':
        if modle.split('-')[1]=='SUB':
            filelist=glob.glob(os.path.join(simdir['ET'],'output_???.sub'))
            filelist.sort()
        elif modle.split('-')[1]=='HRU':
            filelist=glob.glob(os.path.join(simdir['ET'],'output_???.hru'))
            filelist.sort()
        if modle.split('-')[-1]=='Mon':
            obvET=ObvET(obvdir['ET'],subdict).get_ET_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            obvET=ObvET(obvdir['ET'],subdict).get_ET_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            obvET=ObvET(obvdir['ET'],subdict).get_ET_days(begin_date2,end_date2)
        obv=obvET
        weig=1/len(obv)
        args_list = [(filename, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date,weight) for filename in filelist]
        with Pool(processes=pro_num) as pool:  # 并行进程的数量，根据CPU核心数量来设置
            results = pool.map(process_file, args_list)

    elif modle.split('-')[0]=='SW':
        filelist=glob.glob(os.path.join(simdir['SW'],'output_???.swr'))
        filelist.sort()
        if modle.split('-')[-1]=='Mon':
            obvSW=ObvSW(obvdir['SW'],subdict).get_SW_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            obvSW=ObvSW(obvdir['SW'],subdict).get_SW_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            obvSW=ObvSW(obvdir['SW'],subdict).get_SW_days(begin_date2,end_date2)
        obv=obvSW
        weig=1/len(obv)
        args_list = [(filename, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date,weight) for filename in filelist]
        with Pool(processes=pro_num) as pool:  # 并行进程的数量，根据CPU核心数量来设置
            results = pool.map(process_file, args_list)

    elif modle.split('-')[0]=='flow&ET':
        filelist_flow=glob.glob(os.path.join(simdir['flow'],'output_???.rch'))
        filelist_flow.sort()
        if modle.split('-')[1]=='SUB':
            filelist_ET=glob.glob(os.path.join(simdir['ET'],'output_???.sub'))
            filelist_ET.sort()
        elif modle.split('-')[1]=='HRU':
            filelist_ET=glob.glob(os.path.join(simdir['ET'],'output_???.hru'))
            filelist_ET.sort()
        if modle.split('-')[-1]=='Mon':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_month(begin_date2,end_date2)
            obvET=ObvET(obvdir['ET'],subdict).get_ET_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_8day(begin_date2,end_date2)
            obvET=ObvET(obvdir['ET'],subdict).get_ET_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_day(begin_date2,end_date2)
            obvET=ObvET(obvdir['ET'],subdict).get_ET_days(begin_date2,end_date2)
        obv={}
        weig={}
        filelist={}
        obv['flow']=obvflow
        obv['ET']=obvET
        weig['flow']=1/len(obvflow)
        weig['ET']=1/len(obvET)
        filelist['flow']=filelist_flow
        filelist['ET']=filelist_ET
        args_list = [({'flow':filename1,'ET':filename2}, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date, weight) for filename1,filename2 in zip(filelist['flow'],filelist['ET'])]
        with Pool(processes=pro_num) as pool:  # 并行进程的数量，根据CPU核心数量来设置
            results = pool.map(process_file, args_list)
    # weig=1/len(obv)
    # # print(obv)
    # args_list = [(filename, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date) for filename in filelist]
    # with Pool(processes=4) as pool:  # 并行进程的数量，根据CPU核心数量来设置
    #     results = pool.map(process_file, args_list)

    elif modle.split('-')[0]=='flow&SW':
        filelist_flow=glob.glob(os.path.join(simdir['flow'],'output_???.rch'))
        filelist_flow.sort()
        filelist_SW=glob.glob(os.path.join(simdir['SW'],'output_???.swr'))
        filelist_SW.sort()
        if modle.split('-')[-1]=='Mon':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_month(begin_date2,end_date2)
            obvSW=ObvSW(obvdir['SW'],subdict).get_SW_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_8day(begin_date2,end_date2)
            obvSW=ObvSW(obvdir['SW'],subdict).get_SW_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            obvflow=ObvFlow(obvdir['flow'],rchdict,begin_date,end_date).getflow_day(begin_date2,end_date2)
            obvSW=ObvSW(obvdir['SW'],subdict).get_SW_days(begin_date2,end_date2)
        obv={}
        weig={}
        filelist={}
        obv['flow']=obvflow
        obv['SW']=obvSW
        weig['flow']=1/len(obvflow)
        weig['SW']=1/len(obvSW)
        filelist['flow']=filelist_flow
        filelist['SW']=filelist_SW
        args_list = [({'flow':filename1,'SW':filename2}, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date, weight) for filename1,filename2 in zip(filelist['flow'],filelist['SW'])]
        with Pool(processes=pro_num) as pool:  # 并行进程的数量，根据CPU核心数量来设置
            results = pool.map(process_file, args_list)
    elif modle.split('-')[0]=='TC':
        if modle.split('-')[1]=='SUB':
            filelist=glob.glob(os.path.join(simdir['ET'],'output_???.sub'))
            filelist.sort()
        elif modle.split('-')[1]=='HRU':
            filelist=glob.glob(os.path.join(simdir['ET'],'output_???.hru'))
            filelist.sort()
        #
        if modle.split('-')[-1]=='Mon':
            obvET_1=ObvET(obvdir['TC'][0],subdict).get_ET_month(begin_date2,end_date2)
            obvET_2=ObvET(obvdir['TC'][1],subdict).get_ET_month(begin_date2,end_date2)
        elif modle.split('-')[-1]=='8days':
            obvET_1=ObvET(obvdir['TC'][0],subdict).get_ET_8days(begin_date2,end_date2)
            obvET_2=ObvET(obvdir['TC'][1],subdict).get_ET_8days(begin_date2,end_date2)
        elif modle.split('-')[-1]=='days':
            obvET_1=ObvET(obvdir['TC'][0],subdict).get_ET_days(begin_date2,end_date2)
            obvET_2=ObvET(obvdir['TC'][1],subdict).get_ET_days(begin_date2,end_date2)
        obv=[obvET_1,obvET_2]
        weig=1/len(obvET_1)
        args_list = [(filename, obv, weig, begin_date2, end_date2, modle, rchdict, subdict, begin_date, end_date,weight) for filename in filelist]
        with Pool(processes=pro_num) as pool:  # 并行进程的数量，根据CPU核心数量来设置
            results = pool.map(process_file, args_list)
    return results


def evaluate(modle, begin_date, end_date, begin_date2, end_date2, pro_num=50, obvdir={}, simdir={}, rchdict=None, subdict=None, weight=None,endogfile=r'D:\new_method_output\ceshi\test.csv'):
    results=evaluate_model(modle, begin_date, end_date, begin_date2, end_date2,pro_num=pro_num, obvdir=obvdir, simdir=simdir, rchdict=rchdict, subdict=subdict, weight=weight)
    new_data = {
        'r_square': {},
        'nes': {},
        'pbias': {},
        'kge': {}
    }
    for item in results:
        for key in item:
            new_data[key].update(item[key])
    if modle.split('-')[0]=='SW':
        df1 = pd.DataFrame()
        for key, value in new_data['r_square'].items():
            row, _, col = key.partition('-')
            df1.at[row, col] = value
        series_with_duplicates  = pd.Series(['r_square%s'%(re.findall(r'[0-9]+-?([0-9]?)',col)[0]) for col in new_data['r_square'].keys()])
        series_without_duplicates = series_with_duplicates.drop_duplicates()
        new_columns=series_without_duplicates.tolist()
        df1.columns=new_columns
        #
        df2 = pd.DataFrame()
        for key, value in new_data['nes'].items():
            row, _, col = key.partition('-')
            df2.at[row, col] = value
        series_with_duplicates  = pd.Series(['Nes%s'%(re.findall(r'[0-9]+-?([0-9]?)',col)[0]) for col in new_data['nes'].keys()])
        series_without_duplicates = series_with_duplicates.drop_duplicates()
        new_columns=series_without_duplicates.tolist()
        df2.columns=new_columns
        #
        df3 = pd.DataFrame()
        for key, value in new_data['pbias'].items():
            row, _, col = key.partition('-')
            df3.at[row, col] = value
        series_with_duplicates  = pd.Series(['PBIAS%s'%(re.findall(r'[0-9]+-?([0-9]?)',col)[0]) for col in new_data['pbias'].keys()])
        series_without_duplicates = series_with_duplicates.drop_duplicates()
        new_columns=series_without_duplicates.tolist()
        df3.columns=new_columns
        #
        df4 = pd.DataFrame()
        for key, value in new_data['kge'].items():
            row, _, col = key.partition('-')
            df4.at[row, col] = value
        series_with_duplicates  = pd.Series(['KGE%s'%(re.findall(r'[0-9]+-?([0-9]?)',col)[0]) for col in new_data['kge'].keys()])
        series_without_duplicates = series_with_duplicates.drop_duplicates()
        new_columns=series_without_duplicates.tolist()
        df4.columns=new_columns
        df=pd.concat([df1,df2,df3,df4],axis=1)
    else:
        df=pd.DataFrame(new_data)
        df.to_csv(endogfile, encoding="utf-8")
    return new_data

if __name__=='__main__':
    starttime = datetime.datetime.now()
    # rchdict={49:'JiaQiao',54:'QingYang',85:'NingXian',86:'YuLuoPing'}
    pro_num=50
    endog_file=r'D:\new_method_output\ceshi\LHS_endog_wc.csv'
    rchdict={86:'YuLuoPing'}
    subdict={86:'YuLuoPing'}
    begin_date='2008-01-01'
    end_date='2018-12-31'
    begin_date2='2008-01-01'
    end_date2='2018-12-31'
    remotesensing_path=r'D:\python\SWAT-AIPC\RSdata'
    SWfilelist=[os.path.join(remotesensing_path,'rescale_0-5cm.csv'),os.path.join(remotesensing_path,'rescale_5-15cm.csv'),os.path.join(remotesensing_path,'rescale_15-30cm.csv'),os.path.join(remotesensing_path,'rescale_30-60cm.csv'),os.path.join(remotesensing_path,'rescale_60-100cm.csv')]
    TCfilelist=[r'D:\wangchen_swat\remotesensing\data_pmlv2_86.csv',r'D:\wangchen_swat\remotesensing\data_pmlv2_86.csv']
    obvdir={'flow':r'D:\wangchen_swat\水文站点new','ET':r'D:\wangchen_swat\remotesensing\data_pmlv2_86.csv','SW':SWfilelist,'TC':TCfilelist}
    # simdir=r'D:\new_method_output\ceshi_day\iter1'
    simdir={'flow':r'D:\new_method_output\ceshi\iter1','ET':r'D:\new_method_output\ceshi\iter1','SW':r'D:\new_method_output\ceshi\iter1','TC':r'D:\new_method_output\ceshi\iter1'}
    # ETfile=r'D:\wangchen_swat\remotesensing\data_pmlv2_86.csv'
    modle='flow-SUB-Mon'
    # weight={'flow':0.3,'ET':0.7}
    weight={'SW':0.5,'ET':0.7,'flow':0.5}
    new_data=evaluate( modle, begin_date, end_date, begin_date2, end_date2, pro_num=pro_num, obvdir=obvdir, simdir=simdir, rchdict=rchdict, subdict=subdict, weight=weight, endogfile=endog_file)
    print(new_data)
    endtime = datetime.datetime.now()
    print (endtime - starttime)