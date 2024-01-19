import os
import re
import numpy as np
import codecs


# basedir = 'txtinout'
# filename = '000030000.sub'
# filepath = os.path.join(basedir,filename)

#swat-io-document
#https://docs.python.org/3/library/re.html

class HRU_SUB(object):
    #
    def __init__(self):
        pass
    def __del__(self):
        pass
    #
    #read from '000030000.sub'
    def read(self,filepath):
        #data
        with open(filepath,'r',encoding='unicode_escape') as fh:
            lns = fh.readlines()
            lns = [ln.rstrip() for ln in lns]
        change_combination = []
        change_solo={}
        meta_desc=[]
        nochange = []
        for i in range(len(lns)):
            if i==0:
                s = re.sub('(\s*:\s*)', ':', lns[i])
                subbasin = [v.strip() for v in re.search('Subbasin\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                change_solo[subbasin[0]]=subbasin[1]
            if i==15 or i==17 or i==19:
                change_combination.append(lns[i].split('   ')[1:])
            elif 20 <=i <=22 or 24 <=i <=28 or i == 34:
                if re.match(r'\s*\-?\d+(\.\d+)?\s*|\s*[A-Z]+\w*:.*', lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split('|')[-1].split(':',maxsplit=1)[-1].strip())
                    s = re.sub('(\s*:\s*)', ':', lns[i])
                    val = float(s.split('|')[0].strip())
                    var = s.split('|')[-1].split(':',maxsplit=1)[0].strip()
                    change_solo[var]=val
            else:
                nochange.append(lns[i])
        change_combination=np.array(change_combination).astype(float)
        return change_combination,change_solo,meta_desc,nochange
    def write(self,all,outfile):
        #
        nochange=all[3]
        sub1=all[1]
        ###########################end
        # 第二部分#####################
        number1=all[0][0]
        line14=nochange[14]
        line15=''.join(str(f'{j: .3f}').rjust(8,' ') for j in number1)
        #
        number2=all[0][1]
        line16=nochange[15]
        line17=''.join(str(f'{j: .3f}').rjust(8,' ') for j in number2)
        #
        number3=all[0][2]
        line18=nochange[16]
        line19=''.join(str(f'{j: .3f}').rjust(8,' ') for j in number3)
        #
        illurstration4=all[2][0]
        line20=str(format(sub1['PLAPS'], '.3f')).rjust(16,' ')+"    "+"| "+str('PLAPS')+" "+":"+" "+str(illurstration4)
        #
        illurstration5=all[2][1]
        line21=str(format(sub1['TLAPS'], '.3f')).rjust(16,' ')+"    "+"| "+str('TLAPS')+" "+":"+" "+str(illurstration5)
        #
        illurstration6=all[2][2]
        line22=str(format(sub1['SNO_SUB'], '.3f')).rjust(16,' ')+"    "+"| "+str('SNO_SUB')+" "+":"+" "+str(illurstration6)
        #
        line23=nochange[17]
        #
        illurstration7=all[2][3]
        line24=str(format(sub1['CH_L1'], '.3f')).rjust(16,' ')+"    "+"| "+str('CH_L1')+" "+":"+" "+str(illurstration7)
        #
        illurstration8=all[2][4]
        line25=str(format(sub1['CH_S1'], '.3f')).rjust(16,' ')+"    "+"| "+str('CH_S1')+" "+":"+" "+str(illurstration8)
        #
        illurstration9=all[2][5]
        line26=str(format(sub1['CH_W1'], '.3f')).rjust(16,' ')+"    "+"| "+str('CH_W1')+" "+":"+" "+str(illurstration9)
        #
        illurstration10=all[2][6]
        line27=str(format(sub1['CH_K1'], '.3f')).rjust(16,' ')+"    "+"| "+str('CH_K1')+" "+":"+" "+str(illurstration10)
        #
        illurstration11=all[2][7]
        line28=str(format(sub1['CH_N1'], '.3f')).rjust(16,' ')+"    "+"| "+str('CH_N1')+" "+":"+" "+str(illurstration11)
        #
        line29=nochange[18]
        line30=nochange[19]
        line31=nochange[20]
        line32=nochange[21]
        line33=nochange[22]
        #
        illurstration12=all[2][8]
        line34=str(format(sub1['CO2'], '.3f')).rjust(16,' ')+"    "+"| "+str('CO2')+" "+":"+" "+str(illurstration12)
        #输出文件
        object=codecs.open(outfile,'w','utf-8')
        for OS1 in range(len(nochange[:14])):
            #    for j in range(len(OS2[i])):
            object.write(str(nochange[OS1])+'\n')
        object.write(line14+'\n')
        object.write(line15+'\n')
        object.write(line16+'\n')
        object.write(line17+'\n')
        object.write(line18+'\n')
        object.write(line19+'\n')
        object.write(line20+'\n')
        object.write(line21+'\n')
        object.write(line22+'\n')
        object.write(line23+'\n')
        object.write(line24+'\n')
        object.write(line25+'\n')
        object.write(line26+'\n')
        object.write(line27+'\n')
        object.write(line28+'\n')
        object.write(line29+'\n')
        object.write(line30+'\n')
        object.write(line31+'\n')
        object.write(line32+'\n')
        object.write(line33+'\n')
        object.write(line34+'\n')
        for OS2 in range(23,len(nochange)):
            #    for j in range(len(OS2[i])):
            object.write(str(nochange[OS2])+'\n')
        object.close()
'''
 .sub file Subbasin: 1 2023/3/11 0:00:00 ArcSWAT 2012.10_6.24
      125.000100    | SUB_KM : Subbasin area [km2]

Climate in subbasin
       37.321428    | LATITUDE : Latitude of subbasin [degrees]
         1607.63    | ELEV : Elevation of subbasin [m]
               1    | IRGAGE: precip gage data used in subbasin
               1    | ITGAGE: temp gage data used in subbasin
               1    | ISGAGE: solar radiation gage data used in subbasin
               1    | IHGAGE: relative humidity gage data used in subbasin
               1    | IWGAGE: wind speed gage data used in subbasin
000010000.wgn       | WGNFILE: name of weather generator data file
               1    | FCST_REG: Region number used to assign forecast data to the subbasin
Elevation Bands
| ELEVB: Elevation at center of elevation bands [m]
   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000
| ELEVB_FR: Fraction of subbasin area within elevation band
   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000
| SNOEB: Initial snow water content in elevation band [mm]
     0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0
           0.000    | PLAPS : Precipitation lapse rate [mm/km]
           0.000    | TLAPS : Temperature lapse rate [��C/km]
           0.000    | SNO_SUB : Initial snow water content [mm]
Tributary Channels
          19.448    | CH_L1 : Longest tributary channel length [km]
           0.026    | CH_S1 : Average slope of tributary channel [m/m]
          23.374    | CH_W1 : Average width of tributary channel [m]
           0.000    | CH_K1 : Effective hydraulic conductivity in tributary channel [mm/hr]
           0.014    | CH_N1 : Manning's "n" value for the tributary channels
Impoundments
000010000.pnd       | PNDFILE: name of subbasin impoundment file
Consumptive Water Use
000010000.wus       | WUSFILE: name of subbasin water use file
Climate Change
         330.000    | CO2 : Carbon dioxide concentration [ppmv]
| RFINC:  Climate change monthly rainfall adjustment (January - June)
   0.000   0.000   0.000   0.000   0.000   0.000
| RFINC:  Climate change monthly rainfall adjustment (July - December)
   0.000   0.000   0.000   0.000   0.000   0.000
| TMPINC: Climate change monthly temperature adjustment (January - June)
   0.000   0.000   0.000   0.000   0.000   0.000
| TMPINC: Climate change monthly temperature adjustment (July - December)
   0.000   0.000   0.000   0.000   0.000   0.000
| RADINC: Climate change monthly radiation adjustment (January - June)
   0.000   0.000   0.000   0.000   0.000   0.000
| RADINC: Climate change monthly radiation adjustment (July - December)
   0.000   0.000   0.000   0.000   0.000   0.000
| HUMINC: Climate change monthly humidity adjustment (January - June)
   0.000   0.000   0.000   0.000   0.000   0.000
| HUMINC: Climate change monthly humidity adjustment (July - December)
   0.000   0.000   0.000   0.000   0.000   0.000
| HRU data
               3    | HRUTOT : Total number of HRUs modeled in subbasin

HRU: Depressional Storage/Pothole

Floodplain

HRU: Riparian

HRU: General
000010001.hru000010001.mgt000010001.sol000010001.chm 000010001.gw             000010001.sep
000010002.hru000010002.mgt000010002.sol000010002.chm 000010002.gw             000010002.sep
000010003.hru000010003.mgt000010003.sol000010003.chm 000010003.gw             000010003.sep
'''
