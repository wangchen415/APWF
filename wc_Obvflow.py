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

class ObvFlow(object):
    def __init__(self,excel_dir,rchdict,begin_date,end_date):
        self.excel_dir=excel_dir
        self.rchdict=rchdict
        self.begin_date=begin_date
        self.end_date=end_date
    def getEveryDay(self,begin_date,end_date):
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list
    def getflow(self,sheet_name,sub_num):
        all_csv = glob.glob(os.path.join(self.excel_dir,'flow_*'))
        all_data_frames = []
        for csv in sorted(all_csv):
            exc=pd.read_excel(csv,sheet_name=sheet_name,index_col=0)  # 添加列标题
            excel=exc[:31]
            all_data_frames.append(excel)
        # print(all_data_frames)
        data_frame_concat = pd.concat(all_data_frames,axis=1,ignore_index=True) # axis = 0 表示数据垂直合并,等于1表示并排合并.
        a={}
        data=0
        for j in list(data_frame_concat.columns):
            for i in data_frame_concat[j]:
                if np.isnan(i):
                    pass
                else:
                    a.update({data:i})
                    data=data+1
        da=pd.DataFrame.from_dict(a, orient='index')
        da.rename(columns={0:'FLOW_OUT'},inplace=True)
        t=self.getEveryDay(self.begin_date,self.end_date)
        # #print(da)
        da['DAY']=t
        flow={}
        flow.update({sub_num:da})
        return flow
    def getflow_day(self,begin_date,end_date):
        flow={}
        for i in self.rchdict.keys():
            sub_num=i
            flow.update(ObvFlow(self.excel_dir,i,self.begin_date,self.end_date).getflow(self.rchdict[i],sub_num))
            flow[i].index=pd.to_datetime(flow[i]['DAY'])
            flow[i]=flow[i][pd.to_datetime(flow[i]['DAY']).between(begin_date, end_date)]
        # flow=pd.concat(flow,axis=0)
        return flow
    def getflow_8day(self,begin_date,end_date):
        flow={}
        begin_year=int(begin_date[0:4])
        end_year=int(end_date[0:4])
        for i in self.rchdict.keys():
            sub_num=i
            flow.update(ObvFlow(self.excel_dir,i,self.begin_date,self.end_date).getflow(self.rchdict[i],sub_num))
            flow[i].index=pd.to_datetime(flow[i]['DAY'])
            days8_data=pd.DataFrame(data=None,columns=flow[i].columns)
            for y in range(begin_year,end_year+1):
                tmp=flow[i][flow[i].index.astype(str).str[0:4].astype(int) == y]
                tmp.index=pd.to_datetime(tmp.index)
                flow[i] = flow[i].resample('8D').mean(numeric_only=True)
                flow[i]=pd.concat([flow[i],days8_data])
            flow[i]['DAY']=flow[i].index
            flow[i]=flow[i][pd.to_datetime(flow[i]['DAY']).between(begin_date, end_date)]
        # flow=pd.concat(flow,axis=0)
        return flow
    def getflow_month(self,begin_date,end_date):
        flow={}
        for i in self.rchdict.keys():
            sub_num=i
            flow.update({i:mergebymonth(ObvFlow(self.excel_dir,i,self.begin_date,self.end_date).getflow(self.rchdict[i],sub_num)[i])})
            flow[i]=flow[i][pd.to_datetime(flow[i]['DAY']).between(begin_date, end_date)]
        # flow=pd.concat(flow,axis=0)
        return flow

if __name__=='__main__':
    z={20:'HongDe',49:'JiaQiao',54:'QingYang',84:'NingXian',85:'YuLuoPing'}
    excel_dir=r'D:\wangchen_swat\水文站点new'
    begin_date='2008-01-01'
    end_date='2018-12-31'
    flow=ObvFlow(excel_dir,z,begin_date,end_date).getflow_month('2009-01-01','2018-12-31')