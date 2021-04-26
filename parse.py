#   
# Brad Schoenrock -- 9/12/18
# 

import os
import re
import sys
import re

import datetime
from datetime import datetime
from datetime import timedelta  

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas import DataFrame



def readMy(rdir, myFile):

    with open(os.path.join(rdir, myFile)) as inFile:
        content = inFile.readlines()
        
    col_names =  ['ELAPSED', 'CPU%', 'RSS(mb)', 'SIZE(mb)']
    newDF = pd.DataFrame(columns = col_names)  
    
    countTot=0
    countSusp=0
    
    for line in content:
        thing = line.split(r'\\[0\;[0-9][0-9]m')[0].rstrip('\n')
        thing = thing[7:] # strip off first 8 chars for formatting
        thing = thing[:-4] # strip off last 5 chars for formatting
        if "defunct" not in line:
            offset = 0
            getIn=False
            if 'Jan' in thing or 'Dec' in thing or 'Nov' in thing or 'Oct' in thing or 'Sep' in thing:
                offset=1
                getIn=True
            elif re.match(r'\d+',thing):
                getIn=True
            if getIn:
                arr = thing.split(" ")
                arr = list(filter(None,arr))
                temp=""
                if "-" in arr[2+offset]:
                    splitTemp = arr[2+offset].split("-")
                    temp=datetime.strptime(splitTemp[1],'%H:%M:%S')
                    temp=temp+timedelta(days=int(splitTemp[0]))
                elif len(arr[2+offset])>5:
                    temp= datetime.strptime(arr[2+offset],'%H:%M:%S')
                elif len(arr[2+offset])>2:
                    temp= datetime.strptime(arr[2+offset],'%M:%S')
                elif len(arr[2+offset])==2:
                    temp= datetime.strptime(arr[2+offset],'%S')    
                my_date = datetime(day=1, year=1900, month=1)
                tDelta = temp - my_date
                
                #print ("arr=",len(arr),offset,arr)
                countTot = countTot + 1
                if tDelta > timedelta(hours=0.5): 
                    countSusp = countSusp + 1

                tmpData = pd.DataFrame([[tDelta,arr[4+offset],arr[5+offset],arr[6+offset]]],index = [arr[1+offset]],columns = col_names)
                newDF = pd.concat([newDF,tmpData])
                #print (newDF)
    print ("countTot=",countTot)
    print ("countSusp=",countSusp)

    return newDF



def parseData(rdir,inFile):
    
    if os.path.isdir(rdir):
        pass
    else:
        print ("ERROR: directory",rdir,"doesn't exist, try pulling the files or specifying a different date. Exiting with code 1")
        sys.exit(1)
        
    print ("b")
    myData = readMy(rdir, inFile)
    print ("c")

    print ("Done reading: Current time:",datetime.now())

    return myData



def main():
    print ("Hello World: Current time:",datetime.now())

    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    
    inpath=""

    try:
        inpath=sys.argv[1]
    except:
        inpath="/home/bschoenrock/git/Insights/StaleSessions"

    rdir =inpath

    print ("Directory read :",rdir)

    try:
        inFile=sys.argv[2]
    except:
        inFile = "reno-vca.txt"
        
    print ("a")
    myData = parseData(rdir,inFile)
    print ("d")

    #***********put analysis here***********
        
    myData[['SIZE(mb)', 'RSS(mb)', 'CPU%']] = myData[['SIZE(mb)', 'RSS(mb)', 'CPU%']].apply(pd.to_numeric)

    myData['SIZE(mb)'] = myData['SIZE(mb)']/1000
    myData['RSS(mb)'] = myData['RSS(mb)']/1000

    #print (myData)

    print ("size of my data = ", myData.shape)
    print (myData.dtypes)
    
    print (myData.describe())

    #print ("Making Plot: Current time:",datetime.now())

    #holder = (myData['ELAPSED']).astype('timedelta64[s]')
    
    #print (type(holder))
    #print (type(holder[0]))

    #plt.plot(holder,myData['RSS(mb)'], 'bo')
    #plt.gcf().autofmt_xdate()
    #plt.xscale('log')
    #plt.xlabel("time(s)")
    #plt.ylabel("RSS(mb)")
    #plt.title("size vs time of html5client processes")
    #plt.tight_layout()
    #plt.show()
    #plt.close()

    #plt.plot(holder,myData['CPU%'], 'bo')
    #plt.gcf().autofmt_xdate()
    #plt.xlabel("time(s)")
    #plt.ylabel("CPU%")
    #plt.title("CPU vs time of html5client processes")
    #plt.tight_layout()
    #plt.show()
    #plt.close()

    #plt.figure(figsize=(16,9))
    #plt.xlabel("time(s)")
    #plt.ylabel("session count")
    #plt.xscale('log')
    #plt.yscale('log')
    #plt.xlim(right=100000)
    #plt.title("sessions over time")
    #holder.hist(bins=500)
    #plt.tight_layout()
    #plt.show()
    #plt.close()


    print ("Goodnight World: Current time:",datetime.now())



if __name__ == '__main__':
    main()



