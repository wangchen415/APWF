import pandas as pd
import os
import re
import glob
import numpy as np
import datetime,calendar

class ObvSW(object):
    def __init__(self,SWfilelist,hrudict):
        self.SWfilelist=SWfilelist
        self.hrudict=hrudict
    def mon_statistics(self,year_para, month_para):
        # 当月第一天
        first_day_mon = datetime.date(year_para, month_para, day=1)
        first_day_next_mon = datetime.date(year_para + 1, month=1, day=1) if month_para == 12 \
                            else datetime.date(year_para, month_para + 1, day=1)
        # 当月最后一天
        last_day_mon = first_day_next_mon - datetime.timedelta(days=1)
        # 当月天数
        days_mon = last_day_mon.day
        return first_day_mon, last_day_mon, days_mon
    def Monthly_scale_conversion(self,begin_date,end_date):
        sw=[]
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])
        for SWfile in self.SWfilelist:   
            SWdata=pd.read_csv(SWfile,index_col=0)
            df_ = pd.DataFrame(data=None,columns=SWdata.columns)
            SWdata['Mon']=SWdata.index.astype(str).str[0:7]
            df=SWdata.groupby(by=['Mon'],dropna=True,group_keys=False).last()
            for y_idx in range(begin_year, end_year+1):
                for m_idx in range(1, 13):
                    for i in range(len(df.index)):
                        date = datetime.datetime.strptime(df.index[i], '%Y-%m')
                        year, month, day = date.year, date.month, date.day
                        if year == y_idx and month == m_idx: 
                            df_.loc[df.index[i]]=df.loc[df.index[i]]
            sw.append(df_)
        return sw
    def get_SW_month(self,begin_date,end_date):
        s=[]
        SW=self.Monthly_scale_conversion(begin_date,end_date)
        for SWdata,i in zip(SW,range(len(SW))):
            SWdata.columns=SWdata.columns.astype(int)
            sub={}
            for j in self.hrudict.keys():
                sub.update({j:pd.DataFrame(SWdata[j].values, columns=['Layer%s'%str(i+1)],index=SWdata[j].index)})
            sub=pd.concat(sub,axis=0)
            s.append(sub)
        combined_index = pd.concat(s, axis=1)
        df_dict = {level: combined_index.xs(level) for level in combined_index.index.get_level_values(0).unique()}
        sub_ = {k: df.loc[pd.to_datetime(df.index).to_series().between(pd.Timestamp(begin_date), pd.Timestamp(end_date))] for k, df in df_dict.items()}
        return sub_ 

    def days8_scale_conversion(self,begin_date,end_date):
        sw=[]
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])
        for SWfile in self.SWfilelist:   
            SWdata=pd.read_csv(SWfile,index_col=0)
            SWdata.columns.astype(int)
            df =pd.read_csv(SWfile,index_col=0)
            days8_data=pd.DataFrame(data=None,columns=SWdata.columns)
            for y in range(begin_year,end_year+1):
                tmp=df[df.index.astype(str).str[0:4].astype(int) == y]
                tmp.index=pd.to_datetime(tmp.index)
                days8_data_tmp = tmp.resample('8D').last()
                days8_data=pd.concat([days8_data_tmp,days8_data])
            days8_data=days8_data.sort_index()
            days8_data.replace(0, np.nan, inplace=True)
            sw.append(days8_data)
        return sw

    def get_SW_8days(self,begin_date,end_date):
        s=[]
        SW=self.days8_scale_conversion(begin_date,end_date)
        for SWdata,i in zip(SW,range(len(SW))):
            SWdata.columns=SWdata.columns.astype(int)
            sub={}
            for j in self.hrudict.keys():
                sub.update({j:pd.DataFrame(SWdata[j].values, columns=['Layer%s'%str(i+1)],index=SWdata[j].index)})
                # print(sub)
                # if i==len(SW)-1:
                #     result = pd.concat(sub[j], axis=1)
            sub=pd.concat(sub,axis=0)
            s.append(sub)
        # #print(ETdata.index,ETdata.values)
        # 假设multiindex_array为包含多个MultiIndex对象的数组
        # 将多个MultiIndex对象按照列名组合在一起
        combined_index = pd.concat(s, axis=1)
        df_dict = {level: combined_index.xs(level) for level in combined_index.index.get_level_values(0).unique()}
        sub_ = {k: df[(pd.to_datetime(df.index).to_series().between(pd.Timestamp(begin_date), pd.Timestamp(end_date)))] for k, df in df_dict.items()}
        return sub_
        
    def days_scale_conversion(self,begin_date,end_date):
        sw=[]
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])
        for SWfile in self.SWfilelist:
            SWdata=pd.read_csv(SWfile,index_col=0)
            SWdata.columns.astype(int)
            df =pd.read_csv(SWfile,index_col=0)
            days_data=pd.DataFrame(data=None,columns=SWdata.columns)
            for y in range(begin_year,end_year+1):
                tmp=df[df.index.astype(str).str[0:4].astype(int) == y]
                tmp.index=pd.to_datetime(tmp.index)
                days_data_tmp = tmp
                days_data=pd.concat([days_data_tmp,days_data])
            days_data=days_data.sort_index()
            days_data.replace(0, np.nan, inplace=True)
            sw.append(days_data)
        return sw
        
    def get_SW_days(self,begin_date,end_date):
        s=[]
        SW=self.days_scale_conversion(begin_date,end_date)
        for SWdata,i in zip(SW,range(len(SW))):
            SWdata.columns=SWdata.columns.astype(int)
            sub={}
            for j in self.hrudict.keys():
                sub.update({j:pd.DataFrame(SWdata[j].values, columns=['Layer%s'%str(i+1)],index=SWdata[j].index)})
                # print(sub)
                # if i==len(SW)-1:
                #     result = pd.concat(sub[j], axis=1)
            sub=pd.concat(sub,axis=0)
            s.append(sub)
        # #print(ETdata.index,ETdata.values)
        # 假设multiindex_array为包含多个MultiIndex对象的数组
        # 将多个MultiIndex对象按照列名组合在一起
        combined_index = pd.concat(s, axis=1)
        df_dict = {level: combined_index.xs(level) for level in combined_index.index.get_level_values(0).unique()}
        sub_ = {k: df[(pd.to_datetime(df.index).to_series().between(pd.Timestamp(begin_date), pd.Timestamp(end_date)))] for k, df in df_dict.items()}
        return sub_

if __name__=='__main__':
    modle='SW-HRU'
    begin_date='2008-01-01'
    end_date='2012-12-31'
    z={20:'HongDe',49:'JiaQiao',54:'QingYang',84:'NingXian',85:'YuLuoPing'}
    remotesensing_path=r'D:\python\SWAT-AIPC\RSdata'
    SWfilelist=[os.path.join(remotesensing_path,'rescale_0-5cm.csv'),os.path.join(remotesensing_path,'rescale_5-15cm.csv'),os.path.join(remotesensing_path,'rescale_15-30cm.csv'),os.path.join(remotesensing_path,'rescale_30-60cm.csv'),os.path.join(remotesensing_path,'rescale_60-100cm.csv')]
    SW=ObvSW(SWfilelist,z).get_SW_8days(begin_date,end_date)
    # print(SW)