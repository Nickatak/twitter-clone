class DevConfig(object):
    # It's very unfortunate that you can't enable development-mode without setting Env variables.

    SQLALCHEMY_TRACK_MODIFICATIONS = False