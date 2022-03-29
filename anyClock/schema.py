import graphene
import graphql_jwt
from core.schema import Query as CoreQuery
from core.schema import Mutation as CoreMutation
from users.schema import Query as UserQuery
from users.schema import Mutation as UserMutation

class Query(CoreQuery, UserQuery):
    pass

class Mutation(CoreMutation, UserMutation, graphene.ObjectType):
    obtainToken = graphql_jwt.ObtainJSONWebToken.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
