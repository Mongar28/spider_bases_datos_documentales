# !/bin/bash

echo 


for ((i=0; i < 100; i++)) 
do
    if (( i % 2 == 0))
    then
        echo "El numero $i es par"

    elif (( i % 2 == 0))
    then
        echo "El numero $i es par"else echo "El numero $i es impar"
        continue
    
    elif (( i == 9))
    then
        echo "Ha llegado al numero $i y se parará el bucle."
        break
    fi
done

