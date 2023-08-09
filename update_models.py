from datetime import datetime
from time import sleep

from app.market_trading.model.trading_thread_model import TradingThreadModel
from core.app_provider.main import file_exist
from core.database.database import create_db

import os.path

create_db()

from app.market_trading.api import get_all_trading, get_trading

trades = get_all_trading()
# trades = [get_trading(2)]

for trade in trades:
    name = trade.currency_disp()
    print(name)

    thread = TradingThreadModel(trade, None, None, None, None)

    if file_exist('trade_model_' + thread.trade.currency_disp() + '_' + thread.ml_trading.candle + '.pkl',
                  'File/trade_models/'):
        last_modified = datetime.fromtimestamp(os.path.getmtime(thread.ml_trading.model_name))
        if (datetime.now() - last_modified).total_seconds() > 1 * 60 * 60:
            thread.ml_trading.counter = 730
            start_train_time = datetime.now()
            thread.model_thread.start()
            sleep(5)
            thread.stop_thread = True
            thread.model_thread.join()
            end_train_time = datetime.now()
            print("total train time for ", name, " is : ", (end_train_time - start_train_time).total_seconds(),
                  "seconds")
