import logging
from django.db.models import Q
from ..models import Bucket, TodoItem
from ..utils.exceptions import CustomException

class DatabaseController:   

    logger = logging.getLogger(__name__)

    # Buckets
    def get_buckets(self):
        try:
            ERROR_CODE = 'DATABASE_READ_ERROR'
            all_buckets = Bucket.objects.filter(is_deleted=False).order_by('-updated_at')
            self.logger.info('Buckets retrieved from DB')
            return all_buckets
        except Exception:
            raise CustomException(ERROR_CODE)

    def create_bucket(self, name):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            bucket_obj = Bucket.objects.filter(name=name)
            if len(bucket_obj) > 0:
                ERROR_CODE = 'BUCKET_NAME_EXIST'
                raise Exception    
            bucket = Bucket(name=name)
            bucket.save()
            self.logger.info('Bucket created in DB')
            return bucket
        except Exception:
            raise CustomException(ERROR_CODE)

    def create_bucket_from_existing(self, name, copy_from):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            copy_from_bucket_obj = Bucket.objects.filter(Q(uuid=copy_from) & Q(is_deleted=False))
            self.logger.info('Copy from bucket details retrieved from DB')
            
            if len(copy_from_bucket_obj) < 1:
                ERROR_CODE = 'INVALID_BUCKET_ID'
                raise Exception 
            if name == copy_from_bucket_obj[0].name:
                ERROR_CODE = 'BUCKET_NAME_EXIST'
                raise Exception 

            bucket = Bucket(name=name)
            bucket.save()
            self.logger.info('New Bucket created in DB')
            
            new_bucket_obj = Bucket.objects.filter(Q(name=name) & Q(is_deleted=False))
            self.logger.info('New Bucket details retrieved from DB')
            
            todo_items_objs = TodoItem.objects.filter(Q(bucket=copy_from_bucket_obj[0]) & Q(is_deleted=False))
            self.logger.info('Copy from Bucket TodoItems retrieved from DB')
            
            # preparing list of todoitems to insert for new bucket
            todo_items = []
            for todo_item_obj in todo_items_objs:
                todo_items.append(TodoItem(**{
                    'bucket': new_bucket_obj[0],
                    'title': todo_item_obj.title,
                    'body': todo_item_obj.body
                    }))
            if len(todo_items) > 0:
                TodoItem.objects.bulk_create(todo_items)
                self.logger.info('TodoItems added to new Bucket in DB')

            return new_bucket_obj[0]

        except Exception:
            raise CustomException(ERROR_CODE)

    def rename_bucket(self, bucket_uuid, new_name):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            bucket_obj = Bucket.objects.filter(Q(name=new_name) & Q(is_deleted=False))
            if len(bucket_obj) > 0:
                ERROR_CODE = 'BUCKET_NAME_EXIST'
                raise Exception
            bucket_obj = Bucket.objects.filter(Q(uuid=bucket_uuid) & Q(is_deleted=False))
            if len(bucket_obj) < 1:
                ERROR_CODE = 'INVALID_BUCKET_ID'
                raise Exception 
                
            bucket_obj[0].name = new_name
            bucket_obj[0].save()
            self.logger.info('Bucket name updated in DB')
        except Exception:
            raise CustomException(ERROR_CODE)

    def delete_bucket(self, bucket_uuid):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            bucket_obj = Bucket.objects.filter(Q(uuid=bucket_uuid) & Q(is_deleted=False))
            if len(bucket_obj) < 1:
                ERROR_CODE = 'INVALID_BUCKET_ID'
                raise Exception
            bucket_obj[0].is_deleted = True
            bucket_obj[0].save()
            self.logger.info('Bucket delete flag updated in DB')
        except Exception:
            raise CustomException(ERROR_CODE)
        
    # TodoItems
    def get_todo_items(self, bucket_uuid):
        try:
            ERROR_CODE = 'DATABASE_READ_ERROR'
            bucket_obj = Bucket.objects.filter(Q(uuid=bucket_uuid) & Q(is_deleted=False))
            self.logger.info('Bucket retrieved from DB')
            if len(bucket_obj) < 0:
                ERROR_CODE = 'INVALID_BUCKET_ID'
                raise Exception    
            all_todo_items = TodoItem.objects.filter(Q(bucket=bucket_obj[0]) & Q(is_deleted=False)).order_by('-updated_at')
            self.logger.info('TodoItems retrieved from DB')
            return all_todo_items
        except Exception:
            raise CustomException(ERROR_CODE)

    def add_todo_item(self, data):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            bucket_obj = Bucket.objects.filter(Q(uuid=data.get('bucket_uuid')) & Q(is_deleted=False))
            self.logger.info('New Bucket details retrieved from DB')
            if len(bucket_obj) < 1:
                ERROR_CODE = 'INVALID_BUCKET_ID'
                raise Exception    
            todo_item = TodoItem(bucket=bucket_obj[0], title=data.get('title'), body=data.get('body'))
            todo_item.save()
            self.logger.info('TodoItem added in DB')
            return todo_item
        except Exception:
            raise CustomException(ERROR_CODE)
    
    def update_todo_item(self, todo_item_uuid, title, body, is_completed):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            todo_item_obj = TodoItem.objects.filter(Q(uuid=todo_item_uuid) & Q(is_deleted=False))
            if len(todo_item_obj) < 1:
                ERROR_CODE = 'INVALID_TODO_ITEM_ID'
                raise Exception    
            todo_item_obj[0].title = title
            todo_item_obj[0].body = body
            todo_item_obj[0].is_completed = is_completed
            todo_item_obj[0].save()
            self.logger.info('TodoItem updated in DB')
        except Exception:
            raise CustomException(ERROR_CODE)
    
    def delete_todo_item(self, todo_item_uuid):
        try:
            ERROR_CODE = 'DATABASE_WRITE_ERROR'
            todo_item_obj = TodoItem.objects.filter(Q(uuid=todo_item_uuid) & Q(is_deleted=False))
            if len(todo_item_obj) < 1:
                ERROR_CODE = 'INVALID_TODO_ITEM_ID'
                raise Exception    
            todo_item_obj[0].is_deleted = True
            todo_item_obj[0].save()
            self.logger.info('TodoItem delete flag updated in DB')
        except Exception:
            raise CustomException(ERROR_CODE)
    