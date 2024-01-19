import pandas as pd
import os
import re
import glob
import numpy as np
import datetime,calendar
import dask.dataframe as dd


def mergebymonth(flow):  
    merge=flow
    merge['DAY']= merge['DAY'].str.slice(0,7)
    mean_mon=merge.groupby(merge['DAY'],as_index=False).mean()
    return mean_mon
day8 = None
class SimET(object):
    def __init__(self,parfile,subdict,begin_date,end_date,modle):
        self.parfile=parfile
        self.subdict=subdict
        self.begin_date=begin_date
        self.end_date=end_date
        self.modle=modle
    def getEveryDay(self):
        return pd.date_range(start=self.begin_date, end=self.end_date).strftime('%Y-%m-%d').tolist()

    def mysub_day(self):
        dtype_dict = { 'LULC': np.str_,'GIS': np.str_, 'MON': np.int64, 'AREA': np.float16, 'MON-AREA': np.str_,
            'PRECIP': np.float16, 'SNOMELT': np.float16, 'PET': np.float16, 'ET': np.float16, 
            'SW': np.float16, 'PERC': np.float16, 'SURQ': np.float16, 'GW_Q': np.float16, 
            'WYLD': np.float16, 'SYLD': np.float16, 'ORGN': np.float16, 'ORGP': np.float16, 
            'NSURQ': np.float16, 'SOLP': np.float16, 'SEDP': np.float16}
        if self.modle.split('-')[1]=='SUB':
            col_names = ['SUB', 'GIS', 'MON', 'AREA', 'PRECIP', 'SNOMELT', 'PET', 'ET', 'SW', 'PERC', 'SURQ', 'GW_Q', 'WYLD', 'SYLD', 'ORGN', 'ORGP', 'NSURQ', 'SOLP', 'SEDP']
            col_widths = [11, 9, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
            tab = pd.read_fwf(self.parfile, widths=col_widths, skiprows=9, names=col_names, dtype=dtype_dict,na_values=['*******'])
            # tab = tab.compute()
            # chunksize = 10000
            # chunks = []
            # for chunk in dd.read_fwf(self.parfile, widths=col_widths, skiprows=9, names=col_names, chunksize=chunksize, dtype=dtype_dict,na_values='*******'):
            #     chunks.append(chunk)
            # tab = pd.concat(chunks, axis=0)
        elif self.modle.split('-')[1]=='HRU' or 'landuse':
            col_names = ['LULC','SUB', 'GIS', 'MON-AREA', 'PRECIP', 'SNOMELT', 'PET', 'ET', 'SW']
            col_specs = [(0, 4),(0, 9), (9, 19), (31,44), (44, 54), (64, 74), (84, 94), (97, 104), (114, 124)]
            # chunksize = 10000
            # chunks = []
            # for chunk in pd.read_fwf(self.parfile, colspecs=col_specs, skiprows=9, names=col_names, chunksize=chunksize, dtype=dtype_dict,na_values='*******'):
            #     chunks.append(chunk)
            # tab = pd.concat(chunks, axis=0)
            tab = pd.read_fwf(self.parfile, colspecs=col_specs, skiprows=9, names=col_names,dtype=dtype_dict,na_values=['*******'])
            # tab = tab.compute()
            split_df = tab['MON-AREA'].str.split('.', expand=True)
            tab['MON'] = split_df[0].astype(int)
            tab['AREA'] = split_df[1].astype(float)
        # tab = pd.read_fwf(self.parfile, widths=col_widths, skiprows=9, names=col_names)
        tab['SUB'] = tab['SUB'].apply(lambda x: re.findall('[A-Z]+\s*(\d+)', x)[0]).astype(int)
        day = pd.date_range(start=self.begin_date, end=self.end_date).strftime('%Y-%m-%d').tolist()
        subes = tab['SUB'].unique()
        # print(subes)
        outsub = {i: tab.loc[tab['SUB'] == i].copy() for i in subes}
        sub = {i: outsub[i].assign(DAY=day) for i in self.subdict}
        # sub = {j: outsub[j].set_index('DAY') for j in self.subdict.keys()}
        return sub

    def getet_days(self,begin_date,end_date):
        sub=self.mysub_day()
        begin_date = pd.to_datetime(begin_date)
        end_date = pd.to_datetime(end_date)
        for k, df in sub.items():
            if 'DAY' not in df.columns:
                print(f"Key 'DAY' not found in dataframe for key {k}")
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        return sub_

    def getet_8days(self,begin_date,end_date):
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
            cols_to_sum = ['ET']
            sub_[k]=sub_[k].groupby(by=["GRP"])[cols_to_sum].sum()
            sub_[k]['DAY']=sub_[k].index
            # print(sub_[k])
            sub_[k]=sub_[k][pd.to_datetime(sub_[k]['DAY']).between(begin_date, end_date)]
        return sub_ 

           
    def mysub_month(self):
        dtype_dict = { 'GIS': np.float16, 'MON': np.int64, 'AREA': np.float16, 'MON-AREA': np.str_,
            'PRECIP': np.float16, 'SNOMELT': np.float16, 'PET': np.float16, 'ET': np.float16, 
            'SW': np.float16, 'PERC': np.float16, 'SURQ': np.float16, 'GW_Q': np.float16, 
            'WYLD': np.float16, 'SYLD': np.float16, 'ORGN': np.float16, 'ORGP': np.float16, 
            'NSURQ': np.float16, 'SOLP': np.float16, 'SEDP': np.float16}
        if self.modle.split('-')[1]=='SUB':
            col_names = ['SUB', 'GIS', 'MON', 'AREA', 'PRECIP', 'SNOMELT', 'PET', 'ET', 'SW', 'PERC', 'SURQ', 'GW_Q', 'WYLD', 'SYLD', 'ORGN', 'ORGP', 'NSURQ', 'SOLP', 'SEDP']
            col_widths = [11, 9, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
            tab = pd.read_fwf(self.parfile, widths=col_widths, skiprows=9, names=col_names,dtype=dtype_dict,na_values='*******')
        elif self.modle.split('-')[1]=='HRU' or 'landuse':
            col_names = ['SUB', 'GIS', 'MON-AREA', 'PRECIP', 'SNOMELT', 'PET', 'ET', 'SW']
            col_specs = [(0, 9), (11, 20), (29,44), (47, 54), (68, 73), (84, 94), (97, 104), (116, 124)]
            tab = pd.read_fwf(self.parfile, colspecs=col_specs, skiprows=9, names=col_names,dtype=dtype_dict,na_values='*******')
            split_df = tab['MON-AREA'].str.split('.', expand=True)
            tab['MON'] = split_df[0].astype(int)
            tab['AREA'] = split_df[1].astype(float)
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
   

    def getet_month(self, begin_date, end_date):
        sub = self.mysub_month()
        begin_date = pd.to_datetime(begin_date)
        end_date = pd.to_datetime(end_date)
        for k, df in sub.items():
            if 'DAY' not in df.columns:
                print(f"Key 'DAY' not found in dataframe for key {k}")
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        return sub_




if __name__=="__main__":
    # parfile=r'D:\new_method_output\ceshi\iter1'
    # filelist=glob.glob(os.path.join(parfile,'output_???.sub'))
    # filelist.sort()
    # # subdict={80:'Yuluoping',86:'Yuluoping'}
    # sub='52-53,55-76,79-84,86'
    # tmp=re.findall('([0-9\-\,]*)?',sub)
    # if tmp[0]=='':
    #     subbsn=None
    # else:
    #     sub_dict={}
    # for num in tmp[0].split(','):
    #     if num.isdigit():
    #         sub_dict[int(num)]=(" ")
    #     else:
    #         lb,ub=num.split('-')
    #         for i in range(int(lb),int(ub)+1):
    #             sub_dict[int(i)]=(" ")
    # print(sub_dict)
    # begin_date='2008-01-01'
    # end_date='2018-12-31'
    # begin_date2='2008-08-01'
    # end_date2='2014-08-01'
    # modle='flow-HRU-calibration-Mon'
    # mod= modle.split('-')[1]
    # chose_begin_date=int(begin_date[0:4])
    # chose_end_date=int(end_date[0:4])
    # for filename in filelist:   
    #     simET=SimETOutput(filename,sub_dict,begin_date,end_date,modle).getet_month(begin_date2,end_date2)
    # print(simET)
    parfile=r'D:\new_method_output\ceshi_day\iter1'
    filelist=glob.glob(os.path.join(parfile,'output_???.hru'))
    filelist.sort()
    print(filelist)
    subdict={86:'Yuluoping'}
    begin_date='2008-01-01'
    end_date='2018-12-31'
    begin_date2='2009-08-01'
    end_date2='2018-12-31'
    modle='flow-HRU-calibration-8days'
    for filename in filelist:   
        simET=SimET(filename,subdict,begin_date,end_date,modle).getet_8days(begin_date2,end_date2)