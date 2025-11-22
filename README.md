# Foodsaver (Django 食材管理アプリ)

Django を使って食材の登録・検索・期限管理・月次分析を行う Web アプリです。  
ログインユーザーごとにデータを管理し、カテゴリ別の支出分析（円グラフ表示）にも対応しています。

## 構成
- Web Framework: **Django 5**
- DB: **SQLite3**（デフォルト）
- 認証: **Django Auth（ログイン必須）**
- グラフ生成: **matplotlib**
- 日本語フォント: **NotoSansCJKjp-Regular.otf**

---

## 1. プロジェクトセットアップ

```bash
# プロジェクトフォルダへ移動
cd ~/Java_practice/foodsaver_project

# 仮想環境作成
python3 -m venv venv

# 仮想環境を有効化 (WSL/Linux/Mac)
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 依存ライブラリインストール
pip install -r requirements.txt

# データベース初期化
python manage.py migrate

# ログインユーザー作成(ここで設定するUsernameとPasswordはログインする際に必要になります)
# メールアドレスは架空のもので構いません(dummy@outlook.jp など)
python manage.py createsuperuser

# 開発サーバー起動
python manage.py runserver

# 下記のブラウザにアクセスしてください
http://127.0.0.1:8000 