import numpy as np
import pandas as pd
import os

durations = {"对数的定义(上)":500320,
            "集合的基本运算-交集":626591,
            "平方根":294613,
            "点到圆的距离":555724,
            "对数的化简与求值":640384}

def get_data():
    for (name,dur) in durations.items():
        filepath = "..\\xlsx\\%s.xlsx" % name
        df = pd.read_excel(filepath,header = 0,index_col = 1)
#        extract_click_video_exit(df,name)
#        extract_finish_video(df,name,dur)
#        extract_learn_time(df,name,dur)
        extract_drag_forward_video(df,name,dur,5000,10000)
        extract_drag_backward_video(df,name,dur,5000,10000)
#        extract_drag_forward_video_duration(df,name)
#        extract_drag_backward_video_duration(df,name)

#退出时间点(比值)     
def extract_click_video_exit(df,subject_name):
    cve = df.loc["clickVideoExit"]["exit_ratio"]
    cve[cve < 0.0] = 0.0
    cve[cve >= 1.0] = 0.999
    
    cve_dire = "..\\csv\\clickVideoExit"
    if not os.path.exists(cve_dire):
        os.makedirs(cve_dire)
    
    cve_filepath = os.path.join(cve_dire,"%s_clickVideoExit.csv" % subject_name)
    cve.to_csv(cve_filepath,index = False,header = ["head"])
    
#视频完成情况（比值）
def extract_finish_video(df,subject_name,subject_duration):
    fv = df.loc["finishVideo"]["learn_time"]
    fv = fv / subject_duration * 1000
    fv[fv < 0.0] = 0.0
    fv[fv >= 1.0] = 0.999
    fv_dire = "..\\csv\\finishVideo"
    if not os.path.exists(fv_dire):
        os.makedirs(fv_dire)
    fv_filepath = os.path.join(fv_dire,"%s_finishVideo.csv" % subject_name)
    fv.to_csv(fv_filepath,index = False,header = ["head"])
    
#观看时长
def extract_learn_time(df,subject_name,subject_duration):
    fv = pd.concat([df.loc["finishVideo"]["learn_time"],
                    df.loc["clickVideoExit"]["learn_time"]])
    fv = fv / subject_duration * 1000
    fv[fv < 0.0] = 0.0
    fv[fv >= 1.0] = 0.999
    fv_dire = "..\\csv\\learnTime"
    if not os.path.exists(fv_dire):
        os.makedirs(fv_dire)
    fv_filepath = os.path.join(fv_dire,"%s_learnTime.csv" % subject_name)
    fv.to_csv(fv_filepath,index = False,header = ["head"])
    
#向前拖拽行为
def extract_drag_forward_video(df,subject_name,subject_duration,interval_min,
                               interval_max):
    fv = df.loc["dragVideo"]
    fv = fv[(fv["c_start"] - fv["c_end"]) > interval_min]
    fv = fv[(fv["c_start"] - fv["c_end"]) <= interval_max]["c_start"]
    fv = fv / subject_duration
    fv[fv < 0.0] = 0.0
    fv[fv >= 1.0] = 0.999
    fv_dire = "..\\csv\\dragVideoForward0"
    if not os.path.exists(fv_dire):
        os.makedirs(fv_dire)
    fv_filepath = os.path.join(fv_dire,
                               "%s_dragVideoForward0.csv" % subject_name)
    fv.to_csv(fv_filepath,index = False,header = ["head"])
    
#向后拖拽行为
def extract_drag_backward_video(df,subject_name,subject_duration,interval_min,
                                interval_max):
    fv = df.loc["dragVideo"]
    fv = fv[(fv["c_end"] - fv["c_start"]) > interval_min]
    fv = fv[(fv["c_end"] - fv["c_start"]) <= interval_max]["c_start"]
    fv = fv / subject_duration
    fv[fv < 0.0] = 0.0
    fv[fv >= 1.0] = 0.999
    fv_dire = "..\\csv\\dragVideoBackward0"
    if not os.path.exists(fv_dire):
        os.makedirs(fv_dire)
    fv_filepath = os.path.join(fv_dire,
                               "%s_dragVideoBackward0.csv" % subject_name)
    fv.to_csv(fv_filepath,index = False,header = ["head"])
    
#向前拖拽时长
def extract_drag_forward_video_duration(df,subject_name):
    fv = df.loc["dragVideo"]
    fv = fv[fv["c_start"] > fv["c_end"]]
    fv = (fv["c_start"] - fv["c_end"]) / 1000
    fv[fv >= 700] = 699.99

    fv_dire = "..\\csv\\dragVideoForwardDuration"
    if not os.path.exists(fv_dire):
        os.makedirs(fv_dire)
    fv_filepath = os.path.join(fv_dire,
                               "%s_dragVideoForwardDuration.csv" % subject_name)
    fv.to_csv(fv_filepath,index = False,header = ["head"])
    
#向后拖拽时长
def extract_drag_backward_video_duration(df,subject_name):
    fv = df.loc["dragVideo"]
    fv = fv[fv["c_start"] < fv["c_end"]]
    fv = (fv["c_end"] - fv["c_start"]) / 1000
    fv[fv >= 700] = 699.99

    fv_dire = "..\\csv\\dragVideoBackwardDuration"
    if not os.path.exists(fv_dire):
        os.makedirs(fv_dire)
    fv_filepath = os.path.join(fv_dire,
                               "%s_dragVideoBackwardDuration.csv" % subject_name)
    fv.to_csv(fv_filepath,index = False,header = ["head"])
        
   
get_data()
