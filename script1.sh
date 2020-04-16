#!/bin/bash
a=2
b=1
z=0
v=$1
val2=`expr $1 % $a`
if [ $val2 != $z ]
then
v=`expr $1 + $b`
fi
thousand=1000
pull=7500 

for (( k=0; k<$v; k+=2 ))
do  
   portpull=`expr $pull + $thousand + $k`
   python collector1.py  $portpull  >> collector1$k.txt&
   echo $portpull
done

#python collector.py >> collector.txt&
for (( c=0,j=0; c<$1; c++,j+=1))
do  
   #push port in consumer side
   val1=`expr $j % $a`
   if [ $val1 == $z ]
   then
   portP=`expr $pull + $thousand + $j`
   fi
   echo $portP
   portPush=`expr $pull + $c`
   python consumer1.py $portPush $portP >>consumer1$c.txt&
done

python producer1.py  $2 $1 $pull >>producer1.txt
