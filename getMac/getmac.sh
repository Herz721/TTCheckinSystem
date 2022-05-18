#! /bin/zsh

#get IP Mac informations
arp -d -a # sudo run
sleep 600
touch macAdrs.txt
command arp -a > macAdrs.txt

#To csv file
g++ matchIP.cc -lstdc++ -Wall -Wextra -std=c++11 -o matchIP
./matchIP macAdrs.txt macAdrs.csv

#clear
rm matchIP
rm macAdrs.txt

