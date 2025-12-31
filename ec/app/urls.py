from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import  views as auth_views
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(),name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(),name="category-title"),
    path("product-details/<int:pk>", views.ProductDetails.as_view(),name="product-details"),
    path("profile/", views.ProfileView.as_view(),name="profile"),
    path("address/", views.address,name="address"),
    path("updateddress/<int:pk>",views.UpdateAddress.as_view(), name="updateaddress"),


    path("add-to-cart/",views.add_to_cart,name="add-to-cart"),
    path("cart/",views.show_cart,name="showcart"),
    path("checkout/",views.checkout.as_view(),name="checkout"),
    path("paymentdone/",views.payment_done,name="paymentdone"),
    path("orders/",views.orders, name="orders"),

    path("pluscart/",views.plus_cart),
    path("minuscart/",views.minus_cart),
    path("removecart/",views.remove_cart),
    path("wishlist/",views.show_wishlist,name="show_wishlist"),
    path("wishlist/add/", views.add_wishlist, name="add_wishlist"),
    path("wishlist/remove/", views.remove_wishlist, name="remove_wishlist"),
    path("search/",views.search, name="search"),

    #login authentication
    path("registration/", views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path("account/login/",auth_views.LoginView.as_view(template_name="app/login.html",authentication_form=LoginForm),name="login"),
    path("passwordchange/",auth_views.PasswordChangeView.as_view(template_name="app/changepassword.html",form_class=MyPasswordChangeForm, success_url="/passwordchangedone"), name="passwordchange"),
    path("passwordchangedone/",auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"), name="passwordchangedone"),
    path("logout/",views.CustomLogoutView.as_view(next_page="login"), name="logout"),
   

    #related to password
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name="app/password_reset.html",form_class=MyPasswordResetForm),name="password_reset"),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"),name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html",form_class=MySetPasswordForm),name="password_reset_confirm"),
    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"),name="password_reset_complete"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header = "K2K Product"
admin.site.site_title = "K2K Product"
admin.site.site_index_title = "welcome to K2K Product shop"