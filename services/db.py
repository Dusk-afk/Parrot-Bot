import json
import os

from services.singleton import singleton

class Config:
    pass

@singleton
class Db:
    def __init__(self):
        self._db: dict[str, Config] = {}
        
        if not os.path.exists("db.json"):
            with open("db.json", "w") as json_file:
                json.dump({}, json_file)

        self.load_db()
    
    def load_db(self):
        db = {}
        with open("db.json", "r") as json_file:
            db = json.load(json_file)
        
        for key in db:
            self._db[key] = Config(self, key, db[key])
    
    def save_db(self):
        db = {}
        for key in self._db:
            db[key] = self._db[key].to_json()
        
        with open("db.json", "w") as json_file:
            json.dump(db, json_file, indent=2)
    
    def add_guild(self, guild_id: str | int):
        guild_id = str(guild_id)
        if guild_id in self._db: return
        self._db[guild_id] = Config(self, guild_id)
        self.save_db()
    
    def of(self, guild_id: str | int) -> Config:
        return self._db[str(guild_id)]

class Config:
    def __init__(self, db: Db, guild_id: str | int, json: dict | None = None):
        self._db = db
        self.guild_id = guild_id
        self._json = json if json else self.default_json()
    
    def default_json(self):
        return {
            "lang": "en",
            "say_enabled": False,
        }
    
    def to_json(self):
        return self._json

    def get(self, key: str, default = None):
        if key in self._json:
            return self._json[key]
        else:
            return default
    
    def set(self, key: str, value):
        self._json[key] = value
        self._db.save_db()
    
    def get_language(self):
        return self.get("lang", "en")

    def set_language(self, lang: str):
        self.set("lang", lang)
    
    def is_say_enabled(self):
        return self.get("say_enabled", False)

    def set_say_enabled(self, enabled: bool):
        self.set("say_enabled", enabled)
