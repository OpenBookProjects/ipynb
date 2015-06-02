# -*- coding: utf-8 -*-
'''check and merge as .csv
'''
import os
import sys
import fnmatch

def _load_log(aim_path,fname):
    _exp = {}
    for l in open("%s/%s"%(aim_path,fname)).readlines()[1:]:
        _log = l[:-1].split(',')
        _exp[_log[0]] = _log[1:]

    return _exp

def _merge_split_log(aim_path,r1,r2,a0):
    merge = {}
    merge[r1] = _load_log(aim_path,r1)
    merge[r2] = _load_log(aim_path,r2)
    merge[a0] = merge[r1]
    for k in merge[r2]:
        #print k
        if k in merge[a0]:
            merge[a0][k][0] = float(merge[r2][k][0])+float(merge[r1][k][0])
        else:
            merge[a0][k] = merge[r2][k]
    print merge[a0]

if __name__ == '__main__':
    if 5 != len(sys.argv) :
        print '''Usage:
$ pre_data_merge.py path/2/[数据目录] atl2_150101-150106.csv atl2_150106-150201.csv  atl2_150101-150201.csv
        '''
    else:
        aim_path = sys.argv[1]
        r1 = sys.argv[2]
        r2 = sys.argv[3]
        a0 = sys.argv[4]
        print r1,r2,a0
        _merge_split_log(aim_path,r1,r2,a0)
        


