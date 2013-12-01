"Mixins for serializing objects."
import json
import cPickle as pickle


class PassThroughSerializer(object):
    "Don't serialize."
    def serialize(self, obj):
        "Support for serializing objects stored in Redis."
        return obj

    def deserialize(self, obj):
        "Support for deserializing objects stored in Redis."
        return obj


class PickleSerializer(PassThroughSerializer):
    "Serialize values using pickle."
    def serialize(self, obj):
        return pickle.dumps(obj)

    def deserialize(self, obj):
        "Deserialize values using pickle."
        return pickle.loads(obj)


class JSONSerializer(PassThroughSerializer):
    "Serialize values using JSON."
    def serialize(self, obj):
        return json.dumps(obj)

    def deserialize(self, obj):
        "Deserialize values using JSON."
        return json.loads(obj)

