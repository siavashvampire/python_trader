main_unit = 1000


class PredictSellEnums:
    def __init__(self):
        self.id = 0

    @staticmethod
    def get_unit() -> int:
        return -main_unit

    def __repr__(self) -> str:
        return "Sell"


class PredictBuyEnums:
    def __init__(self):
        self.id = 1

    @staticmethod
    def get_unit() -> int:
        return main_unit

    def __repr__(self) -> str:
        return "Buy"


class PredictNeutralEnums:
    def __init__(self):
        self.id = 2

    @staticmethod
    def get_unit() -> int:
        return 0

    def __repr__(self) -> str:
        return "Neutral"


class PredictEnums:
    neutral: PredictNeutralEnums
    buy: PredictBuyEnums
    sell: PredictSellEnums

    def __init__(self):
        self.sell = PredictSellEnums()
        self.buy = PredictBuyEnums()
        self.neutral = PredictNeutralEnums()
