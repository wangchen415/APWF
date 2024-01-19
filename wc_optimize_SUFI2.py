import pandas as pd
import os
import math
import codecs
import warnings
import shutil
warnings.filterwarnings("ignore")
import re
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy.stats import t
from sklearn import preprocessing
from wc_global import *
from wc_lhs3 import LHS
from wc_swat import run_swat
from wc_evaluate import evaluate

#ps -ef | grep swat.exe | awk '{ print $2 }' | xargs kill -9
def param_rank(param_file,param_begin,modle):
    param_csv=pd.read_csv(param_file)
    param={}
    param_end={}
    for col in param_csv:
        if col=='param_name':
            pass
        else:
            for i in range(len(param_csv[col])):
                if i ==0:
                    param[col]={param_csv['param_name'][i]:param_csv[col][i]}
                else:
                    param[col].update({param_csv['param_name'][i]:param_csv[col][i]})
    if modle.split('-')[0]=='TC':
        param_rank=param['ET']
    else:
        param_rank=param[modle.split('-')[0]]
    for i in param_begin:
        for j in param_rank:
            if i == j and param_rank[j]!=2:
                param_end[i]=param_rank[j]
            elif i == j and param_rank[j]==2:
                param_rank[j]=1.75
                param_end[i]=param_rank[j]
    return param_end
    
def estimateRange_(data,inpar,param_end,alpha=0.975,y='nes',exog=None):
    # n=len(exog.columns)-len(param_end)
    J=np.empty((len(data)*(len(data)-1)//2, len(param_end)))
    row=0
    for var1 in range(len(data)-1):
        for var2 in range(var1+1,len(data)):
            g=data.iloc[var1][y]-data.iloc[var2][y]
            for col in range(0,len(exog.columns)):
                if re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',exog.columns[col])[0] in param_end:
                    # zz.append(re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',exog.columns[col])[0])
                    b = data.iloc[var1][col] - data.iloc[var2][col]
                    J[row,col] = g/b
            row=row+1
    # print(len(data))
    H=J.T.dot(J)
    C=data[y].var()*np.linalg.inv(H)
    c=np.sqrt(np.diagonal(C))
    ss={}
    for name,s in zip(exog.columns,c):
        ss[name]=s*t.ppf(alpha,len(data)-len(exog.columns))
    bj={}
    for cc in exog.columns:
        if re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',cc)[0] in param_end:
            bj[cc]=data[cc][data[y].idxmax()]
    lower={}
    up={}
    bmin={}
    bmax={}
    for xx in bj:
        # print(bj[xx],ss[xx],xx)
        if np.isnan(ss[xx]):
            lower[xx]=inpar[xx]['min']
            up[xx]=inpar[xx]['max']
        else:
            lower[xx]=bj[xx]-ss[xx]
            up[xx]=bj[xx]+ss[xx]
        bmin[xx]=lower[xx]-max((lower[xx]-inpar[xx]['min'])/2,(up[xx]-inpar[xx]['max'])/2)*param_end[re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',xx)[0]]
        bmax[xx]=lower[xx]+max((lower[xx]-inpar[xx]['min'])/2,(up[xx]-inpar[xx]['max'])/2)*param_end[re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',xx)[0]]
    return bmin,bmax

def estimateRange(data,inpar,inpar0,param_end,alpha=0.975,y='nes',exog=None,endog=None):
    # print(par)
    if exog is None or endog is None:
        return None
    dic={'param':[],'low':[],'up':[]}
    low_,up_=estimateRange_(data,inpar,param_end,alpha=alpha,y=y,exog=exog)
    for x in exog:
        dic['param'].append(x)
        if re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',x)[0] in param_end:
            dic['low'].append(inpar0[x]['min']) if inpar0[x]['min']> low_[x] else dic['low'].append(low_[x])
            dic['up'].append(inpar0[x]['max']) if inpar0[x]['max']< up_[x] else dic['up'].append(up_[x])
            # dic['low'].append(low_[x])
            # dic['up'].append(up_[x])
        else:
            dic['low'].append(inpar[x]['min'])
            dic['up'].append(inpar[x]['max'])
    df_=pd.DataFrame(dic)
    return df_
  
def readPar(parfile):
    par={}
    count=0
    with open(parfile) as fh:
        for ln in fh:
            if len(ln.strip())==0:
                continue
            if count<2:
                res=re.findall('\s*(\d+)\s*:.*',ln)
                if res is None:
                    print("error")
                else:
                    if count==0:
                        par["par_num"]=int(res[0])
                        # print(par)
                    else:
                        par["sim_num"]=int(res[0])
                        # print(par)
                    count+=1
            else:
                res=re.findall('\s*([0-9a-zA-Z_\.\(\)\{\},-]+)\s*([0-9\.\-]+)\s*([0-9\.\-]+)',ln)
                if res is None:
                    print("error")
                else:
                    # print(par)
                    par[res[0][0]]={"min":float(res[0][1]),"max":float(res[0][2])}
                    count+=1
            if count-2==par["par_num"]:
                break
    # print(self.par)
    return par

def writePar(outparfile,par,simnum):
    object=codecs.open(outparfile,'w','utf-8')
    object.write(str(len(par)).ljust(3,' ')+': Number of Parameters (the program only reads the first 4 parameters or any number indicated here)'+'\n')
    object.write(str(simnum).ljust(5,' ')+': number of simulations'+'\n')
    object.write('\n')
    object.write('\n')
    for l in range(len(par)):
        object.write(str(par['param'][l]).ljust(60,' ')+str(format(par['low'][l],'.6f')).rjust(20,' ')+str(format(par['up'][l],'.6f')).rjust(20,' ')+'\n')
    object.close()  

def optimize(fileinpar0,file_inpar,file_outpar,file_exog,file_endog,param_file,modle='flow-1',y='nes',simnum=10):
    inpar0=readPar(fileinpar0)
    inpar=readPar(file_inpar)
    #exog 外生变量（自变量）； endog 内生变量（因变量）
    exog=pd.read_csv(file_exog,index_col=0)
    endog=pd.read_csv(file_endog,index_col=0)
    #
    exog_lookup=[[exog.columns[i],'x%s'%(i)] for i in range(len(exog.columns))]
    # endog_lookup=[[endog.columns[i],'y%s'%i] for i in range(len(endog.columns))]
    dic=dict(exog_lookup)
    # print(exog_lookup)
    par={}
    param_begin=[]
    for key in inpar:
        if re.match(r'[a-z]+__[A-Z0-9a-z_\-\(\)]*.*',key):
            pp=re.findall(r'[a-z]+__([A-Z0-9a-z_\-\(\)]*).*',key)[0]
            param_begin.append(pp)
        # if dic.get(key,None) is not None:
        #     par[dic[key]]=inpar[key]
        #     if inpar[key]['max']==inpar[key]['min']:
        #         comm_num[key]=key
        #         n=n+1
        #     else:
        #         comm_num[key]=0
    #
    # print(comm_num)
    param_end=param_rank(param_file,param_begin,modle)
    # print(param_end)
    data=exog.join(endog)
    # threshold_=calThreshold(data,threshold,y=y)
    # data1=data[data[y]>threshold_]
    #
    # for v in exog_lookup:
    #     data1.rename({v[0]:v[1]}
    #                  ,axis='columns'
    #                 ,inplace=True)
    #
    # df=estimateRange(data1,par,exog=[v[1] for v in  exog_lookup],endog=endog.columns)
    # df[['param']] = df[['param']].replace([v[1] for v in exog_lookup], [v[0] for v in exog_lookup])
    # 
    df=estimateRange(data,inpar,inpar0,param_end,y=y,exog=exog,endog=endog)
    writePar(file_outpar,df,simnum)




if __name__ == "__main__":
    '''
    file_inpar=os.path.join(swatcup_parfile_path,'parfile_in.txt')
    file_inpar0=os.path.join(swatcup_parfile_path,'parfile_in.txt')
    cp=1
    file_outpar=os.path.join(SUFI_path,pathfile%(cp))
    file_exog=os.path.join(LHS_path,exogfile%(cp))
    file_endog=os.path.join(LHS_path,endogfile%(cp))
    print(file_inpar,file_outpar,file_exog,file_endog)
    optimize(file_inpar0,file_inpar,file_outpar,file_exog,file_endog,y=indicator,threshold=threshold,simnum=simulation_num)
    '''
    file_inpar0=os.path.join(swatcup_parfile_path,'parfile_in.txt')
    for cp in range(loop): 
        #lhs
        if cp == 0:
            swatcup_parfile=os.path.join(swatcup_parfile_path,'parfile_in.txt')
        else:
            swatcup_parfile=os.path.join(SUFI_path,pathfile%(cp))
        exog_file=os.path.join(LHS_path,exogfile%(cp+1))
        lhs=LHS(swatcup_parfile,exog_file)
        lhs.run()
        # print(lhs)
        #swat
        starttime1 = datetime.datetime.now()
        csv=pd.read_csv(exog_file,index_col=0)
        simulations=csv.to_dict(orient ='records')
        outputpath=os.path.join(output_path,'iter%d'%(cp+1))
        simdir={'flow':outputpath,'ET':outputpath,'SW':outputpath,'TC':outputpath}
        run_swat(simulations,templatefile_path,outputpath=outputpath,cachepath=cache_path,cachenum=cache_num,clean=False,prefix=cache_prefix)
        endtime1 = datetime.datetime.now()
        print (endtime1 - starttime1)
        #evaluate
        starttime2 = datetime.datetime.now()
        endog_file=os.path.join(LHS_path,endogfile%(cp+1))
        evaluate( modle, begin_date, end_date, begin_date2, end_date2, pro_num=cache_num , obvdir=obvdir, simdir=simdir, rchdict=rch_dict, subdict=sub_dict, weight=weight, endogfile=endog_file)
        # df.to_csv(endog_file, encoding="utf-8")
        endtime2 = datetime.datetime.now()
        print (endtime2 - starttime2)
        # df=evaluate(rch_dict,begin_date,end_date,obvdir=flow_path,simdir=outputpath,endogfile=endog_file)
        #optimize
        starttime3 = datetime.datetime.now()
        if cp == 0:
            file_inpar=os.path.join(swatcup_parfile_path,'parfile_in.txt')
        else:
            file_inpar=os.path.join(SUFI_path,pathfile%(cp))
        file_outpar=os.path.join(SUFI_path,pathfile%(cp+1))
        file_exog=os.path.join(LHS_path,exogfile%(cp+1))
        file_endog=os.path.join(LHS_path,endogfile%(cp+1))
        # print(file_inpar,file_outpar,file_exog,file_endog)
        optimize(file_inpar0,file_inpar,file_outpar,file_exog,file_endog,param_file,modle=modle,y=indicator,simnum=simulation_num)
        endtime3 = datetime.datetime.now()
        print (endtime3 - starttime3)
        print (endtime3 - starttime1)
        print ('********FINISH**********')