import csv
import sys
import matplotlib.pyplot as plt

if len(sys.argv)!=2:
  print('{} logfile'.format(sys.argv[0]))
  exit()

data_dict = {}

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count += 1
        #print(f'\t{row[0]} {row[1]} {row[2]}')
        if not row[1] in data_dict.keys():
            data_dict[row[1]] = []
        try:
            data_dict[row[1]].append((float(row[0]),float(row[2])))
        except ValueError:
            pass
    print('Processed {} lines.'.format(line_count))
    #print(data_dict)

plot_keys = [k for k in data_dict if len(data_dict[k])>1]
print(plot_keys)

for i,key in enumerate(plot_keys):
  if i==0:
    ax=plt.subplot(len(plot_keys),1,i+1)
    top_ax = ax
  else:
    ax=plt.subplot(len(plot_keys),1,i+1,sharex=top_ax)
  plt.plot([d[0] for d in data_dict[key]],[d[1] for d in data_dict[key]])
  plt.title(key)

plt.show()
