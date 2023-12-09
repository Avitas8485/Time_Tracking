import sqlite3
import plotly.express as px
import pandas as pd
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, db_name='dist\\window_tracker.db'):
        self.db_name = db_name
        
    
    
   
            
    def get_data(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM window_activity")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
        return rows, column_names
    
class DataProcessor:
    def __init__(self, rows: List[Tuple], column_names: List[str]):
        self.df = pd.DataFrame(rows, columns=column_names)
        self.process_dataframe()
        
    def process_dataframe(self):
        self.df['start_date'] = pd.to_datetime(self.df['start_date'])
        self.df['start_datetime'] = pd.to_datetime(self.df['start_date'].astype(str) + ' ' + self.df['start_time'])
        self.df['hour'] = self.df['start_datetime'].dt.hour
        self.df['day_of_week'] = self.df['start_datetime'].dt.day_name()
        self.df['month'] = self.df['start_datetime'].dt.month_name()
        self.df['year'] = self.df['start_datetime'].dt.year
        self.df['date'] = self.df['start_datetime'].dt.date
        # convert active time from seconds to minutes
        self.df['active_time'] = self.df['active_time'].astype(float)
        self.df['active_time'] = self.df['active_time'] / 60        
    def get_exes(self):
        exes = self.df['exe'].unique()
        return exes  
        
    def extract_idle_time(self):
        idle_time = self.df[self.df['exe'] == 'idle']
        return idle_time    
    
    def clean_df(self):
        self.df.drop(self.df[self.df['exe'] == 'None'].index, inplace=True)
        self.df.drop(self.df[self.df['exe'] == 'idle'].index, inplace=True)
        self.df = self.df.drop(columns=['id', 'pid', 'path', 'start_time', 'program_name'])
        self.df = self.df.sort_values(by='start_datetime')
        self.df = self.df.reset_index(drop=True)
        self.df['active_time'] = self.df['active_time'].astype(float)
        self.df['active_time'] = self.df['active_time'].round(2)
        
class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def get_total_active_time(self):
        return self.df.groupby(['exe'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)
    
    def get_total_active_time_by_range(self, range: str):
        if range not in ['day', 'hour', 'day_of_week', 'month', 'year', 'date']:
            return self.get_total_active_time()
        return self.df.groupby([range, 'exe'])['active_time'].sum().reset_index().sort_values(by='active_time', ascending=False)
        
    
    
    def get_program_frequency(self):
        return self.df.groupby(['exe'])['exe'].count().reset_index(name='count').sort_values(by='count', ascending=False)
    
    def get_program_frequency_by_range(self, range: str):
        if range not in ['day', 'hour', 'day_of_week', 'month', 'year', 'date']:
            return self.get_program_frequency()
        return self.df.groupby([range, 'exe'])['exe'].count().reset_index(name='count').sort_values(by='count', ascending=False)
        
    
    
class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.analyzer = DataAnalyzer(df)
        
    def visualize_total_active_time(self):
        fig = px.bar(self.df, x='exe', y='active_time', color='exe', title='Total Active Time')
        return fig
    
    def visualize_total_active_time_by_range(self, range: str):
        total_active_time_by_range = self.analyzer.get_total_active_time_by_range(range)
        title = f'Total Active Time by {range.capitalize()} if {range} in ["day", "hour", "day_of_week", "month", "year", "date"] else "Total Active Time"'
        return px.bar(total_active_time_by_range, x=range, y='active_time', color='exe', title=title)
        
    
    def visualize_program_frequency(self):
        df = self.df.groupby(['exe'])['exe'].count().reset_index(name='count').sort_values(by='count', ascending=False)
        fig = px.bar(df, x='exe', y='count', color='exe', title='Program Frequency')
        return fig
    def visualize_program_frequency_by_range(self, range: str):
        
        program_frequency_by_range = self.analyzer.get_program_frequency_by_range(range)
        title = f'Program Frequency by {range.capitalize()} if {range} in ["day", "hour", "day_of_week", "month", "year", "date"] else "Program Frequency"'
        return px.bar(program_frequency_by_range, x=range, y='count', color='exe', title=title)
        
    
    def visualize_proportion_of_time_spent_on_each_program(self):
        fig = px.pie(self.df, values='active_time', names='exe', title='Proportion of Time Spent on Each Program')
        return fig
    
    def visualize_timeline(self):
        fig = px.timeline(self.df, x_start="start_datetime", x_end="start_datetime", y="exe", title='Timeline of Program Usage')
        return fig
    
    def visualize_frequency_of_program_usage_per_day_of_week(self):
        fig = px.density_heatmap(self.df, x="day_of_week", y="exe", title='Frequency of Program Usage per Day of the Week')
        return fig
    
    def visualize_idle_time(self, df_idle_time: pd.DataFrame):
        fig = px.line(df_idle_time, x="date", y="active_time", title='Idle Time per Day')
        return fig
    
    
    def visualize(self):
        self.visualize_total_active_time().show()
        self.visualize_program_frequency().show()
        self.visualize_proportion_of_time_spent_on_each_program().show()
        self.visualize_timeline().show()
        self.visualize_frequency_of_program_usage_per_day_of_week().show()
        
if __name__ == '__main__':
    db_manager = DatabaseManager()
    rows, column_names = db_manager.get_data()
    data_processor = DataProcessor(rows, column_names)
    idle_time = data_processor.extract_idle_time()
    data_processor.clean_df()
    data_visualizer = DataVisualizer(data_processor.df)
    data_visualizer.visualize()
    

    
    
    