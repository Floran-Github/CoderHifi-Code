from django.contrib import admin
from .models import *
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models
# Register your models here.

class AdminPublicChatroom(admin.ModelAdmin):
    list_display = ['id','room_name']
    search_fields = ['id','room_name']
    readonly_fields = ['id',]

    class Meta:
        model = PublicChatRoom

admin.site.register(PublicChatRoom, AdminPublicChatroom)

class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

class PublicRoomChatMessageAdmin(admin.ModelAdmin):
    list_filter = ['room',  'user', "time"]
    list_display = ['room',  'user', 'content',"time"]
    search_fields = ['room__title', 'user__username','content']
    readonly_fields = ['id', "user", "room", "time"]

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = PublicChatMsg


admin.site.register(PublicChatMsg, PublicRoomChatMessageAdmin)
admin.site.register(Message)
admin.site.register(Chat)