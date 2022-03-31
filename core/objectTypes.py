import graphene
from graphene_django import DjangoObjectType
from datetime import datetime, timedelta
from core.models import Clock
from core.utils.clock import sum_clocked_hours, get_list_clocks


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
        clocks = get_list_clocks(user, midnight)
        return sum_clocked_hours(clocks, midnight)

    def resolve_current_week(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
        today = datetime.today()
        current_week_first_day = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0,
                                                                               microsecond=0)
        clocks = get_list_clocks(user, current_week_first_day)
        return sum_clocked_hours(clocks, current_week_first_day)

    def resolve_current_month(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
        current_month_first_day = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        clocks = get_list_clocks(user, current_month_first_day)
        return sum_clocked_hours(clocks, current_month_first_day)
