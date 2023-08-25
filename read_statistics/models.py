from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core import exceptions
from django.utils import timezone


class ReadNum(models.Model):
    read_num = models.IntegerField(verbose_name='阅读数', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod:
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.id)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0
        

class ReadDetail(models.Model):
    '''
        记录更加详细的信息，比如某一天的阅读量
    '''
    date = models.DateField(verbose_name='日期时间', default=timezone.now)
    read_num = models.IntegerField(verbose_name='阅读数', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')