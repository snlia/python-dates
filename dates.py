import re
import datetime
from numbers import NumberService


class DateService(object):

    """Initialize a DateService for extracting dates from text.

    Args:
        tz: An optional Pytz timezone. All datetime objects returned will
            be relative to the supplied timezone, or timezone-less if none
            is supplied.
        now: The time to which all returned datetime objects should be
            relative. For example, if the text is "In 5 hours", the
            datetime returned will be now + datetime.timedelta(hours=5).
            Uses datetime.datetime.now() if none is supplied.

    Returns:
        A DateService which uses tz and now for all of its computations.
    """

    def __init__(self, tz=None, now=None):
        self.tz = tz
        if now:
            self.now = now
        else:
            self.now = datetime.datetime.now(tz=self.tz)

    __startMonths__ = ['jan', 'feb', 'mar', 'apr', 'may',
                       'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    __daysOfWeek__ = ['monday', 'tuesday', 'wednesday',
                      'thursday', 'friday', 'saturday', 'sunday']

    __relativeDates__ = ['tomorrow', 'tonight', 'next']

    __todayMatches__ = ['tonight', 'today', 'this morning', 'now'
                        'this evening', 'this afternoon']

    __tomorrowMatches__ = ['yesterday', 'last morning', 'last night'
                           'last evening', 'last afternoon']

    __yesterdayMatches__ = ['tomorrow', 'next morning', 'next night'
                           'next evening', 'next afternoon']

    __dateDescriptors__ = {
        'a': 1, '1st': 1, 'one': 1, 'first': 1,
        '2nd': 2, 'two': 2, 'second': 2,
        '3rd': 3, 'three': 3, 'third': 3,
        '4th': 4, 'four': 4, 'fourth': 4,
        '5th': 5, 'five': 5, 'fifth': 5,
        '6th': 6, 'six': 6, 'sixth': 6,
        '7th': 7, 'seven': 7, 'seventh': 7,
        '8th': 8, 'eight': 8, 'eighth': 8,
        '9th': 9, 'nine': 9, 'ninth': 9,
        '10th': 10, 'ten': 10, 'tenth': 10,
        '11th': 11, 'eleven': 11, 'eleventh': 11,
        '12th': 12, 'twelve': 12, 'twelth': 12,
        '13th': 13, 'thirteen': 13, 'thirteenth': 13,
        '14th': 14, 'fourteen': 14, 'fourteenth': 14,
        '15th': 15, 'fifteen': 15, 'fifteenth': 15,
        '16th': 16, 'sixteen': 16, 'sixteenth': 16,
        '17th': 17, 'seventeen': 17, 'seventeenth': 17,
        '18th': 18, 'eighteen': 18, 'eighteenth': 18,
        '19th': 19, 'nineteen': 19, 'nineteenth': 19,
        '20th': 20, 'twenty': 20, 'twentieth': 20,
        '21st': 21, 'twenty one': 21, 'twenty first': 21,
        '22nd': 22, 'twenty two': 22, 'twenty second': 22,
        '23rd': 23, 'twenty three': 23, 'twenty third': 23,
        '24th': 24, 'twenty four': 24, 'twenty fourth': 24,
        '25th': 25, 'twenty five': 25, 'twenty fifth': 25,
        '26th': 26, 'twenty six': 26, 'twenty sixth': 26,
        '27th': 27, 'twenty seven': 27, 'twenty seventh': 27,
        '28th': 28, 'twenty eight': 28, 'twenty eighth': 28,
        '29th': 29, 'twenty nine': 29, 'twenty ninth': 29,
        '30th': 30, 'thirty': 30, 'thirtieth': 30,
        '31st': 31, 'thirty one': 31, 'thirty first': 31
    }

# will extract semantic dates
# (number)?(week|day(s)?\ from\ )?
# |tomorrow|today|tonight
# |next|this|last (morning|afternoon|evening|Monday|...|Sunday|Month)
# |(Monday|...|Sunday)
    _dayRegex = re.compile(
        r"""(?ix)
        ((week|day|month|year)s?\ (ago|before|from)\ ?)?
        (
            tomorrow
            |now
            |tonight
            |today
            |yesterday
            |(next|this|last)[\ \b](morning|afternoon|evening|night
                    |week|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday
                    |Month|(Jan\.?(?:uary)?|Feb\.?(?:ruary)?|Mar\.?(?:ch)?|Apr\.?(?:il)?|May\.?|Jun\.?e?|Jul\.?y?|Aug\.?(?:ust)?|Sept?\.?(?:tember)?|Oct\.?(?:ober)?|Nov\.?(?:ember)?|Dec\.?(?:ember)?))
                    |year
            |(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)
        )?
        """)

    # mon day year
    _dayRegex2 = re.compile(
            r'(?ix)(\bJan\.?(?:uary)?\b|\bFeb\.?(?:ruary)?\b|\bMar\.?(?:ch)?\b|\bApr\.?(?:il)?\b|\bMay\.?\b|\bJun\.?e?\b|\bJul\.?y?\b|\bAug\.?(?:ust)?\b|\bSept?\.?(?:tember)?\b|\bOct\.?(?:ober)?\b|\bNov\.?(?:ember)?\b|\bDec\.?(?:ember)?\b)[., ]+(\w{,5})(.{,4}(\b\d{4}\b))?'
    )

    # day mon year
    _dayRegex3 = re.compile(
            r'(?ix)(\w{,5})[., ]+(\bJan\.?(?:uary)?\b|\bFeb\.?(?:ruary)?\b|\bMar\.?(?:ch)?\b|\bApr\.?(?:il)?\b|\bMay\.?\b|\bJun\.?e?\b|\bJul\.?y?\b|\bAug\.?(?:ust)?\b|\bSept?\.?(?:tember)?\b|\bOct\.?(?:ober)?\b|\bNov\.?(?:ember)?\b|\bDec\.?(?:ember)?\b)(.{,4}(\b\d{4}\b))?'
    )

    # month/day/year
    _dayRegex4 = re.compile(r'(\D|\b)(\d{1,2}/\d{1,2}/\d{4})(\D|\b)')

    #only year
    _dayRegex5 = re.compile('\D(\d{4})\D')


    _timeRegex = re.compile(
        r"""(?ix)
        .*?
        (
            morning
            |afternoon
            |evening
            |(\d{1,2}\:\d{2})\ ?(am|pm)?
            |in\ (.+?)\ (hours|minutes)(\ (?:and\ )?(.+?)\ (hours|minutes))?
        )
        .*?""")

    def _preprocess(self, input):
        return input.replace('-', ' ').lower()

    def combineDays(self, DaysA, DaysB):
        DaysA = [day for day in DaysA if day]
        DaysB = [day for day in DaysB if day]
        if not DaysA:
            return DaysB
        if not DaysB:
            return DaysA

        def combine(A, B):
            if (not A) and (not B):
                return []
            if not A:
                return B
            if not B:
                return A
            itemA = A[0]
            itemB = B[0]
            if (itemA[1].stop <= itemB[1].start):
                return [itemA] + combine(A[1:], B)
            if (itemB[1].stop <= itemA[1].start):
                return [itemB] + combine(A, B[1:])
            if (itemA[0].count('X') >= itemB[0].count('X')):
                return [itemB] + combine(A[1:], B[1:])
            else:
                return [itemA] + combine(A[1:], B[1:])
        return combine(DaysA, DaysB)

    def extractDays(self, input):
        def safe(exp):
            """For safe evaluation of regex groups"""
            try:
                return exp()
            except:
                return None

        def extractMonth(dayMatch):
            if dayMatch[:3] in self.__startMonths__:
                return self.__startMonths__.index(dayMatch[:3]) + 1

        def extractDay(dayMatch):
            if dayMatch in self.__dateDescriptors__:
                return self.__dateDescriptors__[dayMatch]
            elif dayMatch.isalnum() and \
                (int(dayMatch) in self.__dateDescriptors__.values()):
                return int(dayMatch)

        def extractYear(dayMatch):
            if (not dayMatch):
                return None
            if (not dayMatch.isalnum()):
                return None
            year = int(dayMatch)
            if (1800 <= year <= 2020):
                return year

        def handleMatch(dateMatch):
            month = safe(lambda: extractMonth(dateMatch.group(1)))
            day = safe(lambda: extractDay(dateMatch.group(2)))
            year = safe(lambda: extractYear(dateMatch.group(4)))

            if year and day:
                d = '/'.join(['%02d' % month, '%02d' % day, str(year)])
                return (d, range(dateMatch.start(1), dateMatch.end(4)))
            elif day:
                d = '/'.join(['%02d' % month, '%02d' % day, str(self.now.year)])
                return (d, range(dateMatch.start(1), dateMatch.end(2)))
            elif year:
                d = '/'.join(['%02d' % month, 'XX', str(year)])
                return (d, range(dateMatch.start(1), dateMatch.end(4)))
            else:
                d = '/'.join(['%02d' % month, 'XX', str(self.now.year)])
                return (d, range(dateMatch.start(1), dateMatch.end(1)))

        def handleMatch2(dateMatch):
            month = safe(lambda: extractMonth(dateMatch.group(2)))
            day = safe(lambda: extractDay(dateMatch.group(1)))
            year = safe(lambda: extractYear(dateMatch.group(4)))

            if year and day:
                d = '/'.join(['%02d' % month, '%02d' % day, str(year)])
                return (d, range(dateMatch.start(1), dateMatch.end(4)))
            elif day:
                d = '/'.join(['%02d' % month, '%02d' % day, str(self.now.year)])
                return (d, range(dateMatch.start(1), dateMatch.end(2)))
            elif year:
                d = '/'.join(['%02d' % month, 'XX', str(year)])
                return (d, range(dateMatch.start(2), dateMatch.end(4)))
            else:
                d = '/'.join(['%02d' % month, 'XX', str(self.now.year)])
                return (d, range(dateMatch.start(2), dateMatch.end(2)))

        def handleMatch3(dateMatch):
            month, day, year = dateMatch.group(2).split('/')
            month = int(month)
            day = int(day)
            year = int(year)
            try:
                datetime.datetime(year, month, day)
                d = '/'.join(['%02d' % month, '%02d' % day, str(year)])
                return (d, range(dateMatch.start(2), dateMatch.end(2)))
            except:
                return None

        def handleMatch4(dateMatch):
            if extractYear(dateMatch.group(1)):
                return ('XX/XX/%d' % extractYear(dateMatch.group(1)),
                        range(dateMatch.start(1), dateMatch.end(1)))
            else:
                return None

        # format1 month, day, year
        matches = self._dayRegex2.finditer(input)
        Days = [safe(lambda: handleMatch(dateMatch)) for dateMatch in matches]

        # format2 day, month, year
        matches = self._dayRegex3.finditer(input)
        Days = self.combineDays(Days,
                                [safe(lambda: handleMatch2(dateMatch)) for dateMatch in matches])

        # month/day/year
        matches = self._dayRegex4.finditer(input)
        Days = self.combineDays(Days,
                                [safe(lambda: handleMatch3(dateMatch)) for dateMatch in matches])

        # only year
        matches = self._dayRegex5.finditer(input)
        Days = self.combineDays(Days,
                                [safe(lambda: handleMatch4(dateMatch)) for dateMatch in matches])
        return Days

    def extractIrrDays(self, input):
        """Extracts all day-related information from an input string.
        Ignores any information related to the specific time-of-day.

        Args:
            input (str): Input string to be parsed.

        Returns:
            A list of datetime objects containing the extracted date from the
            input snippet, or an empty list if none found.
        """
        def safe(exp):
            """For safe evaluation of regex groups"""
            try:
                return exp()
            except:
                return None

        def extractDayOfWeek(dateMatch):
            if dateMatch.group(8) in self.__daysOfWeek__:
                return self.__daysOfWeek__.index(dateMatch.group(8))
            if dateMatch.group(6) in self.__daysOfWeek__:
                return self.__daysOfWeek__.index(dateMatch.group(6))

        def extractDaysFrom(dateMatch):
            if not dateMatch.group(1):
                return 0

            def numericalPrefix(dateMatch):
                # Grab 'three' of 'three weeks from'
                prefixStr = input[max(0, dateMatch.start() - 50):dateMatch.start()]
                prefixStr = re.search('^[0-9a-zA-Z- ,]+', prefixStr[::-1]).group()[::-1]
                prefixAll = prefixStr.split(' ')
                prefixAll.reverse()
                prefix = [(idx, x) for idx, x in enumerate(prefixAll)
                          if x != '' and x != 'and' and x != ',']
                # Generate best guess number
                service = NumberService()
                res = (1, 0)
                for i in range(len(prefix)):
                    num = ' '.join([st for idx, st in prefix[i::-1]])
                    print(num)
                    if not service.isValid(num):
                        return res
                    else:
                        res = (service.parse(num),
                               -len(' '.join(prefixAll[:prefix[i][0] + 1])))
                return res

            factor, off = numericalPrefix(dateMatch)
            if (dateMatch.group(3) == 'before' or dateMatch.group(3) == 'ago'):
                factor = -factor

            if dateMatch.group(2) == 'week':
                return (factor * 7, off)
            elif dateMatch.group(2) == 'day':
                return (factor * 1, off)
            elif dateMatch.group(2) == 'month':
                return (factor * 30, off)
            elif dateMatch.group(2) == 'year':
                return (factor * 365, off)

        def extractMonth(dayMatch):
            if dayMatch[:3] in self.__startMonths__:
                return self.__startMonths__.index(dayMatch[:3]) + 1

        def handleMatch(dateMatch):
            def generateDate(year, month):
                '''generate date from year and month'''
                while (month <= 0):
                    year -= 1
                    month += 12
                while (month > 12):
                    year += 1
                    month -= 12
                return '%02d/XX/%d' % (month, year)

            days_from = safe(lambda: extractDaysFrom(dateMatch))
            today = safe(lambda: dateMatch.group(4) in self.__todateMatches__)
            tomorrow = safe(lambda: dateMatch.group(4)
                            in self.__tomorrowMatches__)
            yesterday = safe(lambda: dateMatch.group(4)
                             in self.__yesterdateMatches__)
            next_week = safe(lambda: dateMatch.group(5) == 'next')
            last_week = safe(lambda: dateMatch.group(5) == 'last')
            isMonth = safe(lambda: dateMatch.group(6) == 'month' or
                         dateMatch.group(2) == 'month')
            isYear = safe(lambda: dateMatch.group(6) == 'year' or
                         dateMatch.group(2) == 'year')
            month_of_year = safe(lambda:extractMonth(dateMatch.group(7)))
            day_of_week = safe(lambda: extractDayOfWeek(dateMatch))

            if not dateMatch:
                return None

            stIdx = dateMatch.start()
            edIdx = dateMatch.end()

            if days_from:
                days_from, off = days_from
                stIdx += off

            def ck(days, st):
                if (st == 'day') and (abs(days) == 1): return True
                if (st == 'week') and (abs(days) == 7): return True
                if (st == 'year') and (abs(days) == 365): return True
                return False
            if days_from and dateMatch.group(1) and \
            (ck(days_from, dateMatch.group(2)) == 1) and \
                    ('s' in dateMatch.group(1)):
                return None

            if (isYear):
                year = self.now.year
                if days_from:
                    year += days_from // 365
                else:
                    if next_week:
                        year += 1
                    elif last_week:
                        year -= 1
                return ('XX/XX/%d' % year, range(stIdx, edIdx))
            elif (isMonth):
                year = self.now.year
                month = self.now.month
                if days_from:
                    month += days_from // 30
                else:
                    if next_week:
                        month += 1
                    elif last_week:
                        month -= 1
                return (generateDate(year, month), range(stIdx, edIdx))
            elif (month_of_year):
                year = self.now.year
                month = self.now.month
                if next_week:
                    if month >= month_of_year:
                        year += 1
                elif last_week:
                    if month <= month_of_year:
                        year -= 1
                month = month_of_year
                return (generateDate(year, month), range(stIdx, edIdx))
            # Convert extracted terms to datetime object
            elif today:
                d = self.now
            elif tomorrow:
                d = self.now + datetime.timedelta(days=1)
            elif yesterday:
                d = self.now - datetime.timedelta(days=-1)
            elif (not day_of_week is None) or (dateMatch.group(6) == 'week'):
                num_days_away = 0
                if not day_of_week is None:
                    current_day_of_week = self.now.weekday()
                    num_days_away = (day_of_week - current_day_of_week) % 7

                if next_week:
                    num_days_away += 7
                if last_week:
                    num_days_away -= 7

                d = self.now + \
                    datetime.timedelta(days=num_days_away)
            elif days_from:
                d = self.now
            else:
                return None

            if days_from:
                d += datetime.timedelta(days=days_from)
            year, mon, day = d.isoformat().split('-')
            d = '/'.join([mon, day[:2], year])

            return (d, range(stIdx, edIdx))

        matches = self._dayRegex.finditer(input)

        return [safe(lambda: handleMatch(dateMatch)) for dateMatch in matches]

    def extractDay(self, input):
        """Returns the first time-related date found in the input string,
        or None if not found."""
        day = self.extractDays(input)
        if day:
            return day[0]
        return None

    def extractDates(self, input, irregular=True):
        """Extract semantic date information from an input string.
        In effect, runs both parseDay and parseTime on the input
        string and merges the results to produce a comprehensive
        datetime object.

        Args:
            input (str): Input string to be parsed.
            irregular: get irregular date

        Returns:
            A list of datetime objects containing the extracted dates from the
            input snippet, or an empty list if not found.
        """
        input = self._preprocess(input)

        days = self.extractDays(input)
        if (irregular):
            days = self.combineDays(days, self.extractIrrDays(input))
        return days

    def extractDate(self, input):
        """Returns the first date found in the input string, or None if not
        found."""
        dates = self.extractDates(input)
        if dates:
            return dates[0]
        return None

    def convertDay(self, day, prefix="", weekday=False):
        """Convert a datetime object representing a day into a human-ready
        string that can be read, spoken aloud, etc.

        Args:
            day (datetime.date): A datetime object to be converted into text.
            prefix (str): An optional argument that prefixes the converted
                string. For example, if prefix="in", you'd receive "in two
                days", rather than "two days", while the method would still
                return "tomorrow" (rather than "in tomorrow").
            weekday (bool): An optional argument that returns "Monday, Oct. 1"
                if True, rather than "Oct. 1".

        Returns:
            A string representation of the input day, ignoring any time-related
            information.
        """
        def sameDay(d1, d2):
            d = d1.day == d2.day
            m = d1.month == d2.month
            y = d1.year == d2.yaer
            return d and m and y

        tom = self.now + datetime.timedelta(days=1)

        if sameDay(day, self.now):
            return "today"
        elif sameDay(day, tom):
            return "tomorrow"

        if weekday:
            dayString = day.strftime("%A, %B %d")
        else:
            dayString = day.strftime("%B %d")

        # Ex) Remove '0' from 'August 03'
        if not int(dayString[-2]):
            dayString = dayString[:-2] + dayString[-1]

        return prefix + " " + dayString

    def convertTime(self, time):
        """Convert a datetime object representing a time into a human-ready
        string that can be read, spoken aloud, etc.

        Args:
            time (datetime.date): A datetime object to be converted into text.

        Returns:
            A string representation of the input time, ignoring any day-related
            information.
        """
        # if ':00', ignore reporting minutes
        m_format = ""
        if time.minute:
            m_format = ":%M"

        timeString = time.strftime("%I" + m_format + " %p")

        # if '07:30', cast to '7:30'
        if not int(timeString[0]):
            timeString = timeString[1:]

        return timeString

    def convertDate(self, date, prefix="", weekday=False):
        """Convert a datetime object representing into a human-ready
        string that can be read, spoken aloud, etc. In effect, runs
        both convertDay and convertTime on the input, merging the results.

        Args:
            date (datetime.date): A datetime object to be converted into text.
            prefix (str): An optional argument that prefixes the converted
                string. For example, if prefix="in", you'd receive "in two
                days", rather than "two days", while the method would still
                return "tomorrow" (rather than "in tomorrow").
            weekday (bool): An optional argument that returns "Monday, Oct. 1"
                if True, rather than "Oct. 1".

        Returns:
            A string representation of the input day and time.
        """
        dayString = self.convertDay(
            date, prefix=prefix, weekday=weekday)
        timeString = self.convertTime(date)
        return dayString + " at " + timeString


def extractDates(input, tz=None, now=None, irregular=True):
    """Extract semantic date information from an input string.
    This is a convenience method which would only be used if
    you'd rather not initialize a DateService object.

    Args:
        input (str): The input string to be parsed.
        tz: An optional Pytz timezone. All datetime objects returned will
            be relative to the supplied timezone, or timezone-less if none
            is supplied.
        now: The time to which all returned datetime objects should be
            relative. For example, if the text is "In 5 hours", the
            datetime returned will be now + datetime.timedelta(hours=5).
            Uses datetime.datetime.now() if none is supplied.

    Returns:
        A list of datetime objects extracted from input.
    """
    service = DateService(tz=tz, now=now)
    return service.extractDates(input, irregular)
