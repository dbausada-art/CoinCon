# Conversor de Monedas

Aplicación de escritorio desarrollada en Python para realizar conversiones entre algunas de las monedas más utilizadas del mundo mediante una interfaz gráfica simple y rápida.

Las tasas de cambio se obtienen en tiempo real utilizando la API de cambio de divisas de [FXRatesAPI](https://fxratesapi.com/), que ofrece datos actualizados para más de 175 monedas internacionales.

## Características

* Conversión entre múltiples monedas internacionales.
* Tasas de cambio actualizadas en tiempo real.
* Interfaz gráfica desarrollada con CustomTkinter.
* Diseño simple e intuitivo.
* Soporte para las monedas más utilizadas del mundo.

## Requisitos

* Python 3.10 o superior

### Dependencias

```bash
customtkinter==5.2.2
pyinstaller==6.16.0
```

## Instalación

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Este proyecto utiliza la API de FXRatesAPI para obtener las cotizaciones de las monedas.

1. Crea una cuenta en [FXRatesAPI](https://fxratesapi.com/).
2. Obtén tu clave API.
3. Configura tu clave en el archivo correspondiente del proyecto.

La API utiliza autenticación mediante una clave (`api_key`) incluida en las solicitudes.

## Ejecución

```bash
python main.py
```

## Generar Ejecutable

```bash
pyinstaller --onefile --windowed main.py
```

## Tecnologías Utilizadas

* Python
* CustomTkinter
* FXRatesAPI
* PyInstaller

## Fuente de Datos

Las tasas de cambio son proporcionadas por FXRatesAPI y se actualizan periódicamente para ofrecer conversiones precisas entre monedas.

## Autor

# Diego Bausada
