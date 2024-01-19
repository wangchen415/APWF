import os
import re
import numpy as np
import codecs

class HRU_BSN(object):
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
            ['Comment line', 2, 'character', 'a80'],
            ['Comment line', 3, 'character', 'a80'],
            ['SFTMP', 4, 'real', 'free'],
            ['SMTMP', 5, 'real', 'free'],
            ['SMFMX', 6, 'real', 'free'],
            ['SMFMN', 7, 'real', 'free'],
            ['TIMP', 8, 'real', 'free'],
            ['SNOCOVMX', 9, 'real', 'free'],
            ['SNO50COV', 10, 'real', 'free'],
            ['IPET', 11, 'integer', 'free'],
            ['PETFILE', 12, 'character', 'a13'],
            ['ESCO', 13, 'real', 'free'],
            ['EPCO', 14, 'real', 'free'],
            ['EVLAI', 15, 'real', 'free'],
            ['FFCB', 16, 'real', 'free'],
            ['Comment line', 17, 'character', 'a80'],
            ['IEVENT', 18, 'real', 'free'],  
            ['ICRK', 19, 'real', 'free'],  
            ['SURLAG', 20, 'real', 'free'],  
            ['ADJ_PKR', 21, 'real', 'free'],  
            ['PRF_BSN', 22, 'real', 'free'],  
            ['SPCON', 23, 'real', 'free'],  
            ['SPEXP', 24, 'real', 'free'],   
        ]
        meta_desc = []
        special=[]
        #
        param = {}
        for i in range(len(lns)):
            # print(i,'------------------')
            #TITLE, P.256
            if i==0 or i ==1 or i ==2 or i==16:
                meta_desc.append(lns[i])
            elif  i<24:
                if re.match(r'\s*\d+(\.\d+)*\s*\|\s*[A-Z]+\w*\s*:.*', lns[i], re.DOTALL) or re.match(r'\s*.*\s*|\s*[A-Z]+\w*\s*:.*',lns[i], re.DOTALL):
                    meta_desc.append(lns[i].split('|')[-1].split(':',maxsplit=1)[-1].strip())
                    s = re.sub('(\s*:\s*)', ':', lns[i])
                    val = s.split('|')[0].strip()
                    if 0<i<24 :
                        var = meta[i][0]
                        if meta[i][2].lower()=='integer':
                            val = int('%.0f' % float(val))
                        elif meta[i][2].lower()=='real':
                            val = float(val)                  
                    param[var]=val
                #Comment line
            else:
                special.append(lns[i])
        return meta,meta_desc,param,special


    def write(self,all,outfile):
        #
        special=all[3]
        #
        head1=all[1][0]
        head2=all[1][1]
        head3=all[1][2]
        bsn1=all[2]
        ###########################end
        # 第二部分#####################
        illurstration1=all[1][3]
        line1=str(format(bsn1['SFTMP'], '.3f')).rjust(16,' ')+"    "+"| "+str('SFTMP')+" "+":"+" "+str(illurstration1)
        #
        illurstration2=all[1][4]
        line2=str(format(bsn1['SMTMP'],'.3f')).rjust(16,' ')+"    "+"| "+str('SMTMP')+" "+":"+" "+str(illurstration2)
        #
        illurstration3=all[1][5]
        line3=str(format(bsn1['SMFMX'], '.3f')).rjust(16,' ')+"    "+"| "+str('SMFMX')+" "+":"+" "+str(illurstration3)
        #
        illurstration4=all[1][6]
        line4=str(format(bsn1['SMFMN'], '.3f')).rjust(16,' ')+"    "+"| "+str('SMFMN')+" "+":"+" "+str(illurstration4)
        #
        illurstration5=all[1][7]
        line5=str(format(bsn1['TIMP'], '.3f')).rjust(16,' ')+"    "+"| "+str('TIMP')+" "+":"+" "+str(illurstration5)
        #
        illurstration6=all[1][8]
        line6=str(format(bsn1['SNOCOVMX'], '.3f')).rjust(16,' ')+"    "+"| "+str('SNOCOVMX')+" "+":"+" "+str(illurstration6)
        #
        illurstration7=all[1][9]
        line7=str(format(bsn1['SNO50COV'], '.3f')).rjust(16,' ')+"    "+"| "+str('SNO50COV')+" "+":"+" "+str(illurstration7)
        #
        illurstration8=all[1][10]
        line8=str(format(bsn1['IPET'], '.0f')).rjust(16,' ')+"    "+"| "+str('IPET')+":"+" "+str(illurstration8)
        #
        illurstration9=all[1][11]
        line9=str(bsn1['PETFILE']).rjust(16,' ')+"    "+"| "+str('PETFILE')+":"+" "+str(illurstration9)
        #
        illurstration10=all[1][12]
        line10=str(format(bsn1['ESCO'], '.3f')).rjust(16,' ')+"    "+"| "+str('ESCO')+":"+" "+str(illurstration10)
        #
        illurstration11=all[1][13]
        line11=str(format(bsn1['EPCO'], '.3f')).rjust(16,' ')+"    "+"| "+str('EPCO')+":"+" "+str(illurstration11)
        #
        illurstration12=all[1][14]
        line12=str(format(bsn1['EVLAI'], '.3f')).rjust(16,' ')+"    "+"| "+str('EVLAI')+" "+":"+" "+str(illurstration12)
        #
        illurstration13=all[1][15]
        line13=str(format(bsn1['FFCB'], '.3f')).rjust(16,' ')+"    "+"| "+str('FFCB')+" "+":"+" "+str(illurstration13)
        #
        line_=str(all[1][16])
        #
        illurstration14=all[1][17]
        line14=str(format(bsn1['IEVENT'], '.0f')).rjust(16,' ')+"    "+"| "+str('IEVENT')+" "+":"+" "+str(illurstration14)
        #
        illurstration15=all[1][18]
        line15=str(format(bsn1['ICRK'], '.0f')).rjust(16,' ')+"    "+"| "+str('ICRK')+" "+":"+" "+str(illurstration15)
        #
        illurstration16=all[1][19]
        line16=str(format(bsn1['SURLAG'], '.3f')).rjust(16,' ')+"    "+"| "+str('SURLAG')+" "+":"+" "+str(illurstration16)
        #
        illurstration17=all[1][20]
        line17=str(format(bsn1['ADJ_PKR'], '.3f')).rjust(16,' ')+"    "+"| "+str('ADJ_PKR')+" "+":"+" "+str(illurstration17)
        #
        illurstration18=all[1][21]
        line18=str(format(bsn1['PRF_BSN'], '.3f')).rjust(16,' ')+"    "+"| "+str('PRF_BSN')+" "+":"+" "+str(illurstration18)
        #
        illurstration19=all[1][22]
        line19=str(format(bsn1['SPCON'], '.4f')).rjust(16,' ')+"    "+"| "+str('SPCON')+" "+":"+" "+str(illurstration19)
        #
        illurstration20=all[1][23]
        line20=str(format(bsn1['SPEXP'], '.3f')).rjust(16,' ')+"    "+"| "+str('SPEXP')+" "+":"+" "+str(illurstration20)
        #输出文件
        object=codecs.open(outfile,'w','utf-8')
        object.write(head1+'\n')
        object.write(head2+'\n')
        object.write(head3+'\n')
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
        object.write(line_+'\n')
        object.write(line14+'\n')
        object.write(line15+'\n')
        object.write(line16+'\n')
        object.write(line17+'\n')
        object.write(line18+'\n')
        object.write(line19+'\n')
        object.write(line20+'\n')
        for OS in range(len(special)):
            #    for j in range(len(OS2[i])):
            object.write(str(special[OS])+'\n')
        object.close()
'''
Basin data           .bsn file 2023/3/11 0:00:00 ArcSWAT 2012.10_6.24
Modeling Options: Land Area
Water Balance:
           1.000    | SFTMP : Snowfall temperature [oC]
           0.500    | SMTMP : Snow melt base temperature [oC]
           4.500    | SMFMX : Melt factor for snow on June 21 [mm H2O/oC-day]
           4.500    | SMFMN : Melt factor for snow on December 21 [mm H2O/oC-day]
           1.000    | TIMP : Snow pack temperature lag factor
           1.000    | SNOCOVMX : Minimum snow water content that corresponds to 100% snow cover [mm]
           0.500    | SNO50COV : Fraction of snow volume represented by SNOCOVMX that corresponds to 50% snow cover
               1    | IPET: PET method: 0=priest-t, 1=pen-m, 2=har, 3=read into model
                    | PETFILE: name of potential ET input file
           0.950    | ESCO: soil evaporation compensation factor
           1.000    | EPCO: plant water uptake compensation factor
           3.000    | EVLAI : Leaf area index at which no evaporation occurs from water surface [m2/m2]
           0.000    | FFCB : Initial soil water storage expressed as a fraction of field capacity water content
Surface Runoff:
               0    | IEVENT : rainfall/runoff code: 0=daily rainfall/CN
               0    | ICRK : crack flow code: 1=model crack flow in soil
           4.000    | SURLAG : Surface runoff lag time [days]
           1.000    | ADJ_PKR : Peak rate adjustment factor for sediment routing in the subbasin (tributary channels)
           1.000    | PRF_BSN : Peak rate adjustment factor for sediment routing in the main channel
          0.0001    | SPCON : Linear parameter for calculating the maximum amount of sediment that can be reentrained during channel sediment routing
           1.000    | SPEXP : Exponent parameter for calculating sediment reentrained in channel sediment routing
Nutrient Cycling:
           0.000    | RCN : Concentration of nitrogen in rainfall [mg N/l]
         0.00030    | CMN : Rate factor for humus mineralization of active organic nitrogen
          20.000    | N_UPDIS : Nitrogen uptake distribution parameter
          20.000    | P_UPDIS : Phosphorus uptake distribution parameter
           0.200    | NPERCO : Nitrogen percolation coefficient
          10.000    | PPERCO : Phosphorus percolation coefficient
         175.000    | PHOSKD : Phosphorus soil partitioning coefficient
           0.400    | PSP : Phosphorus sorption coefficient
           0.050    | RSDCO : Residue decomposition coefficient
Pesticide Cycling:
           0.500    | PERCOP : Pesticide percolation coefficient
Algae/CBOD/Dissolved Oxygen:
               0    | ISUBWQ: subbasin water quality parameter
Bacteria:
           0.000    | WDPQ : Die-off factor for persistent bacteria in soil solution. [1/day]
           0.000    | WGPQ : Growth factor for persistent bacteria in soil solution [1/day]
           0.000    | WDLPQ : Die-off factor for less persistent bacteria in soil solution [1/day]
           0.000    | WGLPQ : Growth factor for less persistent bacteria in soil solution. [1/day]
           0.000    | WDPS : Die-off factor for persistent bacteria adsorbed to soil particles. [1/day]
           0.000    | WGPS : Growth factor for persistent bacteria adsorbed to soil particles. [1/day]
           0.000    | WDLPS : Die-off factor for less persistent bacteria adsorbed to soil particles. [1/day]
           0.000    | WGLPS : Growth factor for less persistent bacteria adsorbed to soil particles. [1/day]
         175.000    | BACTKDQ : Bacteria partition coefficient
           1.070    | THBACT : Temperature adjustment factor for bacteria die-off/growth
           0.000    | WOF_P: wash-off fraction for persistent bacteria on foliage
           0.000    | WOF_LP: wash-off fraction for less persistent bacteria on foliage
           0.000    | WDPF: persistent bacteria die-off factor on foliage
           0.000    | WGPF: persistent bacteria growth factor on foliage
           0.000    | WDLPF: less persistent bacteria die-off factor on foliage
           0.000    | WGLPF: less persistent bacteria growth factor on foliage
               0    | ISED_DET:
Modeling Options: Reaches
               0    | IRTE: water routing method 0=variable travel-time 1=Muskingum
           0.750    | MSK_CO1 : Calibration coefficient used to control impact of the storage time constant (Km) for normal flow
           0.250    | MSK_CO2 : Calibration coefficient used to control impact of the storage time constant (Km) for low flow
           0.200    | MSK_X : Weighting factor controlling relative importance of inflow rate and outflow rate in determining water storage in reach segment
               0    | IDEG: channel degradation code
               1    | IWQ: in-stream water quality: 1=model in-stream water quality
   basins.wwq       | WWQFILE: name of watershed water quality file
           0.000    | TRNSRCH: reach transmission loss partitioning to deep aquifer
           1.000    | EVRCH : Reach evaporation adjustment factor
               0    | IRTPEST : Number of pesticide to be routed through the watershed channel network
               0    | ICN  : Daily curve number calculation method
           1.000    | CNCOEF : Plant ET curve number coefficient
           1.400    | CDN : Denitrification exponential rate coefficient
           1.100    | SDNCO : Denitrification threshold water content
           0.150    | BACT_SWF : Fraction of manure applied to land areas that has active colony forming units
          10.000    | BACTMX : Bacteria percolation coefficient [10 m3/Mg].
           0.000    | BACTMINLP : Minimum daily bacteria loss for less persistent bacteria [# cfu/m2]
           0.000    | BACTMINP : Minimum daily bacteria loss for persistent bacteria [# cfu/m2]
           0.000    | WDLPRCH: Die-off factor for less persistent bacteria in streams (moving water) at 20 C [1/day]
           0.000    | WDPRCH : Die-off factor for persistent bacteria in streams (moving water) at 20 C [1/day]
           0.000    | WDLPRES : Die-off factor for less persistent bacteria in water bodies (still water) at 20 C [1/day]
           0.000    | WDPRES : Die-off factor for persistent bacteria in water bodies (still water) at 20 C [1/day]
           0.000    | TB_ADJ : New variable in testing ...Adjustment factor for subdaily unit hydrograph basetime
           0.000    | DEPIMP_BSN : Depth to impervious layer for modeling perched water tables [mm]
           0.000    | DDRAIN_BSN : Depth to the sub-surface drain [mm]
           0.000    | TDRAIN_BSN : Time to drain soil to field capacity [hours]
           0.000    | GDRAIN_BSN : Drain tile lag time [hours]
        0.000862    | CN_FROZ : Parameter for frozen soil adjustment on infiltration/runoff
           0.000    | DORM_HR : Time threshold used to define dormancy [hours]
           1.000    | SMXCO : Adjustment factor for maximum curve number S factor
           0.500    | FIXCO : Nitrogen fixation coefficient
          20.000    | NFIXMX : Maximum daily-n fixation [kg/ha]
           0.200    | ANION_EXCL_BSN : Fraction of porosity from which anions are excluded
           0.000    | CH_ONCO_BSN : Channel organic nitrogen concentration in basin [ppm]
           0.000    | CH_OPCO_BSN : Channel organic phosphorus concentration in basin [ppm]
           5.000    | HLIFE_NGW_BSN : Half-life of nitrogen in groundwater [days]
           1.000    | RCN_SUB_BSN : Concentration of nitrate in precipitation [ppm]
           0.100    | BC1_BSN : Rate constant for biological oxidation of NH3 [1/day]
           0.100    | BC2_BSN : Rate constant for biological oxidation NO2 to NO3 [1/day]
           0.020    | BC3_BSN : Rate constant for hydrolosis of organic nitrogen to ammonia [1/day]
           0.350    | BC4_BSN : Rate constant for decay of organic phosphorus to dissolved phosphorus [1/day]
           0.010    | DECR_MIN: Minimum daily residue decay
           0.000    | ICFAC : C-factor calculation method
           0.300    | RSD_COVCO : Residue cover factor for computing fraction of cover
           5.000    | VCRIT : Critical velocity
               0    | CSWAT : Code for new carbon routines
           0.184    | RES_STLR_CO : Reservoir sediment settling coefficient
           0.750    | BFLO_DIST 0-1 (1:profile of baseflow in a day follows rainfall pattern, 0:baseflow evenly distributed to each time step during a day
               1    | IUH : Unit hydrograph method: 1=triangular UH, 2=gamma function UH
           5.000    | UHALPHA : alpha coefficient for gamma function unit hydrograph. Required if iuh=2 is selected
Land Use types in urban.dat that do not make runoff to urban BMPs:

Subdaily Erosion:
           1.000    | EROS_SPL: The splash erosion coefficient ranges 0.9 - 3.1
           0.700    | RILL_MULT: Multiplier to USLE_K for soil susceptible to rill erosion, ranges 0.5 - 2.0
           1.200    | EROS_EXPO: an exponent in the overland flow erosion equation, ranges 1.5 - 3.0
           0.000    | SUBD_CHSED: 1=Brownlie(1981) model, 2=Yang(1973,1984) model
           0.030    | C_FACTOR: Scaling parameter for Cover and management factor in ANSWERS erosion model
            50.0    | CH_D50 : median particle diameter of channel bed [mm]
           1.570    | SIG_G : geometric standard deviation of particle sizes
           50.00    | RE_BSN: Effective radius of drains
        15000.00    | SDRAIN_BSN: Distance between two drain or tile tubes
           10.00    | DRAIN_CO_BSN: Drainage coefficient
           1.042    | PC_BSN: Pump capacity
            1.00    | LATKSATF_BSN: Multiplication factor to determine lateral ksat from SWAT ksat input value for HRU
               0    | ITDRN: Tile drainage equations flag
               0    | IWTDN: Water table depth algorithms flag
               0    | SOL_P_MODEL: if = 1, use new soil P model
            1.00    | IABSTR: Initial abstraction on impervious cover (mm)
               0    | IATMODEP: 0 = average annual inputs 1 = monthly inputs
               1    | R2ADJ_BSN: basinwide retention parm adjustment factor
               0    | SSTMAXD_BSN: basinwide retention parm adjustment factor
               0    | ISMAX: max depressional storage code
               0    | IROUTUNIT:
           0.000    | CO2_X2: Quadratic coefficient for incrementinig  future CO2 concentrations using a quadratic equation.
           0.000    | CO2_X: Linear coefficient for incrementinig  future CO2 concentrations using a quadratic equation.
               0    | SFSEDMEAN: Mean sediment concentration coming out of sand filter.
               0    | SFSEDSTDEV: Standard deviation of sediment concentration coming out of sand filter.
'''

