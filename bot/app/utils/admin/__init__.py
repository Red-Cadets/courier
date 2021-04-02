from app import app


def is_admin(ID):
    if ID in app.config['ADMINS']:
        return True
    return False
