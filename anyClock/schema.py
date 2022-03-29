import graphene
import graphql_jwt
from core.schema import Query as CoreQuery
from core.schema import Mutation as CoreMutation

class Query(CoreQuery):
    pass

class Mutation(CoreMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
