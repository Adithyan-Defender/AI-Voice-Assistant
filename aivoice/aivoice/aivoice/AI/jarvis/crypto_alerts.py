import requests
from Mouth import speak
# API Keys
CMC_API_KEY = "59e335a5-a231-454d-9389-fea70e6c28b0"  # CoinMarketCap API Key
NEWS_API_KEY = "3994c8a488894aab913a1433d8d61635"  # NewsAPI.org Key

# Crypto price thresholds for alerts
thresholds = {
    "BTC": 11000.0,  # Bitcoin alert at $95,000
    "ETH": 3000.0,   # Ethereum alert at $3,000
}

def get_crypto_prices():
    """Fetches live crypto prices and checks alerts."""
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={CMC_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        alerts = []
        top_gainers = []
        top_losers = []
        
        for coin in data.get("data", []):
            symbol = coin.get("symbol")
            price = coin.get("quote", {}).get("USD", {}).get("price")
            percent_change_24h = coin.get("quote", {}).get("USD", {}).get("percent_change_24h", 0)
            
            if symbol in thresholds and price is not None:
                if price >= thresholds[symbol]:
                    alerts.append(f"{symbol} ALERT! Price reached {price:.2f} USD")

            # Identify top gainers and losers
            if percent_change_24h is not None:
                if percent_change_24h > 10:  # Adjust threshold for gainers
                    top_gainers.append(f"{symbol} +{percent_change_24h:.2f}% (Now: {price:.2f} USD)")
                elif percent_change_24h < -10:  # Adjust threshold for losers
                    top_losers.append(f"{symbol} {percent_change_24h:.2f}% (Now: {price:.2f} USD)")

        return alerts, top_gainers, top_losers

    except requests.RequestException as e:
        return [f"Error fetching crypto data: {e}"], [], []

def get_crypto_news():
    """Fetches today's top cryptocurrency news headlines."""
    url = f"https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        news_headlines = [article["title"] for article in data.get("articles", [])[:5]]
        return news_headlines

    except requests.RequestException as e:
        return [f"Error fetching news: {e}"]

def fetch_crypto_data():
    """Fetch and display crypto price alerts, top gainers, and top losers."""
    alerts, top_gainers, top_losers = get_crypto_prices()

    print("\n🔔 Crypto Price Alerts:")
    print("\n".join(alerts) if alerts else "No alerts triggered.")

    print("\n🚀 Top Gainers:")
    print("\n".join(top_gainers) if top_gainers else "No significant gainers today.")

    print("\n📉 Top Losers:")
    print("\n".join(top_losers) if top_losers else "No significant losers today.")

def fetch_crypto_news():
    """Fetch and display latest cryptocurrency news headlines."""
    crypto_news = get_crypto_news()

    print("\n📰 Crypto News Headlines:")
    print("\n".join(crypto_news) if crypto_news else "No news available.")

