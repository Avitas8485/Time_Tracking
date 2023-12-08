
import sqlite3
import streamlit as st
import plotly.express as px
import pandas as pd

# Create a connection to the database
conn = sqlite3.connect('window_tracker.db')
c = conn.cursor()

# Execute a query to get all the data from the table
c.execute("SELECT * FROM window_activity")
rows = c.fetchall()

# Create a dataframe from the query results
df = pd.DataFrame(rows, columns=['id', 'title', 'exe', 'pid', 'path', 'start_time', 'start_date', 'active_time', 'program_name'])

# Convert the start_time column to a datetime object
df['start_time'] = pd.to_datetime(df['start_time'])

# Create a new column for the date and time
df['date_time'] = df['start_date'] + " " + df['start_time'].dt.time.astype(str)

# Convert the date_time column to a datetime object
df['date_time'] = pd.to_datetime(df['date_time'])

# Create a new column for the hour
df['hour'] = df['date_time'].dt.hour

# Create a new column for the day of the week
df['day_of_week'] = df['date_time'].dt.day_name()

# Create a new column for the day of the month
df['day_of_month'] = df['date_time'].dt.day

# Create a new column for the month
df['month'] = df['date_time'].dt.month_name()

# Create a new column for the year
df['year'] = df['date_time'].dt.year

# Create a new column for the date
df['date'] = df['date_time'].dt.date

# Create a new column for the time
df['time'] = df['date_time'].dt.time

# convert the active_time column to a float
df['active_time'] = df['active_time'].astype(float)



print(df.head())

# Create a new dataframe for the total active time per program
df_total_active_time = df.groupby(['exe'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)


# Create a new dataframe for the total active time per program per day
df_total_active_time_per_day = df.groupby(['exe', 'date'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)

# Create a new dataframe for the total active time per program per hour
df_total_active_time_per_hour = df.groupby(['exe', 'hour'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)

# Create a new dataframe for the total active time per program per day of the week
df_total_active_time_per_day_of_week = df.groupby(['exe', 'day_of_week'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)

# Create a new dataframe for the total active time per program per day of the month
df_total_active_time_per_day_of_month = df.groupby(['exe', 'day_of_month'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)

# Create a new dataframe for the total active time per program per month
df_total_active_time_per_month = df.groupby(['exe', 'month'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)

# Create a new dataframe for the total active time per program per year
df_total_active_time_per_year = df.groupby(['exe', 'year'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)

# create a new dataframe for idle time
df_idle_time = df[df['exe'] == 'idle']

# create a new dataframe for frequency of programs
df_program_frequency = df.groupby(['exe'])['exe'].count().reset_index(name='count').sort_values(by='count', ascending=False)


