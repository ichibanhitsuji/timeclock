import graphene
from graphene_django import DjangoObjectType
from datetime import datetime, timedelta
from core.models import Clock

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
        todayClock = Clock.objects.filter(user=user, clocked_in__date=datetime.today())
        hoursAggregated = sum([(c.clocked_out - c.clocked_in).total_seconds() for c in todayClock])
        return round(hoursAggregated/3600)

    def resolve_current_week(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
      # Get the datetime of monday of this week at midnight
        today = datetime.today()
        thisWeekFirstDay = today - timedelta(days=today.weekday())
        thisWeekClock = Clock.objects.filter(user=user, clocked_in__date__gte=thisWeekFirstDay)
        hoursAggregated = sum([(c.clocked_out - c.clocked_in).total_seconds() for c in thisWeekClock])
        return round(hoursAggregated/3600)

    def resolve_current_month(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
      # Get the datetime of the first day of this month at midnight
        thisMonthFirstDay = datetime.today().replace(day=1)
        thisMonthClock = Clock.objects.filter(user=user, clocked_in__date__gte=thisMonthFirstDay)
        hoursAggregated = sum([(c.clocked_out - c.clocked_in).total_seconds() for c in thisMonthClock])
        return round(hoursAggregated/3600)