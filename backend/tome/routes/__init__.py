from tome.routes import api_key, auth

routes = [*auth.routes, *api_key.routes]
