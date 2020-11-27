import seaborn as sn
import matplotlib.pyplot as plt
import argparse

ap = argparse.ArgumentParser()

ap.add_argument('-d', '--dat', required = True,
                help = 'Path to .dat file with memory profile info')

args = vars(ap.parse_args())
path = args['dat']

def read_dat(path):
    with open(path, 'r') as f:
        data = f.readlines()
    data.remove(data[0])
    mems = [float(data[i].split()[1]) for i in range(len(data))]
    return mems

data = read_dat(path)
times = [0.1 * i for i in range(len(data))]

sn.set_style('whitegrid')
plt.plot(times, data)
plt.xlabel('Time, seconds')
plt.ylabel('Memory usage, MiB')

plt.savefig(path + '_.png')
plt.show()