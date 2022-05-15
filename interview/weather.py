import pandas as pd
import datetime

def readDataset(reader):
    return pd.read_csv(reader, usecols=['Station Name', 'Measurement Timestamp', 'Air Temperature'])

def preprocessDataset(dataset):
    dataset['Measurement Timestamp'] = pd.to_datetime(dataset['Measurement Timestamp'])
    dataset.dropna(axis=0, inplace=True)
    return (sorted(dataset['Station Name'].unique().tolist()), dataset)

def addStationToDailyStats(dataset_input, station, daily_statistics):
    station_data = (dataset_input.loc[dataset_input['Station Name'] == station]).copy()
    station_data['Date'] = station_data['Measurement Timestamp'].dt.date
    for date in sorted(station_data['Date'].unique().tolist()):
        data_single_day = (station_data.loc[station_data['Date'] == date]).copy()
        data_single_day.sort_values('Measurement Timestamp', axis=0, inplace=True, ignore_index=True)
        daily_temp_info = {
            'Station Name': [station],
            'Date': [date],
            'Min Temp': [data_single_day['Air Temperature'].min()],
            'Max Temp': [data_single_day['Air Temperature'].max()],
            'First Temp': [data_single_day.iloc[0]['Air Temperature']],
            'Last Temp': [data_single_day.iloc[-1]['Air Temperature']]
        }
        daily_statistics = pd.concat([daily_statistics, pd.DataFrame(daily_temp_info)], axis=0, ignore_index=True)
    return daily_statistics

def postprocessDailyStats(daily_statistics):
    daily_statistics['Date'] = pd.to_datetime(daily_statistics['Date'])
    return daily_statistics

def printDailyStatistics(daily_statistics, writer):
    daily_statistics.to_csv(writer, index=False, date_format='%m/%d/%Y')

def process_csv(reader, writer):
    dataset_raw = readDataset(reader)
    stations, dataset_proc = preprocessDataset(dataset_raw)
    daily_statistics_raw = pd.DataFrame(columns=['Station Name', 'Date', 'Min Temp', 'Max Temp', 'First Temp', 'Last Temp'])
    for station in stations:
        daily_statistics_raw = addStationToDailyStats(dataset_proc, station, daily_statistics_raw)
    daily_statistics = postprocessDailyStats(daily_statistics_raw)
    # tmp = open('data/chicago_beach_weather_test_expected_output_tmp.csv', 'w')
    # printDailyStatistics(daily_statistics, tmp)
    printDailyStatistics(daily_statistics, writer)
