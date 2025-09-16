from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()
#商品を追加するメソッドのテスト
class ProductModelTests(TestCase):
    def test_str_returns_name(self):
        p = Product.objects.create(name='テスト商品', description='説明', price=1000, stock=1)
        self.assertEqual(str(p), 'テスト商品')

class AuthAndViewTests(TestCase):
     # テスト用ユーザーといくつかの商品を作成するテスト
    def setUp(self):
        self.username = 'testuser'
        self.password = 'TestPass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        Product.objects.create(name='AAA', description='foo', price=100, stock=10)
        Product.objects.create(name='BBB', description='bar', price=200, stock=5)

    
    def test_signup_creates_user_and_redirects(self):
        # サインアップ用の POST リクエストを送って新規ユーザー作成を試みる
        resp = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        # 正常ならビューがリダイレクトを返す（ユーザー作成後の遷移を期待）
        self.assertIn(resp.status_code, (302, 303))
        # 実際に DB にユーザーが作成されていることを検証
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_works_and_redirects_to_index(self):
        resp = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        # ログイン成功で index にリダイレクト
        self.assertIn(resp.status_code, (302, 303))
        # セッションでログイン状態か確認
        resp2 = self.client.get(reverse('index'))
        self.assertNotIn(resp2.status_code, (302,))  # ログイン必須なら 302 にならないこと



    def test_index_search_returns_matching(self):
        # テスト用ユーザーでログイン（検索ページはログインが必要な想定）
        self.client.login(username=self.username, password=self.password)

        # 検索クエリ ?q=AAA を付けて index ビューへ GET リクエストを送る
        resp = self.client.get(reverse('index') + '?q=AAA')

        # レスポンスが正常（HTTP 200 OK）であることを確認
        self.assertEqual(resp.status_code, 200)

        # レスポンスの HTML に検索語に一致する商品名 'AAA' が含まれていることを検証
        self.assertContains(resp, 'AAA')
