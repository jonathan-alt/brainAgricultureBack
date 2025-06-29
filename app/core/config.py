import logging
import os

logger = logging.getLogger(__name__)


class ConfigSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ConfigSingletonMeta):
    def __init__(self, **kwargs):
        self.setup_params(**kwargs)
        self.populate_settings()

    def setup_params(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_vars(self):
        raise NotImplementedError()

    def populate_settings(self):
        vars = self.get_vars()
        self.AGRICULTURE_DB_USER = vars.get("USER")
        self.AGRICULTURE_DB_PASSWORD = vars.get("PASSWORD")
        self.AGRICULTURE_DB_HOST = vars.get("HOST")
        self.AGRICULTURE_DB_PORT = vars.get("PORT_DB")
        self.AGRICULTURE_DB_DATABASE = vars.get("DATABASE")
        self.ENVIRONMENT = vars.get("ENVIRONMENT")
        self.ENCRYPTION_KEY = vars.get("ENCRYPTION_KEY")
        self.AGRICULTURE_QUEUE = f"report_{self.ENVIRONMENT}"
        self.PORT = int(vars.get("PORT", 8000))


class ConfigFromEnviron(Config):
    def get_vars(self):
        return os.environ


class ConfigFromSecretManager(Config):
    def get_vars(self):
        raise NotImplementedError()


class ConfigFactory:
    def get_config(self):
        environment = os.environ.get("ENVIRONMENT", "undefined")
        # idealmente em dev carregamentos os secrets/config diretamente das variaveis de ambiente
        # em prod/staging devemos usar um secret manager como vault da hashicorp
        # ou secret manager da AWS ou secret manager do GCP, etc...
        if environment == "development":
            return ConfigFromEnviron()
        elif environment == "staging":
            return ConfigFromEnviron()
        elif environment == "production":
            return ConfigFromEnviron()
        elif environment == "test":
            return ConfigFromEnviron()
        else:
            logger.critical(f"Invalid environment: {environment}")
            raise Exception("Invalid")


config = ConfigFactory().get_config()
