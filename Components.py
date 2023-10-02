# libs
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
from math import floor
import json 
#import torch
#print(torch.is_vulkan_available())
#print(torch.cuda.is_available())

data = {
    "esp32":{
        'sleep (µA)':10,
        'peak (mA)':240,
        'receive only (mA)':100
    },
    "esp8684":{
        'sleep (µA)':5,
        'peak (mA)':370,
        'receive only (mA)':65
    },
    "esp8685":{
        'sleep (µA)':5,
        'peak (mA)':335,
        'receive only (mA)':87
    },
    "esp8266":{
        'sleep (µA)':20,
        'peak (mA)':170,
        'receive only (mA)':0
    },
    "esp8266+BLE":{
        'sleep (µA)':3020,
        'peak (mA)':210,
        'receive only (mA)':0
    },
    "stm32":{
        'sleep (µA)':0,
        'peak (mA)':340,
        'receive only (mA)':0
    }
}

# plotting
x=np.arange(len(data.keys()))
width=.25
multiplier=0

fig,ax = plt.subplots(layout='constrained')

attributes = data[list(data.keys())[0]].keys()
for attribute, measurement in zip(attributes, [[board[attribute] for board in data.values()] for attribute in attributes]):
    offset = width * multiplier
    rects = ax.bar(x+offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier+=1

ax.legend(loc='best', ncols=3)
ax.set_title("MCU Power Consumption")
ax.set_xticks(x + width, data.keys())
ax.set_ylim(0, 500)
plt.savefig("/tmp/plot.pdf")
plt.show()

for key, device in data.items():
    print(f"{key}\nsleep:\t\t{str(device['sleep (µA)'])+' µA' if device['sleep (µA)'] > 0 else 'none'}\npeak:\t\t{device['peak (mA)']} mA\nreceive only:\t{str(device['receive only (mA)'])+' mA' if device['receive only (mA)'] > 0 else 'none'}\n")


device = None

def genData(d):
    global device
    # print(f"\r{d['i']}", end="")
    if not d['i']%3600:
        print(f"\rProgress: {d['i']}", end="")
    return sum([data[d['d']]['sleep (µA)'] if i%d['i'] else data[d['d']]['peak (mA)']*1000 for i in range(1, 86400)])

with  mp.Pool(4) as p:
    results = {}
    for key in data.keys():
        device = key
        if not data[key]['sleep (µA)']:
            print(f"Device {key} has missing data")
            continue
        print(f'device: {key}, data: {data[key]}')
        results[key] = p.map(genData, [{'i':i, 'd':key} for i in range(10, 86400)])
        print()

print("finished executing")
# print(esp32)
# print(esp8685)


if not results:
    with open("component_results.json", "r") as file:
        import json
        results = json.loads(file.read())

breakpoints = {} 
for device in results.keys():
    breakpoints[device] = 0
    for i in range(1, len(results['esp32'])):
        if results[device][i] <= results['esp32'][i]:
            pass
            #print(i)
            #print(esp32[i])
            #print(esp8685[i])
            #print(esp8685[i] < esp32[i])
            #print()
        else:
            breakpoints[device] = i

    #print(f"breakpoint: {breakpoint}")
    print(f'{device} breakpoint:\t{str(floor(breakpoints[device]/3600))+" hours" if breakpoints[device] < 80000 else "None"}')

#print(breakpoints)

ax = plt.subplot()

ax.bar(breakpoints.keys(), breakpoints.values())
ax.set_ylim(0, 25000)

ax.set_ylabel("seconds (s)")

plt.plot()

with open("component_results.json", "w") as file:
    file.write(json.dumps(results, indent=4))
with open("component_breakpoints.json", "w") as file:
    file.write(json.dumps(breakpoints, indent=4))