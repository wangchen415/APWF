import os
import re
import numpy as np
import codecs


# basedir = 'txtinout'
# filename = '000010001.gw'
# filepath = os.path.join(basedir,filename)

#swat-io-document
#https://docs.python.org/3/library/re.html

class HRU_GW(object):
    #
    def __init__(self):
        pass
    def __del__(self):
        pass
    #
    #read from '000010002.gw'
    def read(self,filepath):
        #data
        with open(filepath) as fh:
            lns = fh.readlines()
            lns = [ln.rstrip() for ln in lns]
        #data type - Variable name, Line#, Format, F90 Format
        meta = [
            ['TITLE', 1, 'character', 'a80'],
            ['SHALLST', 2, 'real', 'free'],
            ['DEEPST', 3, 'real', 'free'],
            ['GW_DELAY', 4, 'real', 'free'],
            ['ALPHA_BF', 5, 'real', 'free'],
            ['GWQMN', 6, 'real', 'free'],
            ['GW_REVAP', 7, 'real', 'free'],
            ['REVAPMN', 8, 'real', 'free'],
            ['RCHRG_DP', 9, 'real', 'free'],
            ['GWHT', 10, 'real', 'free'],
            ['GW_SPYLD', 11, 'real', 'free'],
            ['SHALLST_N', 12, 'real', 'free'],
            ['GWSOLP', 13, 'real', 'free'],
            ['HLIFE_NGW', 14, 'real', 'free'],
            ['LAT_ORGN', 15, 'real', 'free'],
            ['LAT_ORGP', 16, 'real', 'free'],
            ['ALPHA_BF_D', 16, 'real', 'free'],
            
        ]
        meta_desc = []
        #
        param = {}
        for i in range(len(lns)):
            # print(i,'------------------')
            #TITLE, P.256
            if i==0:
                meta_desc.append(lns[i])
                s = re.sub('(\s*:\s*)', ':', lns[i])
                watershed_hru = [v.strip() for v in re.search('Watershed HRU\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                param[watershed_hru[0]]=watershed_hru[1]
                subbasin = [v.strip() for v in re.search('Subbasin\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                param[subbasin[0]]=subbasin[1]
                hru = [v.strip() for v in re.search('HRU\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                param[hru[0]]=hru[1]
                slope = [v.strip() for v in re.search('Slope\s*:\s*\d+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
                param[slope[0]]=slope[1]
                landuse = [v.strip() for v in re.search('Luse\s*:\s*\w+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
                param[landuse[0]]=landuse[1]
                soil = [v.strip() for v in re.search('Soil\s*:\s*\w+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
                param[soil[0]]=soil[1]
                # re.search('[0-9]{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', s,re.IGNORECASE)
                # re.search('ArcSWAT\s+[0-9]{4}\.\d+_\d+\.\d+', s,re.IGNORECASE)
                # selected = re.findall('([A-Za-z]+:[0-9]+-?[0-9]+)', s)
                # selected = re.findall('([A-Za-z]+:[0-9]+\-?\d+)', s)
                # param.extend([v.split(':') for v in selected])
            else:
                #N
                if re.match(r'\s*\d+(\.\d+)?\s*\|\s*[A-Z]+\w*\s*:.*', lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split('|')[-1].split(':',maxsplit=1)[-1].strip())
                    s = re.sub('(\s*:\s*)', ':', lns[i])
                    val = s.split('|')[0].strip()
                    if i<len(meta):
                        var = meta[i][0]
                        if meta[i][2].lower()=='integer':
                            val = int(val)
                        elif meta[i][2].lower()=='real':
                            val = float(val)
                    else:
                        var = s.split('|')[-1].split(':',maxsplit=1)[0].strip()
                        if val.isdigit():
                            val = int(val)
                        elif re.match('\d+(\.\d+)?',val):
                            val = float(val)
                    param[var]=val
                #Comment line, P256
                else:
                    meta_desc.append(lns[i])
        return meta,meta_desc,param
    #
    #save to '000010002.gw'
    def write(self,all,outfile):

        # 第一部分########################
        head1=all[1][0]
        gw1=all[2]
        ###########################end
        # 第二部分#####################
        illurstration1=all[1][1]
        line1=str(format(gw1['SHALLST'],'.4f')).rjust(16,' ')+"    "+"| "+str('SHALLST')+" "+":"+" "+str(illurstration1)
        #
        illurstration2=all[1][2]
        line2=str(format(gw1['DEEPST'],'.4f')).rjust(16,' ')+"    "+"| "+str('DEEPST')+" "+":"+" "+str(illurstration2)
        #
        illurstration3=all[1][3]
        line3=str(format(gw1['GW_DELAY'], '.4f')).rjust(16,' ')+"    "+"| "+str('GW_DELAY')+" "+":"+" "+str(illurstration3)
        #
        illurstration4=all[1][4]
        line4=str(format(gw1['ALPHA_BF'], '.4f')).rjust(16,' ')+"    "+"| "+str('ALPHA_BF')+" "+":"+" "+str(illurstration4)
        #
        illurstration5=all[1][5]
        line5=str(format(gw1['GWQMN'], '.4f')).rjust(16,' ')+"    "+"| "+str('GWQMN')+" "+":"+" "+str(illurstration5)
        #
        illurstration6=all[1][6]
        line6=str(format(gw1['GW_REVAP'], '.4f')).rjust(16,' ')+"    "+"| "+str('GW_REVAP')+" "+":"+" "+str(illurstration6)
        #
        illurstration7=all[1][7]
        line7=str(format(gw1['REVAPMN'], '.4f')).rjust(16,' ')+"    "+"| "+str('REVAPMN')+":"+" "+str(illurstration7)
        #
        illurstration8=all[1][8]
        line8=str(format(gw1['RCHRG_DP'], '.4f')).rjust(16,' ')+"    "+"| "+str('RCHRG_DP')+" "+":"+" "+str(illurstration8)
        #
        illurstration9=all[1][9]
        line9=str(format(gw1['GWHT'], '.4f')).rjust(16,' ')+"    "+"| "+str('GWHT')+" "+":"+" "+str(illurstration9)
        #
        illurstration10=all[1][10]
        line10=str(format(gw1['GW_SPYLD'], '.4f')).rjust(16,' ')+"    "+"| "+str('GW_SPYLD')+" "+":"+" "+str(illurstration10)
        #
        illurstration11=all[1][11]
        line11=str(format(gw1['SHALLST_N'], '.4f')).rjust(16,' ')+"    "+"| "+str('SHALLST_N')+" "+":"+" "+str(illurstration11)
        #
        illurstration12=all[1][12]
        line12=str(format(gw1['GWSOLP'], '.4f')).rjust(16,' ')+"    "+"| "+str('GWSOLP')+" "+":"+" "+str(illurstration12)
        #
        illurstration13=all[1][13]
        line13=str(format(gw1['HLIFE_NGW'], '.4f')).rjust(16,' ')+"    "+"| "+str('HLIFE_NGW')+" "+":"+" "+str(illurstration13)
        #
        illurstration14=all[1][14]
        line14=str(format(gw1['LAT_ORGN'], '.4f')).rjust(16,' ')+"    "+"| "+str('LAT_ORGN')+" "+":"+" "+str(illurstration14)
        #
        illurstration15=all[1][15]
        line15=str(format(gw1['LAT_ORGP'], '.4f')).rjust(16,' ')+"    "+"| "+str('LAT_ORGP')+" "+":"+" "+str(illurstration15)
        #
        try:
            illurstration16=all[1][16]
            line16=str(format(gw1['ALPHA_BF_D'], '.4f')).rjust(16,' ')+"    "+"| "+str('ALPHA_BF_D')+" "+":"+" "+str(illurstration16)
        except:
            print("该数据缺少变量")
               ##################end
        #输入文件
        object=codecs.open(outfile,'w','utf-8')
        object.write(head1+'\n')
        object.write(line1+'\n')
        object.write(line2+'\n')
        object.write(line3+'\n')
        object.write(line4+'\n')
        object.write(line5+'\n')
        object.write(line6+'\n')
        object.write(line7+'\n')
        object.write(line8+'\n')
        object.write(line9+'\n')
        object.write(line10+'\n')
        object.write(line11+'\n')
        object.write(line12+'\n')
        object.write(line13+'\n')
        object.write(line14+'\n')
        object.write(line15+'\n')
        try:
            object.write(line16+'\n')
        except:
            print("该数据缺少变量")
        object.close()
'''
 .gw file Watershed HRU:3 Subbasin:1 HRU:3 Luse:BARR Soil: GRIDCODE1 Slope: 0-9999 2023/3/11 0:00:00 ArcSWAT 2012.10_6.24
       1000.0000    | SHALLST : Initial depth of water in the shallow aquifer [mm]
       2000.0000    | DEEPST : Initial depth of water in the deep aquifer [mm]
         31.0000    | GW_DELAY : Groundwater delay [days]
          0.0480    | ALPHA_BF : Baseflow alpha factor [days]
       1000.0000    | GWQMN : Threshold depth of water in the shallow aquifer required for return flow to occur [mm]
          0.0200    | GW_REVAP : Groundwater "revap" coefficient
        750.0000    | REVAPMN: Threshold depth of water in the shallow aquifer for "revap" to occur [mm]
          0.0500    | RCHRG_DP : Deep aquifer percolation fraction
          1.0000    | GWHT : Initial groundwater height [m]
          0.0030    | GW_SPYLD : Specific yield of the shallow aquifer [m3/m3]
          0.0000    | SHALLST_N : Initial concentration of nitrate in shallow aquifer [mg N/l]
          0.0000    | GWSOLP : Concentration of soluble phosphorus in groundwater contribution to streamflow from subbasin [mg P/l]
          0.0000    | HLIFE_NGW : Half-life of nitrate in the shallow aquifer [days]
          0.0000    | LAT_ORGN : Organic N in the base flow [mg/L]
          0.0000    | LAT_ORGP : Organic P in the base flow [mg/L]
          0.0100    | ALPHA_BF_D : Baseflow alpha factor for deep aquifer [days]
'''