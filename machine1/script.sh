#!/bin/bash
python collector.py >> collector.txt&
for (( c=1; c<=$1; c++ ))
do  
   python consumer.py >> consumer$c.txt&
done
python producer1.py >> producer1.txt