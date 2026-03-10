import json

def get_exchange_rate(currency_pair: str) -> json:
    print(f"[Mock] Getting exchange rate for {currency_pair}...")
    rate = "Unknown"
    if "USD_TWD" in currency_pair:
        rate = "32.0"
    elif "JPY_TWD" in currency_pair:
        rate = "0.2"
    elif "EUR_USD" in currency_pair:
        rate = "1.2"
    else:
        return json.dumps({"error": "Data not found"})

    return json.dumps({"currency_pair": currency_pair, "rate": rate})

def get_stock_price(symbol: str) -> json:
    print(f"[Mock] Getting stock price for {symbol}...")
    price = "Unknown"
    if "AAPL" in symbol:
        price = "260.00"
    elif "TSLA" in symbol:
        price = "430.00"
    elif "NVDA" in symbol:
        price = "190.00"
    else:
        return json.dumps({"error": "Data not found"})

    return json.dumps({"symbol": symbol, "price": price})

available_functions = {
    "get_exchange_rate": get_exchange_rate,
    "get_stock_price": get_stock_price
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get the current exchange rate for a currency pair",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {"type": "string", "description": "The currency pair (e.g., USD_TWD)"}
                },
                "required": ["currency_pair"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current stock price for a symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "The stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]