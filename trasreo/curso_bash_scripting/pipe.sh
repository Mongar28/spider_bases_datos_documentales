# !/bin/bash

# Los pipes sirven para ejecutar un comando luego de ejecutar uno primero


MESSAGE=$(ls | wc -l)
#echo $MESSAGE

ls | wc > wc.txt
