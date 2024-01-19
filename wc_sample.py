import re
import os
import pandas as pd
import numpy as np


def ParameterArray(sample_size, dimension, bounds):
    """
    根据输入的各变量的范围矩阵以及希望得到的样本数量，输出样本参数矩阵
    :sample_size:候选解数量（希望输出的样本数量）
    :dimension:维度（参与模型率定的变量数量）
    :bounds:变量上下限矩阵,shape为(m,2),m为变量个数
    :return:样本参数矩阵
    """
    uniform_samples = np.random.uniform(low=0, high=1, size=(sample_size, dimension))
    scaled_samples = np.zeros_like(uniform_samples)
    for i, (low, high) in enumerate(bounds):
        scaled_samples[:, i] = uniform_samples[:, i] * (high - low) + low
    return  scaled_samples

class DoE(object):
    def __init__(self, name_value):
        self.name = name_value
        self.type = "DoE"
        self.result = None
        
class DoE_PSO(DoE):
    # 粒子群样本生成
    def __init__(self, name_value, sample_size, dimension, bounds):
        DoE.__init__(self, name_value)
        self.type = "PSO"
        self.sample_size = sample_size
        self.dimension = dimension
        self.bounds = bounds
        self.ParameterArray = ParameterArray(sample_size, dimension, bounds)
    def write_to_dataframe(self):
        """
        将样本数据写入dataframe
        """
        sample_data = pd.DataFrame(self.ParameterArray, columns=self.name)
        sample_data.index=sample_data.index
        return sample_data
    
class Sampling(object):
    def __init__(self,parfile,exogfile):
        self.parfile=parfile
        self.exogfile=exogfile
    #
    """
    4  : Number of Parameters (the program only reads the first 4 parameters or any number indicated here)
    5  : number of simulations

    r__CN2.mgt	          -0.2       0.2
    v__ALPHA_BF.gw             0.0       1.0
    v__GW_DELAY.gw	           30.0      450.0
    v__GWQMN.gw                0.0       2.0

    r__SOL_AWC(1).sol________1      -0.2       0.1
    r__SOL_K(1).sol________1	-0.8       0.8
    r__SOL_BD(1).sol________1       -0.5       0.6
    a__ESCO.hru________1             0.0       0.2
    r__HRU_SLP.hru________1          0.0       0.2
    r__OV_N.hru________1            -0.2       0.0
    r__SLSUBBSN.hru________1         0.0       0.2
    a__GWQMN.gw________1             0.0      25.0
    a__GW_REVAP.gw________1         -0.1       0.0
    v__REVAPMN.gw________1           0.0      10.0
    """
    def readPar(self):
        par={}
        count=0
        with open(self.parfile) as fh:
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
        return par
    def PSO_FIR_SAM(self,par):
        # random_seed = 5201314
        random_seed = 5211314
        #random_seed = 5221314
        np.random.seed(random_seed)
        keys=[k for k in par if k!='par_num' and k!='sim_num']
        min_value=[]
        for k in keys:
            min_value.append(par[k]['min'])
        max_value=[]
        for k in keys:
            max_value.append(par[k]['max'])
        arr_limit = np.array([min_value,max_value]).T
        keys_=[]
        keys_no=[]
        arr_limit_=[]
        for i,k in zip(range(len(arr_limit)),keys):
            if arr_limit[i][0]==arr_limit[i][1]:
                keys_no.append(k)
            else:
                keys_.append(k)
                arr_limit_.append(arr_limit[i])
        bounds=np.array(arr_limit_)
        dimension=len(bounds)
        sample_size=par['sim_num']
        q= DoE_PSO(keys_, sample_size, dimension, bounds).write_to_dataframe()
        if keys_no is not None:
            for ki in keys_no:
                q[ki]=par[ki]['max']
        q.to_csv(self.exogfile)
        return q

if __name__ == "__main__":
    p=r'H:\U-SWAT'
    swatcup_parfile=os.path.join(p,'parfile_in.txt')
    exogfile=os.path.join(p,'LHS_exog_2.csv')
    PSO_Sample=Sampling(swatcup_parfile,exogfile)
    par=PSO_Sample.readPar()
    PSO_Sample.PSO_FIR_SAM(par)