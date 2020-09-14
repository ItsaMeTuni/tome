from tome.routes import account, api_key, auth, signup

routes = [*auth.routes, *api_key.routes, *account.routes, *signup.routes]
