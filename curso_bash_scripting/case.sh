# !/bin/bash


echo "Operaciones matemáticas con dos numeros"
echo 

echo "Escribe los dos numeros: "

# Declamro el tipo para los valores
declare -i valor_1
declare -i valor_2

# Leo los argumentos pasados por el usuario
read -r valor_1
read -r valor_2

# Imprimo en pantalla los valores declarados por el usuario
echo
echo "Has seleccionado los valores: $valor_1 y $valor_2 para las operaciones matemáticas"
echo 

echo "Ahora elige la opcion del operador matematico para realizar las operaciones con los numeros: 1. Suma, 2. Resta, 3. Multiplicacion, 4. División: "
echo

declare -i operador
read -r operador

case $operador in
    1)
    echo "Haz elegido la operacion suma"
    echo "El resultado de la suma entre $valor_1 y $valor_2 es: " $(( valor_1 + valor_2))
    ;;
    2)
    echo "Haz elegido la operacion resta"
    echo "El resultado de la resta entre $valor_1 y $valor_2 es: " $(( valor_1 - valor_2))
    ;;
    3)
    echo "Haz elegido la operacion multipliacion"
    echo "El resultado de la multiplicion entre $valor_1 y $valor_2 es: "$(( valor_1 * valor_2))
    ;;
    4)
    echo "Haz elegido la operacion división"
    echo "El resultado de la división  entre $valor_1 y $valor_2 es: "$(( valor_1 / valor_2))
esac
