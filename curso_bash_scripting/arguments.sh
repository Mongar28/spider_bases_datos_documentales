# !/bin/bash

# Se pasan los argumentos enumerandolos de la siguiente manera $1, $2, $3...

echo $1 $2 $3

# El argumento $0 es el nombre del script

nombre_script=$0
echo "Este es el nombre del script: $nombre_script"

# Con $@ coge todos los argumetnos que se le manden

argumentos=$@
echo $argumentos

# Con $# contamos los argumentos que se pasaron

echo "Se pasaton $# argumentos."

# De esta forma se puede hacer una lista de argumentos 
list_arg=("$@")
for a in "${list_arg[@]}"
do
    echo "$a"
done

echo "Este es el valor 3 de la lista: ${list_arg[2]}"
