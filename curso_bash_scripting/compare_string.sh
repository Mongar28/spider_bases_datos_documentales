# !/bin/bash

echo "Please enter your password"
read password_1


echo "Repeat enter your password"
read password_2

echo "Password1: $password_1"
echo "Password2: $password_2"


if [ $password_1 == $password_2 ]
then 
    echo "the passwords match"
else
    echo "the passwords do not match"
fi

# concatenacion

echo "Escribe un nombre"
read nombre

echo "Escribe un adjetivo"
read adjetivo

echo "$nombre es $nombre"
