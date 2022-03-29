import graphene
from graphene_django import DjangoObjectType

from core.models import Clock

class ClockType(DjangoObjectType):
    class Meta:
        model = Clock

class Query(graphene.ObjectType):
    all_clocks = graphene.List(ClockType)

    def resolve_all_clocks(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication credentials were not provided')
        return Clock.objects.all()

class Mutation(graphene.ObjectType):
    pass