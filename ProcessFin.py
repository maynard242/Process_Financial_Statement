# Program to read ascii files from banks and translste it to banktivity readable files\

import pandas as pd
import re, sys
from datetime import datetime

opt = sys.argv[1] # d - dbs, u - uob, t - tabula
ifile = sys.argv[2]
ofile = sys.argv[3]

# For DBS

def dbs (ifile, ofile):
    fi = open(ifile,'r')
    fw = open(ofile, 'w')
    for line in fi:
        line = line.rstrip()
        if re.match('[0-9]+',line):
            words = line.split(',')
            words[0] = datetime.strptime(words[0],'%d %b %Y').strftime('%d-%m-%Y')
            nline = ''
            for i in range(0,len(words)):
                nline = nline + words[i] + ','
                i=+1
            print (nline, file=fw)
        else:
            continue

    fi.close()
    fw.close()
    return

# For tabula

def tabula (ifile, ofile):
    temp = pd.read_csv(ifile, header=None)
    temp.iloc[:,0] = pd.to_datetime(temp.iloc[:,0])
    temp = temp.dropna()
    temp.to_csv(ofile, header=False, index=False)
    return

# For UOB
    
def uob (ifile, ofile):
    temp = pd.read_excel(ifile)
    temp = temp.dropna()
    temp.columns = temp.iloc[0,:]
    temp = temp.iloc[1:,:]
    temp.iloc[:,0] = pd.to_datetime(temp.iloc[:,0])
    temp.iloc[:,1] = temp.iloc[:,1].str.upper()
    temp2 = temp.iloc[:,1].str.extract(pat='(INTEREST.*)|(INWARD.*)|^MISC DR-DEBIT CARD\\n(.+)\\n')
    temp.iloc[:,1] = temp2.iloc[:,0].fillna('') + temp2.iloc[:,1].fillna('') + temp2.iloc[:,2].fillna('')
    temp.to_csv(ofile, header=False, index=False)   
    return

# Main Program

if opt == 'd':
    dbs (ifile, ofile)
elif opt == 't':
    tabula (ifile, ofile)
elif opt == 'u':
    uob (ifile, ofile)
else: 
    print ('!!Error - Not processed!!')


