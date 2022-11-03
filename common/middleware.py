from functools import partial as pt
from django.db.models import signals
from django.utils.deprecation import MiddlewareMixin


class UpdateFieldMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.method in ("GET", "HEAD", "OPTIONS", "TRACE"):
            if hasattr(request, "user") and request.user.is_authenticated:
                user = request.user

            else:
                user = None

            who_updated = pt(self.who_update, user)
            signals.pre_save.connect(who_updated, dispatch_uid=(self.__class__, request), weak=False)
    
    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request))
        return response

    def who_update(self, user, sender, instance, **kwargs):
        for i in instance._meta.fields:
            if i.name == "created_by" and not instance.created_on:
                instance.created_by = user
            if i.name == "modified_by" and instance.created_on:
                instance.modified_by = user
            if i.name == "deleted_by" and instance.deleted_on is not None:
                instance.deleted_by = user
            if i.name == "deleted_by" and not instance.deleted_on:
                instance.deleted_by = None
