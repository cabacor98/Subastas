# auctions/urls.py
from django.urls import path
from .views import RegisterUser, OperationListCreate, BidCreate,index, operation_list, bid_list,CustomAuthToken, login_page, OperationDetail


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('login-page/', login_page, name='login_page'),
    path('operations/', OperationListCreate.as_view(), name='operation-list-create'),
    path('operations/<int:pk>/', OperationDetail.as_view(), name='operation-detail'),
    path('bids/', BidCreate.as_view(), name='bid-create'),
    path('', index, name='index'),
    path('operations/open/', operation_list, name='operation-list'),
    path('operations/<int:operation_id>/bids/', bid_list, name='bid-list'),
]
