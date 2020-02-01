import logging

LOG = None


def setup_logging(
    log_path='./gladia.log',
    file_level='debug',
    stream=True,
    stream_level='debug',
):
    global LOG
    LOG = logging.getLogger('gladia')
    LOG.setLevel(logging.DEBUG)

    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, file_level.upper()))

    if stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(getattr(logging, stream_level.upper()))

    formatter = logging.Formatter(
        '[%(asctime)s]  %(name)s:%(levelname)s - %(message)s'
    )

    if log_path:
        file_handler.setFormatter(formatter)
        LOG.addHandler(file_handler)

    if stream:
        stream_handler.setFormatter(formatter)
        LOG.addHandler(stream_handler)
