import os
import re

log_dir = 'C:/Users/xypyf/Desktop/hwHangZhou/pack/STREAM/STREAM/results/log_97/node'
core_per_cluster = 38
operations = ['Copy', 'Scale', 'Add', 'Triad']
results = {}
min_numa = int(1e9)
max_numa = int(-1)
min_cluster = int(1e9)
max_cluster = int(-1)
min_epoch = int(1e9)
max_epoch = int(-1)

# print("log_dir:",log_dir)
for path,dirs,files in os.walk(log_dir):
    for file in files:
        filename=re.split(r'[_.]', file)
        dirs=re.split(r'[/\\]',path)
        # print(dirs)
        # assert 'epoch' in dirs[-2]
        epoch=0
        for dr in dirs:
            if 'epoch' in dr:
                epoch=int(dr.split('epoch')[-1])
        min_epoch = min(min_epoch, epoch)
        max_epoch = max(max_epoch, epoch)
        # print(filename)
        if len(filename) == 5 and 'Task' in filename[0] and filename[4] == 'log':
            f = open(os.path.join(path, file), "r")
            core_id = int(filename[1][4:].split('-')[0])
            numa_id = int(filename[2][4:])
            cluster_id = core_id // core_per_cluster
            min_cluster = min(min_cluster, cluster_id)
            max_cluster = max(max_cluster, cluster_id)
            min_numa = min(min_numa, numa_id)
            max_numa = max(max_numa, numa_id)
            res = {}
            for line in f:
                content = line.strip().split()
                if content[0].strip() in operations:
                    res[content[0].strip()] = float(content[1].strip())
            results[(epoch, numa_id, cluster_id)] = res
            # print("results[",(epoch, numa_id, cluster_id), "]=", res)
# print(min_numa, max_numa, min_cluster, max_cluster)

for numa_id in range(min_numa, max_numa + 1):
    for op in operations:
        sum_bw=0
        sum_epoch=0
        for epoch in range(min_epoch, max_epoch + 1):
            for cluster_id in range(min_cluster, max_cluster+1):
                if (epoch, numa_id, cluster_id) in results.keys():
                    if op in results[(epoch, numa_id, cluster_id)].keys():
                        print(results[(epoch, numa_id, cluster_id)][op], end='\t')
                        if abs(results[(epoch, numa_id, cluster_id)][op]) > 1e-5:
                            sum_epoch+=1
                            sum_bw+=results[(epoch, numa_id, cluster_id)][op]
                    else:
                        print(0.0, end='\t')
                        # pass
                else:
                    # print(0.0, end='\t')
                    pass
        # if sum_epoch == 0:
        #     print("0.0",end='\t')
        # else:
        #     print(sum_bw / sum_epoch,end='\t')
        print('\n', end='')