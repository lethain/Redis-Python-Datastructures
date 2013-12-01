"Mixins for serializing objects."
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

