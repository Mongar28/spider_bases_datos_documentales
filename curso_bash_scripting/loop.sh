# !/bin/bash


declare -i valor
valor=0



echo "Programa para el bucle while"
while [ $valor -lt 10 ] 
do
    echo "El valor del numero es: $valor"
    valor=$((valor + 1))
done
echo "El bucle while se ha terminado porque $valor no es menor a 10"


echo 
echo "Programa para el bucle for"


for i in $(seq 0 $valor) 
do
    echo "El resultado de sumar $valor y $i es: " $(( valor + i))
done


# Forma dos de hacer el bucle for

echo 
echo "Forma dos de hacer el bucle for"

for i in {1..10..2} 
do
    echo "El resultado de sumar $valor y $i es: " $(( valor + i))
done

# Forma tres de hacer el bucle for

echo 
echo "Forma tres de hacer el bucle for"

for ((i=0; i < 10; i++)) 
do
    echo "El resultado de sumar $valor y $i es: " $(( valor + i))
done
