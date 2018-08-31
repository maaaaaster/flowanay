import time
import numpy as np
state_size=10
markovLen = 10 # first n packets
stateLen = state_size**2
markovKeys = {'times': 1000, 'lens': 150}

def str2time(time_str,ns):
    ns = int(str(ns)[:6])
    return time.mktime(time.strptime(time_str,'%Y-%m-%d %H:%M:%S'))*(10**6)+ns
def secAndNs(time,ns):
    ns = int(str(ns)[:6])
    return time*(10**6)+ns

def chain2markov(array_data):
    state_matrix = [0]*stateLen
    arr_len = min(len(array_data),markovLen)
    for i in range(arr_len-1):
        state_matrix[array_data[i]*state_size+array_data[i+1]]+=1
    for i in range(state_size):
        all_count = sum(state_matrix[i*state_size:(i+1)*state_size])
        if all_count<=0:
            continue
        for j in range(state_size):
            state_matrix[i*state_size+j] /= all_count
    return state_matrix


def Packets2Time(packets):
    times = []
    lens = []
    for packet in packets:
        lens.append(min(abs(packet['Len'])//markovKeys['lens'],state_size-1))
        if len(times)==0:
            pretime = secAndNs(packet['Sec'],packet['nSec'])
        nowtime = secAndNs(packet['Sec'], packet['nSec'])
        gap = max((nowtime-pretime)//markovKeys['times'],0)
        times.append(min(state_size-1,gap))
        pretime=nowtime
    data = {'times':times,'lens':lens}
    result = {}
    for key in markovKeys:
        result[key + 'Max']=max(data[key])
        result[key + 'Min']=min(data[key])
        result[key + 'Mean']=np.mean(data[key])
        result[key + 'Std']=np.std(data[key])
        states = chain2markov(data[key])
        for i in range(len(states)):
            state = states[i]
            result['%s_%d'%(key,i)]=state
    return result
