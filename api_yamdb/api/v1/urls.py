from rest_framework.routers import SimpleRouter
from api import views

router = SimpleRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('titles', views.TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    views.CommentViewSet,
    basename='comments'
)