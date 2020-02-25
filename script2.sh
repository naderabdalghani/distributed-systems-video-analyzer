#!/bin/bash
a=2
z=0
portConstant=2000
pull=10500
finalCollectorPort=15000

python collector2.py  $finalCollectorPort >>collector2f.txt &
for (( c=0,j=0; c<$1; c++,j+=1))
do
   portPull=`expr $pull + $c`
   python consumer2.py $portPull $finalCollectorPort >> consumer2$c.txt &   
done


