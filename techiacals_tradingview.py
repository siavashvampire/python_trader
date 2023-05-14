# Tradingview Technical Analysis (tradingview-ta)
# Author: deathlyface (https://github.com/deathlyface)
# Rewritten from https://www.tradingview.com/static/bundles/technicals.f2e6e6a51aebb6cd46f8.js
# License: MIT


class Analysis(object):
    exchange = ""
    symbol = ""
    screener = ""
    time = ""
    interval = ""
    summary = {}
    oscillators = {}
    moving_averages = {}
    indicators = {}


class Interval:
    INTERVAL_1_MINUTE = "1m"
    INTERVAL_5_MINUTES = "5m"
    INTERVAL_15_MINUTES = "15m"
    INTERVAL_30_MINUTES = "30m"
    INTERVAL_1_HOUR = "1h"
    INTERVAL_2_HOURS = "2h"
    INTERVAL_4_HOURS = "4h"
    INTERVAL_1_DAY = "1d"
    INTERVAL_1_WEEK = "1W"
    INTERVAL_1_MONTH = "1M"


class Exchange:
    FOREX = "FX_IDC"
    CFD = "TVC"


class Recommendation:
    buy = "BUY"
    strong_buy = "STRONG_BUY"
    sell = "SELL"
    strong_sell = "STRONG_SELL"
    neutral = "NEUTRAL"
    error = "ERROR"


class Compute:
    def MA(ma, close):
        """Compute Moving Average

        Args:
            ma (float): MA value
            close (float): Close value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (ma < close):
            return Recommendation.buy
        elif (ma > close):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def RSI(rsi, rsi1):
        """Compute Relative Strength Index

        Args:
            rsi (float): RSI value
            rsi1 (float): RSI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """

        print(rsi)
        print(rsi1)
        if (rsi < 30 and rsi1 < rsi):
            return Recommendation.buy
        elif (rsi > 70 and rsi1 > rsi):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Stoch(k, d, k1, d1):
        """Compute Stochastic

        Args:
            k (float): Stoch.K value
            d (float): Stoch.D value
            k1 (float): Stoch.K[1] value
            d1 (float): Stoch.D[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (k < 20 and d < 20 and k > d and k1 < d1):
            return Recommendation.buy
        elif (k > 80 and d > 80 and k < d and k1 > d1):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def CCI20(cci20, cci201):
        """Compute Commodity Channel Index 20

        Args:
            cci20 (float): CCI20 value
            cci201 ([type]): CCI20[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (cci20 < -100 and cci20 > cci201):
            return Recommendation.buy
        elif (cci20 > 100 and cci20 < cci201):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def ADX(adx, adxpdi, adxndi, adxpdi1, adxndi1):
        """Compute Average Directional Index

        Args:
            adx (float): ADX value
            adxpdi (float): ADX+DI value
            adxndi (float): ADX-DI value
            adxpdi1 (float): ADX+DI[1] value
            adxndi1 (float): ADX-DI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (adx > 20 and adxpdi1 < adxndi1 and adxpdi > adxndi):
            return Recommendation.buy
        elif (adx > 20 and adxpdi1 > adxndi1 and adxpdi < adxndi):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def AO(ao, ao1, ao2):
        """Compute Awesome Oscillator

        Args:
            ao (float): AO value
            ao1 (float): AO[1] value
            ao2 (float): AO[2] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (ao > 0 and ao1 < 0) or (ao > 0 and ao1 > 0 and ao > ao1 and ao2 > ao1):
            return Recommendation.buy
        elif (ao < 0 and ao1 > 0) or (ao < 0 and ao1 < 0 and ao < ao1 and ao2 < ao1):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Mom(mom, mom1):
        """Compute Momentum

        Args:
            mom (float): Mom value
            mom1 (float): Mom[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (mom < mom1):
            return Recommendation.sell
        elif (mom > mom1):
            return Recommendation.buy
        else:
            return Recommendation.neutral

    def MACD(macd, signal):
        """Compute Moving Average Convergence/Divergence

        Args:
            macd (float): MACD.macd value
            signal (float): MACD.signal value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (macd > signal):
            return Recommendation.buy
        elif (macd < signal):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def BBBuy(close, bblower):
        """Compute Bull Bear Buy

        Args:
            close (float): close value
            bblower (float): BB.lower value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (close < bblower):
            return Recommendation.buy
        else:
            return Recommendation.neutral

    def BBSell(close, bbupper):
        """Compute Bull Bear Sell

        Args:
            close (float): close value
            bbupper (float): BB.upper value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (close > bbupper):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def PSAR(psar, open):
        """Compute Parabolic Stop-And-Reverse

        Args:
            psar (float): P.SAR value
            open (float): open value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (psar < open):
            return Recommendation.buy
        elif (psar > open):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Recommend(value):
        """Compute Recommend

        Args:
            value (float): recommend value

        Returns:
            string: "STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL", or "ERROR"
        """
        if value >= -1 and value < -.5:
            return Recommendation.strong_sell
        elif value >= -.5 and value < -.1:
            return Recommendation.sell
        elif value >= -.1 and value <= .1:
            return Recommendation.neutral
        elif value > .1 and value <= .5:
            return Recommendation.buy
        elif value > .5 and value <= 1:
            return Recommendation.strong_buy
        else:
            return Recommendation.error

    def Simple(value):
        """Compute Simple

        Args:
            value (float): Rec.X value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (value == -1):
            return Recommendation.sell
        elif (value == 1):
            return Recommendation.buy
        else:
            return Recommendation.neutral


def calculate(indicators, indicators_key, screener, symbol, exchange, interval):
    oscillators_counter, ma_counter = {"BUY": 0, "SELL": 0, "NEUTRAL": 0}, {
        "BUY": 0, "SELL": 0, "NEUTRAL": 0}
    computed_oscillators, computed_ma = {}, {}

    indicators = list(indicators.values())

    # RECOMMENDATIONS
    if None not in indicators[0:2]:
        recommend_oscillators = Compute.Recommend(indicators[0]) # this was calculated in the server _ useless to us
        recommend_summary = Compute.Recommend(indicators[1]) # this was calculated in the server _ useless to us
        recommend_moving_averages = Compute.Recommend(indicators[2]) # this was calculated in the server _ useless to us
    else:
        return None

    # OSCILLATORS
    # RSI (14)
    if None not in indicators[3:5]:
        computed_oscillators["RSI"] = Compute.RSI(indicators[3], indicators[4])
        oscillators_counter[computed_oscillators["RSI"]] += 1
    # Stoch %K
    if None not in indicators[5:9]:
        computed_oscillators["STOCH.K"] = Compute.Stoch(
            indicators[5], indicators[6], indicators[7], indicators[8])
        oscillators_counter[computed_oscillators["STOCH.K"]] += 1
    # CCI (20)
    if None not in indicators[9:11]:
        computed_oscillators["CCI"] = Compute.CCI20(
            indicators[9], indicators[10])
        oscillators_counter[computed_oscillators["CCI"]] += 1
    # ADX (14)
    if None not in indicators[11:16]:
        computed_oscillators["ADX"] = Compute.ADX(
            indicators[11], indicators[12], indicators[13], indicators[14], indicators[15])
        oscillators_counter[computed_oscillators["ADX"]] += 1
    # AO
    if None not in indicators[16:18] and indicators[86] != None:
        computed_oscillators["AO"] = Compute.AO(
            indicators[16], indicators[17], indicators[86])
        oscillators_counter[computed_oscillators["AO"]] += 1
    # Mom (10)
    if None not in indicators[18:20]:
        computed_oscillators["Mom"] = Compute.Mom(
            indicators[18], indicators[19])
        oscillators_counter[computed_oscillators["Mom"]] += 1
    # MACD
    if None not in indicators[20:22]:
        computed_oscillators["MACD"] = Compute.MACD(
            indicators[20], indicators[21])
        oscillators_counter[computed_oscillators["MACD"]] += 1
    # Stoch RSI
    if indicators[22] != None:
        computed_oscillators["Stoch.RSI"] = Compute.Simple(indicators[22])
        oscillators_counter[computed_oscillators["Stoch.RSI"]] += 1
    # W%R
    if indicators[24] != None:
        computed_oscillators["W%R"] = Compute.Simple(indicators[24])
        oscillators_counter[computed_oscillators["W%R"]] += 1
    # BBP
    if indicators[26] != None:
        computed_oscillators["BBP"] = Compute.Simple(indicators[26])
        oscillators_counter[computed_oscillators["BBP"]] += 1
    # UO
    if indicators[28] != None:
        computed_oscillators["UO"] = Compute.Simple(indicators[28])
        oscillators_counter[computed_oscillators["UO"]] += 1

    # MOVING AVERAGES
    ma_list = ["EMA10", "SMA10", "EMA20", "SMA20", "EMA30", "SMA30",
               "EMA50", "SMA50", "EMA100", "SMA100", "EMA200", "SMA200"]
    close = indicators[30]
    ma_list_counter = 0
    for index in range(33, 45):
        if indicators[index] != None:
            computed_ma[ma_list[ma_list_counter]] = Compute.MA(
                indicators[index], close)
            ma_counter[computed_ma[ma_list[ma_list_counter]]] += 1
            ma_list_counter += 1

    # MOVING AVERAGES, pt 2
    # ICHIMOKU
    if indicators[45] != None:
        computed_ma["Ichimoku"] = Compute.Simple(indicators[45])
        ma_counter[computed_ma["Ichimoku"]] += 1
    # VWMA
    if indicators[47] != None:
        computed_ma["VWMA"] = Compute.Simple(indicators[47])
        ma_counter[computed_ma["VWMA"]] += 1
    # HullMA (9)
    if indicators[49] != None:
        computed_ma["HullMA"] = Compute.Simple(indicators[49])
        ma_counter[computed_ma["HullMA"]] += 1

    analysis = Analysis()
    analysis.screener = screener
    analysis.exchange = exchange
    analysis.symbol = symbol
    analysis.interval = interval
    analysis.time = datetime.datetime.now()

    for x in range(len(indicators)):
        analysis.indicators[indicators_key[x]] = indicators[x]

    analysis.indicators = analysis.indicators.copy()

    analysis.oscillators = {"RECOMMENDATION": recommend_oscillators,
                            "BUY": oscillators_counter["BUY"], "SELL": oscillators_counter["SELL"], "NEUTRAL": oscillators_counter["NEUTRAL"], "COMPUTE": computed_oscillators}
    analysis.moving_averages = {"RECOMMENDATION": recommend_moving_averages,
                                "BUY": ma_counter["BUY"], "SELL": ma_counter["SELL"], "NEUTRAL": ma_counter["NEUTRAL"], "COMPUTE": computed_ma}
    analysis.summary = {"RECOMMENDATION": recommend_summary, "BUY": oscillators_counter["BUY"] + ma_counter["BUY"],
                        "SELL": oscillators_counter["SELL"] + ma_counter["SELL"], "NEUTRAL": oscillators_counter["NEUTRAL"] + ma_counter["NEUTRAL"]}

    return analysis
