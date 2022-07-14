import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "harder to guess string"
    TEMPORAL_FOLDER = os.environ.get("TEMPORAL_FOLDER") or "tmp"
    TEMPLATES_AUTORELOAD = True
    SPARQL_ENDPOINT = 'https://fuseki.matolab.org/alutrace/sparql'
    SPARKLIS_OPTIONS = "&entity_lexicon_select=http%3A//www.w3.org/2000/01/rdf-schema%23label&concept_lexicons_select=http%3A//www.w3.org/2000/01/rdf-schema%23label&concept_tooltips_select=http%3A//www.w3.org/2000/01/rdf-schema%23comment"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}