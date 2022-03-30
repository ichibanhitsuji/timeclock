from core.models import Clock
import graphene
from datetime import datetime
from core.objectTypes import ClockType

class ClockIn(graphene.Mutation):
    clock = graphene.Field(ClockType)

    class Arguments:
        pass

    def mutate(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')

        # Get the most recent clocked_in for the user
        clock = Clock.objects.filter(user=user).order_by('-clocked_in').first()

        # if clock is null or if clock-out of clock is none return null
        if not clock or clock.clocked_out:
            new_clock = Clock()
            new_clock.user = user
            new_clock.save()
            return ClockIn(clock=new_clock)
        else:
            raise Exception('You have already clocked in')





class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType)

    class Arguments:
        pass

    def mutate(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')

        # Get the most recent clocked_in for the user
        clock = Clock.objects.filter(user=user).order_by('-clocked_in').first()

        if not clock or clock.clocked_out:
            raise Exception('You have not clocked in yet')
        else:
            clock.clocked_out = datetime.now()
            clock.save()
            return ClockOut(clock=clock)