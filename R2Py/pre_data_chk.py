# -*- coding: utf-8 -*-
'''check and clean and export as .csv

- 150601 make handlog export all date into *_all.csv
- 150525 make handlog wxport 2types files
'''
import os
import sys
import fnmatch

ZDATA=[]
        
def _load_timeline(flines,fpath):
    _titles = flines[0]
    _exp = ""
    for l in flines[1:]:
        _l = l[:-1].split(',')
        if 1 == len(_l):
            pass
        else:        
            _exp += _format_log_line(l)    
            #as_year = ["20%s-%s-%s"% (_l[0][:2],_l[0][2:4],_l[0][-2:])]
            ##print ",".join(as_year+_l[1:])
            #_exp += ",".join(as_year+_l[1:])
            #_exp += "\n"
    #print fpath.split('-')[-1]
    f_exp = _titles+_exp
    open("./data/zq_%s"% fpath.split('-')[-1],'w').write(f_exp)
    return _titles,_exp,""

def _format_log_line(crt_line):
    _exp = ""
    _l = crt_line[:-1].split(',')
    as_year = ["20%s-%s-%s"% (_l[0][:2],_l[0][2:4],_l[0][-2:])]
    _exp += ",".join(as_year+_l[1:])
    _exp += "\n"
    return _exp
    

def _load_pomodoro(flines,fpath):
    _titles = flines[0].split()
    _pom = ""   # "date,"+_titles[1]+"\n"
    _exp = ""   # _titles[0]+"\n"
    #print _pom
    #print _exp
    #print flines[1:]
    #return None 
    for l in flines[1:]:
        _l = l[:-1].split()
        #print _l
        #print len(_l)
        if 1 == len(_l):
            _exp += _format_log_line(l)
        else:
            c_l = l.split()
            if 0 == len(c_l):
                pass
            else:
                _exp += _format_log_line(c_l[0])
                crt_date = c_l[0][:6]
                #print crt_date,c_l[1:]
                _pom += _reformat_csv(crt_date, c_l[1:])
            #print l.split()
            #print len(l.split())
    #print _exp
    #print _pom
    f_pom = "date,"+_titles[1]+"\n" + _pom
    f_exp = _titles[0]+"\n" + _exp
    open("./data/zq_%s"% fpath.split('-')[-1],'w').write(f_exp)
    open("./data/pom_%s"% fpath.split('-')[-1],'w').write(f_pom)
    return _titles,_exp,_pom

def _reformat_csv(crt_date, crt_line):
    as_year = "20%s-%s-%s"% (crt_date[:2],crt_date[2:4],crt_date[-2:])
    _exp = as_year
    for i in crt_line:
        if "," in i:
            _exp += ","+i[:-1]
        else:
            _exp += ","+i
    _exp += "\n"
    return _exp

def chk_all_log(aim_path):
    _spath = aim_path.split('/')
    t_titles = ""
    f_pom = "" #"date,"+_titles[1]+"\n"
    p_titles = ""
    f_exp = "" #_titles[0]+"\n"
    
    if "log" == _spath[-1]:
        for file in os.listdir('./log'):
            if fnmatch.fnmatch(file, '*.txt'):
                #pd.read_csv('./data/%s' % file)
                #_load_data('./log/%s' % file)
                fpath = './log/%s' % file
                print fpath
                fl = open(fpath).readlines()
                #print fl[0]
                if "Pt" in fl[0]:
                    #print fpath
                    _titles,_exp,_pom = _load_pomodoro(fl,fpath)
                    #print _exp
                    f_pom += _pom
                    f_exp += _exp
                    p_titles = _titles
                else:
                    _titles,_exp,_pom = _load_timeline(fl,fpath)
                    t_titles = _titles
                    f_exp += _exp
                    #print _exp
        f_pom = "date,"+_titles[1]+"\n"+f_pom
        f_exp = _titles[0]+"\n"+f_exp
        open("./data/zq_all.csv" ,'w').write(f_exp)
        open("./data/pom_all.csv",'w').write(f_pom)
    elif "csv" == _spath[-1]:
        for file in os.listdir('./csv'):
            if fnmatch.fnmatch(file, '*.csv'):
                fpath = './csv/%s' % file
                print fpath
                fl = open(fpath).readlines()
                _load_atl(fl,file)

            #print _exp,_pom
    print "*_all export..."
    #print "t_titles:", t_titles
    #print "p_titles:", p_titles

def _load_atl(flines,fname):
    """load and pick time log from aTimeLogger2 export
    """
    _titles = ""
    _exp = ""
    _gotit = 0
    no_grp = 0
    l_exp = []

    for l in flines:
        if ("%" in l):
            no_grp = 1
        if ("Percent" in l)or("%" in l):
            _gotit = 1
        if _gotit:
            if "+" in l:
                pass
            elif "/" in l:
                pass
            else:
                _exp += l
                l_exp.append(l)
    if no_grp:
        _exp = "活动类别,持续时间,Percent\n"
        _total,grp_act = _reformat_log(l_exp)
        for k in grp_act:
            _exp += "%s,"%k + ",".join(grp_act[k]) + "\n"
        _exp += "总计,%.2f"% _total

    f_exp = _titles+_exp
    _expf = fname.split("_")[1]
    open("./data/atl2_%s.csv"% _expf,'w').write(f_exp)
    #return _titles,_exp,""

def _reformat_log(log):
    '''reformt log
    - clean ""
    - merge no grp. logs
    '''
    act_map = {'Chaos':['Chaos',]
        , 'Life':['Life','运动','交通','Air','用餐','家务']
        , 'Input':['Input','阅读','学习','上网']
        , 'Output':['Output','交流','工作','GDG','OBP','Pt0']
        , 'Livin':['Livin','睡眠','购物','就医','Ukulele','电影','娱乐']
        , 'Untracked':['其他','Untracked']
        }
    grp_act = {}
    for l in log:
        #print ",".join([i[1:-1] for i in l[:-1].split(',')])
        crt_line = [i[1:-1] for i in l[:-1].split(',')]
        if "%" in crt_line:
            pass
        else:
            #print crt_line[0].split()[0]
            for k in act_map.keys():
                if crt_line[0].split()[0] in act_map[k]:
                    #print k,crt_line[0],crt_line[1:]
                    if k in grp_act:
                        grp_act[k].append(crt_line[1:])
                    else:
                        grp_act[k] = [crt_line[1:]]
    
    _total = 0
    for k in grp_act:
        #print k,grp_act[k]
        k_time = 0
        k_precent = 0
        for i in grp_act[k]:
            _time = i[0].split(':')
            d_time = int(_time[0])+float(_time[1])/60
            k_time += d_time
            _total += d_time
            k_precent += float(i[1])
            #print type(d_time)
        #print k_time, k_precent
        grp_act[k] = ["%.2f"%k_time, str(k_precent)]
    #print grp_act
    return _total,  grp_act

if __name__ == '__main__':
    if 2 != len(sys.argv) :
        print '''Usage:
$ pre_data_chk.py path/2/[数据目录] 
        '''
    else:
        aim_path = sys.argv[1]
        chk_all_log(aim_path)
        


