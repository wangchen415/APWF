import pandas as pd
import os
import re
import glob
import numpy as np
import datetime,calendar



def mergebymonth(ET):  
    merge=ET
    merge['DAY']= merge['DAY'].str.slice(0,7)
    mean_mon=merge.groupby(merge['DAY'],as_index=False).mean()
    return mean_mon

class ObvET(object):
    def __init__(self,ETfile,subdict):
        self.ETfile=ETfile
        self.subdict=subdict
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
    ####monthly#####
    def Monthly_scale_conversion(self,begin_date,end_date):
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])
        ETdata=pd.read_csv(self.ETfile,index_col=0)
        df_ = pd.DataFrame(data=None,columns=ETdata.columns)
        # print(os.path.split(self.ETfile)[-1])
        if re.match('.*ssebop.*',os.path.split(self.ETfile)[-1]):
            ETdata['Mon']=ETdata.index.astype(str).str[0:6]
            df=ETdata.groupby(by=['Mon'],dropna=True,group_keys=False).sum()
            ind=[]
            for i in range(len(df.index)):
                ind.append('%d-%02d'%(df.index.astype(str).str[0:4].astype(int)[i],df.index.astype(str).str[4:6].astype(int)[i])) 
            df.index=ind
            for y_idx in range(begin_year, end_year+1):
                for m_idx in range(1, 13):
                    for i in range(len(df.index)):
                        date = datetime.datetime.strptime(df.index[i], '%Y-%m')
                        year, month, day = date.year, date.month, date.day
                        if year == y_idx and month == m_idx: 
                            df_.loc[df.index[i]]=df.loc[df.index[i]]
        elif re.match('.*pmlv2.*',os.path.split(self.ETfile)[-1]) or re.match('.*glass.*',os.path.split(self.ETfile)[-1]) :
            begin_year=int(begin_date[0:4])
            end_year=int(end_date[0:4])      
            ETdata=pd.read_csv(self.ETfile,index_col=0)
            ETdata.columns.astype(int)
            
            df =pd.read_csv(self.ETfile,index_col=0)
            days_data=pd.DataFrame(data=None,columns=ETdata.columns)
            for y in range(begin_year,end_year+1):
                tmp=df[df.index.astype(str).str[0:4].astype(int) == y]
                tmp.index=pd.to_datetime(tmp.index)
                days_data_tmp = tmp
                days_data=pd.concat([days_data_tmp,days_data])
            days_data=days_data.sort_index()
            df_=days_data.groupby(by=days_data.index.astype(str).str[:7],dropna=True,group_keys=False,).sum()
            return df_
            
        else:
            for y_idx in range(begin_year, end_year+1):
                for m_idx in range(1, 13):
                    df = pd.DataFrame(data=None,columns=ETdata.columns)
                    for i in range(len(ETdata.index)):
                        try: 
                            date = datetime.datetime.strptime(ETdata.index[i], '%Y-%m-%d')
                        except:
                            date = datetime.datetime.strptime(ETdata.index[i], '%Y_%m_%d')
                        year, month, day = date.year, date.month, date.day
                        if year == y_idx:
                            if month == m_idx:
                                df.loc['%s'%(ETdata.index[i])] =ETdata.loc[ETdata.index[i]]*1
                    name_mon_first = df.index[0]
                    # #print(df.index[0])
                    try:
                        date_mon_first = datetime.datetime.strptime(name_mon_first, '%Y-%m-%d')
                    except:
                        date_mon_first = datetime.datetime.strptime(name_mon_first, '%Y_%m_%d')
                    # #print(date_mon_first)
                    if date_mon_first.day != 1:  # 当月第一景数据不是从1日开始，则加入上一景数据
                        # 往前推8天找到上一景影像
                        date_last_mon = date_mon_first - datetime.timedelta(days=8)
                        # #print(date_last_mon)
                        # 在影像列表中查找并插入上个月最后一景影像（权重暂时分配为默认值1）
                        try:
                            df.loc['%d-%02d-%02d'%(date_last_mon.year,date_last_mon.month,date_last_mon.day)]=ETdata.loc['%d-%02d-%02d'%(date_last_mon.year,date_last_mon.month,date_last_mon.day)]*1
                        except:
                            df.loc['%d_%02d_%02d'%(date_last_mon.year,date_last_mon.month,date_last_mon.day)]=ETdata.loc['%d_%02d_%02d'%(date_last_mon.year,date_last_mon.month,date_last_mon.day)]*1

                        df=df.sort_index()
                    ## 为每月首尾可能跨月影像分配权重
                    try:
                        date_mon_list_first = datetime.datetime.strptime(df.index[0], '%Y-%m-%d')
                        date_mon_list_last = datetime.datetime.strptime(df.index[-1], '%Y-%m-%d')
                    except:
                        date_mon_list_first = datetime.datetime.strptime(df.index[0], '%Y_%m_%d')
                        date_mon_list_last = datetime.datetime.strptime(df.index[-1], '%Y_%m_%d')                        
                    ## 每月首尾景影像年月日
                    year_mon_list_first, month_mon_list_first, day_mon_list_first = date_mon_list_first.year, \
                                                                                    date_mon_list_first.month, \
                                                                                    date_mon_list_first.day
                    year_mon_list_last, month_mon_list_last, day_mon_list_last = date_mon_list_last.year, \
                                                                                date_mon_list_last.month, \
                                                                                date_mon_list_last.day
                    ## 判断首景影像是否属于上月跨月影像（注：判断其是否从1日开始）
                    if day_mon_list_first != 1:
                        # 属于跨月影像，则获取上个月第一天/最后一天/天数
                        first_day_mon, last_day_mon, days_mon = self.mon_statistics(year_mon_list_first, month_mon_list_first)
                        try:
                            last_day_mon_datetime = datetime.datetime.strptime(str(last_day_mon), '%Y-%m-%d')
                        except:
                            last_day_mon_datetime = datetime.datetime.strptime(str(last_day_mon), '%Y_%m_%d')
                        # 求首景影像（跨月）在上个月所占天数
                        delta_last_mon_last = (last_day_mon_datetime - date_mon_list_first).days + 1
                        # 求首景影像（跨月）在当月所占天数并据此分配影像权重
                        delta_this_mon_first = 8 - delta_last_mon_last
                        df.iloc[0]=df.iloc[0]*(delta_this_mon_first / 8)
                    ## 当年当月第一天/最后一天/天数
                    first_day_this_mon, last_day_this_mon, days_this_mon = self.mon_statistics(y_idx, m_idx)
                    ## 判断尾景数据是否属于下月跨月数据（注：判断尾景数据起始日期与当月最后一日是否相等，注：12月尾景不考虑跨月问题）
                    if (day_mon_list_last + 7) != days_this_mon and m_idx != 12:
                        try:
                            last_day_this_mon_datetime = datetime.datetime.strptime(str(last_day_this_mon), '%Y-%m-%d')
                        except:
                            last_day_this_mon_datetime = datetime.datetime.strptime(str(last_day_this_mon), '%Y_%m_%d')
                        # 获取尾景影像（跨月）当月所占天数并据此分配影像权重
                        delta_this_mon_last = (last_day_this_mon_datetime - date_mon_list_last).days + 1
                        df.iloc[-1]=df.iloc[-1]*(delta_this_mon_last / 8)
                    #
                    df_.loc['%d-%02d'%(y_idx,m_idx)] =df.apply(lambda x:x.sum())
                    df_.replace(0, np.nan, inplace=True)
        return df_
        
    def get_ET_month(self,begin_date,end_date):
        ETdata=self.Monthly_scale_conversion(begin_date,end_date)
        ETdata.columns=ETdata.columns.astype(int)
        sub={}
        for j in self.subdict.keys():
            sub.update({j:pd.DataFrame(ETdata[j].values, columns=['ET'],index=pd.to_datetime(ETdata[j].index).strftime('%Y-%m'))})
            sub[j]['DAY']=sub[j].index
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        # print(begin_date,end_date)
        # sub=pd.concat(sub,axis=0)
        return sub_       
    ####8days#####
    def days8_scale_conversion(self,begin_date,end_date):
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])  
        ETdata=pd.read_csv(self.ETfile,index_col=0)
        ETdata.columns.astype(int)
        if re.match('.*ssebop.*', os.path.split(self.ETfile)[-1]): 
            dates = []
            values = []
            for i, m, d in zip(ETdata.index, ETdata.index.astype(str).str[0:6], ETdata.index.astype(str).str[-1]):
                date = datetime.datetime.strptime(m, '%Y%m')
                if d == '1':
                    dates.extend(['%d-%02d-%02d'%(date.year, date.month, rag+1) for rag in range(10)])
                    values.extend([ETdata.loc[i]/10]*10)
                elif d == '2':
                    dates.extend(['%d-%02d-%02d'%(date.year, date.month, rag) for rag in range(11, 21)])
                    values.extend([ETdata.loc[i]/10]*10)
                elif d == '3':
                    days_in_month = calendar.monthrange(date.year, date.month)[1]
                    dates.extend(['%d-%02d-%02d'%(date.year, date.month, rag) for rag in range(21, days_in_month+1)])
                    values.extend([ETdata.loc[i]/(days_in_month-20)]*(days_in_month-20))

            # Create a new DataFrame with values and dates
            df = pd.DataFrame(values, index=pd.to_datetime(dates), columns=ETdata.columns)

            # Resample
            days8_data = df.resample('8D').sum()
            days8_data.replace(0, np.nan, inplace=True)
        elif re.match('.*pmlv2.*',os.path.split(self.ETfile)[-1]):
            df =pd.read_csv(self.ETfile,index_col=0)
            days8_data=pd.DataFrame(data=None,columns=ETdata.columns)
            for y in range(begin_year,end_year+1):
                tmp=df[df.index.astype(str).str[0:4].astype(int) == y]
                tmp.index=pd.to_datetime(tmp.index)
                days8_data_tmp = tmp.resample('8D').sum()
                days8_data=pd.concat([days8_data_tmp,days8_data])
            days8_data=days8_data.sort_index()
            days8_data.replace(0, np.nan, inplace=True)
        else:
            df = pd.DataFrame(data=None,columns=ETdata.columns)
            for y_idx in range(begin_year, end_year+1):
                for m_idx in range(1, 13):
                    for i in range(len(ETdata.index)):
                        try: 
                            date = datetime.datetime.strptime(ETdata.index[i], '%Y-%m-%d')
                        except:
                            date = datetime.datetime.strptime(ETdata.index[i], '%Y_%m_%d')
                        year, month, day = date.year, date.month, date.day
                        if year == y_idx:
                            if month == m_idx:
                                df.loc['%s'%(ETdata.index[i])] =ETdata.loc[ETdata.index[i]]
            days8_data=df
        return days8_data

    def get_ET_8days(self,begin_date,end_date):
        ETdata=self.days8_scale_conversion(begin_date,end_date)
        ETdata.columns=ETdata.columns.astype(int)
        sub={}
        for j in self.subdict.keys():
            sub.update({j:pd.DataFrame(ETdata[j].values, columns=['ET'],index=ETdata[j].index)})
            sub[j]['DAY']=sub[j].index
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        # sub=pd.concat(sub,axis=0)
        # print(sub,'sssssssssssssssssssssssssssssss')
        # print(ETdata.index,ETdata.values)
        # print(begin_date,end_date)
        return sub_ 
    ####days#####
    def days_scale_conversion(self,begin_date,end_date):
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])      
        ETdata=pd.read_csv(self.ETfile,index_col=0)
        ETdata.columns.astype(int)
        df =pd.read_csv(self.ETfile,index_col=0)
        days_data=pd.DataFrame(data=None,columns=ETdata.columns)
        for y in range(begin_year,end_year+1):
            tmp=df[df.index.astype(str).str[0:4].astype(int) == y]
            tmp.index=pd.to_datetime(tmp.index)
            days_data_tmp = tmp
            days_data=pd.concat([days_data_tmp,days_data])
        days_data=days_data.sort_index()
        days_data.replace(0, np.nan, inplace=True)
        return days_data
        
    def get_ET_days(self,begin_date,end_date):
        ETdata=self.days_scale_conversion(begin_date,end_date)
        ETdata.columns=ETdata.columns.astype(int)
        sub={}
        for j in self.subdict.keys():
            sub.update({j:pd.DataFrame(ETdata[j].values, columns=['ET'],index=ETdata[j].index)})
            sub[j]['DAY']=sub[j].index
        sub_ = {k: df[pd.to_datetime(df['DAY']).between(begin_date, end_date)] for k, df in sub.items()}
        # sub=pd.concat(sub,axis=0)
        return sub_ 

if __name__=='__main__':
    ETfile=r'D:\wangchen_swat\remotesensing\data_pmlv2_86.csv'
    # begin_date='2008-01-01'
    # end_date='2018-12-31'
    begin_date2='2008-08-01'
    end_date2='2018-01-01'
    subdict={10:'',86:'Yuluoping'}
    obvET=ObvET(ETfile,subdict).get_ET_8days(begin_date2,end_date2)