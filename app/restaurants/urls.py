from django.urls import path
from . import views

urlpatterns = [
    path ("",views.index, name="restaurants"),
    path ("<int:restaurant_id>",views.restaurant,name="restaurant"),
    path ("search",views.search,name="search"),
    path ("<int:restaurant_id>/add-comment",views.add_comment,name="add-comment"),
    path ("<int:restaurant_id>/delete-comment",views.delete_comment,name="delete-comment"),
    path ("edit-comment/<int:comment_id>",views.edit_comment,name="edit-comment"),
]