import os
import pandas as pd
from datetime import datetime

class Summary:
    def __init__(self, dir):
        summary_df = pd.DataFrame(columns=['Name', 'Date_Time', 'Balance_Avg', 'Cadence_Avg', 'Power_Avg', 'PES_Combined_Avg', 'PES_Right_Avg', 'PES_Left_Avg', 'Rotation_Count', 'Duration', 'ArrangedPolar'])
        index = 0
        for file in os.listdir(dir):
            if not file == '.DS_Store':
                self.file_path = f'{dir}/{file}'
                self.session_data = pd.read_csv(self.file_path)
                summary_df.loc[index] = self.SessionStats()
                index += 1
        summary_df.to_csv(f'{dir}/summary.csv', index=False)
    
    def SessionStats(self):
        file_list = self.file_path.split('/')
        self.date_time = datetime.fromisoformat(file_list[-1].replace('Z', '')[-23:-4].replace('_', ':'))
        file_name = file_list[-1].split('-')
        self.name = file_name[0] + "-" + file_name[1]

        self.balance_avg = sum(self.session_data['balance']) / len(self.session_data)
        self.cadence_avg = sum(self.session_data['cadence']) / len(self.session_data)
        self.power_avg = sum(self.session_data['power']) / len(self.session_data)
        self.PES_Combined_avg = sum([float(i) for i in self.session_data['pesCombinedCoefficient']]) / len(self.session_data)
        self.PES_Right_avg = sum([float(i) for i in self.session_data['pesRightCoefficient']]) / len(self.session_data)
        self.PES_Left_avg = sum([float(i) for i in self.session_data['pesLeftCoefficient']]) / len(self.session_data)
        self.rotation_count = len(self.session_data)
        self.duration = max(self.session_data['timeStamp'])

        self.polar_avg = []
        for index in range(361):
            element_list = []
            for row in self.session_data['arangedPolar']:
                row = row.replace('[', '').replace(']', '').split(',')
                element_list.append(row[index])
            self.polar_avg.append(sum([float(i) for i in element_list]) / len(element_list))

        return [self.name, self.date_time, self.balance_avg, self.cadence_avg, self.power_avg, self.PES_Combined_avg, self.PES_Right_avg, self.PES_Left_avg, self.rotation_count, self.duration, self.polar_avg]


if __name__ == '__main__':
   Summary('/Users/ben/Desktop/Projects/Wattbike-DataProcessor/sample-data/processed')