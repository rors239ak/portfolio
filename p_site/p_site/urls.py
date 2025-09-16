"""
URL configuration for p_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),# 管理ページ
    path('EC/', include('EC.urls')),  # ECアプリのURL
    path("accounts/login/",auth_views.LoginView.as_view(template_name="EC/login.html"),name="login",), # ログイン機能
    # 明示的に logout を追加（next_page に名前 or URL）
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    # Django の認証用 URL (login/logout/password 等) を一括追加
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    # 開発サーバ(runserver)で /media/ 以下のURLをローカルの MEDIA_ROOT から配信する設定。
    # DEBUG=True のときだけ有効。 本番では nginx 等の静的サーバで配信するのでここは無効にすること。
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

