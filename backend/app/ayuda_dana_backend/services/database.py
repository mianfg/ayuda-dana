from bson import DBRef
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from ayuda_dana_backend.exceptions import InvalidReferenceException

uri = "..."
client = MongoClient(uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["ayuda-dana"]


def dereference(value):
    return db.dereference(value)


def __dereference_dbrefs(data: dict):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = __dereference_dbrefs(value)
    elif isinstance(data, list):
        return [__dereference_dbrefs(item) for item in data]
    elif isinstance(data, DBRef):
        return dereference(data)
    return data


def to_dict(data):
    return __dereference_dbrefs(data.to_mongo().to_dict())


def __fetch_dbref(ref: DBRef):
    print({"_id": ref.id}, db[ref.collection].find_one({"_id": ref.id}))
    if not db[ref.collection].find_one({"_id": ref.id}):
        raise InvalidReferenceException(f"Document with _id {ref.id!s} not found in collection {ref.collection}")


def __check_dbrefs(data: dict):
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, DBRef):
                print("checking dbref:", value)
                __fetch_dbref(value)
            else:
                __check_dbrefs(value)
    elif isinstance(data, list):
        [__check_dbrefs(item) for item in data]


def check_dbrefs(data):
    print(data.to_mongo())
    __check_dbrefs(data.to_mongo().to_dict())
