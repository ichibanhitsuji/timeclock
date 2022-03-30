from core.mutations import ClockIn, ClockOut
from core.objectTypes import ClockType, ClockedHoursType

from core.models import Clock

import graphene

class Query(graphene.ObjectType):
    current_clock = graphene.Field(ClockType)
    clocked_hours = graphene.Field(ClockedHoursType)

    def resolve_current_clock(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')

        # Get the most recent clocked_in for the user
        clock = Clock.objects.filter(user=user).order_by('-clocked_in').first()

        # return clock if clock out is None
        if not clock or clock.clocked_out:
            return None

        return clock

    def resolve_clocked_hours(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
        return ClockedHoursType()



class Mutation(graphene.ObjectType):
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()