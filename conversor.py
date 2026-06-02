from api import get_rate

COMMON_CURRENCIES = [
	"USD (United States)",
	"EUR (Eurozone)",
	"GBP (Great Britain)",
	"JPY (Japan)",
	"CNY (China)",
	"CHF (Switzerland)",
	"CAD (Canada)",
	"AUD (Australia)",
	"NZD (New Zealand)",
	"SEK (Sweden)",
	"NOK (Norway)",
	"DKK (Denmark)",
	"SGD (Singapore)",
	"HKD (Hong Kong)",
	"INR (India)",
	"KRW (South Korea)",
	"MXN (Mexico)",
	"BRL (Brazil)",
	"ZAR (South Africa)",
	"AED (United Arab Emirates)",
]

print("¡BIENVENIDO AL CONVERSOR DE MONEDAS!")
print()


def safe_input(prompt):
	try:
		return input(prompt)
	except (EOFError, RuntimeError):
		print("Error: no hay entrada de consola disponible.")
		print("Ejecuta este script en una terminal o usa la interfaz grafica main.py/main.exe.")
		return None

def do_conversion():
	print("Monedas mas usadas en el mundo:", ", ".join(COMMON_CURRENCIES))
	print()

	from_raw = safe_input("Convertir de  (ej. USD, EUR): ")
	if from_raw is None:
		return False
	to_raw = safe_input("Convertir a  (ej. USD, EUR): ")
	if to_raw is None:
		return False

	from_currency = from_raw.upper()
	to_currency = to_raw.upper()

	if len(from_currency) != 3 or not from_currency.isascii() or not from_currency.isalpha():
		print("Error: la moneda origen debe ser un codigo de 3 letras (ej. USD).")
		return

	if len(to_currency) != 3 or not to_currency.isascii() or not to_currency.isalpha():
		print("Error: la moneda destino debe ser un codigo de 3 letras (ej. EUR).")
		return

	try:
		amount_raw = safe_input("Cantidad (ej. 10.50): ")
		if amount_raw is None:
			return False
		amount = float(amount_raw)
	except ValueError:
		print("Error: la cantidad debe ser un numero.")
		return True

	try:
		rate = get_rate(from_currency, to_currency)
	except (RuntimeError, ValueError) as error:
		print(f"Error: {error}")
		return True

	result = amount * rate
	print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
	return True


while True:
	should_continue = do_conversion()
	if should_continue is False:
		break
	print()
	print("MENU")
	print("1. Hacer otra conversion")
	print("2. Salir")
	option_raw = safe_input("Elige una opcion (1/2): ")
	if option_raw is None:
		break
	option = option_raw.strip()
	if option == "2":
		print("GRACIAS POR USAR EL CONVERSOR DE MONEDAS. ¡HASTA LUEGO!")
		break
	if option != "1":
		print("Opcion invalida, continuando con una nueva conversion.")
	print()