from tome.routes import account, auth

routes = [*auth.routes, *account.routes]
