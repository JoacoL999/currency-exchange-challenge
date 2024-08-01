# Modulo de system para recibir valores por linea de comando | Module to get command line values.
import sys
# Modulo para realizar las request | Module to make an HTTP request
import requests 

# URL para obtener el tipo de tipo de cambio entre una moneda y un dolar | URL to get the rate bettween a currency and a dollar
base_url = "https://api.wise.com/v1/rates?" 
# URL utilizada para segmentar el valor del peso argentino en dolar oficial y blue | URL used to segment the value of Argentine peso into official and blue dollar
base_url_ars = "https://api.bluelytics.com.ar/v2/latest"

# Objeto utilizado para guardar las variables | Object used to store variables 
exchange = {
    "amount": float(sys.argv[1]),
    "currency": sys.argv[2].upper(),
}


# Funcion para obtener el total en pesos argentinos | Function to obtain the total in Argentine pesos
def get_total_ars():
    try:
        # Division entre el monto ingresado y ambos tipos de dolar para obtener el valor total y redondear los decimales | Division between the amount entered and both types of dollars to obtain the total value and round the decimals
        exchange['total'] = {"oficial": round(exchange['amount'] / exchange['dollar']['oficial'], 2) , "blue": round(exchange['amount'] / exchange['dollar']['blue'], 2)}

        # Se imprime en terminal las cotizaciones actualizadas a la fecha, el monto y el valor del mismo en dolares | The quotes updated to date, the amount and its value in dollars are printed on the terminal.
        print(f"COTIZACION DOLAR OFICIAL: {exchange['currency']}$ {exchange['dollar']['oficial']} - COTIZACION DOLAR BLUE: {exchange['currency']}$ {exchange['dollar']['blue']}")
        print(f"Monto recibido: {exchange['currency']}$ {exchange['amount']}")
        print(f"Monto a dolar oficial: USD$ {exchange['total']['oficial']}")
        print(f"Monto a dolar blue: USD$ {exchange['total']['blue']}")
    
    except Exception as error:
        print(f'Error en el proceso de conversion: {error}')
        sys.exit(1)

# Funcion para obtener el total en cualquier moneda soportada por Wise
def get_total_other():
    try:
        # Multiplicacion entre el monto ingresado y el tipo de cambio a dolar para luego redondear en 2 decimales
        exchange['total'] = round(exchange['amount'] * exchange['rate'], 2)
        print(f"COTIZACION DOLAR: {exchange['currency']} {round(1 / exchange['rate'], 2)}")
        print(f"Monto a dolar: USD$ {exchange['total']}")
    except Exception as error:
        print(f'Error en el proceso de conversion: {error}')
        sys.exit(1)

# Funcion para obtener el valor actual del dolar | Function to obtain the current value of the dollar
def get_usd_rate():
    try:
       # Segmentamos con una condicional entre la moneda recibida y el peso argentino para poder diferenciar el dolar en oficial y blue
       if exchange['currency'] == 'ARS':
        response = requests.get(base_url_ars).json()

        # Guardamos en una variable el valor de venta del dolar oficial y blue para cargarlo en la variable exchange
        data = {"oficial": response['oficial']['value_sell'], "blue": response['blue']['value_sell']}
        exchange['dollar'] = data

        return get_total_ars()
       # Si el tipo de moneda no es igual a ARS, se utiliza la api de Wise para realizar la operacion
       else :
         url = f"{base_url}source={exchange['currency']}&target=USD"
         response = requests.get(url, headers={'Authorization': 'Basic OGNhN2FlMjUtOTNjNS00MmFlLThhYjQtMzlkZTFlOTQzZDEwOjliN2UzNmZkLWRjYjgtNDEwZS1hYzc3LTQ5NGRmYmEyZGJjZA=='}).json()
         response = response[0]
         exchange['rate'] = response['rate']
         return get_total_other()


    except Exception as error:
        print(f'Error al obtener obtener la cotizacion actual: {error}')
        sys.exit(1)


get_usd_rate()