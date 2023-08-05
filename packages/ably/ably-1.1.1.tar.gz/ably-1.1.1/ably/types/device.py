from ably.util import case


DevicePushTransportType = {'fcm', 'gcm', 'apns', 'web'}
DevicePlatform = {'android', 'ios', 'browser'}
DeviceFormFactor = {'phone', 'tablet', 'desktop', 'tv', 'watch', 'car', 'embedded', 'other'}


class DeviceDetails(object):

    def __init__(self, id, client_id=None, form_factor=None, metadata=None,
                 platform=None, push=None, update_token=None, app_id=None,
                 device_identity_token=None):

        if push:
            recipient = push.get('recipient')
            if recipient:
                transport_type = recipient.get('transportType')
                if transport_type is not None and transport_type not in DevicePushTransportType:
                    raise ValueError('unexpected transport type {}'.format(transport_type))

        if platform is not None and platform not in DevicePlatform:
            raise ValueError('unexpected platform {}'.format(platform))

        if form_factor is not None and form_factor not in DeviceFormFactor:
            raise ValueError('unexpected form factor {}'.format(form_factor))

        self.__id = id
        self.__client_id = client_id
        self.__form_factor = form_factor
        self.__metadata = metadata
        self.__platform = platform
        self.__push = push
        self.__update_token = update_token
        self.__app_id = app_id
        self.__device_identity_token = device_identity_token

    @property
    def id(self):
        return self.__id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def form_factor(self):
        return self.__form_factor

    @property
    def metadata(self):
        return self.__metadata

    @property
    def platform(self):
        return self.__platform

    @property
    def push(self):
        return self.__push

    @property
    def update_token(self):
        return self.__update_token

    @property
    def app_id(self):
        return self.__app_id

    @property
    def device_identity_token(self):
        return self.__device_identity_token

    def as_dict(self):
        keys = ['id', 'client_id', 'form_factor', 'metadata', 'platform',
                'push', 'update_token', 'app_id', 'device_identity_token']

        obj = {}
        for key in keys:
            value = getattr(self, key)
            if value is not None:
                key = case.snake_to_camel(key)
                obj[key] = value

        return obj

    @classmethod
    def from_dict(cls, obj):
        obj = {case.camel_to_snake(key): value for key, value in obj.items()}
        return cls(**obj)

    @classmethod
    def from_array(cls, array):
        return [cls.from_dict(d) for d in array]

    @classmethod
    def factory(cls, device):
        if isinstance(device, cls):
            return device

        return cls.from_dict(device)


def device_details_response_processor(response):
    native = response.to_native()
    return DeviceDetails.from_array(native)
