import http.client
import json
from urllib.parse import urlencode


def _normalize_api_message(message):
    text = str(message).strip().lower()
    if text in {"not found", "invalid currency", "unknown currency", "invalid base currency"}:
        return "Moneda no valida o no soportada."
    return f"No se pudo obtener la tasa: {message}"


def _extract_error_message(data):
    if not isinstance(data, dict):
        return None

    direct_message = data.get("message") or data.get("detail")
    if isinstance(direct_message, str) and direct_message.strip():
        return direct_message

    error = data.get("error")
    if isinstance(error, str) and error.strip():
        return error
    if isinstance(error, dict):
        nested_message = error.get("message") or error.get("info") or error.get("type")
        if isinstance(nested_message, str) and nested_message.strip():
            return nested_message

    return None


def get_latest_raw():
    conn = http.client.HTTPSConnection("api.fxratesapi.com", timeout=10)
    try:
        conn.request("GET", "/latest")
        response = conn.getresponse()
        body = response.read().decode("utf-8")
    except OSError as exc:
        raise RuntimeError("No se pudo conectar con el servicio de cambio.") from exc
    finally:
        conn.close()

    return body


def get_supported_currencies():
    try:
        data = json.loads(get_latest_raw())
    except json.JSONDecodeError as exc:
        raise RuntimeError("La respuesta del servicio no es valida.") from exc

    message = _extract_error_message(data)
    if message:
        raise ValueError(_normalize_api_message(message))

    if not isinstance(data, dict):
        raise RuntimeError("La respuesta del servicio no es valida.")

    rates = data.get("rates")
    base = str(data.get("base", "")).upper().strip()
    if not isinstance(rates, dict) or not rates:
        raise RuntimeError("No se pudo obtener la lista de monedas disponibles.")

    currency_codes = {str(code).upper().strip() for code in rates.keys() if str(code).strip()}
    if base:
        currency_codes.add(base)

    return sorted(currency_codes)


def get_rate(from_currency, to_currency):
    base = from_currency.upper()
    target = to_currency.upper()
    query = urlencode({"base": base, "currencies": target})
    path = f"/latest?{query}"

    conn = http.client.HTTPSConnection("api.fxratesapi.com", timeout=10)
    try:
        conn.request("GET", path)
        response = conn.getresponse()
        body = response.read().decode("utf-8")

        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("La respuesta del servicio no es valida.") from exc

        if response.status >= 400:
            message = _extract_error_message(data)
            if message:
                raise ValueError(_normalize_api_message(message))
            raise RuntimeError("Error al consultar el servicio de cambio.")

        if isinstance(data, dict) and data.get("success") is False:
            message = _extract_error_message(data)
            if message:
                raise ValueError(_normalize_api_message(message))
            raise RuntimeError("Error al consultar el servicio de cambio.")
    except OSError as exc:
        raise RuntimeError("No se pudo conectar con el servicio de cambio.") from exc
    finally:
        conn.close()

    rates = data.get("rates") if isinstance(data, dict) else None
    if not isinstance(rates, dict) or target not in rates:
        message = _extract_error_message(data)
        if message:
            raise ValueError(_normalize_api_message(message))
        raise ValueError(f"No hay tasa disponible para {base} -> {target}.")

    return rates[target]


if __name__ == "__main__":
    print(get_latest_raw())