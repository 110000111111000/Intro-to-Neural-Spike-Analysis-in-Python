import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import pingouin as pg
     
import requests

url = "https://uni-bonn.sciebo.de/s/mLMkb2TwbNx3Yg6"
fname = "flash_spikes.parquet"
response = requests.get(f"{url}/download")
print("Downloading Data ...")
with open(fname, "wb") as file:
    file.write(response.content)
print("Done!")    

## Exercise 1
df = pd.read_parquet("flash_spikes.parquet")
print (df.head(5))
print("All possible questions : 1- what is brain area?LM ")
print("All possible questions : 2- what is unit for spike_time? Second")


