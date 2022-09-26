from datetime import datetime


def media_upload_to(instance, filename):
    name = instance.__class__.__name__

    current = datetime.now()
    path = current.strftime("%Y/%m/%d")
    time = current.strftime("%H-%M-%S")

    return '{}/{}s/{}-{}'.format(path, str(name).lower(), time, filename)
