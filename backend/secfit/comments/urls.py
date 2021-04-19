from django.urls import path, include
from backend.secfit.comments.models import Comment, Like
from backend.secfit.comments.views import CommentList, CommentDetail, LikeList, LikeDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/comments/", CommentList.as_view(), name="comment-list"),
    path("api/comments/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
    path("api/likes/", LikeList.as_view(), name="like-list"),
    path("api/likes/<int:pk>/", LikeDetail.as_view(), name="like-detail"),
]
