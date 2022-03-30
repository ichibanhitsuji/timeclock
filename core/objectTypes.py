import graphene
from graphene_django import DjangoObjectType
from datetime import datetime, timedelta
from core.models import Clock
from django.db.models import Q


class ClockType(DjangoObjectType):
    class Meta:
        model = Clock


class ClockedHoursType(graphene.ObjectType):
    today = graphene.Int()
    current_week = graphene.Int()
    current_month = graphene.Int()

    def resolve_today(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')

        midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return sum_clocked_hours(user, midnight)

    def resolve_current_week(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
        today = datetime.today()
        current_week_first_day = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        return sum_clocked_hours(user, current_week_first_day)

    def resolve_current_month(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
        current_month_first_day = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return sum_clocked_hours(user, current_month_first_day)

def sum_clocked_hours(user, start_date):
    clocks = Clock.objects.filter(user=user).filter(
        Q(clocked_out__date__gte=start_date, clocked_out__date__lte=datetime.today()) | Q(
            clocked_out__isnull=True))

    today_clocks = list(map(lambda clock: (
        clock.clocked_in if clock.clocked_in.date() >= start_date.date() else start_date,
        clock.clocked_out or datetime.now()),
                            clocks))

    # convert all the date to a naive format
    today_clocks = list(
        map(lambda clock: (clock[0].replace(tzinfo=None), clock[1].replace(tzinfo=None)), today_clocks))

    # calculate the sum of the timedelta of all the clocked_in and clocked_out for each tuple
    s = sum([(t[1] - t[0]).total_seconds() for t in today_clocks])
    return round(s / 3600)