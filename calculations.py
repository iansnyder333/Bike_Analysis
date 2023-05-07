import os
import pandas as pd
import datetime
import time
import numpy as np
from collections import defaultdict
from math import isnan


class Calculations:
    def __init__(self, files):
        self.trips = self.produce_trips_table(files)
        self.daily_counts = self.calculate_daily_counts(self.get_trips())
        self.monthly_counts = self.calculate_monthly_counts(self.get_trips())
        

     
    
    def get_trips(self):
        return self.trips

    def get_daily_counts(self):
        return self.daily_counts

    def get_monthly_counts(self):
        return self.monthly_counts

    def produce_trips_table(self, files: list):
        if len(files)<1:
            return 
        infile = files[0]
        if isinstance(infile, str):
            data = pd.read_csv(infile)
            
        else:
            data = infile.copy()
        for index, file in enumerate(files, start=1):
            if isinstance(file, str):
                cur = pd.read_csv(file)
                data = pd.concat([data, cur], ignore_index=True)
                
            else:
                cur = file.copy()
                data = pd.concat([data, cur], ignore_index=True)
        
      
        # DataFrame must have at least the 'Bikeid', 'Starttime', 'Trip id', 'From station id', 'To station id' columns
    
        df = data[['Bikeid', 'Starttime', 'Trip id', 'From station id', 'To station id']].copy()
        df['Starttime'] = pd.to_datetime(
            df['Starttime'], format="%m/%d/%Y %H:%M")
        df['day'] = df['Starttime'].dt.strftime('%m/%d/%Y')
        df['hour'] = df['Starttime'].dt.strftime('%H')
        df['month'] = df['Starttime'].dt.strftime('%m/%Y')
        df['date'] = df['Starttime'].dt.date
        

        #df['month'] = months
        #df['day']=day
        #df['hour']=hours
        
        
        return df
    
    def calculate_daily_counts(self, trips):
        df2 = df = trips.copy()
        df2.drop_duplicates(
            subset=['Bikeid', 'Starttime', 'Trip id', 'From station id', 'To station id'], inplace=True)

        from_df = df2.groupby(['day', 'From station id']
                         ).size().reset_index(name='fromCNT')
        to_df = df2.groupby(['day', 'To station id']
                         ).size().reset_index(name='toCNT')
        from_df = from_df.rename(columns={'From station id': 'station_id'})


        to_df = to_df.rename(columns={'To station id': 'station_id'})
        rebals2 = self.runte()
        rebals2['origin']='rebals'
        rebals2 = rebals2.rename(columns={'From station id':'station_id'})
        rebals2['toCNT']=0
        rebals2['fromCNT']=0
        # Merge the DataFrames
        from_df['origin']='from'
        to_df['origin']='to'
        from_df['toCNT'] = 0
        from_df['rebalCNT']=0

        to_df['fromCNT'] = 0
        to_df['rebalCNT']=0
        # Concatenate the DataFrames
        combined_df = pd.concat([from_df, to_df,rebals2], ignore_index=True)

        # Group by 'day' and 'station_id', sum 'fromCNT' and 'toCNT', and reset the index
        daily_counts = combined_df.groupby(['day', 'station_id'], as_index=False).sum(numeric_only=True)

        #print(combined_df.head(10))
        
    
        daily_counts['station_id'] = daily_counts['station_id'].astype(int)
        daily_counts['fromCNT'] = daily_counts['fromCNT'].astype(int)
        daily_counts['toCNT'] = daily_counts['toCNT'].astype(int)
        daily_counts['rebalCNT'] = daily_counts['rebalCNT'].astype(int)
        daily_counts.sort_values(['day', 'station_id'], inplace=True)
       
        return daily_counts
   
    
    def rebals(self):
        df = self.trips
        


        
        df_curDay = df.sort_values(['Bikeid', 'Starttime'])
        #df_curDay.dropna(subset=['From station id'], inplace=True)
        
        df_curDay.dropna(subset=['From station id'], inplace=True)
        df_curDay['prevStation'] = df_curDay['To station id'].shift(1)
        df_curDay['prevBike'] = df_curDay['Bikeid'].shift(1)
        df_curDay['first'] = df_curDay.duplicated(
            subset=['Bikeid'], keep='first')
        df_curDay = df_curDay[df_curDay['first']==True]
        df_curDay = df_curDay[df_curDay['Bikeid']==df_curDay['prevBike']]
        df_curDay.drop_duplicates(subset=['Trip id'],inplace=True)
        
       
        dailyRebals = (df_curDay['From station id'] != df_curDay['prevStation']
                       ) & (df_curDay['prevBike'] == df_curDay['Bikeid'])
        rebalances = df_curDay[dailyRebals].groupby(
            ['day', 'From station id']).size().reset_index(name='rebalCNT')
        
        #rebalances.dropna(subset=['From station id'], inplace=True)
        
        return rebalances
       
    def calculate_monthly_counts(self, trips):
        df = self.get_daily_counts().copy()
        df['day'] = pd.to_datetime(df['day'], format='%m/%d/%Y')
       
        df['month'] = df['day'].dt.strftime('%m/%Y')
        monthly_frequency = df.groupby(['month', 'station_id']).agg(
            {'fromCNT': 'sum', 'toCNT': 'sum', 'rebalCNT': 'sum'}).reset_index()
        monthly_frequency.sort_values(['month', 'station_id'], inplace=True)
        return monthly_frequency


    def runte(self):
        data = self.trips.copy()
        data.drop_duplicates(subset=['Trip id'], inplace=True)
        sorted_data = data.sort_values(['Bikeid', 'Starttime'])
        rebalancing_counts = {}
        previous_bikeid = None


        previous_station = None

        for index, row in sorted_data.iterrows():
            bikeid = row['Bikeid']
            from_station = row['From station id']
            to_station = row['To station id']
            date = row['day']

            # Check if the bikeID has changed
            if bikeid != previous_bikeid:
                previous_bikeid = bikeid
                previous_station = to_station
            else:
                # If the bikeID is the same but the from_station has changed, a rebalancing event occurred
                if from_station != previous_station and not isnan(from_station):
                    if (date, from_station) not in rebalancing_counts:
                        rebalancing_counts[(date, from_station)] = 1
                    else:
                        rebalancing_counts[(date, from_station)] += 1

                previous_station = to_station
        


        # Convert the dictionary to a list of tuples
        rebalancing_list = [(date, station, count)
                            for (date, station), count in rebalancing_counts.items()]

        # Create a DataFrame from the list of tuples
        rebalancing_df = pd.DataFrame(rebalancing_list, columns=[
                                    'day', 'From station id', 'rebalCNT'])

     
        return rebalancing_df 






  
    
    
    
        
if __name__ == "__main__":
    calculations = Calculations(['HealthyRideRentals2021-Q1.csv', 'HealthyRideRentals2021-Q2.csv', 'HealthyRideRentals2021-Q3.csv'])
   
    print("-------------- All Trips ---------------")
    #print(calculations.get_trips())
    print("-------------- Daily Counts ---------------")
    print(calculations.get_daily_counts())
    print()
    print("------------- Monthly Counts---------------")
    print(calculations.get_monthly_counts())
    print()
  