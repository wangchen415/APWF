import os
import re
import numpy as np
import codecs


# basedir = 'txtinout'
# filename = '000010001.sol'
# filepath = os.path.join(basedir,filename)

#swat-io-document
#https://docs.python.org/3/library/re.html

class HRU_SOL(object):
    #
    def __init__(self):
        pass
    def __del__(self):
        pass
    #
    #read from '000010002.sol'
    def read(self,filepath):
        #data
        with open(filepath) as fh:
            lns = fh.readlines()
            lns = [ln.rstrip() for ln in lns]
        #data type - Variable name, Line#, Format, F90 Format
        meta = [
            ['TITLE', 1, 'character', 'a80'],
            ['Soil Name', 2, 'character', 'a16'],
            ['Soil Hydrologic Group', 3, 'character', 'a1'],
            ['SOL_ZMX', 4, 'decimal(xxxxxxxxx.xx)', 'f12.2'],
            ['ANION_EXCL', 5, 'integerdecimal(x.xxx)', 'f5.3'],
            ['SOL_CRK', 6, 'decimal(x.xxx)', 'f5.3'],
            ['Texture 1', 7, 'character', 'a80'],
            
        ]
        meta_desc = []
        #
        param = {}
        param_sol_op = {}
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
                # re.search('[0-9]{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', s,re.IGNORECASE)
                # re.search('ArcSWAT\s+[0-9]{4}\.\d+_\d+\.\d+', s,re.IGNORECASE)
                # selected = re.findall('([A-Za-z]+:[0-9]+-?[0-9]+)', s)
                # selected = re.findall('([A-Za-z]+:[0-9]+\-?\d+)', s)
                # param.extend([v.split(':') for v in selected])
            elif i>=7:
                if re.match(r'\s*\w+.*:\s*\d+.*', lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split(':')[-2].strip())
                    val = lns[i].split(':')[-1].strip()
                    var = lns[i].split(':')[0].strip()
                    nval=[]
                    nval =re.findall(r"\d+\.?\d*",val)
                    param_sol_op[var]=nval
                else:
                    meta_desc.append(lns[i])
                
            if 0<i<7:
                #
                if re.match(r'\s*.*:\s*\d+.*', lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split(':')[-2].strip())
                    s = re.sub('(\s*:\s*)', ':', lns[i])
                    val = s.split(':')[1].strip()
                    var = meta[i][0]
                    val = float(val)
                    param[var]=val
                elif re.match(r'\s*.*:\s*\w+.*', lns[i], re.DOTALL):
                    var = meta[i][0]
                    w=re.sub('(\s*:\s*)', ':', lns[i])
                    val = w.split(':')[1].strip()
                    val = str(val)
                    param[var]=val
                #Comment line
                else:
                        meta_desc.append(lns[i])
        return meta,meta_desc,param,param_sol_op
    #
    #save to '000010002.sol'
    def write(self,all,outfile):
        # 第一部分########################
        head1=all[1][0]
        sol1=all[2]
        sol2=all[3]
        ###########################end
        # 第二部分#####################
        line1=" "+'Soil Name'+": "+str(sol1['Soil Name'])
        #
        line2=" "+'Soil Hydrologic Group'+": "+str(sol1['Soil Hydrologic Group'])
        #
        element3=all[1][1]
        line3=" "+str(element3)+" "+": "+str(format(sol1['SOL_ZMX'],'.2f'))
        #
        element4=all[1][2]
        line4=" "+str(element4)+": "+str(format(sol1['ANION_EXCL'],'.3f'))
        #
        element5=all[1][3]
        line5=" "+str(element5)+": "+str(format(sol1['SOL_CRK'],'.3f'))
        #
        line6=" "+'Texture 1'+": "+str(sol1['Texture 1'])
        #
        number7=sol2['Depth                [mm]']
        number7_1=''.join(str(j).rjust(12,' ') for j in number7)
        line7=" "+str('Depth                [mm]')+":"+str(number7_1)
        #
        number8=sol2['Bulk Density Moist [g/cc]']
        number8_1=''.join(str(j).rjust(12,' ') for j in number8)
        line8=" "+str('Bulk Density Moist [g/cc]')+":"+str(number8_1)
        #
        number9=sol2['Ave. AW Incl. Rock Frag']
        number9_1=''.join(str(j).rjust(12,' ') for j in number9)
        line9=" "+str('Ave. AW Incl. Rock Frag')+"  "+":"+str(number9_1)
        #
        number10=sol2['Ksat. (est.)      [mm/hr]']
        number10_1=''.join(str(j).rjust(12,' ') for j in number10)
        line10=" "+str('Ksat. (est.)      [mm/hr]')+":"+str(number10_1)
        #
        number11=sol2['Organic Carbon [weight %]']
        number11_1=''.join(str(j).rjust(12,' ') for j in number11)
        line11=" "+str('Organic Carbon [weight %]')+":"+str(number11_1)
        #
        number12=sol2['Clay           [weight %]']
        number12_1=''.join(str(j).rjust(12,' ') for j in number12)
        line12=" "+str('Clay           [weight %]')+":"+str(number12_1)
        #
        number13=sol2['Silt           [weight %]']
        number13_1=''.join(str(j).rjust(12,' ') for j in number13)
        line13=" "+str('Silt           [weight %]')+":"+str(number13_1)
        #
        number14=sol2['Sand           [weight %]']
        number14_1=''.join(str(j).rjust(12,' ') for j in number14)
        line14=" "+str('Sand           [weight %]')+":"+str(number14_1)
        #
        number15=sol2['Rock Fragments   [vol. %]']
        number15_1=''.join(str(j).rjust(12,' ') for j in number15)
        line15=" "+str('Rock Fragments   [vol. %]')+":"+str(number15_1)
        #
        number16=sol2['Soil Albedo (Moist)']
        number16_1=''.join(str(j).rjust(12,' ') for j in number16)
        line16=" "+str('Soil Albedo (Moist)')+"      "+":"+str(number16_1)
        #
        number17=sol2['Erosion K']
        number17_1=''.join(str(j).rjust(12,' ') for j in number17)
        line17=" "+str('Erosion K')+"                "+":"+str(number17_1)
        #
        number18=sol2['Salinity (EC, Form 5)']
        number18_1=''.join(str(j).rjust(12,' ') for j in number18)
        line18=" "+str('Salinity (EC, Form 5)')+"    "+":"+str(number18_1)
        #
        try:
            number19=sol2['Soil pH']
            number19_1=''.join(str(j).rjust(12,' ') for j in number19)
            line19=" "+str('Soil pH')+"                  "+":"+str(number19_1)
        #
            number20=sol2['Soil CACO3']
            number20_1=''.join(str(j).rjust(12,' ') for j in number20)
            line20=" "+str('Soil CACO3')+"               "+":"+str(number20_1)
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
        object.write(line16+'\n')
        object.write(line17+'\n')
        try:
            object.write(line18+'\n')
            object.write(line19+'\n')
            object.write(line20+'\n')
        except:
            print("该数据缺少变量")
        object.write('	                              ')
        # for i in range(len(OS2)):
        #     #    for j in range(len(OS2[i])):
        #         str1 = ' '.join(OS2[i])
        #         object.write(str1+'\n')
        object.close()

'''
 .Sol file Watershed HRU:1 Subbasin:1 HRU:1 Luse:RNGE Soil: GRIDCODE1 Slope: 0-9999 2023/3/11 0:00:00 ArcSWAT 2012.10_6.24
 Soil Name: GRIDCODE1
 Soil Hydrologic Group: B
 Maximum rooting depth(mm) : 2000.00
 Porosity fraction from which anions are excluded: 0.500
 Crack volume potential of soil: 0.500
Depth                [mm] 
 Depth                [mm]:       50.00      150.00      300.00      600.00     1000.00     2000.00
 Bulk Density Moist [g/cc]:        2.94        2.94        2.97        2.99        2.99        3.03
 Ave. AW Incl. Rock Frag  :        0.04        0.04        0.04        0.04        0.04        0.04
 Ksat. (est.)      [mm/hr]:       29.62       29.62       25.64       20.39       17.92       26.25
 Organic Carbon [weight %]:        0.93        0.87        0.72        0.55        0.47        0.42
 Clay           [weight %]:       12.49       12.42       12.32       13.20       13.04       10.44
 Silt           [weight %]:       47.43       47.19       49.90       50.40       54.06       51.61
 Sand           [weight %]:       40.08       40.38       37.78       36.40       32.90       37.95
 Rock Fragments   [vol. %]:        4.00        4.00        6.00        8.00       10.00        9.00
 Soil Albedo (Moist)      :        0.01        0.01        0.01        0.01        0.00        0.01
 Erosion K                :        0.33        0.33        0.35        0.36        0.37        0.36
 Salinity (EC, Form 5)    :        0.00        0.00        0.00        0.00        0.00        0.00
 Soil pH                  :        0.00        0.00        0.00        0.00        0.00        0.00
 Soil CACO3               :        0.00        0.00        0.00        0.00        0.00        0.00
	                              
'''