# !/bin/bash

# Programa para revisar la declaraciń de variables

opcion=0
nombre=Cristian

echo "Opcion: $opcion --- Nombre: $nombre"

# Exportar la varible nombre para que este disponible a los demas procesos

export nombre


# llamar al siguiente escript para recuperar la variable

./2_variables_2.sh
