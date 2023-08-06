import six

from django.contrib.contenttypes.models import ContentType

from django_comments_tree.views.moderation import perform_flag
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from django_comments_tree.views import comments as views
from django_comments_tree.api import serializers
from django_comments_tree.conf import settings
from django_comments_tree.models import TreeComment, TreeCommentFlag
from django_comments_tree.permissions import IsOwner, IsModerator


class CommentCreate(generics.CreateAPIView):
    """Create a comment."""
    serializer_class = serializers.WriteCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response = super().post(request, *args, **kwargs)
        else:
            return Response([k for k in six.iterkeys(serializer.errors)],
                            status=400)
        if self.resp_dict['code'] == 201:  # The comment has been created.
            return response
        elif self.resp_dict['code'] in [202, 204, 403]:
            return Response(status=self.resp_dict['code'])

    def perform_create(self, serializer):
        self.resp_dict = serializer.save()


class CommentList(generics.ListAPIView):
    """List all comments for a given ContentType and object ID."""
    serializer_class = serializers.ReadCommentSerializer

    def get_queryset(self):
        content_type_arg = self.kwargs.get('content_type', None)
        object_id_arg = self.kwargs.get('object_id', None)
        app_label, model = content_type_arg.split("-")
        try:
            content_type = ContentType.objects.get_by_natural_key(app_label,
                                                                  model)
        except ContentType.DoesNotExist:
            qs = TreeComment.objects.none()
        else:
            qs = TreeComment.objects.filter(content_type=content_type,
                                            object_id=object_id_arg,
                                            site__pk=settings.SITE_ID,
                                            is_public=True)
        return qs


class CommentCount(generics.GenericAPIView):
    """Get number of comments posted to a given ContentType and object ID."""
    serializer_class = serializers.ReadCommentSerializer

    def get_queryset(self):
        content_type_arg = self.kwargs.get('content_type', None)
        object_id_arg = self.kwargs.get('object_id', None)
        app_label, model = content_type_arg.split("-")
        content_type = ContentType.objects.get_by_natural_key(app_label, model)
        qs = TreeComment.objects.filter(content_type=content_type,
                                        object_id=object_id_arg,
                                        is_public=True)
        return qs

    def get(self, request, *args, **kwargs):
        return Response({'count': self.get_queryset().count()})


class ToggleFeedbackFlag(generics.CreateAPIView, mixins.DestroyModelMixin):
    """Create and delete like/dislike flags."""

    serializer_class = serializers.FlagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.created:
            return response
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        f = getattr(views, 'perform_%s' % self.request.data['flag'])
        self.created = f(self.request, serializer.validated_data['comment'])


class CreateReportFlag(generics.CreateAPIView):
    """Create 'removal suggestion' flags."""

    serializer_class = serializers.FlagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        perform_flag(self.request, serializer.validated_data['comment'])


class RemoveReportFlag(generics.DestroyAPIView):
    queryset = TreeCommentFlag.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsModerator,)
