""" main.py
"""
import sys
import calendar
from datetime import datetime, timedelta

from internal import S3Blockchain

def generate_dates_from_args(args):
    # Check if there are more than one argument and the second argument has a length of 6 (assumed to be in YYYYMM format)
    if len(args) > 1 and len(args[1]) == 6:
        year = args[1][:4]  # Extract the year
        month = args[1][4:]  # Extract the month
        # Return a list of all dates for the specified year and month
        return [f'{year}-{month}-{str(day).zfill(2)}' for day in range(1, calendar.monthrange(int(year), int(month))[1]+1)]
    if len(args) > 1 and len(args[1]) == 8:
        year = args[1][:4]  # Extract the year
        month = args[1][4:6]  # Extract the month
        day = args[1][6:]  # Extract the day
        # Return a list of the specified day
        return [f'{year}-{month}-{day}']
    else:
        # If the arguments do not meet the condition, return yesterday's date
        yesterday = datetime.now() - timedelta(days=1)
        return [yesterday.strftime('%Y-%m-%d')]

def download_transactions(dates):
    # Create an instance of the S3Blockchain class
    s3 = S3Blockchain()
    # Loop through the list of dates passed as an argument
    for date in dates:
        # Download Bitcoin transaction data for the specified date
        s3.download_btc_transactions(date)

if __name__ == '__main__':
    dates = generate_dates_from_args(sys.argv)
    download_transactions(dates)
