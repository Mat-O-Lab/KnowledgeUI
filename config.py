import os

class Config:
    """
    This class defines some general configs 

    ....

    Attributes
    ----------
    SECRET_KEY: str
        get the private_key from environment variable
    TEMPORAL_FOLDER: str
        defines a temporary folders to use as tmp
    TEMPLATES_AUTORELOAD: boolean
        defines autoreload property 
    SPARQL_ENDPOINT: str
        get sparql endpoint
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "harder to guess string"
    TEMPORAL_FOLDER = os.environ.get("TEMPORAL_FOLDER") or "tmp"
    TEMPLATES_AUTORELOAD = True
    SPARQL_ENDPOINT = 'https://fuseki.matolab.org/alutrace/sparql'
    SPARKLIS_OPTIONS = "&entity_lexicon_select=http%3A//www.w3.org/2000/01/rdf-schema%23label&concept_lexicons_select=http%3A//www.w3.org/2000/01/rdf-schema%23label&concept_tooltips_select=http%3A//www.w3.org/2000/01/rdf-schema%23comment"

class DevelopmentConfig(Config):
    """
    Attributes
    ----------
    config: object
    """

    DEBUG = True

class ProductionConfig(Config):
    """
    Attributes
    ----------
    config: object
    """

    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
