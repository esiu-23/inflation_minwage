'''
For urban areas in the Western US: 
-Does min. wage track inflation over time? 
    Yes, it appears to for NY, IL, and CA
-Which state has the best min. wage? 
    In 2021, CA has the highest minimum wage

EVELYN SIU
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def clean_data(minwage_df, cpi_df):

### Data Used:  "Minimum_Wage_Data.csv", "CPI-U.csv"

    minwage = pd.read_csv(minwage_df)
    cpi = pd.read_csv(cpi_df)

    # Select only state minimum wage data
    minwage = minwage.iloc[:, :3]

    # Remove empty rows (from CSV formatting), and rename columns (Year, Months (1-12), Annual)
    cpi= cpi.iloc[11:,:14]
    for i in range(0, len(cpi.columns)):
        cpi= cpi.rename(columns={cpi.columns[i]:i})
        cpi= cpi.astype({i:float})

    cpi= cpi.rename(columns={cpi.columns[0]:"Year"})
    cpi= cpi.astype({"Year":int})
    cpi["Annual"] = cpi.mean(axis = 1)

    # Merge inflation & minimum wage datasets by year, by state
    full_df = pd.merge(minwage, cpi, on = "Year", how="left")
    full_df.set_index("Year")
    # Data for CPI only starts from 1980, remove all instances before that
    full_df = full_df [ full_df["Year"] >= 1980]

    # Save cleaned CSV for future use
    full_df.to_csv("minwage_{cpi_name}".format(minwage_name = minwage_df, cpi_name = cpi_df))

    return full_df
    

def calculate_annual_increases(full_df):
    unique_states = len(full_df["State"].unique())
    full_state = full_df.set_index("State")
    #full_state["min wage rate increase"] = full_state["State.Minimum.Wage"].pct_change(periods = unique_states)
    full_state["annual cpi increase"] = full_state["Annual"].pct_change(periods = unique_states)

    return full_state

def state_level_analyses(full_state, state):
    state_name = (full_state.loc[state])
    state_name["min wage keep up with inflation"] = state_name["State.Minimum.Wage"]
    state_name["min wage keep up with inflation"] = (state_name["min wage keep up with inflation"] * (1 + state_name["annual cpi increase"])).shift(1)
    state_name["min wage rate change"] = state_name["min wage keep up with inflation"].pct_change()
    
    return state_name


# Graphing 3 states: California, New York, and Illinois
full_df = clean_data("Minimum_Wage_Data.csv", "CPI-U.csv")
full_state = calculate_annual_increases(full_df)

ax = state_level_analyses(full_state, "California").plot(label = ["California - min wage", "California - inflation-adj. min wage"], x = "Year", y=["State.Minimum.Wage", "min wage keep up with inflation"], kind="line", color = ["#76EE00", "#458B00"])
state_level_analyses(full_state, "Illinois").plot(ax=ax, label = ["Illinois - min wage", "Illinois - inflation-adj. min wage"], x = "Year", y=["State.Minimum.Wage", "min wage keep up with inflation"], kind="line", color = ["#98F5FF", "#53868B"])
state_level_analyses(full_state, "New York").plot(ax=ax, label = ["New York - min wage", "New York - inflation-adj. min wage"], x = "Year", y=["State.Minimum.Wage", "min wage keep up with inflation"], kind="line", color = ["#FF7256", "#CD3333"])
ax.set_title("Minimum Wage in 3 States")
ax.set_ylabel("Minimum Wage ($)")
plt.show()




    






