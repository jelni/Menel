from os import getenv

import motor.motor_asyncio


class Database:
    def __init__(self):
        self.connection = motor.motor_asyncio.AsyncIOMotorClient(
            getenv('MONGODB_HOST'),
            tz_aware=False,
            connect=True,
            directConnection=False,
            appname='MiauBot',
            retryWrites=True,
            retryReads=True,
            w=1,
            readPreference='primaryPreferred',
            tls=True
        )

        self.config = self.connection['config']