import seaborn as sn
import matplotlib.pyplot as plt

def read_dat(path):
    with open(path, 'r') as f:
        data = f.readlines()
    data.remove(data[0])
    mems = [float(data[i].split()[1]) for i in range(len(data))]
    return mems

data1 = read_dat('/home/mikhail/Desktop/CF_and_CS_grammars_comparsion/stats/100000_bad_cf.dat')
times1 = [0.1 * i for i in range(len(data1))]

data2 = read_dat('/home/mikhail/Desktop/CF_and_CS_grammars_comparsion/stats/100000_bad_cs.dat')
times2 = [0.1 * i for i in range(len(data2))]

sn.set_style('whitegrid')
plt.plot(times1, data1, 'r', label='Parser generator')
plt.plot(times2, data2, label='Parser combinator')
plt.xlabel('Time, seconds')
plt.ylabel('Memory usage, MiB')
plt.legend()

plt.savefig('100000_.png', dpi = 500)
plt.show()