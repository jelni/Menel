from datetime import datetime, timedelta
from typing import Optional


class Cooldowns:
    def __init__(self):
        self.cooldowns = dict()


    def set(self, user_id: int, command: str, time: int) -> None:
        self.cooldowns.update({user_id: {command: (datetime.utcnow() + timedelta(seconds=time)).timestamp()}})


    def get(self, user_id: int, command: str) -> Optional[int]:
        if user_id not in self.cooldowns or command not in self.cooldowns[user_id]:
            return None

        if self.cooldowns[user_id][command] <= datetime.utcnow().timestamp():
            return None
        else:
            return self.cooldowns[user_id][command] - datetime.utcnow().timestamp()


    def auto(self, user_id: int, command: str, time: int):
        cooldown = self.get(user_id, command)

        if not cooldown:
            self.set(user_id, command, time)

        return cooldown


cooldowns = Cooldowns()