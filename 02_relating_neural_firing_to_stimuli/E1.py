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
print("Spike DataFrame containing Five rows:",spikes.head(5)) 
stimuli = pd.read_parquet("flash_stimuli.parquet")
print("Stimuli DataFrame containing ten rows:",stimuli.head(10))


    
