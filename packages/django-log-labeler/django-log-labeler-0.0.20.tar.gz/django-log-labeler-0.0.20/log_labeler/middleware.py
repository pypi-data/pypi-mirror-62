import json
import time
import logging
import traceback
from .encoders import BytesToUtf8JsonEncoder
from django.core.exceptions import ImproperlyConfigured

from .utils import Utils
from django.conf import settings
from log_labeler import local, LOG_LABEL_REQUEST_SETTING, DEFAULT_HEADER_VALUE, \
        LOG_LABEL_LOGGER_NAME, MAX_REQUEST_RESPONSE_SIZE, DEFAULT_LOG_LEVEL, \
        NIM_DJANGO_REQUEST_LOG_LEVEL_NAME

if hasattr(settings, LOG_LABEL_LOGGER_NAME):
    logger = logging.getLogger(getattr(settings, LOG_LABEL_LOGGER_NAME))
else:
    logger = logging.getLogger(__name__)


class HeaderToLabelMiddleware(object):
    """
    Provides full logging of requests and responses
    """
    _initial_http_body = None
    _request_start_time = None
    _TRUNCATE_INDICATOR = "---[TRUNCATED]---"

    def __init__(self, get_response=None):
        if not hasattr(settings, LOG_LABEL_REQUEST_SETTING):
            raise ImproperlyConfigured("Please set LOG_LABEL_REQUEST_SETTING, it is the dictionary of header names and values that need to be appended to the log")

        if not hasattr(settings, LOG_LABEL_LOGGER_NAME):
            logger.warning(f"No logger specified in LOG_LABEL_LOGGER_NAME '{__name__}' will be used instead")

        if not hasattr(settings, MAX_REQUEST_RESPONSE_SIZE):
            raise ImproperlyConfigured("Please set MAX_REQUEST_RESPONSE_SIZE, it is the value of the max length of the response")

        if not hasattr(settings, DEFAULT_LOG_LEVEL):
            raise ImproperlyConfigured("Please set DEFAULT_LOG_LEVEL, it is the value of the log level")

        if not hasattr(settings, NIM_DJANGO_REQUEST_LOG_LEVEL_NAME):
            raise ImproperlyConfigured("Please set NIM_DJANGO_REQUEST_LOG_LEVEL_NAME, it is the value of the header name containing the correlation id")

        self.get_response = get_response

    def __get_time_in_milliseconds(self):
        return int(round(time.time() * 1000))

    def _get_header(self, request, header_name):
        return request.META.get(header_name, DEFAULT_HEADER_VALUE)

    def process_request(self, request):
        self._initial_http_body = request.body
        self._request_start_time = self.__get_time_in_milliseconds()
        log_label_request_settings = getattr(settings, LOG_LABEL_REQUEST_SETTING, dict())
        for label, header_name in log_label_request_settings.items():
            header_value = self._get_header(request, header_name)
            setattr(local, label, header_value)
            setattr(request, label, header_value)

    def process_response(self, request, response):
        nim_headers = Utils.get_nim_headers(request)
        log_entry = dict(
            nim_headers=nim_headers,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=self.__get_time_in_milliseconds(),
            method=request.method,
            body=Utils.adjust_string_length(self._initial_http_body, getattr(settings, MAX_REQUEST_RESPONSE_SIZE)),
            status_code=response.status_code,
            response=Utils.adjust_string_length(response.content,
                                                settings.MAX_REQUEST_RESPONSE_SIZE) if response.status_code < 400 else response.content,
            tags=dict(
                url=request.build_absolute_uri()
            )
        )

        log_label_request_settings = getattr(settings, LOG_LABEL_REQUEST_SETTING, dict())
        for label in log_label_request_settings:
            log_entry[label] = getattr(request, label)

        if response.status_code < 400:
            logger.debug(
                '', **log_entry
            )
        else:
            logger.error(
                '', **log_entry
            )
        return response

    def process_exception(self, request, exception):
        nim_headers = Utils.get_nim_headers(request)
        log_entry = dict(
            nim_headers=nim_headers,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=self.__get_time_in_milliseconds(),
            method=request.method,
            body=Utils.adjust_string_length(self._initial_http_body, getattr(settings, MAX_REQUEST_RESPONSE_SIZE)),
            status_code=500,
            exception=str(exception),
            tags=dict(
                url=request.build_absolute_uri()
            ),
            stack_trace=traceback.format_exc()
        )

        log_label_request_settings = getattr(settings, LOG_LABEL_REQUEST_SETTING, dict())
        for label in log_label_request_settings:
            log_entry[label] = getattr(request, label)

        logger.error(
            '', **log_entry
        )
        return exception
