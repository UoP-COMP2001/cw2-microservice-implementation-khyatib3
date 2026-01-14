from config.config import create_connexion_app, basedir

def create_app():
    connex_app = create_connexion_app()
    connex_app.add_api(basedir.parent / "swagger" / "swagger.yml")
    return connex_app.app
