# -*- coding: utf-8 -*-
"""FastAPI CamelCase Parser Module

Module adds aliases to pydantic models 
Module will decode the body and decamilize (camelCase => snake_case) its keys
then encode it back again.

example if the request.body = {"myVal":"Hello_world"},
the module will convert it to {"my_val":"Hello_world"}
and viceversa

"""
from humps import camelize
from pydantic import BaseModel


def to_camel(string):
    return camelize(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

