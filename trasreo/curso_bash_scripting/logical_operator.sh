#! /bin/bash

# Este será un programa para ver  que tipo de poblacion eres: niño, jodevn, adulto mayor

echo "Por favor ingresa la edad para saber a que tipo de población perteneces"
# Declaromos que la variable edad sera un entero
declare -i edad

# Solicitamos el valor por consola
read -r edad


# iniciamos la lógica condicional
if (( $edad < 14 ))
then
    echo "Tue edad es: $edad y eres un niño o niña"

elif (( $edad >= 14 )) && (( $edad <= 28 ))
then
    echo "Tu edad es: $edad y eres una joven o un joven."

elif (( $edad > 28 ))
then
    echo "Tu edad es: $edad y eres una adulta o adulto."
fi
