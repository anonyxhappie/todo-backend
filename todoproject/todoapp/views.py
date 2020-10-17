import sys
import logging
import traceback
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BucketSerializer, TodoItemSerializer
from .utils.utilities import Utilities as Util
from .utils.constants import Constants as Const
from .utils.exceptions import CustomException
from .services.db_service import DatabaseController

"""
    With assumption that API request authorization is checked on API Gateway
    Can validate for permissions if receiving in request header 
"""
class BucketView(APIView):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.dbc = DatabaseController()

    def get(self, request, uuid=None):
        try:
            result = []
            if uuid:
                self.logger.info('Get TodoItems request received')
                SUCCESS_MESSAGE = 'TodoItems retrieved successfully'
                todo_items_objs = self.dbc.get_todo_items(uuid)
                serializer = TodoItemSerializer(todo_items_objs, many=True)
            else:
                self.logger.info('Get Buckets request received')
                SUCCESS_MESSAGE = 'Buckets retrieved successfully'
                buckets_objs = self.dbc.get_buckets()
                serializer = BucketSerializer(buckets_objs, many=True)
            result = serializer.data
            self.logger.info(SUCCESS_MESSAGE)
            return Response({
                Const.STATUS: status.HTTP_200_OK,
                Const.MESSAGE: SUCCESS_MESSAGE,
                Const.RESULT: result
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })

    def post(self, request):
        try:
            self.logger.info('Bucket create request received')
            SUCCESS_MESSAGE = 'Bucket created successfully'
            result = {}
            request_data = request.data
            serializer = BucketSerializer(data=request_data)
            if (serializer.is_valid()):
                bucket = None
                if (request_data.get('copy_from', False)):
                    bucket = self.dbc.create_bucket_from_existing(request_data.get('name', 'untitled'), request_data.get('copy_from'))
                else:
                    bucket = self.dbc.create_bucket(request_data.get('name', 'untitled'))
                serializer = BucketSerializer(bucket)
                result = serializer.data
                self.logger.info(SUCCESS_MESSAGE)
            else:
                raise CustomException('INVALID_REQUEST')
            return Response({
                Const.STATUS: status.HTTP_201_CREATED,
                Const.MESSAGE: SUCCESS_MESSAGE,
                Const.RESULT: result
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })

    def put(self, request, uuid):
        try:
            self.logger.info('Bucket rename request received')
            SUCCESS_MESSAGE = 'Bucket renamed successfully'
            request_data = request.data
            serializer = BucketSerializer(data=request_data)
            if (serializer.is_valid()):
                self.dbc.rename_bucket(uuid, request_data.get('name', 'untitled'))
                self.logger.info(SUCCESS_MESSAGE)
            else:
                raise CustomException('INVALID_REQUEST')
            return Response({
                Const.STATUS: status.HTTP_204_NO_CONTENT,
                Const.MESSAGE: SUCCESS_MESSAGE
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })

    def delete(self, request, uuid):
        try:
            self.logger.info('Bucket delete request received')
            SUCCESS_MESSAGE = 'Bucket deleted successfully'
            self.dbc.delete_bucket(uuid)
            self.logger.info(SUCCESS_MESSAGE)
            return Response({
                Const.STATUS: status.HTTP_204_NO_CONTENT,
                Const.MESSAGE: SUCCESS_MESSAGE
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })


class TodoItemView(APIView):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.dbc = DatabaseController()

    def post(self, request):
        try:
            self.logger.info('TodoItem add request received')
            SUCCESS_MESSAGE = 'TodoItem added successfully'
            result = {}
            request_data = request.data
            serializer = TodoItemSerializer(data=request_data)
            if (serializer.is_valid()):
                todo_item = self.dbc.add_todo_item(request_data)
                serializer = TodoItemSerializer(todo_item)
                result = serializer.data
                self.logger.info(SUCCESS_MESSAGE)
            else:
                raise CustomException('INVALID_REQUEST')
            return Response({
                Const.STATUS: status.HTTP_201_CREATED,
                Const.MESSAGE: SUCCESS_MESSAGE,
                Const.RESULT: result
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })

    def put(self, request, uuid):
        try:
            self.logger.info('TodoItem update request received')
            SUCCESS_MESSAGE = 'TodoItem updated successfully'
            request_data = request.data
            serializer = TodoItemSerializer(data=request_data)
            if (serializer.is_valid()):
                self.dbc.update_todo_item(uuid, request_data.get('title'), request_data.get('body'), request_data.get('is_completed'))
                self.logger.info(SUCCESS_MESSAGE)
            else:
                raise CustomException('INVALID_REQUEST')
            return Response({
                Const.STATUS: status.HTTP_204_NO_CONTENT,
                Const.MESSAGE: SUCCESS_MESSAGE
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })

    def delete(self, request, uuid):
        try:
            self.logger.info('TodoItem delete request received')
            SUCCESS_MESSAGE = 'TodoItem deleted successfully'
            self.dbc.delete_todo_item(uuid)
            self.logger.info(SUCCESS_MESSAGE)
            return Response({
                Const.STATUS: status.HTTP_204_NO_CONTENT,
                Const.MESSAGE: SUCCESS_MESSAGE
            })
        except CustomException as e:
            traceback.print_exc()
            return Response({
                Const.STATUS: e.error_code,
                Const.MESSAGE: e.error_message
            })
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('Internal Server Error')
            return Response({
                Const.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR,
                Const.MESSAGE: 'Something went wrong. Please contact support team.'
            })
