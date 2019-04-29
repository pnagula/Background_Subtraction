#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:58:08 2017

@author: pivotalit
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 11:11:20 2017

@author: pivotalit
"""
import os
import numpy as np
from scipy import misc
import math


os.chdir('/Users/pivotalit/Downloads/frames/')
rootdir='/Users/pivotalit/Downloads/frames/'
np.set_printoptions(threshold=np.nan)

np.random.seed(0)
estimator={}
cf=.1
alpha=0.00245  # 407 frames are there 1/407=.00245
dec=' '

def BGMM(rownum,colnum,pixelvalue):    
     dec=' '
     key=str(rownum)+str(colnum)  
     lst=[]
     if key in estimator:
        tw=0.0 
        found_component=0
        if (len(estimator[key])>4):
           estimator[key]=deleteelement(estimator[key],len(estimator[key])-1)

        for row in estimator[key]:
            rownum=row[0]
            colnum=row[1]
            weight=row[2]
            r_to_w=alpha/weight*1.0
            weight=weight+(alpha*-weight) + (-alpha*.05)
            if found_component==0:
               dev=(pixelvalue*1.0-row[3])
               zscore=dev/math.sqrt(row[4])*1.0
               if (tw < .95) and (abs(zscore)<3.0):
                  dec='B' 
               if abs(zscore)<3.0:
                  weight=row[2]  
                  weight+=alpha*(1-weight) + (-alpha*.05)
                  row[3]=row[3]+r_to_w*dev				#mean
                  row[4]=row[4]+r_to_w*(dev*dev-row[4])			#variance
                  found_component=1
                  if row[4] < 5.0: 
                     row[4] = 5.0
                  else:
                     if row[4] > 20.0:
                        row[4]=20.0
            if weight<(alpha*.05):
               estimator[key]=deleteelement(estimator[key],estimator[key].index(row))
            else:
               tw+=weight
               row[2]=weight

        if found_component==0:
           estimator[key].append([int(rownum),int(colnum),alpha,pixelvalue,11,len(estimator[key])])
            
        for row in estimator[key]:
            row[2]=row[2]/tw
            lst.append(row)
        estimator[key]=sorted(lst,reverse=True)   
        del lst[:]
     else:
        value=[int(rownum),int(colnum),1,pixelvalue,11,1]
        estimator[key]=[value]

     if dec=='B':
        return 'B'
     return dec 

def deleteelement(lst,pos):
    lst.remove(lst[pos])
    return lst


for filename in os.listdir(rootdir):
    if filename.startswith("resized-")==True:
       print filename   
       image=misc.imread(filename)
       for rownum in range(480):
           for colnum in range(640):  
               dec=' '
               dec=BGMM(format(rownum, '03'),format(colnum,'03'),image[rownum][colnum])
               if dec=='B':
                  image[rownum][colnum]=255
               else:
                  image[rownum][colnum]=0  
       nfile='p'+filename           
       misc.imsave(nfile,image)
