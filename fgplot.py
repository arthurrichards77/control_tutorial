import csv
import sys
import os
import matplotlib.pyplot as plt

def import_log(file_name):

    print('Opening {}'.format(file_name))
    data_dict = {}

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if not row[1] in data_dict.keys():
                data_dict[row[1]] = ([], [])
                value = None
                stamp = None
            try:
                value = float(row[2])
                stamp = float(row[0])
            except ValueError:
                pass
            if value and stamp:
                data_dict[row[1]][0].append(stamp)
                data_dict[row[1]][1].append(value)
        print('Processed {} lines.'.format(line_count))
    return(data_dict)

def plot_log(file_name):

    data_dict = import_log(file_name)

    plot_keys = [k for k in data_dict if len(data_dict[k][0]) > 1]
    print(plot_keys)

    for i, key in enumerate(plot_keys):
        if i == 0:
            this_ax = plt.subplot(len(plot_keys), 1, i+1)
            top_ax = this_ax
        else:
            this_ax = plt.subplot(len(plot_keys), 1, i+1, sharex=top_ax)
        plt.plot(data_dict[key][0], data_dict[key][1])
        plt.title(key)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_list = [fn for fn in os.listdir('logs') if fn.endswith('.csv')]
        file_list.sort()
        if len(file_list) == 0:
            print('Unable to find log file')
            sys.exit(1)
        else:
            file_name = 'logs/'+file_list[-1]
    plot_log(file_name)
