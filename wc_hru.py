import os
import re
import numpy as np
import codecs


# basedir = 'txtinout'
# filename = '000010001.hru'
# filepath = os.path.join(basedir,filename)

#swat-io-document
#https://docs.python.org/3/library/re.html

class HRU_HRU(object):
    #
    def __init__(self):
        pass
    def __del__(self):
        pass
    #
    def read(self,filepath):
        #data
        with open(filepath) as fh:
            lns = fh.readlines()
            lns = [ln.rstrip() for ln in lns]
        #data type - Variable name, Line#, Format, F90 Format
        meta = [
            ['TITLE', 1, 'character', 'a80'],
            ['HRU_FR', 2, 'real', 'free'],
            ['SLSUBBSN', 3, 'real', 'free'],
            ['HRU_SLP', 4, 'real', 'free'],
            ['OV_N', 5, 'real', 'free'],
            ['LAT_TTIME', 6, 'real', 'free'],
            ['LAT_SED', 7, 'real', 'free'],
            ['SLSOIL', 8, 'real', 'free'],
            ['CANMX', 9, 'real', 'free'],
            ['ESCO', 10, 'real', 'free'],
            ['EPCO', 11, 'real', 'free'],
            ['RSDIN', 12, 'real', 'free'],
            ['ERORGN', 13, 'real', 'free'],
            ['ERORGP', 14, 'real', 'free'],
            ['POT_FR', 15, 'real', 'free'],
            ['FLD_FR', 16, 'real', 'free'],
            ['RIP_FR', 17, 'real', 'free'],
            ['Comment line', 18, 'character', 'a80'],
            ['POT_TILE', 19, 'real', 'free'],
            ['POT_VOLX', 20, 'real', 'free'],
            ['POT_VOL', 21, 'real', 'free'],
            ['POT_NSED', 22, 'real', 'free'],
            ['POT_NO3L', 23, 'real', 'free'],
            ['DEP_IMP', 24, 'integer', 'free'],
            ['EVPOT', 28, 'real', 'free'],
            ['DIS_STREAM', 29, 'real', 'free'],
            ['CF', 30, 'real', 'free'],
            ['CFH', 31, 'real', 'free'],
            ['CFDEC', 32, 'real', 'free'],
            ['SED_CON', 33, 'real', 'free'],
            ['ORGN_CON', 34, 'real', 'free'],
            ['ORGP_CON', 35, 'real', 'free'],
            ['SOLN_CON', 36, 'real', 'free'],
            ['SOLP_CON', 37, 'real', 'free'],
            ['POT_SOLP', 38, 'real', 'free'],
            ['POT_K', 39, 'real', 'free'],
            ['N_REDUC', 40, 'real', 'free'],
            ['N_LAG', 41, 'real', 'free'],
            ['N_LN', 42, 'real', 'free'],
            ['N_LNCO', 43, 'real', 'free'],
            ['SURLAG', 44, 'real', 'free'],
            ['R2ADJ', 45, 'real', 'free'],
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
                slope = [v.strip() for v in re.search('Slope\s*:?\s*\d+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
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
            #MGT_OP, P.259
            else :
                if re.match(r'\s*\d+(\.\d+)?\s*\|\s*[A-Z]+\w*\s*:.*', lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split('|')[-1].split(':',maxsplit=1)[-1].strip())
                    s = re.sub('(\s*:\s*)', ':', lns[i])
                    val = s.split('|')[0].strip()
                    if i<24:
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
                #Comment line
                else:
                    meta_desc.append(lns[i])
        return meta,meta_desc,param
    
    def write(self,all,outfile):

        head1=all[1][0]
        hru1=all[2]
        ###########################end
        # 第二部分#####################
        illurstration1=all[1][1]
        line1=str(hru1['HRU_FR']).rjust(16,' ')+"    "+"| "+str('HRU_FR')+" "+":"+" "+str(illurstration1)
        #
        illurstration2=all[1][2]
        line2=str(format(hru1['SLSUBBSN'],'.1f')).rjust(16,' ')+"    "+"| "+str('SLSUBBSN')+" "+":"+" "+str(illurstration2)
        #
        illurstration3=all[1][3]
        line3=str(format(hru1['HRU_SLP'], '.3f')).rjust(16,' ')+"    "+"| "+str('HRU_SLP')+" "+":"+" "+str(illurstration3)
        #
        illurstration4=all[1][4]
        line4=str(format(hru1['OV_N'], '.3f')).rjust(16,' ')+"    "+"| "+str('OV_N')+" "+":"+" "+str(illurstration4)
        #
        illurstration5=all[1][5]
        line5=str(format(hru1['LAT_TTIME'], '.3f')).rjust(16,' ')+"    "+"| "+str('LAT_TTIME')+" "+":"+" "+str(illurstration5)
        #
        illurstration6=all[1][6]
        line6=str(format(hru1['LAT_SED'], '.3f')).rjust(16,' ')+"    "+"| "+str('LAT_SED')+" "+":"+" "+str(illurstration6)
        #
        illurstration7=all[1][7]
        line7=str(format(hru1['SLSOIL'], '.3f')).rjust(16,' ')+"    "+"| "+str('SLSOIL')+" "+":"+" "+str(illurstration7)
        #
        illurstration8=all[1][8]
        line8=str(format(hru1['CANMX'], '.3f')).rjust(16,' ')+"    "+"| "+str('CANMX')+" "+":"+" "+str(illurstration8)
        #
        illurstration9=all[1][9]
        line9=str(format(hru1['ESCO'], '.3f')).rjust(16,' ')+"    "+"| "+str('ESCO')+" "+":"+" "+str(illurstration9)
        #
        illurstration10=all[1][10]
        line10=str(format(hru1['EPCO'], '.3f')).rjust(16,' ')+"    "+"| "+str('EPCO')+" "+":"+" "+str(illurstration10)
        #
        illurstration11=all[1][11]
        line11=str(format(hru1['RSDIN'], '.3f')).rjust(16,' ')+"    "+"| "+str('RSDIN')+" "+":"+" "+str(illurstration11)
        #
        illurstration12=all[1][12]
        line12=str(format(hru1['ERORGN'], '.3f')).rjust(16,' ')+"    "+"| "+str('ERORGN')+" "+":"+" "+str(illurstration12)
        #
        illurstration13=all[1][13]
        line13=str(format(hru1['ERORGP'], '.3f')).rjust(16,' ')+"    "+"| "+str('ERORGP')+" "+":"+" "+str(illurstration13)
        #
        illurstration14=all[1][14]
        line14=str(format(hru1['POT_FR'], '.3f')).rjust(16,' ')+"    "+"| "+str('POT_FR')+" "+":"+" "+str(illurstration14)
        #
        illurstration15=all[1][15]
        line15=str(format(hru1['FLD_FR'], '.3f')).rjust(16,' ')+"    "+"| "+str('FLD_FR')+" "+":"+" "+str(illurstration15)
        #
        illurstration16=all[1][16]
        line16=str(format(hru1['RIP_FR'], '.3f')).rjust(16,' ')+"    "+"| "+str('RIP_FR')+" "+":"+" "+str(illurstration16)
        #
        head2=all[1][17]
        #
        illurstration17=all[1][18]
        line17=str(format(hru1['POT_TILE'], '.3f')).rjust(16,' ')+"    "+"| "+str('POT_TILE')+" "+":"+" "+str(illurstration17)
        #
        illurstration18=all[1][19]
        line18=str(format(hru1['POT_VOLX'], '.3f')).rjust(16,' ')+"    "+"| "+str('POT_VOLX')+" "+":"+" "+str(illurstration18)
        #
        illurstration19=all[1][20]
        line19=str(format(hru1['POT_VOL'], '.3f')).rjust(16,' ')+"    "+"| "+str('POT_VOL')+" "+":"+" "+str(illurstration19)
        #
        illurstration20=all[1][21]
        line20=str(format(hru1['POT_NSED'], '.3f')).rjust(16,' ')+"    "+"| "+str('POT_NSED')+" "+":"+" "+str(illurstration20)
        #
        illurstration21=all[1][22]
        line21=str(format(hru1['POT_NO3L'], '.3f')).rjust(16,' ')+"    "+"| "+str('POT_NO3L')+" "+":"+" "+str(illurstration21)
        #
        illurstration22=all[1][23]
        line22=str(format(hru1['DEP_IMP'],'.0f')).rjust(16,' ')+"    "+"| "+str('DEP_IMP')+" "+":"+" "+str(illurstration22)
        #
        #
        illurstration23=all[1][27]
        line23=str(format(hru1['EVPOT'],'.1f')).rjust(16,' ')+"    "+"| "+str('EVPOT')+":"+" "+str(illurstration23)
        #
        illurstration24=all[1][28]
        line24=str(format(hru1['DIS_STREAM'],'.1f')).rjust(16,' ')+"    "+"| "+str('DIS_STREAM')+":"+" "+str(illurstration24)
        #
        illurstration25=all[1][29]
        line25=str(format(hru1['CF'],'.1f')).rjust(16,' ')+"    "+"| "+str('CF')+":"+" "+str(illurstration25)
        #
        illurstration26=all[1][30]
        line26=str(format(hru1['CFH'],'.1f')).rjust(16,' ')+"    "+"| "+str('CFH')+":"+" "+str(illurstration26)
        #
        illurstration27=all[1][31]
        line27=str(format(hru1['CFDEC'],'.3f')).rjust(16,' ')+"    "+"| "+str('CFDEC')+":"+" "+str(illurstration27)
        #
        illurstration28=all[1][32]
        line28=str(format(hru1['SED_CON'],'.1f')).rjust(16,' ')+"    "+"| "+str('SED_CON')+":"+" "+str(illurstration28)
        #
        illurstration29=all[1][33]
        line29=str(format(hru1['ORGN_CON'],'.1f')).rjust(16,' ')+"    "+"| "+str('ORGN_CON')+":"+" "+str(illurstration29)
        #
        illurstration30=all[1][34]
        line30=str(format(hru1['ORGP_CON'],'.1f')).rjust(16,' ')+"    "+"| "+str('ORGP_CON')+":"+" "+str(illurstration30)
        #
        illurstration31=all[1][35]
        line31=str(format(hru1['SOLN_CON'],'.1f')).rjust(16,' ')+"    "+"| "+str('SOLN_CON')+":"+" "+str(illurstration31)
        #
        illurstration32=all[1][36]
        line32=str(format(hru1['SOLP_CON'],'.1f')).rjust(16,' ')+"    "+"| "+str('SOLP_CON')+":"+" "+str(illurstration32)
        #
        try:
            illurstration33=all[1][37]
            line33=str(format(hru1['POT_SOLP'],'.1f')).rjust(16,' ')+"    "+"| "+str('POT_SOLP')+":"+" "+str(illurstration33)
                    #
            illurstration34=all[1][38]
            line34=str(format(hru1['POT_K'],'.1f')).rjust(16,' ')+"    "+"| "+str('POT_K')+":"+" "+str(illurstration34)
            #
            illurstration35=all[1][39]
            line35=str(format(hru1['N_REDUC'],'.1f')).rjust(16,' ')+"    "+"| "+str('N_REDUC')+":"+" "+str(illurstration35)
            #
            illurstration36=all[1][40]
            line36=str(format(hru1['N_LAG'],'.1f')).rjust(16,' ')+"    "+"| "+str('N_LAG')+":"+" "+str(illurstration36)
            #
            illurstration37=all[1][41]
            line37=str(format(hru1['N_LN'],'.1f')).rjust(16,' ')+"    "+"| "+str('N_LN')+":"+" "+str(illurstration37)
            #
            illurstration38=all[1][42]
            line38=str(format(hru1['N_LNCO'],'.1f')).rjust(16,' ')+"    "+"| "+str('N_LNCO')+":"+" "+str(illurstration38)
            #
            illurstration39=all[1][43]
            line39=str(format(hru1['SURLAG'],'.1f')).rjust(16,' ')+"    "+"| "+str('SURLAG')+":"+" "+str(illurstration39)
            #
            illurstration40=all[1][44]
            line40=str(format(hru1['R2ADJ'],'.1f')).rjust(16,' ')+"    "+"| "+str('R2ADJ')+":"+" "+str(illurstration40)
        except:
            print("该数据缺少变量")
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
        object.write(head2+'\n')
        object.write(line17+'\n')
        object.write(line18+'\n')
        object.write(line19+'\n')
        object.write(line20+'\n')
        object.write(line21+'\n')
        object.write(line22+'\n')
        object.write('\n')
        object.write('\n')
        object.write('\n')
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
        try:
            object.write(line33+'\n')
            object.write(line34+'\n')
            object.write(line35+'\n')
            object.write(line36+'\n')
            object.write(line37+'\n')
            object.write(line38+'\n')
            object.write(line39+'\n')
            object.write(line40+'\n')
        except:
             print("该数据缺少变量")

"""""""""
 .hru file Watershed HRU:1 Subbasin:1 HRU:1 Luse:AGRL Soil: HONGRANG1 Slope: 0-9999 2018/2/5 0:00:00 ArcSWAT 2012.10_3.19
       0.0329277    | HRU_FR : Fraction of subbasin area contained in HRU
          60.976    | SLSUBBSN : Average slope length [m]
           0.112    | HRU_SLP : Average slope stepness [m/m]
           0.140    | OV_N : Manning's "n" value for overland flow
           0.000    | LAT_TTIME : Lateral flow travel time [days]
           0.000    | LAT_SED : Sediment concentration in lateral flow and groundwater flow [mg/l]
           0.000    | SLSOIL : Slope length for lateral subsurface flow [m]
           0.000    | CANMX : Maximum canopy storage [mm]
           0.950    | ESCO : Soil evaporation compensation factor
           1.000    | EPCO : Plant uptake compensation factor
           0.000    | RSDIN : Initial residue cover [kg/ha]
           0.000    | ERORGN : Organic N enrichment ratio
           0.000    | ERORGP : Organic P enrichment ratio
           0.000    | POT_FR : Fraction of HRU are that drains into pothole
           0.000    | FLD_FR : Fraction of HRU that drains into floodplain
           0.000    | RIP_FR : Fraction of HRU that drains into riparian zone
Special HRU: Pothole
           0.000    | POT_TILE : Average daily outflow to main channel from tile flow (depth [mm] over entire HRU)
           0.000    | POT_VOLX : Maximum volume of water stored in the pothole (depth [mm] over entire HRU)
           0.000    | POT_VOL : Initial volume of water stored in the pothole (depth [mm] over entire HRU)
           0.000    | POT_NSED : Normal sediment concentration in pothole [mg/l]
           0.000    | POT_NO3L : Nitrate decay rate in pothole [1/day]
            6000    | DEP_IMP : Depth to impervious layer in soil profile [mm]



             0.5    | EVPOT: Pothole evaporation coefficient
            35.0    | DIS_STREAM: Average distance to stream [m]
             1.0    | CF: Decomposition response to soil temperature and moisture
             1.0    | CFH: Maximum humification rate
           0.055    | CFDEC: Undistrurbed soil turnover rate under optimum soil water and temperature
             0.0    | SED_CON: Sediment concentration in runoff, after urban BMP is applied
             0.0    | ORGN_CON: Organic nitrogen concentration in runoff, after urban BMP is applied
             0.0    | ORGP_CON: Organic phosphorus concentration in runoff, after urban BMP is applied
             0.0    | SOLN_CON: Soluble nitrogen concentration un runoff, after urban BMP is applied
             0.0    | SOLP_CON: Soluble phosphorus concentration in runoff, after urban BMP is applied
             0.0    | POT_SOLP: Soluble P loss rate in the pothole
             0.0    | POT_K: Hydraulic conductivity of soil surface of  pothole
           300.0    | N_REDUC: Nitrogen uptake reduction factor not currently used
             0.3    | N_LAG: Lag coefficient for calculating nitrate concentration in subsurface drains
             2.0    | N_LN: Power function exponent for calculating nitrate concentration in subsurface drains
             2.0    | N_LNCO: Coefficient for power function for calculating nitrate concentration in subsurface drains
             2.0    | SURLAG: Surface runoff lag time in the HRU (days)
             1.0    | R2ADJ: Curve number retention parameter adjustment factor to adjust surface runoff for flat slopes

"""""""""