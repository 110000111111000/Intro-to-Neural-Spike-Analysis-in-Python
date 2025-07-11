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

# E5 – Create a new column for relative spike time
df["spike_time_relative_to_start"] = df["spike_time"] - df["start_time"]

# E6 – Filter for spikes where the relative time is greater than 1 second
df_filtered = df[df["spike_time_relative_to_start"] > 1]

# E7 – Plot histogram of the filtered spike times
sns.histplot(data=df_filtered, x="spike_time_relative_to_start", bins=50, kde=False)
plt.xlabel("Spike Time Relative to Stimulus Onset")
plt.ylabel("Count")
plt.title("Histogram of Relative Spike Times (> 1 second)")
plt.show()


