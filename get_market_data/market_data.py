import requests


class MarketData:
    def __init__(self):
        self.index_url = "url"
        self.headers = "headers"
        self.event_type = "dividend"

    def get_corporate_actions_data(self, stock_type=None, event='all'):
        """
        Get corporate actions for all stocks or for selected stock
        """
