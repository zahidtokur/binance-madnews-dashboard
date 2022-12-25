# Binance Madnews Dashboard

Binance Madnews Dashboard is a Binance Futures trading tool which aims to provide a speed boost to news and headline based crypto trading. 

News feed is developed and made public by [TreeOfAlpha](https://twitter.com/Tree_of_Alpha). You can access the feed yourself [here](wss://www.madnews.io/ws).

## Features:

### Multiple Binance Futures accounts

You can add multiple accounts and switch between them seamlessly.

### Market sell and market buy orders with a few clicks

Entering a trade only takes 3 or 4 mouse clicks.

### Automatic position sizing

Since speed is wanted, preset multipliers are provided so that there is no wasted time calculating the position size. 

Notional position size is calculated like so:

`position_size = account_balance * multiplier`

### Setting margin type to "Cross" on all pairs automatically

In order to prevent unwanted liqudations and errors on order creation, margin type is set to "Cross" on all pairs periodically.

### Setting the optimal leverage on all pairs automatically

To prevent margin and position sizing constraints, optimal leverage is calculated. Optimal leverage depends on your account balance, maximum position size the dashboard provides and the margin constraints set by Binance.

For example:

Let's say your account balance is 20,000 USDT. Maximum leverage provided by the dashboard is 2x, which makes the maximum notional size 40,000 USDT.
Maximum leverage you can use to open a 40,000 USDT position on SUSHIUSDT is 8x. So the leverage for SUSHIUSDT is set to 8x automatically.

Maximum capital efficiency is seeked.

# Installation

- Make sure you have Python 3 installed.
- Install Redis and run on port 6379. [Refer to this doc](https://redis.io/docs/getting-started/).
- Create and activate a virtual environment:
```
python -m venv venv

# Windows
venv/Scripts/activate

# Linux/Mac
source venv/bin/activate
```

- Install requirements:
```
pip install -r requirements.txt
```

- Migrate and run the project:
```
python manage.py migrate
python manage.py runserver
```

- Run Celery for periodic tasks:

```
# In another terminal
celery -A dashboard beat -l info
```

```
# In another terminal
# Windows
celery -A dashboard worker -l info -P eventlet

# Linux/Mac
celery -A dashboard worker -l info
```
