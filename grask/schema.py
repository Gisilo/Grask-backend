import graphene

import grabit.schema
import users.schema
import graphql_jwt


class Query(users.schema.Query, grabit.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(users.schema.Mutation, grabit.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
