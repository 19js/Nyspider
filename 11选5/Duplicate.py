#coding:utf-8

import os

def Duplicate():
    for filename in os.listdir('data'):
        if filename.endswith('txt'):
            lines=open('data/'+filename,'r').readlines()
            lines=list(set(lines))
            lines.sort()
            f=open('data/'+filename,'w')
            for line in lines:
                f.write(line)
            f.close()

Duplicate()
