import tpqoa

tpqoa_api = tpqoa.tpqoa("File/Config/oanda.cfg")

# api.get_account_summary()
#
# api.account_type
#
# api.account_id
#
# api.get_instruments()
#
# instr = api.get_instruments()
#
# len(instr)
#
# instr[0]
#
#
# api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-31", granularity="D", price="B")
#
#
# df = api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-31",
#                      granularity="D", price="B")
#
#
#
# api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-01",
#                 granularity="D", price="A")
#
#
#
# api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-01",
#                 granularity="D", price="B")
#
#
# api.get_history("EUR_USD", "2020-08-03", "2020-08-05", "H1", "A")
#
#
# api.get_history("EUR_USD", "2020-08-03", "2020-08-05", "H12", "A")
#
# print(api.get_history("EUR_USD", "2023-05-20", "2023-05-21", "M1", "A"))
#
#
#
# print(api.get_history("EUR_USD", "2020-08-03", "2020-08-04", "S5", "A"))
#
# api.get_instruments()
#
#
#
# api.get_history("SPX500_USD", "2020-08-03", "2020-08-04", "H1", "A")


# msg = api.stream_one_data('EUR_USD')
# # print(msg)
# print(msg.time, float(msg.bids[0].dict()['price']), float(msg.asks[0].dict()['price']))
# api.stop_stream()

# api.create_order(instrument="EUR_USD", units=1000, sl_distance=0.1)
# sleep(3)
# api.create_order(instrument="EUR_USD", units=-10, sl_distance=0.1)
#
# print(api.get_account_summary())
#
# print(api.get_transactions())
#
# print(api.print_transactions(tid=1))