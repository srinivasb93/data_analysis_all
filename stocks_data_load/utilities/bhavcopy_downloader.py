from jugaad_data import nse, holidays
import pandas as pd
import sys


def load_bhav_copy(ext_date=None):
    """function to load bhavcopy"""
    if not ext_date and len(sys.argv) == 2:
        ext_date = pd.to_datetime(sys.argv[1]).date()

    bhav_data = nse.full_bhavcopy_raw(dt=ext_date).split("\n")
    row_columns = bhav_data[0].split(", ")
    data_rows = [row.split(", ") for row in bhav_data[1:]]
    bcopy = pd.DataFrame(data_rows, columns=row_columns)
    bcopy.dropna(inplace=True)
    return bcopy



               
