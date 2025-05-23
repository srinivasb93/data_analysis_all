import nselib
import datetime as dt
from nselib import capital_market as cm

# data = cm.bhav_copy_with_delivery(trade_date='20-01-2024')
data = cm.price_volume_data(symbol='SBIN', period='1W')
print(data)