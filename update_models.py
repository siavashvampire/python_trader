from datetime import datetime
from time import sleep

from app.market_trading.model.trading_thread_model import TradingThreadModel
from core.database.database import create_db

create_db()

from app.market_trading.api import get_all_trading,get_trading

# trades = get_all_trading()
trades = [get_trading(2)]

for trade in trades:
    name = trade.currency_disp()
    print(name)
    thread = TradingThreadModel(trade, None, None, None, None)
    thread.ml_trading.counter = 730
    start_train_time = datetime.now()
    thread.model_thread.start()
    sleep(5)
    thread.stop_thread = True
    thread.model_thread.join()
    end_train_time = datetime.now()
    print("total train time for ", name, " is : ", (end_train_time - start_train_time).total_seconds(), "seconds")
