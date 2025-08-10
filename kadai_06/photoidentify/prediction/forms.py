# ライブラリのインポート
from django import forms

# 画像アップロードのフォームのクラスを定義
class ImageUploadForm(forms.Form):
    image = forms.ImageField()