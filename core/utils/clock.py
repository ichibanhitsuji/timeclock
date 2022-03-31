from datetime import datetime
from core.models import Clock
from django.db.models import Q

def get_list_clocks(user, start_date):
    """
    Return the clocks of the user. Returned clocks have [clock_in, clock_out] in the interval [start_date, now]
    :param user: authenticated user
    :param start_date: date from which you want to get the clocked hours
    :return: list of clocks
    """
    return Clock.objects.filter(user=user).filter(
        Q(clocked_out__date__gte=start_date, clocked_out__date__lte=datetime.today()) | Q(
            clocked_out__isnull=True))


def sum_clocked_hours(list_clocks, start_date):
    """
    Sum the clocked hours of the list of clocks.
    clocked_in is caped using start_date.
    clocked_out is capped using now.
    :param list_clocks: list of clocks
    :param start_date: clocked_in value of the clocks are caped with start_date
    :return:
    """
    today_clocks = list(map(lambda clock: (
        clock.clocked_in.replace(tzinfo=None) if clock.clocked_in.date() >= start_date.date() else start_date.replace(
            tzinfo=None),
        clock.clocked_out.replace(tzinfo=None) if clock.clocked_out else datetime.now().replace(tzinfo=None)),
                            list_clocks))

    # calculate the sum of the timedelta of all the clocked_in and clocked_out for each tuple
    s = sum([(t[1] - t[0]).total_seconds() for t in today_clocks])
    return round(s / 3600)
