# ライブラリのインポート
from django.shortcuts import render
from .forms import ImageUploadForm
import random
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from io import BytesIO
import base64
import os

# モデルの読み込み
model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'vgg16.h5')
model = load_model(model_path)

# 予測する関数
# ニューラルネットワークのVGG16を利用する
def predict(request):
    if request.method == 'GET':
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            # Base64エンコード
            img_bytes = img_file.read()
            img_file_io = BytesIO(img_bytes)
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            img_data_url = f"data:image/jpeg;base64,{img_base64}"
            #　画像の前処理
            img = load_img(img_file_io, target_size=(224, 224)) # ←画像の読み込み
            img_array = img_to_array(img) # ←画像のarray配列化
            img_array = img_array.reshape((1, 224, 224, 3)) # ←画像の形式の変更
            img_array = preprocess_input(img_array)
            # 予測の実行
            result = model.predict(img_array)
            # 確率の高い順にソート
            result_top5 = decode_predictions(result, top=5)
            return render(request, 'home.html', {'form': form, 'prediction': result_top5[0], 'img_data': img_data_url,})
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})