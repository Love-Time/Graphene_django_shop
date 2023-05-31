import graphene
import users.schema as user_schema
import magazin.schema as shop_schema
class Query(user_schema.Query, shop_schema.Query, graphene.ObjectType):
    pass
class Mutation(user_schema.Mutation, shop_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
