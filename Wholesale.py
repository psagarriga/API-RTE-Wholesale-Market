#!/usr/bin/env python
# coding: utf-8

# In[55]:

import pandas as pd
import plotly.express as px

import requests
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

url = "https://digital.iservices.rte-france.com/token/oauth/"
data = { 'Authorization' : 'Basic ZjI3YjM5MTUtMTYzYi00OTFlLTllN2UtYWNlM2FiM2QxMjFiOjk3ZWExOGFkLTkyMDQtNGE1NC1iNmNmLTM4NTkwNmVlOTk4Nw==' ,
        'Content-Type': 'application/x-www-form-urlencoded',
       }


# In[56]:



# In[6]:

response = requests.post(url, headers=data)
status_code = response.status_code
print('status code =',status_code)


# In[57]:



# In[9]:


info_rte_token = response.json()
print('info_rte_token =', info_rte_token)


# In[11]:

token = info_rte_token['access_token']
print('token =', token)


# In[58]:



# In[13]:

from datetime import datetime, timedelta

# Calculate the end date as today's date
ending_date = datetime.now()

# Calculate the start date as 10 days before the end date
starting_date = ending_date - timedelta(days=2)

# Format the dates in the required format
start_date_str = starting_date.strftime("%Y-%m-%dT%H:%M:%S%z")+"%2B02:00"
end_date_str = ending_date.strftime("%Y-%m-%dT%H:%M:%S%z")+"%2B02:00"

print (starting_date, ending_date)
print (start_date_str, end_date_str)

start_date_str = start_date_str.replace("%2B", "+")
end_date_str = end_date_str.replace("%2B", "+")
print(start_date_str)
print(end_date_str)


# In[59]:



url = f"https://digital.iservices.rte-france.com/open_api/wholesale_market/v2/france_power_exchanges?start_date={start_date_str}&end_date={end_date_str}"


data = { 'Authorization' : 'Bearer '+ token,
        'Content-Type': 'application/soap+xml',
        'charset' : 'UTF-8',
       }

response = requests.get(url, headers=data)
status_code = response.status_code
print('status code =',status_code)



# In[60]:


data = response.json()

print (data)


# In[61]:



# Extract the 'values' list which is nested within the data dictionary
values_list = data['france_power_exchanges'][0]['values']

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(values_list)

# Select only the 'start_date' and 'price' columns
df = df[['start_date', 'price']]

# Optionally, convert the 'start_date' to a datetime format for better handling
df['start_date'] = pd.to_datetime(df['start_date'])

print(df.head())  # Show the first few rows of the dataframe


# In[62]:


# Extract the 'values' list which is nested within the data dictionary
values_list = data['france_power_exchanges'][0]['values']

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(values_list)


# In[63]:


print (df)


# In[64]:


df['start_date'] = pd.to_datetime(df['start_date'])

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
# Adjusting mode to 'lines' for the area plot to remove markers
fig.add_trace(go.Scatter(x=df['start_date'], y=df['value'], name="Volumes", fill='tonexty', mode='lines'), secondary_y=False)
fig.add_trace(go.Scatter(x=df['start_date'], y=df['price'], name="Prices", mode='lines', marker=dict(color='orange')), secondary_y=True)

# Add figure title
fig.update_layout(title_text="Volumes and Prices Over Time", plot_bgcolor='white')

# Set y-axes titles
fig.update_yaxes(title_text="Volume [MWh]", secondary_y=False)
fig.update_yaxes(title_text="Price [€/MWh]", secondary_y=True)

# Assuming execution in a compatible environment, this will display the figure.


# In[ ]:

# Export the figure as an HTML file
fig.write_html('Wholesale_market.html')



# In[ ]:




