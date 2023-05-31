import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery, UserNode
import logging
logging.getLogger("graphql.execution.utils").setLevel(logging.ERROR)
from users.models import CustomUser


class UnauthorisedAccessError(GraphQLError):
   def __init__(self, message, *args, **kwargs):
      super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)
class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   update_account = mutations.UpdateAccount.Field()
   resend_activation_email = mutations.ResendActivationEmail.Field()
   send_password_reset_email = mutations.SendPasswordResetEmail.Field()
   password_reset = mutations.PasswordReset.Field()
   password_change = mutations.PasswordChange.Field()

class MyUserQuery(UserQuery):
   users = DjangoFilterConnectionField(UserNode)
   user = graphene.Field(UserNode, pk=graphene.Int(required=True))
   def resolve_users(self, info):
      if not info.context.user.is_staff:
         raise UnauthorisedAccessError(message="ИДИ НАХУЙ, тебе нельзя это делать")
   def resolve_user(self, info, pk):
      if not info.context.user.is_staff and info.context.user.id!=pk:
         raise UnauthorisedAccessError(message="ИДИ НАХУЙ, тебе нельзя это делать")
      try:
         return CustomUser.objects.get(pk=pk)
      except CustomUser.DoesNotExist:
         return None

class Query(MyUserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   pass

