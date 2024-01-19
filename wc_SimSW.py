import pandas as pd
import os
import re
import glob
import numpy as np
import datetime,calendar


def mergebymonth(flow):  
    merge=flow
    merge['DAY']= merge['DAY'].str.slice(0,7)
    mean_mon=merge.groupby(merge['DAY'],as_index=False).mean()
    return mean_mon
day8 = None
class SimSW(object):
    def __init__(self,parfile,subdict,begin_date,end_date,modle):
        self.parfile=parfile
        self.subdict=subdict
        self.begin_date=begin_date
        self.end_date=end_date
        self.modle=modle

    def mysub_day(self):
        colspecs = [(0, 5), (5, 11), (11, 21), (21, 34), (34, 46), (46, 58), (58, 70), (70, 82), (82, 94), (94, 106), (106, 118), (118, 130), (130, 142)]
        col_names = ['Day', 'HRU', 'GIS', 'Layer1', 'Layer2', 'Layer3', 'Layer4', 'Layer5', 'Layer6', 'Layer7', 'Layer8', 'Layer9', 'Layer10']
        chunksize = 10000
        chunks = []
        for chunk in pd.read_fwf(self.parfile, colspecs=colspecs, names=col_names, skiprows=3,chunksize=chunksize):
            chunks.append(chunk)
        tab = pd.concat(chunks, axis=0)
        # tab = tab.dropna(axis=1, how='all')
        # tab = pd.read_fwf(self.parfile, widths=col_widths, skiprows=9, names=col_names)
        tab['HRU'] = tab['HRU'].astype(int)
        day = pd.date_range(start=self.begin_date, end=self.end_date).strftime('%Y-%m-%d').tolist()
        subes = tab['HRU'].unique()
        outsub = {i: tab.loc[tab['HRU'] == i].copy() for i in subes}
        sub = {i: outsub[i].assign(DAY=day) for i in self.subdict}
        # sub = {j: outsub[j].set_index('DAY') for j in self.subdict.keys()}
        return sub

    def getsw_days(self,begin_date,end_date):
        sub=self.mysub_day()
        
        begin_date = pd.to_datetime(begin_date)
        end_date = pd.to_datetime(end_date)
        for k, df in sub.items():
            if 'DAY' not in df.columns:
                print(f"Key 'DAY' not found in dataframe for key {k}")
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)].dropna(axis=1, how='all') for k, df in sub.items()}
        return sub_

    def getsw_8days(self,begin_date,end_date):
        sub=self.mysub_day()
        global day8
        begin_year=int(begin_date[:4])
        end_year=int(end_date[:4])
        if day8 is None:
            #  
            day8=[]
            for y in range(begin_year,end_year+1):
                s=datetime.datetime.strptime('%d-12-31'%(y),'%Y-%m-%d')
                day=datetime.datetime.strftime(s,'%j')
                for d in range(0,int(day)):
                #    print(datetime.datetime.strptime('2008%d'%(d+1),'%Y%j')) 
                    dd=8*(d//8)+1 
                    tmp=datetime.datetime.strptime('%d%d'%(y,dd),'%Y%j')
                    day8.append(datetime.datetime.strftime(tmp,'%Y-%m-%d'))
        #
        sub_={}
        for k in sub:
            tmp=sub[k]['DAY'].apply(lambda df: df[0:4]>=str(begin_year))
            tmpsub=sub[k][tmp]
            tmp=tmpsub['DAY'].apply(lambda df: df[0:4]<=str(end_year))
            sub_[k]=tmpsub[tmp]
            sub_[k]['GRP']=day8
            cols_to_sum = ['Layer1', 'Layer2', 'Layer3', 'Layer4', 'Layer5', 'Layer6', 'Layer7', 'Layer8', 'Layer9', 'Layer10']
            sub_[k]=sub_[k].groupby(by=["GRP"])[cols_to_sum].last()
            sub_[k]['DAY']=sub_[k].index
            sub_[k]=sub_[k][pd.to_datetime(sub_[k]['DAY']).between(begin_date, end_date)]
            sub_[k] = sub_[k].dropna(axis=1, how='all')
        return sub_ 

    def getsw_month(self, begin_date, end_date):
        sub = self.mysub_day()
        sub_={}
        for k in sub:
            sub_[k]=sub[k].groupby(by=sub[k]['DAY'].astype(str).str[:7],dropna=True,group_keys=False,).last()
            sub_[k]['DAY']=sub_[k].index
            sub_[k]=sub_[k][pd.to_datetime(sub_[k]['DAY']).between(begin_date, end_date)]
            sub_[k] = sub_[k].dropna(axis=1, how='all')
            # begin_year=int(begin_date[:4])
            # end_year=int(end_date[:4])
            # tmp=sub[k]['DAY'].apply(lambda df: df[0:4]>=str(begin_year))
            # tmpsub=sub[k][tmp]
            # tmp=tmpsub['DAY'].apply(lambda df: df[0:4]<=str(end_year))
            # sub_[k]=tmpsub[tmp]
            # cols_to_sum = ['Layer1', 'Layer2', 'Layer3', 'Layer4', 'Layer5', 'Layer6', 'Layer7', 'Layer8', 'Layer9', 'Layer10']
            # sub_[k]=sub_[k].groupby(by=["GRP"])[cols_to_sum].last()
            # sub_[k]['DAY']=sub_[k].index
            # print(sub_[k])
            # sub_[k]=sub_[k][pd.to_datetime(sub_[k]['DAY']).between(begin_date, end_date)]
        return sub_

if __name__=='__main__':
    modle='SW-HRU'
    subdict={20:'HongDe',49:'JiaQiao',54:'QingYang',84:'NingXian',85:'YuLuoPing'}
    begin_date='2009-01-01'
    end_date='2009-12-31'
    begin_date2='2009-01-01'
    end_date2='2009-10-20'
    file=r'D:\output.swr'
    SW=SimSW(file,subdict,begin_date,end_date,modle).getsw_days(begin_date2,end_date2)