import os
import re
import numpy as np
import codecs



#swat-io-document
#https://docs.python.org/3/library/re.html

class HRU_RTE(object):
    #
    def __init__(self):
        pass
    def __del__(self):
        pass
    #
    def read(self,filepath):
        #data
        with open(filepath,'r',encoding='unicode_escape') as fh:
            lns = fh.readlines()
            lns = [ln.rstrip() for ln in lns]
        #data type - Variable name, Line#, Format, F90 Format
        meta = [
            ['TITLE', 1, 'character', 'a80'],
            ['CH_W2', 2, 'real', 'free'],
            ['CH_D', 3, 'real', 'free'],
            ['CH_S2', 4, 'real', 'free'],
            ['CH_L2', 5, 'real', 'free'],
            ['CH_N2', 6, 'real', 'free'],
            ['CH_K2', 7, 'real', 'free'],
            ['CH_COV1', 8, 'real', 'free'],
            ['CH_COV2', 9, 'real', 'free'],
            ['CH_WDR', 10, 'real', 'free'],
            ['ALPHA_BNK', 11, 'real', 'free'],
            ['ICANAL', 12, 'integer', 'free'],
            ['CH_ONCO', 13, 'real', 'free'],
            ['CH_OPCO', 14, 'real', 'free'],
            ['CH_SIDE', 15, 'real', 'free'],
            ['CH_BNK_BD', 16, 'real', 'free'],
            ['CH_BED_BD', 17, 'real', 'free'],
            ['CH_BNK_KD', 18, 'real', 'free'],
            ['CH_BED_KD', 19, 'real', 'free'],
            ['CH_BNK_D50', 20, 'real', 'free'],
            ['CH_BED_D50', 21, 'real', 'free'],
            ['CH_BNK_TC', 22, 'real', 'free'],
            ['CH_BED_TC', 23, 'real', 'free'], 
            ['special',24],             
            ['CH_EQN', 25, 'integer', 'free'],
            ['PRF', 26, 'integer', 'free'],
            ['SPCON', 27, 'real', 'free'],
            ['SPEXP', 28, 'real', 'free'],
            ['special',29],
            ['SALT_DEL', 30, 'real', 'free'],       
            
        ]
        meta_desc = []
        special=[]
        #
        param = {}
        for i in range(len(lns)):
            # print(i,'------------------')
            #TITLE, P.256
            if i==0:
                meta_desc.append(lns[i])
                s = re.sub('(\s*:\s*)', ':', lns[i])
                subbasin = [v.strip() for v in re.search('Subbasin\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                param[subbasin[0]]=subbasin[1]
                # re.search('[0-9]{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', s,re.IGNORECASE)
                # re.search('ArcSWAT\s+[0-9]{4}\.\d+_\d+\.\d+', s,re.IGNORECASE)
                # selected = re.findall('([A-Za-z]+:[0-9]+-?[0-9]+)', s)
                # selected = re.findall('([A-Za-z]+:[0-9]+\-?\d+)', s)
                # param.extend([v.split(':') for v in selected])
            #MGT_OP, P.259
            else :
                if re.match(r'\s*\d+(\.\d+)?\s*\|\s*[A-Z]+\w*\s*:.*', lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split('|')[-1].split(':',maxsplit=1)[-1].strip())
                    s = re.sub('(\s*:\s*)', ':', lns[i])
                    val = s.split('|')[0].strip()
                    if 0<i<23 or 23<i<28 or i==29:
                        var = meta[i][0]
                        if meta[i][2].lower()=='integer':
                            val = int('%.0f' % float(val))
                        elif meta[i][2].lower()=='real':
                            val = float(val)                  
                    param[var]=val
                #Comment line
                elif i ==23:
                    special.append(lns[i].split('  ')[1:])
                elif i == 28:
                    try:
                        param[lns[i].split('|')[1].split(' :  ')[0].strip()]=lns[i].split('|')[0].split('  ',maxsplit=12)[1:]
                        meta_desc.append(lns[i].split('|')[1].split(' : ')[1])
                    except Exception as e:
                        param.extend([[lns[i].split('|')[1].split(': ')[0],lns[i].split('|')[0].split('  ',maxsplit=12)[1:]]])
                        meta_desc.append(lns[i].split('|')[1].split(': ')[1])
        return meta,meta_desc,param,special
    
    def write(self,all,outfile):
        head1=all[1][0]
        rte1=all[2]
        ###########################end
        # 第二部分#####################
        illurstration1=all[1][1]
        line1=str(format(rte1['CH_W2'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_W2')+" "+":"+" "+str(illurstration1)
        #
        illurstration2=all[1][2]
        line2=str(format(rte1['CH_D'],'.3f')).rjust(14,' ')+"    "+"| "+str('CH_D')+" "+":"+" "+str(illurstration2)
        #
        illurstration3=all[1][3]
        line3=str(format(rte1['CH_S2'], '.4f')).rjust(14,' ')+"    "+"| "+str('CH_S2')+" "+":"+" "+str(illurstration3)
        #
        illurstration4=all[1][4]
        line4=str(format(rte1['CH_L2'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_L2')+" "+":"+" "+str(illurstration4)
        #
        illurstration5=all[1][5]
        line5=str(format(rte1['CH_N2'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_N2')+" "+":"+" "+str(illurstration5)
        #
        illurstration6=all[1][6]
        line6=str(format(rte1['CH_K2'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_K2')+" "+":"+" "+str(illurstration6)
        #
        illurstration7=all[1][7]
        line7=str(format(rte1['CH_COV1'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_COV1')+":"+" "+str(illurstration7)
        #
        illurstration8=all[1][8]
        line8=str(format(rte1['CH_COV2'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_COV2')+" "+":"+" "+str(illurstration8)
        #
        illurstration9=all[1][9]
        line9=str(format(rte1['CH_WDR'], '.3f')).rjust(14,' ')+"    "+"| "+str('CH_WDR')+" "+":"+" "+str(illurstration9)
        #
        illurstration10=all[1][10]
        line10=str(format(rte1['ALPHA_BNK'], '.3f')).rjust(14,' ')+"    "+"| "+str('ALPHA_BNK')+" "+":"+" "+str(illurstration10)
        #
        illurstration11=all[1][11]
        line11=str(format(rte1['ICANAL'], 'd')).rjust(14,' ')+"    "+"| "+str('ICANAL')+" "+":"+" "+str(illurstration11)
        #
        illurstration12=all[1][12]
        line12=str(format(rte1['CH_ONCO'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_ONCO')+" "+":"+" "+str(illurstration12)
        #
        illurstration13=all[1][13]
        line13=str(format(rte1['CH_OPCO'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_OPCO')+" "+":"+" "+str(illurstration13)
        #
        illurstration14=all[1][14]
        line14=str(format(rte1['CH_SIDE'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_SIDE')+" "+":"+" "+str(illurstration14)
        #
        illurstration15=all[1][15]
        line15=str(format(rte1['CH_BNK_BD'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BNK_BD')+" "+":"+" "+str(illurstration15)
        #
        illurstration16=all[1][16]
        line16=str(format(rte1['CH_BED_BD'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BED_BD')+" "+":"+" "+str(illurstration16)
        #
        illurstration17=all[1][17]
        line17=str(format(rte1['CH_BNK_KD'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BNK_KD')+" "+":"+" "+str(illurstration17)
        #
        illurstration18=all[1][18]
        line18=str(format(rte1['CH_BED_KD'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BED_KD')+" "+":"+" "+str(illurstration18)
        #
        illurstration19=all[1][19]
        line19=str(format(rte1['CH_BNK_D50'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BNK_D50')+" "+":"+" "+str(illurstration19)
        #
        illurstration20=all[1][20]
        line20=str(format(rte1['CH_BED_D50'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BED_D50')+" "+":"+" "+str(illurstration20)
        #
        illurstration21=all[1][21]
        line21=str(format(rte1['CH_BNK_TC'], '.2f')).rjust(14,' ')+"    "+"| "+str('CH_BNK_TC')+" "+":"+" "+str(illurstration21)
        #
        illurstration22=all[1][22]
        line22=str(format(rte1['CH_BED_TC'],'.2f')).rjust(14,' ')+"    "+"| "+str('CH_BED_TC')+" "+":"+" "+str(illurstration22)
        #
        spec=[]
        for i in all[3][0]:
            spec.append(str(format(float(i),'.2f')).rjust(6,' '))
        line23="".join(spec)
        #
        illurstration24=all[1][23]
        line24=str(format(rte1['CH_EQN'],'d')).rjust(14,' ')+"    "+"| "+str('CH_EQN')+":"+" "+str(illurstration24)
        #
        try:
            illurstration25=all[1][24]
            line25=str(format(rte1['PRF'],'.2f')).rjust(14,' ')+"    "+"| "+str('PRF')+":"+" "+str(illurstration25)
            #
            illurstration26=all[1][25]
            line26=str(format(rte1['SPCON'],'.4f')).rjust(14,' ')+"    "+"| "+str('SPCON')+":"+" "+str(illurstration26)
            #
            illurstration27=all[1][26]
            line27=str(format(rte1['SPEXP'],'.2f')).rjust(14,' ')+"    "+"| "+str('SPEXP')+":"+" "+str(illurstration27)
            #
            illurstration28=all[1][27]
            
            HRU_SALT=[]
            for i in rte1['HRU_SALT']:
                HRU_SALT.append(str(format(float(i),'.2f')).rjust(6,' '))
            number28="".join(HRU_SALT)
            line28=str(number28)+""+"|"+str('HRU_SALT')+":"+" "+str(illurstration28)
            #
            illurstration29=all[1][28]
            line29=str(format(rte1['SALT_DEL'],'.1f')).rjust(14,' ')+"    "+"| "+str('SALT_DEL')+":"+" "+str(illurstration29)
        #
        except:
            pass
            # print("该数据缺少变量")
        ##################end
        #输出文件
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
        object.write(line18+'\n')
        object.write(line19+'\n')
        object.write(line20+'\n')
        object.write(line21+'\n')
        object.write(line22+'\n')
        object.write(line23+'\n')
        object.write(line24+'\n')
        try:
            object.write(line25+'\n')
            object.write(line26+'\n')
            object.write(line27+'\n')
            object.write(line28+'\n')
            object.write(line29+'\n')
        except:
            pass
                # print("该数据缺少变量")
        object.close()

"""""""""
 .rte file Subbasin: 2 2022/2/9 0:00:00 ArcSWAT 2012.10_6.24
        24.391    | CHW2 : Main channel width [m]
         0.923    | CHD : Main channel depth [m]
       0.00261    | CH_S2 : Main channel slope [m/m]
         4.221    | CH_L2 : Main channel length [km]
         0.014    | CH_N2 : Manning's nvalue for main channel
         0.000    | CH_K2 : Effective hydraulic conductivity [mm/hr]
         0.000    | CH_COV1: Channel erodibility factor
         0.000    | CH_COV2 : Channel cover factor
        26.436    | CH_WDR : Channel width:depth ratio [m/m]
         0.000    | ALPHA_BNK : Baseflow alpha factor for bank storage [days]
          0.00    | ICANAL : Code for irrigation canal
          0.00    | CH_ONCO : Organic nitrogen concentration in the channel [ppm]
          0.00    | CH_OPCO : Organic phosphorus concentration in the channel [ppm]
          0.00    | CH_SIDE : Change in horizontal distance per unit vertical distance
          0.00    | CH_BNK_BD : Bulk density of channel bank sediment (g/cc)
          0.00    | CH_BED_BD : Bulk density of channel bed sediment (g/cc)
          0.00    | CH_BNK_KD : Erodibility of channel bank sediment by jet test (cm3/N-s)
          0.00    | CH_BED_KD : Erodibility of channel bed sediment by jet test (cm3/N-s)
          0.00    | CH_BNK_D50 : D50 Median particle size diameter of channel bank sediment (��m)
          0.00    | CH_BED_D50 : D50 Median particle size diameter of channel bed sediment (��m)
          0.00    | CH_BNK_TC : Critical shear stress of channel bank (N/m2)
          0.00    | CH_BED_TC : Critical shear stress of channel bed (N/m2)
  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00
             0    | CH_EQN : Sediment routing methods
          1.00    | PRF :  Peak rate adjustment factor for sediment routing in the main channel
        0.0001    | SPCON :  Linear parameter for calculating the maximum amount of sediment that can be reentrained during channel sediment routing
          1.00    | SPEXP :  Exponent parameter for calculating sediment reentrained in channel sediment routing.
  1.00  1.00  1.00  1.00  1.00  1.00  1.00  1.00  1.00  1.00  1.00  1.00| HRU_SALT :  Monthly adjustment factors for HRU salt loadings.
         1.000    |SALT_DEL :  Salt delivery ratio in reach

"""""""""

