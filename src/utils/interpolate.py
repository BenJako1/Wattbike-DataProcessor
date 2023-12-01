import numpy as np

def Interpolate(x, y):
    data = np.vstack((np.degrees(x), y))
    
    fit = np.zeros((2, 0))

    for i in range(len(data[0])-2):
        a, b, c = np.polyfit(data[0, i:i+3], data[1, i:i+3], 2)

        f = lambda X: a * X**2 + b * X + c

        x_int = np.arange(int(data[0, i]), int(data[0, i+1]) + 1).astype(int)

        y_int = f(x_int)

        fit = np.hstack((fit, np.vstack((np.radians(x_int), y_int))))

    a, b, c = np.polyfit(data[0, -3:], data[1, -3:], 2)

    f = lambda X: a * X**2 + b * X + c

    x_int = np.arange(int(data[0, len(data[0])-2]), int(data[0, len(data[0])-1]) + 1).astype(int)

    y_int = f(x_int)

    fit = np.hstack((fit, np.vstack((np.radians(x_int), y_int))))

    _, unique_indices = np.unique(fit[0, :], return_index=True)

    fit = fit[:, unique_indices]

    return fit[0, :], fit[1, :]