#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 10:47:14 2025

@author: xuzhixun
"""

import numpy as np
import matplotlib.pyplot as plt
import os



# calculate total time
def calculate_avg_total_time(monorail_travel_time,train_processing_time_range,flight_processing_time_range,additional_train_stop,return_time_range):
    #processing time range
    train_processing_time_min = train_processing_time_range[0]
    train_processing_time_max = train_processing_time_range[1]
    flight_processing_time_min = flight_processing_time_range[0]
    flight_processing_time_max = flight_processing_time_range[1]
    #return time range
    return_time_min = return_time_range[0]
    return_time_max = return_time_range[1]
    

    # statistic result
    traveler_number = {0:np.zeros(5),1:np.zeros(5)}
    statistic_result = {0:np.zeros(5),1:np.zeros(5)}
    
    # parameters
    # station ID
    HSR_station_index = 0
    Transit_monorail_station_index = 27
    # travel time list 0: HSR, 1: airplane
    travel_time_list = {0:[97,150,190,230,300], 1:[60,70,80,90,130]}
    
    for i in range(100000):
        # Step 1 generate demand(0＝HSR,1=flight)
        transport_type = np.random.randint(0, 2)
        start_station = np.random.randint(0, 30)
        # destination (Nagoya=0 Osaka=1 Okayama=2 Hiroshima=3 Hakata=4)
        destination_city = np.random.randint(5)
        
        # Step 2 access time
        if transport_type==0:
            access_time = min((start_station-HSR_station_index)%30,(HSR_station_index-start_station)%30)*2
        elif transport_type==1:
            time_transit_to_monorail = np.random.randint(1, 5)
            time_using_monorail = monorail_travel_time
            access_time = min((start_station-Transit_monorail_station_index)%30,(Transit_monorail_station_index-start_station)%30)*2 + time_transit_to_monorail + time_using_monorail 
        
        # Step 3 processing time
        if transport_type==0:
            processing_time = np.random.randint(train_processing_time_min,train_processing_time_max) 
        elif transport_type==1:
            processing_time = np.random.randint(flight_processing_time_min,flight_processing_time_max)
        
        # Step 4 travel time
        if transport_type==0:
            travel_time = travel_time_list[transport_type][destination_city] + 6.5*np.sum(additional_train_stop[:destination_city+1])
        elif transport_type==1:
            travel_time = travel_time_list[transport_type][destination_city]
        
        # Step 5 return time (to downtown)
        if transport_type==0:
            return_time = 0
        elif transport_type==1:
            return_time = np.random.randint(return_time_min, return_time_max)
        
        # Step 6 total time
        total_time = access_time + processing_time + travel_time + return_time
        
        # Step 7 sum up all demands
        traveler_number[transport_type][destination_city]+=1
        statistic_result[transport_type][destination_city]+=total_time
    
    # calculate avg results
    avg_HSR_time = statistic_result[0]/traveler_number[0]
    avg_flight_time = statistic_result[1]/traveler_number[1]
    
    return avg_HSR_time, avg_flight_time


# Calculate competitive range and draw a figure
def draw_figure(avg_HSR_time,avg_flight_time,case_ID,path_save_picture_dir):
    # mileage (km)
    km_list = [366.0,552.6,732.9,894.2,1174.9]

    # calculate competitive range
    diff = avg_HSR_time - avg_flight_time
    x_cross = None
    for i in range(len(diff)-1):
        if diff[i] * diff[i+1] < 0:
            x1 = km_list[i]
            x2 = km_list[i+1]
            y1 = diff[i]
            y2 = diff[i+1]
            # find x to let y = 0
            x_cross = round(x1 - y1 * (x2 - x1) / (y2 - y1),2)
            
            break

    # draw a diagram
    fig = plt.figure(figsize=(8,6))
    ax_1 = fig.add_subplot(1,1,1)
    ax_1.plot(km_list,avg_HSR_time,c='r',label = 'High-Speed Rail')
    ax_1.plot(km_list,avg_flight_time,c='b',label = 'Flight')
    ax_1.set_xlabel('Distance (km)')
    ax_1.set_ylabel('Total time (min)')
    ax_1.set_title('Competitive range: '+str(x_cross)+' km')
    ax_1.legend()
    
    
    plt.savefig(os.path.join(path_save_picture_dir,case_ID+'_comparison'), dpi=300,bbox_inches='tight')
    plt.close()





# create a directory to store figures
work = os.getcwd()
path_save_dir = os.path.join(work,'figures')
if not os.path.exists(path_save_dir):
    os.mkdir(path_save_dir)


# case 1
caseID = 'case1'
# monorail operating time
case1_monorail_travel_time = 25
# processing time 
case1_train_processing_time_range =[20,30]
case1_flight_processing_time_range =[60,90]
# additional stops
case1_additional_train_stop = np.array([0,0,0,0,0])
# return time
case1_return_time_range = [40,60]
# calculate total time
case1_avg_HSR_time, case1_avg_flight_time = calculate_avg_total_time(case1_monorail_travel_time,case1_train_processing_time_range,case1_flight_processing_time_range,case1_additional_train_stop,case1_return_time_range)
# draw a figure
draw_figure(case1_avg_HSR_time,case1_avg_flight_time,caseID,path_save_dir)


# case 2
caseID = 'case2'
# monorail operating time
case2_monorail_travel_time = 25
# processing time 
case2_train_processing_time_range =[20,30]
case2_flight_processing_time_range =[60,90]
# additional stops
case2_additional_train_stop = np.array([1,1,1,1,1])
# return time
case2_return_time_range = [40,60]
# calculate total time
case2_avg_HSR_time, case2_avg_flight_time = calculate_avg_total_time(case2_monorail_travel_time,case2_train_processing_time_range,case2_flight_processing_time_range,case2_additional_train_stop,case2_return_time_range)
# draw a figure
draw_figure(case2_avg_HSR_time,case2_avg_flight_time,caseID,path_save_dir)


# case 3
caseID = 'case3'
# monorail operating time
case3_monorail_travel_time = 25
# processing time 
case3_train_processing_time_range =[20,30]
case3_flight_processing_time_range =[40,60]
# additional stops
case3_additional_train_stop = np.array([0,0,0,0,0])
# return time
case3_return_time_range = [40,60]
# calculate total time
case3_avg_HSR_time, case3_avg_flight_time = calculate_avg_total_time(case3_monorail_travel_time,case3_train_processing_time_range,case3_flight_processing_time_range,case3_additional_train_stop,case3_return_time_range)
# draw a figure
draw_figure(case3_avg_HSR_time,case3_avg_flight_time,caseID,path_save_dir)


# case 4
caseID = 'case4'
# monorail operating time
case4_monorail_travel_time = 25
# processing time 
case4_train_processing_time_range =[20,30]
case4_flight_processing_time_range =[80,120]
# additional stops
case4_additional_train_stop = np.array([0,0,0,0,0])
# return time
case4_return_time_range = [40,60]
# calculate total time
case4_avg_HSR_time, case4_avg_flight_time = calculate_avg_total_time(case4_monorail_travel_time,case4_train_processing_time_range,case4_flight_processing_time_range,case4_additional_train_stop,case4_return_time_range)
# draw a figure
draw_figure(case4_avg_HSR_time,case4_avg_flight_time,caseID,path_save_dir)


# case 5
caseID = 'case5'
# monorail operating time
case5_monorail_travel_time = 25
# processing time 
case5_train_processing_time_range =[20,30]
case5_flight_processing_time_range =[40,60]
# additional stops
case5_additional_train_stop = np.array([1,1,1,1,1])
# return time
case5_return_time_range = [40,60]
# calculate total time
case5_avg_HSR_time, case5_avg_flight_time = calculate_avg_total_time(case5_monorail_travel_time,case5_train_processing_time_range,case5_flight_processing_time_range,case5_additional_train_stop,case5_return_time_range)
# draw a figure
draw_figure(case5_avg_HSR_time,case5_avg_flight_time,caseID,path_save_dir)


