from django.urls import re_path
from core.Views.CursorView import CursorView, CursorChatListing

urlpatterns = [
    re_path(r'^chat/listing/$', CursorChatListing.as_view(), name='chat_listing'),
    re_path(r'^chat/(?P<chat_id>[\w\-]+)/$', CursorView.as_view(), name='chat_detail'),
]