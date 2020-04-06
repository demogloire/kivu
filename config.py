class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = '9462bfc3ca8d37b136173798873d05ea'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SIMPLEMDE_JS_IIFE = False
    SIMPLEMDE_USE_CDN = False


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SECRET_KEY = '9462bfc3ca8d37b136173798873d05ea'
    DEBUG = True
    SIMPLEMDE_JS_IIFE = False
    SIMPLEMDE_USE_CDN = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
