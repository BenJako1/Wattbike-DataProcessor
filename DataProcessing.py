import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_name = 'WB-HUB-BEN-JAKOBS-2023-11-19T14_51_44Z'
file_path = f'ExampleData/raw/{file_name}.csv'
ouput_file_path = f'ExampleData/processed/{file_name}_Processed.csv'

class Visualise:
    def __init__(self):
        pass

    def DisplayCartesian(self, data, outputData):
        plt.plot(data['timeStamp'], data[outputData])
        plt.grid()
        plt.xlabel("time (s)")
        plt.ylabel(f'{outputData}')
        plt.show()
    
    def DisplayPolar(self, data, index):
        force = np.array(data['polarForces'][index])
        angle = np.linspace(0, 2 * np.pi, len(force))

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(angle, force)
        ax.set_rgrids([round(elem, -1) for elem in np.linspace(0, max(force) + 20, 4)[1:]], angle=-67.5)
        ax.grid(True)
        ax.set_theta_offset(np.pi / 2)

        plt.title("Pedal Balance Polar Plot", va='bottom')
        plt.show()

class DataHandler(Visualise):
    def __init__(self, file_path, outputData='power'):
        self.file_path = file_path
        self.outputData = outputData

        self.data = self.FormatData()

        #print(self.SessionStats())
        #self.DisplayCartesian(self.data, self.outputData)
        self.DisplayPolar(self.data, 501)

    def FormatData(self):
        data = pd.read_csv(self.file_path)
        for index in range(len(data)):
            if data['pesCombinedCoefficient'][index] == 'na':
                data.drop([index], inplace=True)
        data.reset_index(inplace=True)
        data['polarForces'] = data['polarForces'].apply(lambda x: [int(i) for i in x.split(',')])

        timeStamp = [0]
        for index in range(len(data)):
            timeStamp.append(timeStamp[-1] + data['time'][index])
        data['timeStamp'] = timeStamp[1:]

        return data
    
    def SessionStats(self):
        self.balance_avg = sum(self.data['balance']) / len(self.data)
        self.cadence_avg = sum(self.data['cadence']) / len(self.data)
        self.power_avg = sum(self.data['power']) / len(self.data)
        self.PES_Combined_avg = sum([float(i) for i in self.data['pesCombinedCoefficient']]) / len(self.data)
        self.PES_Right_avg = sum([float(i) for i in self.data['pesRightCoefficient']]) / len(self.data)
        self.PES_Left_avg = sum([float(i) for i in self.data['pesLeftCoefficient']]) / len(self.data)
        self.rotation_count = len(self.data)

        return self.balance_avg, self.cadence_avg, self.power_avg, self.PES_Combined_avg, self.PES_Right_avg, self.PES_Left_avg, self.rotation_count

class Output_File(DataHandler):
    def __init__(self, file_path, ouput_file_path):
        self.file_path = file_path
        data = self.FormatData()
        data.to_csv(ouput_file_path, index=False)

DataHandler(file_path, 'power')
#Output_File(file_path, ouput_file_path)