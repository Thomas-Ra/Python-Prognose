#!/bin/bash
# Installation script for market_prediction on ubuntu

git_repo='git@github.com:KarlBit/WP_python_ws21.git'
log_location='' 


echo "=================================================="
echo "=====             Logging                     ===="
echo "=================================================="
echo ""


echo "=================================================="
echo "==========  Standard Dependencies  ==============="
echo "=================================================="
echo ""

#PythonPPA
add-apt-repository -y ppa:deadsnakes/ppa

apt update && apt upgrade -y
apt-get install -y software-properties-common curl vim 

sleep 1 

echo "=================================================="
echo "=====     Anaconda & Python [3.10]            ===="
echo "=================================================="
echo ""

#Python3.10 PPA istall 
apt-get install -y python3.10 

#Anaconda 
curl –o /tmp/anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
bash anaconda.sh
sleep 20



echo "=================================================="
echo "=====             Database                    ===="
echo "=================================================="
echo ""


echo "=================================================="
echo "=====            Repository                   ===="
echo "=================================================="
echo ""



echo "=================================================="
echo "=====             Privileges                  ===="
echo "=================================================="
echo ""


echo "=================================================="
echo "=====             FREESPACE                   ===="
echo "=================================================="
echo ""

echo "=================================================="
echo "=====             END OF LINE		    ===="
echo "=================================================="
