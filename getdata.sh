#! /bin/bash

# URL format:
# ftp://ftp.ll.mit.edu/outgoing/darpa/data/1999/training/week1/monday/outside.tcpdump.gz

count=0
base_url="ftp://ftp.ll.mit.edu/outgoing/darpa/data/1999/"

mkdir -p training
mkdir -p testing

echo "Downloading the DARPA 1999 IDS Dataset..."

for dataset in "training" "testing"; do
  if [ $dataset = "training" ]; then
    for week in "week1" "week2" "week3"; do
      for weekday in "monday" "tuesday" "wednesday" "thursday" "friday"; do
        echo wget $base_url$dataset/$week/$weekday/inside.tcpdump.gz
        wget $base_url$dataset/$week/$weekday/inside.tcpdump.gz -O $dataset/$count\_$week\_$weekday\_inside.pcap.gz -q
        gunzip $dataset/$count\_$week\_$weekday\_inside.pcap.gz        

        echo wget $base_url$dataset/$week/$weekday/outside.tcpdump.gz
        wget $base_url$dataset/$week/$weekday/outside.tcpdump.gz -O $dataset/$count\_$week\_$weekday\_outside.pcap.gz -q
        gunzip $dataset/$count\_$week\_$weekday\_outside.pcap.gz
        count=$((count + 1))

        # Also grab the 3 additional days of extra data from week 3
        if [ $week = "week3" ]; then
          if [ $weekday = "monday" ] || [ $weekday = "tuesday" ] || [ $weekday = "wednesday" ]; then
            echo wget $base_url$dataset/$week/extra\_$weekday/inside.tcpdump.gz
            wget $base_url$dataset/$week/extra\_$weekday/inside.tcpdump.gz -O $dataset/$count\_$week\_$weekday\_extra\_inside.pcap.gz -q
            gunzip $dataset/$count\_$week\_$weekday\_extra\_inside.pcap.gz 

            echo wget $base_url$dataset/$week/extra\_$weekday/outside.tcpdump.gz
            wget $base_url$dataset/$week/extra\_$weekday/outside.tcpdump.gz -O $dataset/$count\_$week\_$weekday\_extra\_outside.pcap.gz -q
            gunzip $dataset/$count\_$week\_$weekday\_extra\_outside.pcap.gz 
            count=$((count + 1))
          fi
        fi

      done
    done
  else 
    for week in "week4" "week5"; do
      for weekday in "monday" "tuesday" "wednesday" "thursday" "friday"; do
        echo wget $base_url$dataset/$week/$weekday/inside.tcpdump.gz
        wget $base_url$dataset/$week/$weekday/inside.tcpdump.gz -O $dataset/$count\_$week\_$weekday\_inside.pcap.gz -q 
        gunzip $dataset/$count\_$week\_$weekday\_inside.pcap.gz 

        echo wget $base_url$dataset/$week/$weekday/outside.tcpdump.gz
        wget $base_url$dataset/$week/$weekday/outside.tcpdump.gz -O $dataset/$count\_$week\_$weekday\_outside.pcap.gz -q 
        gunzip $dataset/$count\_$week\_$weekday\_outside.pcap.gz
        count=$((count + 1))
      done
    done
  fi
done