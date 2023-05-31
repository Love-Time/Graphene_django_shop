import logging

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery, UserNode

logging.getLogger("graphql.execution.utils").setLevel(logging.ERROR)
from users.models import CustomUser

from graphql_jwt.decorators import staff_member_required

class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()  # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class MyUserQuery(UserQuery):
    users = DjangoFilterConnectionField(UserNode)
    user = graphene.Field(UserNode, pk=graphene.Int(required=True))
    @staff_member_required
    def resolve_users(self, info):
       pass


    def resolve_user(self, info, pk):
        if not info.context.user.is_staff and info.context.user.id != pk:
            raise UnauthorisedAccessError(message="ИДИ НАХУЙ, тебе нельзя это делать")
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None


class Query(MyUserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass
