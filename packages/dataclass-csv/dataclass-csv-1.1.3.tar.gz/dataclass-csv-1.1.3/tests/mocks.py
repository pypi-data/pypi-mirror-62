import dataclasses

from datetime import datetime

from dataclass_csv import dateformat, accept_whitespaces

from typing import Optional


@dataclasses.dataclass
class User:
    name: str
    age: int

@dataclasses.dataclass
class UserWithoutAcceptWhiteSpacesDecorator:
    name: str


@accept_whitespaces
@dataclasses.dataclass
class UserWithAcceptWhiteSpacesDecorator:
    name: str


@dataclasses.dataclass
class UserWithAcceptWhiteSpacesMetadata:
    name: str = dataclasses.field(metadata={'accept_whitespaces': True})


@dataclasses.dataclass
class UserWithoutDateFormatDecorator:
    name: str
    create_date: datetime


@dateformat('%Y-%m-%d')
@dataclasses.dataclass
class UserWithDateFormatDecorator:
    name: str
    create_date: datetime


@dataclasses.dataclass
class UserWithDateFormatMetadata:
    name: str
    create_date: datetime = dataclasses.field(
        metadata={'dateformat': '%Y-%m-%d'}
    )


@dateformat('%Y-%m-%d')
@dataclasses.dataclass
class UserWithDateFormatDecoratorAndMetadata:
    name: str
    birthday: datetime
    create_date: datetime = dataclasses.field(
        metadata={'dateformat': '%Y-%m-%d %H:%M'}
    )


@dataclasses.dataclass
class DataclassWithBooleanValue:
    boolValue: bool


@dataclasses.dataclass
class DataclassWithBooleanValueNoneDefault:
    boolValue: bool = None


@dataclasses.dataclass
class UserWithInitFalse:
    firstname: str
    lastname: str
    age: int = dataclasses.field(init=False)


@dataclasses.dataclass
class UserWithInitFalseAndDefaultValue:
    firstname: str
    lastname: str
    age: int = dataclasses.field(init=False, default=0)

@dataclasses.dataclass
class UserWithOptionalAge:
    name: str
    age: Optional[int]

