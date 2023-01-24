import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np


np.set_printoptions(suppress=True)
model = load_model('data.h5', compile=False)
class_names = ["sunflower","rose","daisy","ladybug","seaotter"]
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def solve(img,q):
    image = Image.open(img).convert('RGB')
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data,verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index]
    # confidence_score = prediction[0][index]

    return True if class_name.replace('\n','') in q else False

if __name__ == '__main__':
    import time
    start = time.time()
    ans = [solve(f"./fotoz/{img}","each iamge with sunflower") for img in os.listdir('./fotoz')]
    print(f"{ans} solved {time.time()-start}s")
    print(os.listdir('./fotoz'))