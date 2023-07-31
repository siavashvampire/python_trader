from app.data_gathering.main import data_gathering
from core.database.database import create_db

create_db()

from app.market_trading.api import get_all_trading

trades = get_all_trading()

for trade in trades:
    asset = trade.currency_disp()
    print(asset)
    data_gathering(asset)

print("data gathering finished")
