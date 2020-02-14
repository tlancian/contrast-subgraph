import pandas as pd
import argparse
import os
from functools import reduce
import numpy as np
import subprocess


# Arguments for computing Contrast Subgraph

parser = argparse.ArgumentParser(description='Graph Classification via Contrast Subgraph')

parser.add_argument('d', help='dataset', type=str)
parser.add_argument('c1', help='class1', type=str)
parser.add_argument('c2', help='class2', type=str)
parser.add_argument('a', help='alpha', type=float)
parser.add_argument('--p2', help='alpha', action='store_true')

args = parser.parse_args()

dir1 = "datasets/{}/{}/".format(args.d,args.c1)
c1 = ["{}/{}".format(dir1,elem) for elem in os.listdir(dir1)]

dir2 = "datasets/{}/{}/".format(args.d,args.c2)
c2 = ["{}/{}".format(dir2,elem) for elem in os.listdir(dir2)]


# Create and Write Summary Graphs
summary_c1 = reduce(lambda x,y:x+y,map(lambda x: np.array(pd.read_csv(x, header = None, sep = ",")),c1))/len(os.listdir(dir1))
summary_c2 = reduce(lambda x,y:x+y,map(lambda x: np.array(pd.read_csv(x, header = None, sep = ",")),c2))/len(os.listdir(dir2))

if not args.p2:
    diff_net = summary_c1 - summary_c2
else:
    diff_net = abs(summary_c1 - summary_c2)


with open("icdm16-egoscan/net.txt", 'w') as f:
    for row in range(1,summary_c1.shape[1]):
        for col in range(row):
            f.write("{} {} {}".format(row,col,diff_net[row][col])+"\n")
    f.close()

os.chdir("icdm16-egoscan")

# Run Cadena et al.
subprocess.call("python densdp.py net.txt {}".format(args.a), shell = True)

# Take Results
cs = eval(open("tmp/net.txt","r").readline())

# Output
print("Contrast Subgraph {}-{}: {}".format(args.c1, args.c2, cs))
