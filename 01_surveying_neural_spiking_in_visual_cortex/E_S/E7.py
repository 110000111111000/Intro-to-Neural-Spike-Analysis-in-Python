import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import pingouin as pg
     
import requests

#url = "https://uni-bonn.sciebo.de/s/mLMkb2TwbNx3Yg6"
#fname = "flash_spikes.parquet"
#response = requests.get(f"{url}/download")
#print("Downloading Data ...")
#with open(fname, "wb") as file:
#    file.write(response.content)
#print("Done!")    

## Exercise 1
df = pd.read_parquet("flash_spikes.parquet")
#print (df.head(5))
#print("All possible questions : 1- what is brain area?LM ")
#print("All possible questions : 2- what is unit for spike_time? Second")

## Exercise 2 
#print ("number of row or spikes in data",df.shape) 

## Exercise 3 
#print ("name of columns", df.columns)
spike_time = df["spike_time"] 
#print (spike_time)
#first_spike = df["spike_time"].min()
#last_spike = df["spike_time"].max()
#print(f"First spike time: {first_spike}")
#print(f"Last spike time: {last_spike}")

## Exercise 4
brain_area = df["brain_area"]
#print("brain_area",brain_area)
all_brain_area_recorded = df.brain_area.unique()
#print ("all_brain_area_recorded", all_brain_area_recorded)

##Exercise 5
unit =df["unit_id"]
Total_number_of_units_recorded =  len(unit)
#print("Total_number_of_units_recorded:",Total_number_of_units_recorded )

## Exercise 6
#print ("Total_number_of_spikes:",len(spike_time))
spike_counts = df.groupby("unit_id")["spike_time"].count()
#print(spike_counts)

## Exercise 7
unit_recorded_in_each_brain_area = df.groupby("brain_area")["unit_id"].count()
print("unit_recorded_in_each_brain_area:",unit_recorded_in_each_brain_area) 
