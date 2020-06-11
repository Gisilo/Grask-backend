
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Grabit


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class GrabitNode(DjangoObjectType):
    class Meta:
        model = Grabit
        filter_fields = ['name_project', 'name_db', 'created_date', 'update_date']
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    grabit = graphene.relay.Node.Field(GrabitNode)
    all_grabits = DjangoFilterConnectionField(GrabitNode)


class CreateGrabit(graphene.relay.ClientIDMutation):
    msg = graphene.String()
    grabit = graphene.Field(GrabitNode)

    class Input:
        name_project = graphene.String(required=True)
        name_db = graphene.String()
        dbms = graphene.String()
        description = graphene.String()
        port = graphene.Int()
        created_date = graphene.DateTime()
        update_date = graphene.DateTime()
        graph = graphene.String()


    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        try:
            new_grabit, created = Grabit.objects.update_or_create(name_project=input.get("name_project"), defaults=input)

            if created:
                msg = "Created new project {}".format(input.get("name_project"))

            msg = "Update project {}".format(input.get("name_project"))

        except:
            msg = "Can't create or update project {}".format(input["name_project"])


        #grabit.save()
        return CreateGrabit(msg=msg, grabit=new_grabit)


class DeleteGrabit(graphene.relay.ClientIDMutation):
    msg = graphene.Field(type=graphene.String)
    grabit = graphene.Field(GrabitNode)

    class Input:
        name_project = graphene.String(required=True)
        name_db = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        obj = Grabit.objects.get(name_project=input["name_project"])
        try:
            obj.delete()
            msg = "Successful delete project {}".format(input["name_project"])
        except:
            msg = "Can't delete project {}".format(input["name_project"])
        print(msg)
        return DeleteGrabit(msg=msg, grabit=obj)


class Mutation(graphene.AbstractType):
    create_grabit = CreateGrabit.Field()
    delete_grabit = DeleteGrabit.Field()