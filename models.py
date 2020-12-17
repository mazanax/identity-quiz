from datetime import datetime, timedelta
from secrets import token_hex

from peewee import Model, CharField, ForeignKeyField, IntegerField, DateTimeField, TextField

import config
import const


class User(Model):
    lang = CharField(max_length=2)
    source = CharField(max_length=8)
    source_id = CharField()
    name = CharField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    deleted_at = DateTimeField(null=True)

    class Meta:
        database = config.db
        indexes = (
            (('source', 'source_id'), False),
        )

    def get_answer(self):
        return self.answer[0] if self.answer is not None and len(self.answer) else None


class AccessToken(Model):
    user = ForeignKeyField(User, backref='tokens')
    token = CharField(unique=True, index=True)
    created_at = DateTimeField(default=datetime.utcnow)
    expire_at = DateTimeField()

    class Meta:
        database = config.db

    @staticmethod
    def create(user, expire_in_days=None):
        if expire_in_days is None:
            expire_in_days = 1
        token = AccessToken(user=user, token=AccessToken.generate_token(),
                            expire_at=datetime.utcnow() + timedelta(days=expire_in_days))
        if token.save():
            return token

        return None

    @staticmethod
    def generate_token():
        while True:
            token = token_hex(config.token_length)
            if AccessToken.get_or_none(AccessToken.token == token) is not None:
                continue

            return token


class Answer(Model):
    user = ForeignKeyField(User, backref='answer', unique=True)
    value = IntegerField(null=True)
    step = IntegerField(default=const.STEP_SIMPLE_CAPTCHA)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = config.db


class Captcha(Model):
    code = CharField(max_length=10, unique=True, index=True)
    question = CharField(null=True)
    value = CharField(max_length=32)
    expire_at = DateTimeField()

    class Meta:
        database = config.db

    @staticmethod
    def generate_code():
        while True:
            code = token_hex(5)  # to get 10 symbols we need 5 bytes
            if Captcha.get_or_none(Captcha.code == code) is not None:
                continue

            return code


with config.db:
    config.db.create_tables([User, AccessToken, Captcha, Answer], safe=True)

