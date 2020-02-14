#!/bin/bash


"C:\Program Files\MATLAB\R2019a\bin\win64\MATLAB.exe" matlab -nosplash -nodesktop -r "run('cvx/$1.m');exit;"
rm -f $1.m 
