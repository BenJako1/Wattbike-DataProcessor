import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Visualise():
    def __init__(self, summary_path, outputData='pedal', index=2000):
        self.summary_path = summary_path
        self.outputData = outputData

        self.data = pd.read_csv(self.summary_path)
        
        if outputData == 'pedal':
            self.DisplayPolar([float(x) for x in self.data['polarForces'][index].replace('[', '').replace(']', '').split(',')])
        if outputData == 'pedal_avg':
            self.data['ArrangedPolar'] = [[float(x) for x in row.replace('[', '').replace(']', '').split(',')] for row in self.data['ArrangedPolar']]
            self.DisplayPolar(self.data['ArrangedPolar'][index])
        elif outputData == 'stats':
            print(self.SessionStats())
        else:
            self.DisplayCartesian(self.data, self.outputData)

    def DisplayCartesian(self, data, outputData):
        plt.plot(data['Date_Time'], data[outputData])
        plt.grid()
        plt.xlabel("time (s)")
        plt.ylabel(f'{outputData}')
        plt.show()
    
    def DisplayPolar(self, data):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(np.linspace(0, 2 * np.pi, len(data)), data, 'r-')
        ax.set_rgrids([round(elem, -1) for elem in np.linspace(0, max(data) + 20, 4)[1:]], angle=-67.5)
        ax.grid(True)
        ax.set_theta_offset(np.pi / 2)

        plt.title("Pedal Balance Polar Plot", va='bottom')
        plt.show()

if __name__ == '__main__':
    summary_path = f'/Users/ben/Desktop/Projects/Wattbike-DataProcessor/sample-data/processed/summary.csv'
    Visualise(summary_path, outputData='pedal_avg', index=1)