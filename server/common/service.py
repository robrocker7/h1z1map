import json
import logging
import traceback
import datetime
import time

from django.utils import timezone
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError
)


class ServiceError(Exception):

    def __init__(self, message=None, **kwargs):
        self.code = -1
        self.http_response = HttpResponseServerError
        super(ServiceError, self).__init__(message)


class InvalidParameterError(ServiceError):
    """ Not all parameters have been met
    """
    def __init__(self, message=None, **kwargs):
        super(InvalidParameterError, self).__init__(message, **kwargs)
        self.code = 1
        self.http_response_class = HttpResponseBadRequest

        
class api_wrapper(object):

    def __call__(self, service_method, **kwargs):
        
        def BUG_RESPONSE(err=None):
            return {
                'success': False,
                'error': -1,
                'message': err.message if err else None
            }


        def wrapped_f(request, *args, **kwargs):
            try:
                
                result = service_method(request, *args, **kwargs)
                if type(result) is list and len(result) == 0:
                    result = []
                elif type(result) is dict and len(result) == 0:
                    result = {}
                elif not result:
                    result = {}

                response_obj = {
                    'success': True,
                    'result': result,
                }
                response_class = HttpResponse

            except ServiceError as e:
                response_obj = {
                    'success': False,
                    'error': e.code,
                    'message': e.message,
                }
                response_class = e.http_response_class

            except Exception as e:
                # something we did not account for
                logging.error(u"API BUG: {0}".format(e))
                logging.error(traceback.format_exc(e))
                response_obj = BUG_RESPONSE(e)
                response_class = HttpResponseServerError

                response_obj = {
                    'success': False,
                    'error': -1,
                    'message': e.message,
                }

            try:
                response_str = json.dumps(response_obj)
            except Exception as e:
                logging.error(u"BUG: error serializing JSON response: {0}".format(e))
                logging.error(traceback.format_exc(e))
                logging.error(response_obj)
                response_obj = BUG_RESPONSE(e)
                response_class = HttpResponseServerError
                response_str = json.dumps(response_obj)

            ret = response_class(response_str, 'application/json')
            return ret

        return wrapped_f
