from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as __


class BaseQuerySet(models.QuerySet):
    def delete(self):
        for object in self.all():
            object.delete()


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db).filter(deleted=False)

    def all_with_deleted(self):
        return super(BaseManager, self).get_queryset()

    def get_one_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)

        except ObjectDoesNotExist:
            return None
    

class Auditable(models.Model):
    
    class Meta:
        abstract = True
        default_permissions = ("add", "change", "delete", "view", "view_all")

    objects = BaseManager()
    deleted = models.BooleanField(null=False, default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    deleted_on = models.DateTimeField(default=None, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name="%(class)s_createdby")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name="%(class)s_modifiedby")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name="%(class)s_deletedby")

    def delete(self, **kwargs):
        self.deleted = True
        self.deleted_on = timezone.now()
        self.save()

    def permanent_delete(self, **kwargs):
        super().delete(**kwargs)


class BaseModel(Auditable):

    class Meta(Auditable.Meta):
        abstract = True




        






    

