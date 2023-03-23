#include "stdio.h"
#include "math.h"
#include "stdbool.h"
#include "string.h"
#include "stdlib.h"
#include "macros.h"

const int RELEVANT_DECIMALS = 4; // Con 4 el numero es mas preciso

int PRE_CDECL asm_mul(int crypto_price, int currency_price) POST_CDECL;
int convertDecimalPartToInteger(float entire_number, int int_number);
float int2float(int number, int number_of_decimals);

double convert(float crypto_price, float currency_price) {

    /**
     * Dividimos la parte entera de la parte decimal de ambos numeros,
     * a la decimal la convertimos en entero usando solo los primeros n (RELEVANT_DECIMALS) decimales.
     * 
     * crypto_price = crypto_price_int + crypto_price_decimal
     * currency_price = currency_price_int + currency_price_decimal
     */
    int crypto_price_int = (int) crypto_price;
    int crypto_price_decimal = convertDecimalPartToInteger(crypto_price, crypto_price_int);
    int currency_price_int = (int) currency_price;
    int currency_price_decimal = convertDecimalPartToInteger(currency_price, currency_price_int);

    /** 
     * 4 multiplicaciones aplicando propiedad distributiva del producto con respecto a la suma 
     * 
     * Considerando:
     * A : crypto_price_int         ---     B : crypto_price_decimal
     * C : currency_price_int       ---     D : currency_price_decimal
     * 
     * (A + B) * (C + D) = A*C + A*D + B*C + B*D
     * 
     * Convertimos los resultados a decimal (solo los que corresponde convertir)
     * 
     * A y C son enteros, asi que no se convierte el resultado de A*C
     * En el caso de A*D y B*C, solo uno de los terminos de la multiplicacion es decimal, asi que se divide por 10^RELEVANT_DECIMALS
     * En el caso de B*D, ambos terminos de la multiplicacion son decimal, asi que se divide por 10^(RELEVANT_DECIMALS*2)
     */
    float result1 = asm_mul(crypto_price_int, currency_price_int);
    float result2 = int2float(asm_mul(crypto_price_int, currency_price_decimal), RELEVANT_DECIMALS);
    float result3 = int2float(asm_mul(crypto_price_decimal, currency_price_int), RELEVANT_DECIMALS);
    float result4 = int2float(asm_mul(crypto_price_decimal, currency_price_decimal), RELEVANT_DECIMALS*2);

    return (result1 + result2 + result3 + result4);
}

/**
 * Extrae la parte decimal y convierte los primeros n (RELEVANT_DECIMALS) decimales en un entero 
 * 
 * @param entire_number El numero completo, con su parte entera y decimal
 * @param int_number La parte entera del numero
 */
int convertDecimalPartToInteger(float entire_number, int int_number) {
    return (int) ((entire_number - int_number) * pow(10, RELEVANT_DECIMALS));
}

float int2float (int number, int number_of_decimals) {
    return number / pow(10, number_of_decimals);
}
