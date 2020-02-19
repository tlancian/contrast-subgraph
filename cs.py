import argparse
import os
from functools import reduce
import numpy as np
import subprocess


# Arguments for computing Contrast Subgraph

parser = argparse.ArgumentParser(description='Graph Classification via Contrast Subgraph')

parser.add_argument('d', help='dataset', type=str)
parser.add_argument('a', help='Group A', type=str)
parser.add_argument('b', help='Group B', type=str)
parser.add_argument('alpha', help='alpha', type=float)
parser.add_argument('-p', help='Problem Forumlation (default: 1)', default = "1", choices=["1", "2"])

args = parser.parse_args()

dir1 = "datasets/{}/{}/".format(args.d,args.a)
c1 = ["{}{}".format(dir1,elem) for elem in os.listdir(dir1)]


dir2 = "datasets/{}/{}/".format(args.d,args.b)
c2 = ["{}{}".format(dir2,elem) for elem in os.listdir(dir2)]


# Create and Write Summary Graphs

summary_c1 = reduce(lambda x,y:x+y,map(lambda x: np.loadtxt(x, delimiter = " "),c1))/len(os.listdir(dir1))
summary_c2 = reduce(lambda x,y:x+y,map(lambda x: np.loadtxt(x, delimiter = " "),c2))/len(os.listdir(dir2))

if args.p == "1":
    diff_net = summary_c1 - summary_c2
elif args.p == "2":
    diff_net = abs(summary_c1 - summary_c2)


with open("icdm16-egoscan/net.txt", 'w') as f:
    for row in range(1,summary_c1.shape[1]):
        for col in range(row):
            f.write("{} {} {}".format(row,col,diff_net[row][col])+"\n")
    f.close()

os.chdir("icdm16-egoscan")

# Run Cadena et al.
subprocess.call("python densdp.py net.txt {}".format(args.alpha), shell = True)

# Take Results
cs = eval(open("tmp/net.txt","r").readline())

# Output
print("Contrast Subgraph {}-{}: {}".format(args.a, args.b, cs))
