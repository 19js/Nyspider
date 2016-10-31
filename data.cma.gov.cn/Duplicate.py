#coding:utf-8

import os

def Duplicate():
    for filename in os.listdir('.'):
        if filename.endswith('txt'):
            lines=open(filename,'r').readlines()
            lines=list(set(lines))
            lines.sort()
            f=open(filename,'w')
            for line in lines:
                f.write(line)
            f.close()

Duplicate()
