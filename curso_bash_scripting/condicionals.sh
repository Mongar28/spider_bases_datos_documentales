#!/bin/bash


echo "Este programa comparara dos dumeros para saber si el primero que ingreses es mayor que el segundo"
echo "Por favor ingresa los dos valoes"

declare -i valor_1
declare -i valor_2

read -r valor_1
read -r valor_2


echo "Primera forma de escribir la condiciones"
if [ "$valor_1" -gt "$valor_2" ]; then
    echo "El numero $valor_1 es mayor o que $valor_2"
else
    echo "El numero $valor_1 no es mayor o que $valor_2"
fi

echo 
echo "Segunda forma de escribir la condiciones"
if (( valor_1 > valor_2 )) 
then
    echo "El numero $valor_1 es mayor o que $valor_2"
else
    echo "El numero $valor_1 no es mayor o que $valor_2"
fi
