from tome.routes import account, api_key, auth

routes = [*auth.routes, *api_key.routes, *account.routes]
