import requests
import yfinance as yf
from django.shortcuts import render
import datetime
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Watchlist
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

def format_number(n):
    """Format large numbers into readable strings (e.g., 2.45T, 930B, 24.3M)."""
    if n is None:
        return "N/A"
    try:
        n = float(n)
    except:
        return "N/A"

    if n >= 1_000_000_000_000:
        return f"${n/1_000_000_000_000:.2f}T"
    elif n >= 1_000_000_000:
        return f"${n/1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    elif n >= 1_000:
        return f"${n/1_000:.2f}K"
    else:
        return f"${n:.2f}"

def home(request):
    query = request.GET.get("query")
    data = None
    error = None
    chart_labels = []
    chart_prices = []

    if query:
        query = query.strip().lower()
        try:
            # === STOCK HANDLING ===
            ticker = yf.Ticker(query.upper())
            stock_info = ticker.info

            if "regularMarketPrice" in stock_info and stock_info.get("regularMarketPrice") is not None:
                hist = ticker.history(period="1mo")  # 1 month history
                chart_labels = [d.strftime("%Y-%m-%d") for d in hist.index]
                chart_prices = hist["Close"].round(2).tolist()

                data = {
                    "type": "Stock",
                    "symbol": query.upper(),
                    "name": stock_info.get("shortName", "N/A"),
                    "price": stock_info.get("regularMarketPrice", "N/A"),
                    "change": round(stock_info.get("regularMarketChangePercent", 0), 2),
                    "market_cap": format_number(stock_info.get("marketCap")),
                }

            else:
                # === CRYPTO HANDLING ===
                url = f"https://api.coingecko.com/api/v3/coins/{query}/market_chart?vs_currency=usd&days=30"
                r = requests.get(url, timeout=10)

                if r.status_code == 200:
                    c = r.json()
                    prices = c["prices"]  # [ [timestamp, price], ... ]
                    chart_labels = [
                        datetime.datetime.fromtimestamp(p[0] / 1000).strftime("%Y-%m-%d")
                        for p in prices
                    ]
                    chart_prices = [round(p[1], 2) for p in prices]

                    coin_data = requests.get(
                        f"https://api.coingecko.com/api/v3/coins/{query}", timeout=10
                    ).json()

                    data = {
                        "type": "Crypto",
                        "symbol": coin_data["symbol"].upper(),
                        "name": coin_data["name"],
                        "price": coin_data["market_data"]["current_price"]["usd"],
                        "change": coin_data["market_data"]["price_change_percentage_24h"],
                        "market_cap": format_number(
                            coin_data["market_data"]["market_cap"]["usd"]
                        ),
                    }
                else:
                    error = "No stock/crypto found for this query."

        except Exception as e:
            error = f"Error: {str(e)}"

    return render(
        request,
        "dashboard/home.html",
        {
            "data": data,
            "error": error,
            "chart_labels": json.dumps(chart_labels),
            "chart_prices": json.dumps(chart_prices),
        },
    )



@login_required
def watchlist(request):
    if request.method == "POST":
        action = request.POST.get("action")
        symbol = request.POST.get("symbol")
        type_ = request.POST.get("type")
        
        if action == "add":
            Watchlist.objects.get_or_create(user=request.user, symbol=symbol, type=type_)
            messages.success(request, f"Added {symbol} to your watchlist!")
        elif action == "remove":
            Watchlist.objects.filter(user=request.user, symbol=symbol, type=type_).delete()
            messages.success(request, f"Removed {symbol} from your watchlist!")
        
        return redirect('home')  # Redirect to home after any action

    items = Watchlist.objects.filter(user=request.user)
    return render(request, 'dashboard/watchlist.html', {'items': items})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"Redirecting to: {reverse('home')}")  # Debug line
            return redirect('home')
        else:
            print("Form is invalid:", form.errors)  # Debug form errors
    else:
        form = UserCreationForm()
    return render(request, 'dashboard/signup.html', {'form': form})

def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    print(f"Logging out, redirecting to: {reverse('login')}")
    return redirect('login')