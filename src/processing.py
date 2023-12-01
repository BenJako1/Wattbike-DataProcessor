import os
import pandas as pd
import numpy as np
from datetime import datetime
from utils import interpolate

class ProcessData:
    def __init__(self):
        pass

    def FormatRaw(self, file_path):
        data = pd.read_csv(file_path)
        for index in range(len(data)):
            if data['pesCombinedCoefficient'][index] == 'na':
                data.drop([index], inplace=True)
        data.reset_index(inplace=True)
        data['polarForces'] = data['polarForces'].apply(lambda x: [int(i) for i in x.split(',')])
        data['pesCombinedCoefficient'] = data['pesCombinedCoefficient'].apply(lambda x: float(x))
        arranged_polar = [np.round(interpolate.Interpolate(np.linspace(0, 2 * np.pi, len(line)), line)[1], 2).tolist() for line in data['polarForces']]
        data['arangedPolar'] = arranged_polar

        timeStamp = [0]
        for index in range(len(data)):
            timeStamp.append(timeStamp[-1] + data['time'][index])
        data['timeStamp'] = timeStamp[1:]

        file_list = file_path.split('/')
        self.date_time = datetime.fromisoformat(file_list[-1].replace('Z', '')[-23:-4].replace('_', ':'))
        file_name = file_list[-1].split('-')
        self.name = file_name[2] + "-" + file_name[3]

        return data
     
    def OutputData (self, data, output_path):
        data.to_csv(output_path, index=False)
    
    def ProcessSweep(self, dir):
        input_path = dir
        output_path = os.path.join(os.path.dirname(os.path.realpath(dir)), "processed")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for file in os.listdir(input_path):
            data = self.FormatRaw(f'{dir}/{file}')
            datetime_output = self.date_time.strftime('%Y-%m-%dT%H_%M_%S')
            self.OutputData(data, os.path.join(output_path, f'{self.name}-{datetime_output}.csv'))

if __name__ == '__main__':
    run = ProcessData()
    run.ProcessSweep('/Users/ben/Desktop/Projects/Wattbike-DataProcessor/sample-data/raw')