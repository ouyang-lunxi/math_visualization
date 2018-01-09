#coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager,ticker
from collections import namedtuple
import pandas as pd
import os

m_font = font_manager.FontProperties(fname='C:\\Windows\\Fonts\\msyh.ttf',
                                     size = 9) 
m_font_12 = font_manager.FontProperties(fname='C:\\Windows\\Fonts\\msyh.ttf',
                                     size = 12) 
durations = {"对数的定义(上)":500320,
            "集合的基本运算-交集":626591,
            "平方根":294613,
            "点到圆的距离":555724}

subject = namedtuple("subject",["name",
                                "duration",
                                "excel_filepath",
                                "exit_time",
                                "exit_ratio",
                                "drag_start_time",
                                "learn_time",
                                "learn_time_ratio",
                                "finish_ratio"])

def get_data():
    subjects  = {}
    for (name,dur) in durations.items():
        filepath = "..\\xlsx\\" + name + ".xlsx"
        if not os.path.exists(filepath):
            continue
        df = pd.read_excel(filepath,header = 0,index_col = 1)
        click_video_exit = df.loc["clickVideoExit"]
        finish_video = df.loc["finishVideo"]
        c_start = df.loc["dragVideo"]
     
        finish_ratio = finish_video["video_name"].count() /   \
                        (finish_video["video_name"].count() + 
                         click_video_exit["video_name"].count())
        learn_time = pd.concat([finish_video["learn_time"],
                                click_video_exit["learn_time"]])
        learn_time[learn_time > dur / 1000] = dur / 1000
        
        print(name,click_video_exit["video_name"].count(),
                  finish_video["video_name"].count(),
                  learn_time.count())
        s = subject(name = name,
                    duration = dur,
                    excel_filepath = filepath,
                    exit_time = click_video_exit["exit_ratio"] * dur,
                    exit_ratio = click_video_exit["exit_ratio"],
                    drag_start_time = c_start["c_start"],
                    learn_time = learn_time,
                    learn_time_ratio = learn_time / 60 / dur,
                    finish_ratio = finish_ratio)
        subjects.update({name:s})
        
    return subjects
        
def draw_plots():
    subjects = get_data()
    draw_learn_time(subjects)
    
def draw_learn_time(subjects):
    fig = plt.figure()
    fig.set_figwidth(9)
    fig.set_figheight(6.1)
    fig.subplots_adjust(0.1,0.07,0.98,0.98,hspace = 0.18)
    for ((name,sj),ix) in zip(subjects.items(),range(1,5)):  
        xmax = sj.duration // 60000
        
        ax = fig.add_subplot(2,2,ix)
        vc_10 = sj.learn_time.value_counts(sort = False,bins = 10)
        vc_20 = sj.learn_time.value_counts(sort = False,bins = 20)
        vc_50 = sj.learn_time.value_counts(sort = False,bins = 50)
        
        print(name,vc_10)
        
#        ax.set_ylabel("频率：%",fontproperties = m_font)
#        ax.set_ylim([0,48])
#        ax.set_yticks(range(0,50,10))
#        ax.set_yticklabels(range(0,50,10),fontproperties = m_font)
#        
#        ax.set_xlabel("观看时长：分钟",fontproperties = m_font)
#        ax.set_xlim([0,xmax + 1])
#        ax.set_xticks(range(0,xmax + 2,2))
#        ax.set_xticklabels(range(0,xmax + 2,2),fontproperties = m_font)
#        
#        xminor_locator = ticker.MultipleLocator(0.2)
#        ax.xaxis.set_minor_locator(xminor_locator)
#        
#        for vc,lb in zip([vc_10,vc_20,vc_50],
#                            ["bins = 10","bins = 20","bins = 50"]):
#            x = vc.index.mid / 60
#            y = vc.values / sj.learn_time.count() * 100
#            ax.plot(x,y,label = lb)
#        
#        ax.legend(loc = "upper center",handlelength = 2,labelspacing = 0.5,
#                  frameon = False,ncol = 1,prop = m_font)
#        
#        ax.text(xmax * 0.4,30,name,fontproperties = m_font_12)
#    
#    plt.savefig("观看时长分布.jpg",dpi = 600)        
                
                
                
            
draw_plots()   