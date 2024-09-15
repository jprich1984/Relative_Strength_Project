import pandas as pd
import csv
from datetime import datetime, timedelta
from relative_strength import relativeStrength
import pandas_market_calendars as mcal


def main():
    period=20
    start_date = '2018-01-01'
    end_date = '2022-01-01'

    # Get NYSE calendar
    nyse = mcal.get_calendar('NYSE')
    trading_days = nyse.schedule(start_date=start_date, end_date=end_date)
    date_range = trading_days.index

    print(f"Total trading days: {len(date_range)}")

    metrics = ['Slope', 'Corr', 'Product']
    period_end = '2022-01-01'
    invest_date_index=0
    with open(f'best_stocks_{period}_trading_day_period_2016-2022.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Start Date', 'End Date', 'Metric', 'Industry', 'Stock', 'Stock_Rank','Industry_Rank','Stock_Metric_Sign'])

        for metric in metrics:
            end_date_index = period+1
            end_date = date_range[end_date_index]
            while end_date < datetime.strptime(period_end, '%Y-%m-%d'):
                # Find the end date that is k trading days later
                start_date_index = date_range.get_loc(end_date) - period
                if end_date_index >= len(date_range):
                    break
                start_date = date_range[start_date_index]

                rs = relativeStrength(start_date, end_date, metric=metric)
                results = rs.top_stocks
                for row in format_results(results, rs.actual_start_date, rs.actual_end_date, metric):
                    writer.writerow(row)

                #invest_date = date_range[end_date_index + 1] if end_date_index + 1 < len(date_range) else end_date
                end_date_index+=1
                end_date=date_range[end_date_index]


def format_results(results, start_date, end_date, metric):
    for industry_rank, key in enumerate(results.keys(),1):
        for rank, (stock,isPos) in enumerate(results[key], 1):
            row = [start_date, end_date, metric, key, stock, rank,industry_rank,isPos]
            yield row


if __name__ == '__main__':
    main()

