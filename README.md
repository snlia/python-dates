dates
=====
an util to extract date info from string
It's base on [semantic](https://github.com/crm416/semantic)
## Installation
## Features
Can extract dates in 7 different formats from text, including regular formats and irregular formats.

The regular formats include 4 types: 

* Month, Day, Year (e.g., 'August 17 , 1926', 'Aug., 17th, 1926', 'Aug 17 1926') Note that, if year was lost, will use now year for instead.
* Day, Month, Year (e.g., '12 August , 1926', '17th, Aug., 1926', '17 Aug 1926') Note that, if year was lost, will use now year for instead.
* Month/Day/Year (e.g, '08/17/1926', '8/17/1926')
* Year only(must between 1000-2020)

The irregular formats will consider the absolute dates, which include 3 types:

* tomorrow/tonight/today/now
* next/this/last morning/afternoon/evening/night/Monday/.../Sunday/Month (e.g., 'this Monday', 'last night', 'next month')
* Number day(s)/week(s) before/from Date, Date was shown as the 2 type above (e.g., '2 weeks before', 'week from now', 'four days before last Month')

## Samples
Use dates.extractDate to extract dates from string, the output will be a list of tuple, contains date in 'month/day/year' format(use 'XX' to respect lost message) and regex match result

    from dates import extractDates
    extractDates('Jiang (Aug. 17, 1926-inf) was 90 4 days before.')

Use 'now=' to set the current date, the date should be in datetime format

    from dates import extractDates
    from datetime import datetime
    extractDates('Jiang was 90 four days before.', now=datetime(2016, 8, 21))

Use 'irregular=False' will only show regular format.

    from dates import extractDates
    extractDates('Jiang was born in Aug 17, 1926, just 4 days before this Sunday, he was 90.', irregular=False)
