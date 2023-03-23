#!/bin/bash

assert_equals () {
  if [ "$1" = "$2" ]; then
    echo -e "$Green $Check_Mark Success $Color_Off"
  else
    echo -e "$Red Failed $Color_Off"
    echo -e "$Red Expected -$1- to equal -$2- $Color_Off"
    Errors=$((Errors  + 1))
    exit 1
  fi
}

response=$(python3 program.py 3.0 5.0)
result="Fecha de la consulta: 2022-04-05
Precio de la cryptomoneda BTC: 3.0USD
Precio de la moneda: 5.0EUR --> 1USD
Precio de la cryptomoneda en EUR: 15.0"
assert_equals "$response" "$result"

response=$(python3 program.py 0.150495 5.001575)
result="Fecha de la consulta: 2022-04-05
Precio de la cryptomoneda BTC: 0.150495USD
Precio de la moneda: 5.001575EUR --> 1USD
Precio de la cryptomoneda en EUR: 0.7522"
assert_equals "$response" "$result"
