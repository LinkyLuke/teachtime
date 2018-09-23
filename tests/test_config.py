import os

import pytest

def test_testing_config(app):
    app.config.from_object('teachtime.config.TestingConfig')
    assert app.config['TESTING']

def test_development_config(app):
    app.config.from_object('teachtime.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']

def test_production_config(app):
    app.config.from_object('teachtime.config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']