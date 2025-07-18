import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt 
import seaborn as sns
from scipy.stats import wilcoxon 
#%matplotlib inline
## https://www.youtube.com/watch?v=2AqoK8itEFQ related to wilcoxon test

##1.Preparation
#import requests

#urls = [
#    "https://uni-bonn.sciebo.de/s/G64EkHoQkeZeoLm",
#    "https://uni-bonn.sciebo.de/s/mLMkb2TwbNx3Yg6",
#]

#fnames = ["flash_stimuli.parquet", "flash_spikes.parquet"]

#for url, fname in zip(urls, fnames):
#    response = requests.get(f"{url}/download")
#    print("Downloading Data ...")
#    with open(fname, "wb") as file:
#        file.write(response.content)
#    print("Done!")

#### E1
spikes = pd.read_parquet("flash_spikes.parquet")
#print(df.head(5))
#print(spikes.head(5)) 
stimuli = pd.read_parquet("flash_stimuli.parquet")
#print(stimuli.head(10))

#### E2
df = pd.merge_asof(spikes, stimuli, left_on="spike_time", right_on="start_time")
#print(df.head(10))
#print("Get more information about merge_asof function")

## E3
stimuli["analysis_window_start"] = stimuli["start_time"] - 0.5
#print(stimuli.head(10))

## E4 
df = pd.merge_asof(spikes, stimuli, left_on="spike_time", right_on= "analysis_window_start")
#print(df.head(20))

### ?
# I would like to ask a question about Exercise 5.
print('''The question is:

"Subtract the .start_time column from the .spike_time column to get the spike times relative to stimulus onset. Then, print the smallest spike time in df. This value should be very close to -0.5."

To solve the problem, I wrote the following script.
As a result, I got -296.1868826019397 as the minimum spike time.
However, I was expected to get a value around -0.5.''')





## E5
df = pd.merge_asof(spikes, stimuli, left_on="spike_time", right_on= "start_time")
df["spike_time_start_time"] = spikes["spike_time"] - stimuli["start_time"]
print(min(df["spike_time_start_time"]))
    
