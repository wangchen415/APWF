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
class SimFlow(object):
    def __init__(self,parfile,subdict,begin_date,end_date,modle):
        self.parfile=parfile
        self.subdict=subdict
        self.begin_date=begin_date
        self.end_date=end_date
        self.modle=modle
    def getEveryDay(self):
        return pd.date_range(start=self.begin_date, end=self.end_date).strftime('%Y-%m-%d').tolist()

    def mysub_day(self):
        dtype_dict = {
            'SUB': np.str_,'GIS': np.float16,'MON': np.int16,'AREA': np.float16,'FLOW_IN': np.float16,'FLOW_OUT': np.float16
        }
        col_names = ['SUB', 'GIS', 'MON', 'AREA', 'FLOW_IN', 'FLOW_OUT']
        col_specs = [(0, 11), (12, 20), (21, 26), (26, 38), (38, 50), (50, 62)]
        chunksize = 10000
        chunks = []
        for chunk in pd.read_fwf(self.parfile, colspecs=col_specs, skiprows=9, names=col_names, chunksize=chunksize, dtype=dtype_dict,na_values=['*******']):
            chunks.append(chunk)
        tab = pd.concat(chunks, axis=0)
        # tab = pd.read_fwf(self.parfile, widths=col_widths, skiprows=9, names=col_names)
        tab['SUB'] = tab['SUB'].apply(lambda x: re.findall('[A-Z]+\s*(\d+)', x)[0]).astype(int)
        day = pd.date_range(start=self.begin_date, end=self.end_date).strftime('%Y-%m-%d').tolist()
        subes = tab['SUB'].unique()
        outsub = {i: tab.loc[tab['SUB'] == i].copy() for i in subes}
        sub = {i: outsub[i].assign(DAY=day) for i in self.subdict}
        # sub = {j: outsub[j].set_index('DAY') for j in self.subdict.keys()}
        return sub

    def getflow_days(self,begin_date,end_date):
        sub=self.mysub_day()
        begin_date = pd.to_datetime(begin_date)
        end_date = pd.to_datetime(end_date)
        for k, df in sub.items():
            if 'DAY' not in df.columns:
                print(f"Key 'DAY' not found in dataframe for key {k}")
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        return sub_

    def getflow_8days(self,begin_date,end_date):
        sub=self.mysub_day()
        global day8
        begin_date=int(begin_date[:4])
        end_date=int(end_date[:4])
        if day8 is None:
            #  
            day8=[]
            for y in range(begin_date,end_date+1):
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
            tmp=sub[k]['DAY'].apply(lambda df: df[0:4]>=str(begin_date))
            tmpsub=sub[k][tmp]
            tmp=tmpsub['DAY'].apply(lambda df: df[0:4]<=str(end_date))
            sub_[k]=tmpsub[tmp]
            sub_[k]['GRP']=day8
            cols_to_sum = ['FLOW_OUT']
            sub_[k]=sub_[k].groupby(by=["GRP"])[cols_to_sum].sum()
            sub_[k]['DAY']=sub_[k].index
        return sub_ 

           
    def mysub_month(self):
        dtype_dict = {
            'SUB': np.str_,'GIS': np.float16,'MON': np.int16,'AREA': np.float16,'FLOW_IN': np.float16,'FLOW_OUT': np.float16
        }
        col_names = ['SUB', 'GIS', 'MON', 'AREA', 'FLOW_IN', 'FLOW_OUT']
        col_specs = [(0, 11), (12, 20), (21, 26), (26, 38), (38, 50), (50, 62)]
        tab = pd.read_fwf(self.parfile, colspecs=col_specs, skiprows=9, names=col_names,dtype=dtype_dict,na_values='*******')
        tab['SUB'] = tab['SUB'].apply(lambda x: re.findall('[A-Z]+\s*(\d+)', x)[0]).astype(int)        
        months = pd.date_range(start=self.begin_date, end=self.end_date, freq='M').strftime('%Y-%m').tolist()
        subes = tab['SUB'].unique()
        l = len(months) * len(subes)
        tab = tab.iloc[:len(tab)-len(subes)]
        tab = tab[tab['MON'] <= 12]
        df_subes = pd.DataFrame(subes, columns=['SUB'])
        df_monthes = pd.DataFrame(months, columns=['MONTH'])
        # Adding a temporary key for merging
        df_subes['key'] = 1
        df_monthes['key'] = 1
        # Merge on the temporary key to get every combination
        df_result = pd.merge(df_monthes,df_subes, on ='key')
        tab['DAY'] = df_result['MONTH'].values
        outsub = {i: tab.loc[tab['SUB'] == i].copy() for i in self.subdict}
        # sub = {j: outsub[j].set_index('DAY') for j in self.subdict.keys()}
        return outsub
   

    def getflow_month(self, begin_date, end_date):
        sub = self.mysub_month()
        begin_date = pd.to_datetime(begin_date)
        end_date = pd.to_datetime(end_date)
        for k, df in sub.items():
            if 'DAY' not in df.columns:
                print(f"Key 'DAY' not found in dataframe for key {k}")
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        return sub_

if __name__=="__main__":
    parfile=r'D:\new_method_output\ceshi_day\iter1'
    filelist=glob.glob(os.path.join(parfile,'output_???.rch'))
    filelist.sort()
    print(filelist)
    subdict={86:'Yuluoping'}
    begin_date='2008-01-01'
    end_date='2018-12-31'
    begin_date2='2009-08-01'
    end_date2='2018-12-31'
    modle='flow-SUB-calibration-day'
    chose_begin_date=int(begin_date[0:4])
    chose_end_date=int(end_date[0:4])
    for filename in filelist:   
        simflow=SimFlow(filename,subdict,begin_date,end_date,modle).getflow_days(begin_date2,end_date2)
    print(simflow)