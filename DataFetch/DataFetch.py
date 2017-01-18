#!/usr/bin/env python
import os
import sys
import pylab as plb

def load(filename):
    img = plb.imread(filename)
    datas = []
    n = img.shape[0]
    m = img.shape[1]

    for i in range(n):
        for j in range(m):
            p = img[i,j]
            a,b,c,d = p[0],p[1],p[2],p[3]
            if a+b+c+d< (4 - 1E-7) :
                datas.append((j,i))
    return datas
