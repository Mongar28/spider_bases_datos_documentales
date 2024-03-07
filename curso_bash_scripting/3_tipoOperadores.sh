# !/bin/bash

# Es un programa para revisar los tipos de operadores

# Autor: Cristian Montoya Garcés

numA=5
numB=2
numC=8
numD=6
numE=1


echo "Operacdores aritmeticos"
echo "Numeros: A:$numA B:$numB C:$numC D:$numD E:$numE"
echo "sumas A + B =" $((numA + numB))
echo "Resta B - C =" $((numB - numC))
echo "Multiplicacion C * D =" $((numC * numD))
echo "Division D / E =" $((numD / numE))
echo "sumas E % A =" $((numE % numA))

echo ""

# Operadores relacionales
echo "Operadores relacionales"
echo "Numeros: A:$numA B:$numB C:$numC D:$numD E:$numE"
echo "Mayor que  A > B =" $((numA > numB))
echo "Menor que  B < C =" $((numB < numC))
echo "Mayor igual que C >= D =" $((numC >= numD))
echo "Menor igual que D <= E =" $((numD <= numE))
echo "Igual que E ==A =" $((numE == numA)) 
echo "Diferente a E != A =" $((numE != numA))

echo ""

# Operadores de asignacion
echo "Operadores de asignacion"
echo "Numeros: A:$numA B:$numB C:$numC D:$numD E:$numE"
echo "Suma  A += B =" $((numA += numB))
echo "resta  A -= B =" $((numA -= numB))
echo "Multiplicacion  A *= B =" $((numA *= numB))
echo "Division  A /= B =" $((numA /= numB))
