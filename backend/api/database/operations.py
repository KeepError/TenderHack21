import json

path = "api/database/data.json"


class Periodicity:
    key = "periodicity"

    @classmethod
    def get_data(cls):
        with open(path, encoding="utf8") as f:
            return json.load(f)[cls.key]

    @classmethod
    def save_data(cls, data):
        with open(path, encoding="utf8", mode="w") as f:
            db_content = json.load(f)
            db_content[cls.key] = data
            json.dump(db_content, f)

    @classmethod
    def get_records_by_inn(cls, inn_number):
        data = cls.get_data()
        for item in data:
            if str(item["inn"]) == str(inn_number):
                return item["records"]
        return None
