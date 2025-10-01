# Stock & Crypto Dashboard

A dynamic Django web application designed to track and visualize stock and cryptocurrency prices, featuring user authentication, real-time data fetching, interactive charts, and a personalized watchlist. Built as a portfolio project to demonstrate full-stack development skills.

## Features
- **User Authentication**: Secure login, signup, and logout functionality.
- **Real-Time Data**: Fetches stock data (e.g., AAPL) via yFinance and cryptocurrency data (e.g., Bitcoin) via CoinGecko APIs.
- **Interactive Charts**: Displays 30-day price history using Chart.js.
- **Watchlist Management**: Add, view, and remove favorite stocks/crypto with user feedback.
- **Responsive Design**: Styled with Bootstrap for a clean, mobile-friendly interface.

## Tech Stack
- **Backend**: Django 5.2.6, Python 3.12
- **APIs**: yFinance, CoinGecko
- **Frontend**: Bootstrap 5.3.0, Chart.js
- **Database**: SQLite (local), PostgreSQL (production-ready option)
- **Deployment**: Render (live demo), GitHub for version control

## Setup & Run Locally
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/stock-crypto-dashboard.git
   cd stock-crypto-dashboard