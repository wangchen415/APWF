import os
import re
import numpy as np
import codecs


class HRU_MGT(object):
    #
    def __init__(self):
        pass
    def __del__(self):
        pass
    #
    #read from '000010002.mgt'
    def read(self,filepath):
        #data
        with open(filepath,'r',encoding='GBK') as fh:
            lns = fh.readlines()
            lns = [ln.rstrip() for ln in lns]
        #data type - Variable name, Line#, Format, F90 Format
        meta = [
            ['TITLE', 1, 'character', 'a80'],
            ['NMGT', 2, 'integer', 'Free'],
            ['Comment line', 3, 'character', 'a80'],
            ['IGRO', 4, 'integer', 'Free'],
            ['PLANT_ID', 5, 'integer', 'Free'],
            ['LAI_INIT', 6, 'real', 'Free'],
            ['BIO_INIT', 7, 'real', 'Free'],
            ['PHU_PLT', 8, 'real', 'Free'],
            ['COMMENT LINE', 9, 'character', 'a80'],
            ['BIOMIX', 10, 'real', 'free'],
            ['CN2', 11, 'real', 'free'],
            ['USLE_P', 12, 'real', 'free'],
            ['BIO_MIN', 13, 'real', 'free'],
            ['FILTERW', 14, 'real', 'free'],
            ['Comment line', 15, 'character', 'a80'],
            ['IURBAN', 16, 'real', 'free'],
            ['URBLU', 17, 'real', 'free'],
            ['Comment line', 18, 'character', 'a80'],
            ['IRRSC', 19, 'integer', 'free'],
            ['IRRNO', 20, 'integer', 'free'],
            ['FLOWMIN', 21, 'real', 'free'],
            ['DIVMAX', 22, 'real', 'free'],
            ['FLOWFR', 23, 'real', 'free'],
            ['Comment line', 24, 'character', 'a80'],
            ['DDRAIN', 25, 'real', 'free'],
            ['TDRAIN', 26, 'real', 'free'],
            ['GDRAIN', 27, 'real', 'free'],
            ['Comment line', 28, 'character', 'a80'],
            ['NROT', 29, 'real', 'free'],
            ['Comment line', 30, 'character', 'a80'],
        ]
        meta_desc = []
        #
        param = {}
        param_mgt_op = []
        for i in range(len(lns)):
            # print(i,'------------------')
            #TITLE, P.256
            if i==0:
                meta_desc.append(lns[i])
                s = re.sub('(\s*:\s*)', ':', lns[i])
                watershed_hru = [v.strip() for v in re.search('Watershed HRU\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                # param.extend([watershed_hru])
                param[watershed_hru[0]]=watershed_hru[1]
                subbasin = [v.strip() for v in re.search('Subbasin\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                # param.extend([subbasin])
                param[subbasin[0]]=subbasin[1]
                hru = [v.strip() for v in re.search('HRU\s*:\s*\d+', s,re.IGNORECASE).group(0).split(':')]
                # param.extend([hru])
                param[hru[0]]=hru[1]
                slope = [v.strip() for v in re.search('Slope\s*:\s*\d+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
                # param.extend([slope])
                param[slope[0]]=slope[1]
                landuse = [v.strip() for v in re.search('Luse\s*:\s*\w+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
                # param.extend([landuse])
                param[landuse[0]]=landuse[1]
                soil = [v.strip() for v in re.search('Soil\s*:\s*\w+(-\d+)?', s,re.IGNORECASE).group(0).split(':')]
                # param.extend([soil])
                param[soil[0]]=soil[1]               
                # re.search('[0-9]{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', s,re.IGNORECASE)
                # re.search('ArcSWAT\s+[0-9]{4}\.\d+_\d+\.\d+', s,re.IGNORECASE)
                # selected = re.findall('([A-Za-z]+:[0-9]+-?[0-9]+)', s)
                # selected = re.findall('([A-Za-z]+:[0-9]+\-?\d+)', s)
                # param.extend([v.split(':') for v in selected])
            #MGT_OP, P.259
            elif i>=30:
                s = lns[i]
                if len(s)<80:
                    s += ' '*80
                    s = s[:80]
                # print(s)
                vals = s[:3],s[5:6],s[8:15],s[16:18]
                # print(vals)
                mon,day,husc,mgt_op = [v.strip() for v in vals]
                mon=mon.rjust(3," ")
                day=day.rjust(3," ")
                husc=husc.rjust(9," ")
                if mgt_op == '1':
                    mgt_op=mgt_op.rjust(3," ")
                    plant_id,curyr_mat,mgt4,mgt5,mgt6,mgt7,mgt8,mgt9 = s[18:23],s[23:30],s[30:43],s[43:50],s[50:62],s[62:67],s[67:74],s[74:80]
                    param_mgt_op.append([mon,day,husc,mgt_op,plant_id,curyr_mat,mgt4,mgt5,mgt6,mgt7,mgt8,mgt9])
                elif mgt_op == '2':
                    mgt_op=mgt_op.rjust(3," ")
                    irr_sc,irr_no,irr_amt,irr_salt,irr_efm,irr_sq = s[18:27],s[27:30],s[30:43],s[43:50],s[52:62],s[62:67]
                    param_mgt_op.append([mon,day,husc,mgt_op,irr_sc,irr_no,irr_amt,irr_salt,irr_efm,irr_sq])
                elif mgt_op == '3':
                    mgt_op=mgt_op.rjust(3," ")
                    irr_sc,irr_no,irr_amt,irr_salt,irr_efm,irr_sq = s[18:27],s[27:30],s[30:43],s[43:50],s[52:62],s[62:67]
                    param_mgt_op.append([mon,day,husc,mgt_op,irr_sc,irr_no,irr_amt,irr_salt,irr_efm,irr_sq])
                elif mgt_op == '4':
                    mgt_op=mgt_op.rjust(3," ")
                    pest_id,pst_kg,pst_dep = s[18:23],s[23:43],s[43:50]
                    param_mgt_op.append([mon,day,husc,mgt_op,pest_id,pst_kg,pst_dep])    
                elif mgt_op == '5':
                    mgt_op=mgt_op.rjust(3," ")
                    cnop,hi_ovr,frac_harvk = s[18:43],s[43:50],s[50:62]
                    param_mgt_op.append([mon,day,husc,mgt_op,cnop,hi_ovr,frac_harvk])
                elif mgt_op == '6':
                    mgt_op=mgt_op.rjust(3," ")
                    till_id,cnop = s[18:43],s[43:50],s[50:62]
                    param_mgt_op.append([mon,day,husc,mgt_op,till_id,cnop])
                elif mgt_op == '7':
                    mgt_op=mgt_op.rjust(3," ")
                    ihv_gbm,harveff,hi_ovr = s[18:27],s[27:43],s[43:50]
                    param_mgt_op.append([mon,day,husc,mgt_op,ihv_gbm,harveff,hi_ovr])
                elif mgt_op == '8':
                    mgt_op=mgt_op.rjust(3," ")
                    param_mgt_op.append([mon,day,husc,mgt_op])
                elif mgt_op == '9':
                    mgt_op=mgt_op.rjust(3," ")
                    grz_days,manure_id,bio_eat,bio_trmp,manure_kg = s[18:23],s[23:27],s[27:43],s[43:50],s[50:62]
                    param_mgt_op.append([mon,day,husc,mgt_op,grz_days,manure_id,bio_eat,bio_trmp,manure_kg])
                elif mgt_op == '10':
                    mgt_op=mgt_op.rjust(3," ")
                    wstrs_id,irr_sca,irr_noa,auto_wstrs,irr_eff,irr_mx,irr_asq = s[18:23],s[23:27],s[27:30],s[30:43],s[43:50],s[50:62],s[64:67]
                    param_mgt_op.append([mon,day,husc,mgt_op,wstrs_id,irr_sca,irr_noa,auto_wstrs,irr_eff,irr_mx,irr_asq])
                elif mgt_op == '11':
                    mgt_op=mgt_op.rjust(3," ")
                    mgt4,mgt5,mgt6,mgt7,mgt8,mgt9 = s[18:23],s[23:43],s[43:50],s[50:62],s[62:67],s[67:74]
                    param_mgt_op.append([mon,day,husc,mgt_op,mgt4,mgt5,mgt6,mgt7,mgt8,mgt9]) 
                elif mgt_op == '12':
                    mgt_op=mgt_op.rjust(3," ")
                    sweepefe,fr_curb = s[18:43],s[43:50]
                    param_mgt_op.append([mon,day,husc,mgt_op,sweepefe,fr_curb])
                elif mgt_op == '13':
                    mgt_op=mgt_op.rjust(3," ")
                    imp_trig = s[18:23]
                    param_mgt_op.append([mon,day,husc,mgt_op,imp_trig])
                elif mgt_op == '14':
                    mgt_op=mgt_op.rjust(3," ")
                    fert_days,cfrt_id,ifrt_freq,cfrt_kg = s[18:23],s[23:27],s[27:30],s[30:43]
                    param_mgt_op.append([mon,day,husc,mgt_op,fert_days,cfrt_id,ifrt_freq,cfrt_kg])
                elif mgt_op == '15':
                    mgt_op=mgt_op.rjust(3," ")
                    cpst_id,pest_days,ipest_freq,cpst_kg = s[18:23],s[23:27],s[27:30],s[30:43]
                    param_mgt_op.append([mon,day,husc,mgt_op,cpst_id,pest_days,ipest_freq,cpst_kg])
                elif mgt_op == '16':
                    burn_frlb = s[18:43]
                    mgt_op=mgt_op.rjust(3," ")
                    param_mgt_op.append([mon,day,husc,mgt_op,burn_frlb])
                elif mgt_op == '17':
                    end = s[:18]
                    param_mgt_op.append([end])  
                
            else:
                #NMGT, P256
                if re.match(r'\s*\d+(\.\d+)?\s*\|\s*[A-Z]+\w*:.*', lns[i], re.DOTALL):
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
        return meta,meta_desc,param,param_mgt_op
    #
    #save to '000010002.mgt'
    def write(self,all,outfile):
        head1=all[1][0]
        # 第三部分########################
        head8=all[1][29]
        OS2=all[3]
        va=all[2]
        # 第二部分#####################
        illurstration1=all[1][1]
        # element1=all[2][6][0]
        # number1=all[2][6][1]
        line1=str(va['NMGT']).rjust(16,' ')+"    "+"| "+'NMGT'+":"+str(illurstration1)
        #
        head2=all[1][2]
        #
        illurstration2=all[1][3]
        line2=str(va['IGRO']).rjust(16,' ')+"    "+"| "+'IGRO'+": "+str(illurstration2)
        #
        illurstration3=all[1][4]
        line3=str(va['PLANT_ID']).rjust(16,' ')+"    "+"| "+'PLANT_ID'+": "+str(illurstration3)
        #
        illurstration4=all[1][5]
        line4=str(format(va['LAI_INIT'], '.2f')).rjust(16,' ')+"    "+"| "+'LAI_INIT'+": "+str(illurstration4)
        #
        illurstration5=all[1][6]
        line5=str(format(va['BIO_INIT'], '.2f')).rjust(16,' ')+"    "+"| "+'BIO_INIT'+": "+str(illurstration5)
        #
        illurstration6=all[1][7]
        line6=str(format(va['PHU_PLT'], '.2f')).rjust(16,' ')+"    "+"| "+'PHU_PLT'+": "+str(illurstration6)
        #
        head3=all[1][8]
        #
        illurstration7=all[1][9]
        line7=str(format(va['BIOMIX'], '.2f')).rjust(16,' ')+"    "+"| "+'BIOMIX'+": "+str(illurstration7)
        #
        illurstration8=all[1][10]
        line8=str(format(va['CN2'], '.2f')).rjust(16,' ')+"    "+"| "+'CN2'+": "+str(illurstration8)
        #
        illurstration9=all[1][11]
        line9=str(format(va['USLE_P'], '.2f')).rjust(16,' ')+"    "+"| "+'USLE_P'+": "+str(illurstration9)
        #
        illurstration10=all[1][12]
        line10=str(format(va['BIO_MIN'], '.2f')).rjust(16,' ')+"    "+"| "+'BIO_MIN'+": "+str(illurstration10)
        #
        illurstration11=all[1][13]
        line11=str(format(va['FILTERW'], '.3f')).rjust(16,' ')+"    "+"| "+'FILTERW'+": "+str(illurstration11)
        #
        head4=all[1][14]
        #
        illurstration12=all[1][15]
        line12=str(format(va['IURBAN'], '.0f')).rjust(16,' ')+"    "+"| "+'IURBAN'+": "+str(illurstration12)
        #
        illurstration13=all[1][16]

        line13=str(format(va['URBLU'], '.0f')).rjust(16,' ')+"    "+"| "+'URBLU'+": "+str(illurstration13)
        #
        head5=all[1][17]
        #
        illurstration14=all[1][18]
        line14=str(format(va['IRRSC'], '.0f')).rjust(16,' ')+"    "+"| "+'IRRSC'+": "+str(illurstration14)
        #
        illurstration15=all[1][19]
        line15=str(format(va['IRRNO'], '.0f')).rjust(16,' ')+"    "+"| "+'IRRNO'+": "+str(illurstration15)
        #
        illurstration16=all[1][20]
        line16=str(format(va['FLOWMIN'], '.3f')).rjust(16,' ')+"    "+"| "+'FLOWMIN'+": "+str(illurstration16)
        #
        illurstration17=all[1][21]
        line17=str(format(va['DIVMAX'], '.3f')).rjust(16,' ')+"    "+"| "+'DIVMAX'+": "+str(illurstration17)
        #
        illurstration18=all[1][22]
        line18=str(format(va['FLOWFR'], '.3f')).rjust(16,' ')+"    "+"| "+'FLOWFR'+": "+str(illurstration18)
        #
        head6=all[1][23]
        #
        illurstration19=all[1][24]
        line19=str(format(va['DDRAIN'], '.3f')).rjust(16,' ')+"    "+"| "+'DDRAIN'+": "+str(illurstration19)
        #
        illurstration20=all[1][25]
        line20=str(format(va['TDRAIN'], '.3f')).rjust(16,' ')+"    "+"| "+'TDRAIN'+": "+str(illurstration20)
        #
        illurstration21=all[1][26]
        line21=str(format(va['GDRAIN'], '.3f')).rjust(16,' ')+"    "+"| "+'GDRAIN'+": "+str(illurstration21)
        #
        head7=all[1][27]
        #
        illurstration22=all[1][28]
        line22=str(format(va['NROT'],'.0f')).rjust(16,' ')+"    "+"| "+'NROT'+": "+str(illurstration22)
        ##################end
        #输入文件
        object=codecs.open(outfile,'w','utf-8')
        object.write(head1+'\n')
        object.write(line1+'\n')
        object.write(head2+'\n')
        object.write(line2+'\n')
        object.write(line3+'\n')
        object.write(line4+'\n')
        object.write(line5+'\n')
        object.write(line6+'\n')
        object.write(head3+'\n')
        object.write(line7+'\n')
        object.write(line8+'\n')
        object.write(line9+'\n')
        object.write(line10+'\n')
        object.write(line11+'\n')
        object.write(head4+'\n')
        object.write(line12+'\n')
        object.write(line13+'\n')
        object.write(head5+'\n')
        object.write(line14+'\n')
        object.write(line15+'\n')
        object.write(line16+'\n')
        object.write(line17+'\n')
        object.write(line18+'\n')
        object.write(head6+'\n')
        object.write(line19+'\n')
        object.write(line20+'\n')
        object.write(line21+'\n')
        object.write(head7+'\n')
        object.write(line22+'\n')
        object.write(head8+'\n')
        for OS in range(len(OS2)):
            #    for j in range(len(OS2[i])):
            str1 = ''.join(OS2[OS])
            object.write(str1+'\n')
        object.close()
# a=HRU_MGT().read(filepath)

"""""""""
 .mgt file Watershed HRU:1 Subbasin:1 HRU:1 Luse:AGRL Soil: HONGRANG1 Slope: 0-9999 2018/4/20 0:00:00 ArcSWAT 2012.10_3.19
 .mgt file Watershed HRU:408 Subbasin:15 HRU:14 Luse:WATR Soil: SHUIDAOTU1 Slope: 0-9999 2018/4/20 0:00:00 ArcSWAT 2012.10_3.19
               0    | NMGT:Management code
Initial Plant Growth Parameters
               0    | IGRO: Land cover status: 0-none growing; 1-growing
               0    | PLANT_ID: Land cover ID number (IGRO = 1)
            0.00    | LAI_INIT: Initial leaf are index (IGRO = 1)
            0.00    | BIO_INIT: Initial biomass (kg/ha) (IGRO = 1)
            0.00    | PHU_PLT: Number of heat units to bring plant to maturity (IGRO = 1)
General Management Parameters
            0.20    | BIOMIX: Biological mixing efficiency
           87.00    | CN2: Initial SCS CN II value
            1.00    | USLE_P: USLE support practice factor
            0.00    | BIO_MIN: Minimum biomass for grazing (kg/ha)
           0.000    | FILTERW: width of edge of field filter strip (m)
Urban Management Parameters
               0    | IURBAN: urban simulation code, 0-none, 1-USGS, 2-buildup/washoff
               0    | URBLU: urban land type
Irrigation Management Parameters
               0    | IRRSC: irrigation code
               0    | IRRNO: irrigation source location
           0.000    | FLOWMIN: min in-stream flow for irr diversions (m^3/s)
           0.000    | DIVMAX: max irrigation diversion from reach (+mm/-10^4m^3)
           0.000    | FLOWFR: : fraction of flow allowed to be pulled for irr
Tile Drain Management Parameters
           0.000    | DDRAIN: depth to subsurface tile drain (mm)
           0.000    | TDRAIN: time to drain soil to field capacity (hr)
           0.000    | GDRAIN: drain tile lag time (hr)
Management Operations:
               1    | NROT: number of years of rotation
Operation Schedule:
  1  1           1    1          1925.00000   0.00     0.00000 0.00   0.00  0.00
  4  1          11    1             0.00000   0.00     0.00000 0.00   0.00
  7  1           7        0         0.80000   0.00
  8  1           1    1          1925.00000   0.20     0.00000 0.00   0.00  0.00
  8 15          11    1             0.00000   0.00     0.00000 0.00   0.00
 11 15           5                  0.00000
 11 15           1    1          1925.00000   0.00     0.00000 0.00   0.00  0.00
                17
       17
"""""""""