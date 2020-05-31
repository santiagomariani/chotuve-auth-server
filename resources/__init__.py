from resources.users_routes import UsersRoutes, UniqueUserRoutes, UserIdFromTokenRoute
from resources.reset_codes import ResetCodesRoutes, ChangePasswordRoutes

def add_routes(api):
    api.add_resource(UsersRoutes, '/users')
    api.add_resource(UniqueUserRoutes, '/users/<int:user_id>')
    api.add_resource(UserIdFromTokenRoute, '/users/id')

    api.add_resource(ResetCodesRoutes, '/reset-codes')
    api.add_resource(ChangePasswordRoutes, '/change-password-with-reset-code')