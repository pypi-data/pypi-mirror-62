# -*- coding: utf-8 -*-

import logging
import pathlib
import structlog
import traceback

from nplusone.core import exceptions


class Notifier(object):

    CONFIG_KEY = None
    ENABLED_DEFAULT = False

    @classmethod
    def is_enabled(cls, config):
        return (config.get(cls.CONFIG_KEY)
                or (cls.CONFIG_KEY not in config and cls.ENABLED_DEFAULT))

    def __init__(self, config):
        self.config = config  # pragma: no cover

    def notify(self, model, field):
        pass  # pragma: no cover


def get_relevant_spark_frames():
    stack = traceback.extract_stack()
    relevant_frames = [
        frame for frame in reversed(stack)
        if frame.filename.startswith(str(pathlib.Path().absolute()))
        and 'spark' in frame.filename
    ]
    return relevant_frames


class LogNotifier(Notifier):

    CONFIG_KEY = 'NPLUSONE_LOG'
    ENABLED_DEFAULT = True

    def __init__(self, config):
        self.logger = config.get('NPLUSONE_LOGGER', structlog.get_logger())
        self.level = config.get('NPLUSONE_LOG_LEVEL', logging.DEBUG)

        self.verbose = config.get('NPLUSONE_VERBOSE', False)
        log_func_map = {
            logging.INFO: self.logger.info,
            logging.WARN: self.logger.warn,
            logging.ERROR: self.logger.error,
            logging.DEBUG: self.logger.debug,
            logging.CRITICAL: self.logger.critical,
        }
        self.log_func = log_func_map.get(self.level, logging.INFO)

    def notify(self, message):
        stack = traceback.extract_stack()
        relevant_frames = [
            frame for frame in reversed(stack)
            if frame.filename.startswith(str(pathlib.Path().absolute()))
            and 'spark' in frame.filename
        ]
        relevant_frames = get_relevant_spark_frames()
        relevant_frame = relevant_frames[0]

        # This assumes we used structlog.get_logger to create our logger.
        log_info = {
            'filename': relevant_frame.filename,
            'line': relevant_frame.lineno,
            'name': relevant_frame.name,
        }

        if self.verbose:
            log_info['frames'] = '\n'.join([
                f'{frame.filename}, {frame.lineno}, {frame.name}'
                for frame in relevant_frames[1:]
            ])

        self.log_func(message.message, **log_info)


class ErrorNotifier(Notifier):

    CONFIG_KEY = 'NPLUSONE_RAISE'
    ENABLED_DEFAULT = False

    def __init__(self, config):
        self.error = config.get('NPLUSONE_ERROR', exceptions.NPlusOneError)

    def notify(self, message):
        stack = traceback.extract_stack()
        relevant_frame = get_relevant_spark_frames()[0]
        raise self.error(message.message + ', ' +
                         str(relevant_frame)[len('<FrameSummary '):-1])


def init(config):
    return [
        notifier(config) for notifier in (LogNotifier, ErrorNotifier)
        if notifier.is_enabled(config)
    ]
