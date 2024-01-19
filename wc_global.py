import re
import os
#全局路径-输入数据
#arcswat生成的hru文件
templatefile_path='/home/song/wangchen/PSO/TxtInOut'
#swat-cup参数模板配置文件
swatcup_parfile_path='/home/song/wangchen/PSO/input/parfile'
#水文数据excel文件
flow_path='/home/song/wangchen/PSO/input/水文站点'
#遥感文件weight=None
remotesensing_path='/home/song/wangchen/PSO/input/RS'
ETfile='data_pmlv2_86.csv'
#TC分析
ETfile_1='data_pmlv2_86.csv'
ETfile_2='data_glass_86.csv'
SWfilelist=None
TCfilelist='%s;%s'%(os.path.join(remotesensing_path,ETfile_1),os.path.join(remotesensing_path,ETfile_2))
TCfilelist=[os.path.join(remotesensing_path,ETfile_1),os.path.join(remotesensing_path,ETfile_2)]
obvdir={'flow':flow_path,'ET':os.path.join(remotesensing_path,ETfile),'SW':SWfilelist,'TC':TCfilelist}
#全局路径-输出数据
#swat运行结果
output_path='/home/song/wangchen/PSO/output/TC'
#MC+PSO采样方案simulation及方案评价结果
# PSO_path='/home/song/wangchen/PSO/output2/Flow_and_GLASS/parameter'
PSO_path='/home/song/wangchen/PSO/output/TC/parameter/evaluation'
exogfile='PSO_exog_%d.csv'
endogfile='PSO_endog_%d.csv'
C_PSO_path='/home/song/wangchen/PSO/output/TC/parameter/Compara'
P_PSO_path='/home/song/wangchen/PSO/output/TC/parameter/Prior'
#多进程swat
#simulation数目，注意与swat-cup parfile定义相同,方案数目必须大于参数数目
simulation_num=500
#定义多线程临时工作路径
cache_num=50
cache_prefix='cache_pso'
#多线程临时工作路径
cache_path='/home/song/wangchen/PSO/Cache'

#swat调参
#评价时流量和ET的占比（前者为流量，后者为ET）;normal表示按照权重平均分配，area表示按照子流域面积大小分配
weight={'SW':0.5,'ET':0.5,'flow':0.5}
#threshold=0.5
#r_square
#评估河段、子流域
#49:'JiaQiao',54:'QingYang',85:'NingXian',86:'YuLuoPing'
rch_dict={49:'JiaQiao'}
# rch_dict={54:'QingYang'}
# sub_dict={1:''}
#
# subnum=86
# sub_dict={}
# for i  in range(1,subnum+1):
#     sub_dict[i]=(" ")
# sub='1-6,11-16,21-22,24-28,31-35,38-44,47-51,54-57,59-60,63'86-87,94
sub='20-21,27-28,36-37,43-44,49'
# sub = '1-19,22-26,29-35,38-42,45-48,50-51,54'
tmp=re.findall('([0-9\-\,]*)?',sub)
if tmp[0]=='':
    subbsn=None
else:
    sub_dict={}
for num in tmp[0].split(','):
    if num.isdigit():
        sub_dict[int(num)]=(" ")
    else:
        lb,ub=num.split('-')
        for i in range(int(lb),int(ub)+1):
            sub_dict[int(i)]=(" ")
print(sub_dict)
#
# hru_dict={54:'QingYang'}
#数据时间段
begin_date='2008-01-01'
end_date='2018-12-31'
#评估时间段
begin_date2='2010-01-01'
end_date2='2018-12-31'
#迭代次数
loop=8
# #调试类型
# modle='flow-calibration-Mon'
rankfile='/home/song/wangchen/PSO/input/rank.csv'

weight=None