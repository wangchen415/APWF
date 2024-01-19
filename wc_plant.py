############# SWAT-IO Document ################
#Charpter 14
#SWAT Input data: PLANT.DAT
#Source: swat2012.mdb
#############################################

import re

class HRU_PLANT(object):
    ### plant.dat formating
    fmt_str1 = "ICNUM, 4d, CPNM, 5s, IDC, 3d, DESCRIPTION, s"
    fmt_str2 = "BIO_E, 7.2f, HVSTI, 6.2f, BLAI, 7.2f, FRGRW1, 6.2f, LAIMX1, 6.2f, FRGRW2, 6.2f, LAIMX2, 6.2f, DLAI, 6.2f, CHTMX, 7.2f, RDMX, 6.2f"
    fmt_str3 = "T_OPT, 7.2f, T_BASE, 7.2f, CNYLD, 8.4f, CPYLD, 8.4f, PLTNFR(1), 8.4f, PLTNFR(2), 8.4f, PLTNFR(3), 8.4f, PLTPFR(1), 8.4f, PLTPFR(2), 8.4f, PLTPFR(3), 8.4f"
    fmt_str4 = "WSYF, 7.3f, USLE_C, 8.4f, GSI, 8.4f, VPDFR, 6.2f, FRGMAX, 7.3f, WAVP, 7.2f, CO2HI, 9.2f, BIOHI, 8.2f, RSDCO_PL, 8.4f, ALAI_MIN, 7.3f"
    fmt_str5 = "BIO_LEAF, 7.3f, MAT_YRS, 5d, BMX_TREES, 7.2f, EXT_COEF, 7.3f, BMDIEOFF, 7.3f, RSR1C, 7.3f, RSR2C, 7.3f"
    fmt_str = [fmt_str1, fmt_str2, fmt_str3, fmt_str4, fmt_str5]
    #
    fmt_keys = []
    fmt_dict = {}
    for f in fmt_str:
        s = [ v.strip() for v in f.split(',')] 
        keys,vals = [],[]
        for i in range(len(s)//2):
            keys.append(s[2*i])
            vals.append('%'+s[2*i+1])
        fmt_keys.append( keys )
        fmt_dict.update( dict(zip(keys,vals)) )
    keys=fmt_keys
    dicts=fmt_dict

    ### reading
    def parseRec_(self,keys,s, sub=[1]):
        v = re.split(' +',s.strip())
        d = dict( [[keys[i],v[i]] for i in range(len(v))] )
        for i in range(len(v)):
            if i in sub:
                d[keys[i]] = int(d[keys[i]])
            else:
                try:
                    d[keys[i]] = float(d[keys[i]])
                except Exception as e:
                    pass
        return d

    def parseRec(self,keys,s):
        par_dict = {}
        for ks in keys:
            par_dict.update( dict([ [k,None] for k in ks]) )
        #
        for i in range(len(keys)):
            if i==0:
                sub=[0,2]
            elif i==4:
                sub=[1]
            else:
                sub = []
            # print(keys[i],'----------')
            d = self.parseRec_(keys[i],s[i], sub=sub)
            par_dict.update(d)
        return par_dict

    def readFile(self,filename,keys=keys):
        fh = open(filename)
        lns = fh.readlines()
        fh.close()
        #
        dat_dict = {}
        for i in range(len(lns)//5):
            s = lns[i*5:i*5+5]
            par_dict = self.parseRec(keys,s)
            dat_dict[par_dict['ICNUM']] = par_dict
        #
        return dat_dict


    ### writing
    def writeFile(self,filename,dat_dict,keys=keys,dicts=dicts):
        fh = open(filename,'w')
        #
        # dat_dict[1]['GSI']=100
        # print(dat_dict[1]['GSI'])
        # print(dat_dict)
        dat_ = sorted(dat_dict.values(), key=lambda x:x['ICNUM'], reverse=False)
        for d in dat_:
            for i in range(len(keys)):
                s = [dicts[k]%(d[k]) for k in keys[i] if d[k] is not None]
                fh.write( '%s\n' % (' '.join(s)) )
        #
        fh.close()



##########################################
if __name__ == '__main__':
    filename = 'plant.dat'
    dat = HRU_PLANT().readFile(filename)
    print(dat[1]['GSI'])
    #
    filename = 'plant2.dat'
    HRU_PLANT().writeFile(filename,dat)