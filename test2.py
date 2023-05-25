from app.oanda.api import tpqoa_api

# msg = tpqoa_api.stream_one_data('EUR_USD')

# print(msg.time, float(msg.bids[0].dict()['price']), float(msg.asks[0].dict()['price']))

print(tpqoa_api.get_history("EUR_USD", "2020-08-03", "2023-05-21", "M1", "A"))