# -*- coding: utf-8 -*-
"""
"""
import re
import os
import math
import random
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
from wc_sample import Sampling,DoE_PSO
from wc_global import *
from wc_lhs3 import LHS
from wc_swat import run_swat
from wc_evaluate import evaluate


class Prepare_Weight:
    def __init__(self, rankfile=None, fileinpar=None, modle=None):
        self.rankfile=rankfile
        self.fileinpar=fileinpar
        self.modle=modle
        inpar=Sampling(fileinpar,None).readPar()
        self.param_begin=[]
        for key in inpar:
            if re.match(r'[a-z]+__[0-9a-zA-Z_\(\)\{\},-]*.*',key):
                pp=re.findall(r'[a-z]+__([0-9a-zA-Z_\(\)\{\},-]*).*',key)[0]
                self.param_begin.append(pp)

    def param_rank(self):
        param_csv=pd.read_csv(self.rankfile)
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
        if self.modle.split('-')[0]=='TC':
            param_rank=param['ET']
        else:
            param_rank=param[self.modle.split('-')[0]]
        for i in self.param_begin:
            for j in param_rank:
                    if i == j:
                        param_end[i]=param_rank[j]
        return param_end


class PSO:
    def __init__(self, x, y, time, modle, v_low, v_high, rankfile=None, fileinpar=None):
        # 初始化
        self.time = time  # 迭代的代数        
        self.modle = modle   # 校准类型
        self.v_low = v_low
        self.v_high = v_high
        self.x_all = x  # 所有粒子的位置
        self.y = y  # 所有粒子的评价函数
        self.num = 0
        #
        self.rankfile=rankfile
        self.fileinpar=fileinpar
        #
        self.par=Sampling(self.fileinpar,None).readPar()
        keys=[k for k in self.par if k!='par_num' and k!='sim_num']
        min_value=[]
        for k in keys:
            min_value.append(self.par[k]['min'])
        max_value=[]
        for k in keys:
            max_value.append(self.par[k]['max'])
        arr_limit = np.array([min_value,max_value]).T
        self.keys_=[]
        self.keys_no=[]
        arr_limit_=[]
        for i,k in zip(range(len(arr_limit)),keys):
            if arr_limit[i][0]==arr_limit[i][1]:
                self.keys_no.append(k)
            else:
                self.keys_.append(k)
                arr_limit_.append(arr_limit[i])
        self.bound=np.array(arr_limit_)
        self.dimension=len(self.bound)
        self.sample_size=self.par['sim_num']
        #
        self.v = np.zeros((self.sample_size, self.dimension))  # 所有粒子的速度
        self.pe_best = np.zeros((self.sample_size, self.dimension))  # 每个粒子最优的位置
        self.pf_best = np.zeros((self.sample_size, self.dimension))  # 每个粒子最优的位置
        self.ps_best = np.zeros((self.sample_size, self.dimension))  # 每个粒子最优的位置
        self.pyf_best = np.zeros((self.sample_size,1)) # 局部最优的位置对应评价函数值(flow)
        self.pye_best = np.zeros((self.sample_size,1)) # 局部最优的位置对应评价函数值(ET)
        self.pys_best = np.zeros((self.sample_size,1)) # 局部最优的位置对应评价函数值(SW)
        self.ge_best = np.zeros((1, self.dimension))[0]  # 全局最优的位置
        self.gf_best = np.zeros((1, self.dimension))[0]  # 全局最优的位置
        self.gs_best = np.zeros((1, self.dimension))[0]  # 全局最优的位置
        self.gyf_best = float('-inf') # 全局最优的位置对应评价函数值(flow)
        self.gye_best = float('-inf') # 全局最优的位置对应评价函数值(ET)
        self.gys_best = float('-inf') # 全局最优的位置对应评价函数值(SW)
        self.best=[]
        #
        self.x=self.x_all[:,:self.dimension]
        # self.ux=self.x_all[:,self.dimension:]
        # 初始化第0代初始全局最优解
        temp = float('-inf')
        for i in range(self.x.shape[0]):
            for j in range(self.x.shape[1]):
                self.v[i][j] = random.uniform(self.bound[j][0], self.bound[j][1])
            if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC':
                self.pe_best[i] = self.x[i]  # 储存局部最优的个体
                self.pye_best[i] = self.y[i] # 储存局部最优的个体的评价函数
                fit = self.pye_best[i]
            elif self.modle.split('-')[0]=='flow':
                self.pf_best[i] = self.x[i]  # 储存局部最优的个体
                self.pyf_best[i] = self.y[i] # 储存局部最优的个体的评价函数
                fit = self.pyf_best[i]
            elif self.modle.split('-')[0]=='SW':
                self.ps_best[i] = self.x[i]  # 储存局部最优的个体
                self.pys_best[i] = self.y[i] # 储存局部最优的个体的评价函数
                fit = self.pys_best[i]
            # 做出修改
            if fit > temp:
                if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC':
                    self.ge_best = self.pe_best[i]
                    self.pe_best[i] = self.x[i]  # 储存局部最优的个体
                    self.gye_best = self.pye_best[i][0]
                elif self.modle.split('-')[0]=='flow':
                    self.gf_best = self.pf_best[i]
                    self.pf_best[i] = self.x[i]  # 储存局部最优的个体
                    self.gyf_best = self.pyf_best[i][0]
                elif self.modle.split('-')[0]=='SW':
                    self.gs_best = self.ps_best[i]
                    self.ps_best[i] = self.x[i]  # 储存局部最优的个体
                    self.gys_best = self.pys_best[i][0]
                temp = fit
        print('Initial Processing......')
        #

    def update_y(self, new_y):
        """
        更新粒子群的目标函数值 y。
        """
        self.y = new_y
        for i in range(self.x.shape[0]):
            self.y[i] = self.fitness(new_y[i])

    def update_m(self, new_modle):
        """
        更新率定的水文过程。
        """
        self.modle = new_modle

    def update_pre_y(self, new_y_):
        """
        更新粒子群的目标函数值 y。
        """
        self.pre_y = new_y_
        for i in range(self.x.shape[0]):
            self.pre_y[i] = self.fitness(new_y_[i])

                
    def fitness(self, y):
        """
        适应值计算
        """
        try:
            y = round(y,8)
        except:
            y = [round(y[0],8)]
        return y
    
    def pre_update(self,endog_out):
        temp = float('-inf')
        if self.gyf_best == float('-inf'):
            print('gyf_be')
            for i in range(self.x.shape[0]):
                if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC':
                    self.pe_best[i] = self.x[i].copy()  # 储存局部最优的个体
                    self.pye_best[i] = self.y[i].copy()  # 储存局部最优的个体的评价函数
                    fit = self.pye_best[i].copy() 
                    # pass
                elif self.modle.split('-')[0]=='flow':
                    self.pf_best[i] = self.x[i].copy()   # 储存局部最优的个体
                    self.pyf_best[i] = self.y[i].copy()  # 储存局部最优的个体的评价函数
                    fit = self.pyf_best[i].copy() 
                    if fit > temp:
                        self.gf_best = self.pf_best[i].copy() 
                        self.pf_best[i] = self.x[i].copy()   # 储存局部最优的个体
                        self.gyf_best = self.pyf_best[i][0].copy() 
                        temp = fit.copy() 
                elif self.modle.split('-')[0]=='SW':
                    self.ps_best[i] = self.x[i].copy()   # 储存局部最优的个体
                    self.pys_best[i] = self.y[i].copy()  # 储存局部最优的个体的评价函数
                    fit = self.pys_best[i].copy() 
        c1 = 1.5  # 学习因子
        c2 = 1.5
        p = 0.02
        w = list(Prepare_Weight(rankfile=self.rankfile,fileinpar=self.fileinpar,modle=self.modle).param_rank().values())
        # w=[1]*self.x.shape[1]
        # 自身权重因子
        for i in range(self.sample_size):
            # 更新速度(核心公式)
            for j in range(self.x.shape[1]):
                # 计算每个维度的步长
                if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC' or self.modle.split('-')[0]=='flow&ET':
                    delta_p = c1 * random.uniform(0, 0.5) * (self.pe_best[i, j] - self.x[i, j])
                    delta_g = c2 * random.uniform(0, 0.5) * (self.ge_best[j] - self.x[i, j])
                elif self.modle.split('-')[0]=='flow':
                    delta_p = c1 * random.uniform(0, 0.5) * (self.pf_best[i, j] - self.x[i, j])
                    delta_g = c2 * random.uniform(0, 0.5) * (self.gf_best[j] - self.x[i, j])
                # 应用步长
                self.v[i, j] = w[j] *(p* self.v[i, j] + delta_p + delta_g)
                # 应用步长
                # if re.match(r'[a-z]+__[0-9a-zA-Z_\(\)\{\},-]*.*',self.keys_[j]):
                #     nn=re.findall(r'[a-z]+__([0-9a-zA-Z_\(\)\{\},-]*).*',self.keys_[j])[0]
                # if nn in w.values():
                #     self.v[i, j] = w[nn] *(p* self.v[i, j] + delta_p + delta_g)
                # 速度限制
                if self.v[i, j] < self.v_low:
                    self.v[i, j] = self.v_low
                if self.v[i, j] > self.v_high:
                    self.v[i, j] = self.v_high
                #
                self.x[i][j] = self.x[i][j] + self.v[i][j]
                # 范围限制
                if self.x[i][j] < self.bound[j][0]:
                    self.x[i][j] = self.bound[j][0]
                if self.x[i][j] > self.bound[j][1]:
                    self.x[i][j] = self.bound[j][1]
            outcsv=pd.DataFrame(self.x, columns=self.keys_)
            if self.keys_no is not None:
                for ki in self.keys_no:
                    outcsv[ki]=self.par[ki]['max']
            outcsv.to_csv(endog_out)

    def update(self,exog_out_1,exog_out_2):
        g_best=[]
        for i in range(self.sample_size):
            if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC':
                try:
                    # print('kke')
                    # print(self.y[i],self.pye_best[i])
                    # print(self.pre_y[i],self.pyf_best[i])
                    if self.fitness(self.pre_y[i]) >= self.fitness(self.pyf_best[i]) and self.fitness(self.y[i]) >= self.fitness(self.pye_best[i]):
                        print('yes,ET change')
                        self.pe_best[i] = self.x[i]
                        self.pye_best[i]=self.y[i]
                        self.pyf_best[i]=self.pre_y[i]
                    else:
                        self.pe_best[i]=self.pf_best[i]
                        #  print(self.pe_best[i])
                        #  print(self.pf_best[i])
                        #  print(self.x[i])
                    # print(self.y[i],self.pye_best[i])
                    # print(self.pre_y[i],self.pyf_best[i])
                except:
                    print('et',i)
                    print(self.y[i],self.pye_best[i])
                    if self.fitness(self.y[i]) >= self.fitness(self.pye_best[i]):
                        self.pe_best[i] = self.x[i]
                        self.pye_best[i]=self.y[i]
                    else:
                        self.pe_best[i]=self.pe_best[i]
                        print(self.pe_best[i])
                    # print(self.y[i],self.pye_best[i])
                    # print('done')
                g_best.append(self.pe_best[i])
            elif self.modle.split('-')[0]=='flow':
                try:
                    # print('flow',i)
                    # print(self.y[i],self.pyf_best[i])
                    # print('et',i)
                    # print(self.pre_y[i],self.pye_best[i])
                    if self.fitness(self.y[i]) >= self.fitness(self.pyf_best[i]) and self.fitness(self.pre_y[i]) >= self.fitness(self.pye_best[i]):
                        print('yes,flow change')
                        self.pf_best[i] = self.x[i]
                        self.pyf_best[i]=self.y[i]
                        self.pye_best[i]=self.pre_y[i]
                    else:
                         self.pf_best[i]=self.pe_best[i]
                    #      print(self.pe_best[i])
                    #      print(self.pf_best[i])
                    #      print(self.x[i])
                    # print('ssss')
                    # print(self.y[i],self.pyf_best[i])
                    # print(self.pre_y[i],self.pye_best[i])
                except:
                    if self.fitness(self.y[i]) >= self.fitness(self.pyf_best[i]):
                        self.pf_best[i] = self.x[i]
                        self.pyf_best[i]=self.y[i]
                    else:
                        self.pf_best[i]=self.pe_best[i]
                        # print(self.pf_best[i])
                g_best.append(self.pf_best[i])
            elif self.modle.split('-')[0]=='SW':
                if self.fitness(self.y[i]) >= self.fitness(self.pys_best[i]):
                    self.ps_best[i] = self.x[i]
                    self.pys_best[i]=self.y[i]
                g_best.append(self.ps_best[i])
                
            if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC':
                try:
                    if self.fitness(self.y[i]) >= self.fitness(self.gye_best) and self.fitness(self.pre_y[i]) >= self.fitness(self.gyf_best):
                        self.ge_best = self.x[i]
                        self.gye_best=self.y[i]
                        self.gyf_best=self.pre_y[i]
                except:
                    if self.fitness(self.y[i]) >= self.fitness(self.gye_best):
                        self.ge_best = self.x[i]
                        self.gye_best=self.y[i]
            elif self.modle.split('-')[0]=='flow':
                try:
                    if self.fitness(self.y[i]) >= self.fitness(self.gyf_best) and self.fitness(self.pre_y[i]) >= self.fitness(self.gye_best):
                        self.gf_best = self.x[i]
                        self.gyf_best=self.y[i]
                        self.gye_best=self.pre_y[i]
                except:
                    if self.fitness(self.y[i]) >= self.fitness(self.gyf_best):
                        self.gf_best = self.x[i]
                        self.gyf_best=self.y[i]
            elif self.modle.split('-')[0]=='SW':
                if self.fitness(self.y[i]) >= self.fitness(self.gys_best):
                    self.gs_best = self.x[i]
                    self.gys_best=self.y[i]
        if self.modle.split('-')[0]=='ET' or self.modle.split('-')[0]=='TC':
            # try:
            #     self.pf_best=self.pe_best
            # except:
            #     pass
            self.x=self.pe_best.copy()
        elif self.modle.split('-')[0]=='flow':
            # try:
            #     self.pe_best=self.pf_best
            # except:
            #     pass
            self.x=self.pf_best.copy()
        elif self.modle.split('-')[0]=='SW':
            self.x=self.ps_best.copy()
        #
        outcsv=pd.DataFrame(g_best, columns=self.keys_)
        if self.keys_no is not None:
            for ki in self.keys_no:
                outcsv[ki]=self.par[ki]['max']
        outcsv.to_csv(exog_out_1)
        outcsv.to_csv(exog_out_2)
        return g_best


    # def pso(self,endog_out):
    #     self.final_ybest = 0.6
    #     for gen in range(self.time):
    #         pbest=self.update(endog_out)
    #         if self.fitness(self.gy_best) > self.final_ybest:
    #             self.final_best = self.g_best.copy()
    #         print('当前最佳位置：{}'.format(self.final_best))
    #         temp = self.gy_best
    #         print('当前的最佳适应度：{}'.format(temp))
    #         self.best.append(temp)
    #     self.num=self.num+1
    #     # t = [i for i in range(self.num)]
    #     print(self.best)
    #     return self.best[-1],pbest
    
    def pic(self):
        t = [i for i in range(self.num)]
        plt.figure()
        plt.grid(axis='both')
        plt.plot(t, self.best, color='red', marker='.', ms=10)
        plt.rcParams['axes.unicode_minus'] = False
        plt.margins(0)
        plt.xlabel(u"迭代次数")  # X轴标签
        plt.ylabel(u"适应度")  # Y轴标签
        plt.title(u"迭代过程")  # 标题
        plt.show()

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
    
    swatcup_parfile=os.path.join(swatcup_parfile_path,'parfile_in.txt')
    indicator_=['r_square','kge','r_square','kge','r_square','kge','r_square','kge']
    module_=['TC-SUB-Mon','flow-SUB-Mon','TC-SUB-Mon','flow-SUB-Mon','TC-SUB-Mon','flow-SUB-Mon','TC-SUB-Mon','flow-SUB-Mon']
    iter_a = [] 
    para = []
    iter_b = []
    v_low = -1000
    v_high = 1000
    time = 1
    for ii,cp in enumerate(range(loop)): 
        indicator=indicator_[ii]
        modle=module_[ii]
        #MC
        exog_file=os.path.join(PSO_path,exogfile%(cp+1))
        if cp == 0:
            PSO_Sample=Sampling(swatcup_parfile,exog_file)
            par=PSO_Sample.readPar()
            PSO_Sample.PSO_FIR_SAM(par)
        #swat
        #评价指标
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
        endog_file=os.path.join(PSO_path,endogfile%(cp+1))
        evaluate( modle, begin_date, end_date, begin_date2, end_date2, pro_num=cache_num , obvdir=obvdir, simdir=simdir, rchdict=rch_dict, subdict=sub_dict, weight=weight, endogfile=endog_file)
        # df.to_csv(endog_file, encoding="utf-8")
        endtime2 = datetime.datetime.now()
        print (endtime2 - starttime2)
        #optimize
        starttime3 = datetime.datetime.now()
        eval_para=pd.read_csv(endog_file,index_col=0)
        eval_para=eval_para[indicator].values
        y = eval_para.copy()
        fir_para=pd.read_csv(exog_file,index_col=0)
        fir_para=fir_para.values
        x = fir_para.copy()
        if cp == 0:
            fir_para=pd.read_csv(exog_file,index_col=0)
            fir_para=fir_para.values
            x = fir_para.copy()
            pp=PSO(x, y, time, modle, v_low, v_high, rankfile=rankfile, fileinpar=swatcup_parfile)
            pp.pre_update(os.path.join(PSO_path,exogfile%(cp+2)))
            csv=pd.read_csv(os.path.join(PSO_path,exogfile%(cp+2)),index_col=0)
            simulations=csv.to_dict(orient ='records')
            outputpath=os.path.join(output_path,'C_iter%d'%(cp+1))
            simdir={'flow':outputpath,'ET':outputpath,'SW':outputpath,'TC':outputpath}
            run_swat(simulations,templatefile_path,outputpath=outputpath,cachepath=cache_path,cachenum=cache_num,clean=False,prefix=cache_prefix)
            endog_file=os.path.join(C_PSO_path,endogfile%(cp+1))
            evaluate( modle, begin_date, end_date, begin_date2, end_date2, pro_num=cache_num , obvdir=obvdir, simdir=simdir, rchdict=rch_dict, subdict=sub_dict, weight=weight, endogfile=endog_file)
            eval_para=pd.read_csv(endog_file,index_col=0)
            eval_para=eval_para[indicator].values
            y_ = eval_para.copy()
            pp.update_y(y_)
            pp.update(os.path.join(PSO_path,exogfile%(cp+2)),os.path.join(C_PSO_path,exogfile%(cp+2)))
        else:
            pp.update_m(modle)
            pp.update_y(y)
            pp.pre_update(os.path.join(PSO_path,exogfile%(cp+2)))
            csv=pd.read_csv(os.path.join(PSO_path,exogfile%(cp+2)),index_col=0)
            simulations=csv.to_dict(orient ='records')
            outputpath=os.path.join(output_path,'C_iter%d'%(cp+1))
            simdir={'flow':outputpath,'ET':outputpath,'SW':outputpath,'TC':outputpath}
            run_swat(simulations,templatefile_path,outputpath=outputpath,cachepath=cache_path,cachenum=cache_num,clean=False,prefix=cache_prefix)
            endog_file=os.path.join(C_PSO_path,endogfile%(cp+1))
            evaluate( modle, begin_date, end_date, begin_date2, end_date2, pro_num=cache_num , obvdir=obvdir, simdir=simdir, rchdict=rch_dict, subdict=sub_dict, weight=weight, endogfile=endog_file)
            eval_para=pd.read_csv(endog_file,index_col=0)
            eval_para=eval_para[indicator].values
            y_ = eval_para.copy()
            pp.update_y(y_)
            endog_file=os.path.join(P_PSO_path,endogfile%(cp+1))
            modle_ = module_[ii-1]
            evaluate(modle_, begin_date, end_date, begin_date2, end_date2, pro_num=cache_num , obvdir=obvdir, simdir=simdir, rchdict=rch_dict, subdict=sub_dict, weight=weight, endogfile=endog_file)
            eval_para=pd.read_csv(endog_file,index_col=0)
            eval_para=eval_para[indicator_[ii-1]].values
            y_ = eval_para.copy()
            pp.update_pre_y(y_)
            pp.update(os.path.join(PSO_path,exogfile%(cp+2)),os.path.join(C_PSO_path,exogfile%(cp+2)))
            # optimize(file_inpar0,file_inpar,file_outpar,file_exog,file_endog,param_file,modle=modle,y=indicator,simnum=simulation_num)
        endtime3 = datetime.datetime.now()
        print (endtime3 - starttime3)
        print (endtime3 - starttime1)
        print ('********FINISH**********')