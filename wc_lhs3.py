import numpy as np
import random
import pandas as pd
import os
import re
from wc_global import *
'''
该文件目的是：
1.接收到一组变量范围numpy矩阵以及样本需求个数，shape = (m,2)，输出样本numpy矩阵
执行ParameterArray函数即可
'''
def Partition (number_of_sample,limit_array):
    """
    为各变量的变量区间按样本数量进行划分，返回划分后的各变量区间矩阵
    :param number_of_sample: 需要输出的 样本数量
    :param limit_array: 所有变量范围组成的矩阵,为(m, 2)矩阵，m为变量个数，2代表上限和下限
    :return: 返回划分后的个变量区间矩阵（三维矩阵），三维矩阵每层对应于1个变量
    """
    coefficient_lower = np.zeros((number_of_sample, 2))
    coefficient_upper = np.zeros((number_of_sample, 2))
    for i in range(number_of_sample):
        coefficient_lower[i, 0] = 1 - i / number_of_sample
        coefficient_lower[i, 1] = i / number_of_sample
    for i in range(number_of_sample):
        coefficient_upper[i, 0] = 1-(i+1) / number_of_sample
        coefficient_upper[i, 1] = (i+1) / number_of_sample

    partition_lower = coefficient_lower @ limit_array.T  #变量区间下限
    partition_upper = coefficient_upper @ limit_array.T  # 变量区间上限

    partition_range = np.dstack((partition_lower.T, partition_upper.T))  # 得到各变量的区间划分，三维矩阵每层对应于1个变量
    return partition_range #返回区间划分上下限

def Representative(partition_range):
    """
    计算单个随机代表数的函数
    :param partition_range: 一个shape为 (m,N,2) 的三维矩阵，m为变量个数、n为样本个数、2代表区间上下限的两列
    :return: 返回由各变量分区后区间随机代表数组成的矩阵，每列代表一个变量
    """
    number_of_value = partition_range.shape[0]  #获得变量个数
    numbers_of_row = partition_range.shape[1]  # 获得区间/分层个数
    coefficient_random = np.zeros((number_of_value,numbers_of_row, 2))  # 创建随机系数矩阵
    representative_random = np.zeros((numbers_of_row, number_of_value))

    for m in range(number_of_value):
        for i in range(numbers_of_row):
            y = random.random()
            coefficient_random[m,i, 0] = 1 - y
            coefficient_random[m,i, 1] = y

    temp_arr = partition_range * coefficient_random  # 利用*乘实现公式计算（对应位置进行乘积计算），计算结果保存于临时矩阵 temp_arr 中
    for j in range(number_of_value): #计算每个变量各区间内的随机代表数，行数为样本个数n，列数为变量个数m
        temp_random = temp_arr[j, :, 0] + temp_arr[j, :, 1]
        representative_random[:,j] = temp_random
    return representative_random  # 返回代表数向量

def Rearrange(arr_random):
    """
    打乱矩阵各列内的数据
    :param arr_random: 一个N行, m列的矩阵
    :return: 每列打乱后的矩阵
    """
    for i in range(arr_random.shape[1]):
        np.random.shuffle(arr_random[:, i])
    return arr_random



def ParameterArray(limitArray,
                   sampleNumber):
    """
    根据输入的各变量的范围矩阵以及希望得到的样本数量，输出样本参数矩阵
    :param limitArray:变量上下限矩阵，shape为(m,2),m为变量个数
    :param sampleNumber:希望输出的 样本数量
    :return:样本参数矩阵
    """
    arr = Partition(sampleNumber, limitArray)
    parametersMatrix = Rearrange(Representative(arr))
    return  parametersMatrix


'''以下为类创建'''

class DoE(object):
    def __init__(self, name_value, bounds):
        self.name = name_value
        self.bounds = bounds
        self.type = "DoE"
        self.result = None


class DoE_LHS(DoE):
    # 拉丁超立方试验样本生成
    def __init__(self, name_value, bounds, N):
        DoE.__init__(self, name_value, bounds)
        self.type = "LHS"
        self.ParameterArray = ParameterArray(bounds , N)
        self.N = N
    
    # def insert(self,df, i, df_add):
    #     # 指定第i行插入一行数据
    #     df1 = df.iloc[:i, :]
    #     df2 = df.iloc[i:, :]
    #     df_new = pd.concat([df1, df_add, df2], ignore_index=True)
    #     return df_new
    
    # def pandas(self):
    #     data_ = pd.DataFrame(self.ParameterArray, columns=self.name)
    #     add={}
    #     for i in range(len(self.name)):
    #         add.update({self.name[i]:[str(self.bounds.tolist()[i])]})
    #     df_add = pd.DataFrame(add)
    #     data = self.insert(data_, 0, df_add)
    #     data.to_csv("LHS.csv")
    #     print(data,'输出文件csv')
    #     return data


    def write_to_csv(self,exogfile):
        """
        将样本数据写入LHS.csv文件，文件保存至运行文件夹内
        """
        sample_data = pd.DataFrame(self.ParameterArray, columns=self.name)
        sample_data.index=sample_data.index+1
        sample_data.to_csv(exogfile)
        print(sample_data,'输出文件csv')
    def write_to_dataframe(self):
        """
        将样本数据写入dataframe
        """
        sample_data = pd.DataFrame(self.ParameterArray, columns=self.name)
        sample_data.index=sample_data.index+1
        return sample_data



class LHS(object):
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
        # print(par)
        return par
    #
    def lhs(self,par):
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
        arr_limit_=np.array(arr_limit_)
        q= DoE_LHS(N=par['sim_num'], bounds=arr_limit_, name_value=keys_).write_to_dataframe()
        if keys_no is not None:
            for ki in keys_no:
                q[ki]=par[ki]['max']
        q.to_csv(self.exogfile)
        return q
    #
    def run(self):
        par=self.readPar()
        self.lhs(par)

if __name__ == "__main__":
    # iterpath=r'/home/junli/wangchen/swat/LHSandSUFI'
    p=r'D:\new_method_output\parfile'
    swatcup_parfile=os.path.join(p,'parfile_in.txt')
    exogfile=os.path.join(LHS_path,'LHS_exog_2.csv')
    lhs=LHS(swatcup_parfile,exogfile)
    lq=lhs.run()
    print(lq)