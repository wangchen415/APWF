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
import numpy as np
from numpy import append
from numpy import hsplit
from pip import main
# from wc_best_par import *
from wc_mgt import HRU_MGT
from wc_sol import HRU_SOL
from wc_hru import HRU_HRU
from wc_gw import HRU_GW
from wc_rte import HRU_RTE
from wc_bsn import HRU_BSN
from wc_global import *
from wc_simulation import *

###############

class COPY(object):
    def __init__(self,src_dir,dst_dir):
        self.src_dir=src_dir
        self.dst_dir=dst_dir
    def mycopyfile(self,src_dir,dst_dir):
        #self.ext=['*.exe','*.lid','*.pnd','*.rte','*.sub','*.swq','*.wgn','*.wus','*.chm','*.sdr','*.sep','*.ATM','*.bsn','*.wwq','*.out','*.deg','*.cst','*.dat','*.fig','*.cio','*.fin','*.hud','*.std','*.sub','*.swr','*.txt','*.pcp','*.ini','*.out','*.slr','*.qst','*.sqlite','*.Tmp','*.wnd','output*']
        dst_dirlist=[]
        for filename in os.listdir(dst_dir):
            dst_dirlist.append(filename)
        for copyfilename in os.listdir(src_dir):
            if copyfilename not in dst_dirlist:
                try:
                    shutil.copy(src_dir + "/"+str(copyfilename), dst_dir + "/"+str(copyfilename))
                except:
                    shutil.copytree(src_dir + "/"+str(copyfilename), dst_dir + "/"+str(copyfilename))
        # fnamelist=[]
        # for i in self.ext:                 
        #     fnamelist_tem=glob.glob(os.path.join(src_dir,'%s'%i))
        #     if len(fnamelist_tem) !=0:
        #         for j in fnamelist_tem:
        #             fnamelist.append(os.path.split(j)[1])
        #             print(fnamelist)
        #             for fname in list(fnamelist):                   
        #                 shutil.copy(src_dir + "/"+str(fname), dst_dir + "/"+str(fname))          
        #                 #print ("copy %s -> %s"%(src_dir, dst_dir + fname))
    def run(self):
        self.mycopyfile(self.src_dir,self.dst_dir)


####调试
class swatsup(object):
    def __init__(self,swatpath,outputpath,no):
        self.swatpath=swatpath
        self.outputpath=outputpath
        self.no=no
    def run(self):
        main = self.swatpath+"/swat.exe"
        print(self.swatpath)
        f=subprocess.Popen(["wine",main],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=self.swatpath) 
        f.wait()
        output = re.sub(r'\r\n','\n',f.stdout.read().decode())
        print(output)
        if f.returncode == 0:
            #把output.sub拷贝到filepath（新文件）
            filename1='output_%03d.sub'%(self.no)
            filepath1=os.path.join(self.outputpath,filename1)
            filename2='output_%03d.rch'%(self.no)
            filepath2=os.path.join(self.outputpath,filename2)
            filename3='output_%03d.hru'%(self.no)
            filepath3=os.path.join(self.outputpath,filename3)
            filename4='output_%03d.swr'%(self.no)
            filepath4=os.path.join(self.outputpath,filename4)
            shutil.copy(os.path.join(self.swatpath,'output.sub'), filepath1)
            shutil.copy(os.path.join(self.swatpath,'output.rch'), filepath2)
            shutil.copy(os.path.join(self.swatpath,'output.hru'), filepath3)
            try:
                shutil.copy(os.path.join(self.swatpath,'output.swr'), filepath4)
            except Exception as e:
                print('Did not chose .swr file')
            output += '\nSubprogram success'
        else:
            output += '\nSubprogram failed'
        return output


def swat_cache(cachenum,cachepath,templatefilepath,clean=False,prefix='swat_cache'):
    filepath=os.path.join(cachepath,'%s.json'%(prefix))
    flag=False
    dic=None
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8')as fp:
            dic = json.load(fp)
            if len(dic)==cachenum:
                flag=True
    if clean==True:
        if dic is not None:
            for k in dic:
                if os.path.exists(dic[k]):
                    shutil.rmtree(dic[k])
        flag=False
    if flag==False:
        dic={}
        print('caching...',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
        for n in range(cachenum):
            print(n,'copying...')
            # n=1
            # cachepath=r'G:\swap'
            tmpdir=os.path.join(cachepath,'%s%03d'%(prefix,n+1))
            if not os.path.exists(tmpdir):
                os.makedirs(os.path.join(cachepath,'%s%03d'%(prefix,n+1)))
            copy=COPY(templatefilepath,tmpdir)
            copy.run()
            # tmpath=os.path.split(tmpdir.name)[-1]
            dic['%s%03d'%(prefix,n+1)]=tmpdir
        print(cachenum,'cached',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
        # new_data = json.loads(str(dic).replace("'", "\""))
        with open(filepath,'w',encoding='utf-8') as f2:
            # ensure_ascii=False才能输入中文，否则是Unicode字符
            # indent=2 JSON数据的缩进，美观
            json.dump(dic,f2,ensure_ascii=False,indent=2)
    return dic



def swat_plan(simulations,templatefilepath,cachenum=10,cachepath=r'G:\swap',clean=False,prefix='swat_cache'):
    cache_dic=swat_cache(cachenum,cachepath,templatefilepath,clean=clean,prefix=prefix)
    # print(len(cache_dic))
    # print(cachenum)
    solution_dic={}
    cp=0
    for i in range(0,len(simulations),cachenum):
        # print(i,'xunhuan')
        start=i
        if i+cachenum<len(simulations):
            end=i+cachenum
        else:
            end=len(simulations)
        #
        # print(start,end)
        if solution_dic.get(cp,None) is None:
            solution_dic[cp]=[]
        for j in range(start,end):
            solution_dic[cp].append([j,simulations[j],cache_dic['%s%03d'%(prefix,j-start+1)]])
        cp=cp+1
    # print(len(solution_dic),'wwwwwwwww')
    return solution_dic

def swat_run(swatpath,outputpath,i):
    swat=swatsup(swatpath,outputpath,i)
    swat.run()
    # print(swat.run())

from multiprocessing import Pool


def swat_multiprocess(simulations,templatefilepath,outputpath):
    print('process initializing',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
    obj=SWATCUPRule()
    for i,simulation,swatpath in simulations:
        print(i,'transforming...')
        obj.simulate(i,simulation,swatpath,templatefilepath)
    print('process initialized',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
    #
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    #分配进程，时间维度上每个时间的空间数组占一个进程
    jobs = []
    print('process starting',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
    for i,solution,swatpath in simulations:
        p = multiprocessing.Process(target=swat_run, args=(swatpath,outputpath,i))
        jobs.append(p)
        p.start()
        print(i,"start ...")
    for proc in jobs:
        proc.join()
        print("join ...", proc.name, proc._identity)
    #
    # pool=Pool(len(solutions))
    # print('process starting',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
    # for i,solution,swatpath in solutions:
    #     # solution=solutions[i]
    #     # print(i,solution)
    #     pool.apply_async(func=swat_run, args=(swatpath,outputpath,i))
    # pool.close()
    # print("start ...")
    # pool.join()
    #
    # print('process done',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))



def run_swat(simulations,templatefilepath,outputpath=r'G:\swap\iter1',cachenum=10,cachepath=r'/home/junli/wangchen/swat',clean=True,prefix='swat_cache'):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    #
    solution_dic=swat_plan(simulations,templatefilepath,cachenum=cachenum,cachepath=cachepath,clean=clean,prefix=prefix)
    # print(len(solution_dic),'sdasfaefadfdfe')
    for k in solution_dic:
        print(k,'batch starting',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))
        swat_multiprocess(solution_dic[k],templatefilepath,outputpath)
        # print(len(solution_dic[k]),templatefilepath,outputpath)
        # print(k,'batch done',datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H:%M:%S'))


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    # basedir = r'/home/junli/wangchen/swat/python/input/txtinout'
    # filename = 'tttt_wc.txt'
    # z={20:'HongDe',58:'JiaQiao',63:'QingYang',94:'NingXian',95:'YuLuoPing'}
    # templatefilepath=r'/home/junli/wangchen/swat/wangchen.Sufi2.SwatCup/Backup'
    # csv_dir=r'/home/junli/wangchen/swat/水文站点new'
    # outputpath=r'/home/junli/wangchen/swat/iter1'
    # cachepath=r'/home/junli/wangchen/swat/cache'
    # iterpath=r'/home/junli/wangchen/swat/LHSandSUFI'
    # LHSpath=r'/home/junli/wangchen/swat/LHS'
    # SUFIpath=r'/home/junli/wangchen/swat/SUFI'
    exogfile=os.path.join(LHS_path,'LHS_exog_2.csv')
    csv=pd.read_csv(exogfile,index_col=0)
    simulations=csv.to_dict(orient ='records')
    cp=2
    outputpath=os.path.join(output_path,'iter%d'%(cp))
    run_swat(simulations,templatefile_path,outputpath=outputpath,cachepath=cache_path,cachenum=cache_num,clean=False,prefix=cache_prefix)
    endtime = datetime.datetime.now()
    # print (endtime - starttime)






        
        

            





"""
r__CN2.mgt________1	        -0.2       0.2
r__SOL_AWC(1).sol________1      -0.2       0.1
r__SOL_K(1).sol________1	-0.8       0.8
r__SOL_BD(1).sol________1       -0.5       0.6
a__GWQMN.gw________1             0.0      25.0
a__GW_REVAP.gw________1         -0.1       0.0
v__REVAPMN.gw________1           0.0      10.0
a__ESCO.hru________1             0.0       0.2
r__HRU_SLP.hru________1          0.0       0.2
r__OV_N.hru________1            -0.2       0.0
r__SLSUBBSN.hru________1         0.0       0.2



r__CN2.mgt________3-6	          -0.2       0.2
r__SOL_AWC(1).sol________3-6      -0.2       0.1
r__SOL_K(1).sol________3-6	  -0.8       0.8
r__SOL_BD(1).sol________3-6       -0.5       0.6
a__GWQMN.gw________3-6             0.0      25.0
a__GW_REVAP.gw________3-6         -0.1       0.0
v__REVAPMN.gw________3-6           0.0      10.0
a__ESCO.hru________3-6             0.0       0.2
r__HRU_SLP.hru________3-6          0.0       0.2
r__OV_N.hru________3-6            -0.2       0.0
r__SLSUBBSN.hru________3-6         0.0       0.2

r__CN2.mgt________7,12,15,16-20	          -0.2       0.2
r__SOL_AWC(1).sol________7,12,15,16-20     -0.2       0.1
r__SOL_K(1).sol________7,12,15,16-20	  -0.8       0.8
r__SOL_BD(1).sol________7,12,15,16-20      -0.5       0.6
a__GWQMN.gw________7,12,15,16-20            0.0      25.0
a__GW_REVAP.gw________7,12,15,16-20        -0.1       0.0
v__REVAPMN.gw________7,12,15,16-20          0.0       10.0
a__ESCO.hru________7,12,15,16-20            0.0       0.2
r__HRU_SLP.hru________7,12,15,16-20         0.0       0.2
r__OV_N.hru________7,12,15,16-20           -0.2       0.0
r__SLSUBBSN.hru________7,12,15,16-20        0.0       0.2
"""