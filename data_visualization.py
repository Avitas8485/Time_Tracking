import sqlite3
import plotly.express as px
import pandas as pd
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, db_name='dist\\window_tracker.db'):
        self.db_name = db_name
        
    
    
   
            
    def get_data(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM window_activity")
                rows = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
            return rows, column_names
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    
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
        self.df['active_time'] = self.df['active_time'].astype(float) / 60      
        
    def get_exes(self):
        exes = self.df['exe'].unique()
        return exes  
        
    def extract_idle_time(self):
        idle_time = self.df[self.df['exe'] == 'idle']
        return idle_time    
    
    def clean_df(self):
        self.df = self.df[~self.df['exe'].isin(['None', 'idle'])]
        self.df = self.df.drop(columns=['id', 'pid', 'path', 'start_time', 'program_name'])
        self.df = self.df.sort_values(by='start_datetime')
        self.df['active_time'] = self.df['active_time'].round(2)
        
class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def get_total_active_time(self):
        return self.df.groupby(['exe'])['active_time'].sum().sort_values(ascending=False).reset_index()
    
    def get_total_active_time_by_range(self, range: str):
        if range not in ['day', 'hour', 'day_of_week', 'month', 'year', 'date']:
            return self.get_total_active_time()
        return self.df.groupby([range, 'exe'])['active_time'].sum().sort_values(ascending=False).reset_index()
        
    
    
    def get_program_frequency(self):
        return self.df['exe'].value_counts().reset_index(name='count').sort_values(by='count', ascending=False)
    
    def get_program_frequency_by_range(self, range: str):
        if range not in ['day', 'hour', 'day_of_week', 'month', 'year', 'date']:
            return self.get_program_frequency()
        return self.df.groupby([range, 'exe']).size().reset_index(name='count').sort_values(by='count', ascending=False)
        
    
    
class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.analyzer = DataAnalyzer(df)
        
    def visualize_total_active_time(self):
        return px.bar(self.df, x='exe', y='active_time', color='exe', title='Total Active Time')
    
    def visualize_total_active_time_by_range(self, range: str):
        total_active_time_by_range = self.analyzer.get_total_active_time_by_range(range)
        title = f'Total Active Time by {range.capitalize()}'
        return px.bar(total_active_time_by_range, x=range, y='active_time', color='exe', title=title)
    
    def visualize_program_frequency(self):
        df = self.analyzer.get_program_frequency()
        return px.bar(df, x='exe', y='count', color='exe', title='Program Frequency')
        
    
    def visualize_program_frequency_by_range(self, range: str):
        
        program_frequency_by_range = self.analyzer.get_program_frequency_by_range(range)
        title = f'Program Frequency by {range.capitalize()}'
        return px.bar(program_frequency_by_range, x=range, y='count', color='exe', title=title)
        
    
    def visualize_proportion_of_time_spent_on_each_program(self):
        return px.pie(self.df, values='active_time', names='exe', title='Proportion of Time Spent on Each Program')
    
    def visualize_timeline(self):
        return px.timeline(self.df, x_start='start_datetime', x_end='start_datetime', y='exe', color='exe', title='Timeline')
    
    def visualize_frequency_of_program_usage_per_day_of_week(self):
        return px.density_heatmap(self.df, x='day_of_week', y='exe', title='Frequency of Program Usage per Day of Week')
    
    def visualize_idle_time(self, df_idle_time: pd.DataFrame):
        return px.line(df_idle_time, x='start_datetime', y='active_time', title='Idle Time')
    
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
    

    
    
    