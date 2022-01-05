print("\nLoading Library..")
import os
from numpy import expand_dims, argmax
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from PIL import Image
from cv2 import cvtColor, resize, COLOR_BGR2GRAY, INTER_AREA
print("\nLibrary Loaded successfully")

class MNISTModel():
    def __init__(self, model_path):
        self.model = self.load_mnist_model(model_path)

    def img_preprocess(self, image):
        try:
            img =  Image.open(image)
            img = img_to_array(img)
            dim = (28,28)
            img = cvtColor(img, COLOR_BGR2GRAY)
            img = resize(img, dim, interpolation=INTER_AREA)
            img = expand_dims(img, axis=2)
            img = expand_dims(img, axis=0)
            return img

        except Exception as e:
            print(f"[ERROR] {e}")

    def load_mnist_model(self, model_path):
        try:
            print("\nmodel Loading.....")
            model = load_model(model_path)
            print("\nmodel Loaded successfully")
            return model

        except Exception as e:
            print(f"[ERROR] {e}")

    def predict(self, img):
        print("\nPredicting...")
        img = self.img_preprocess(img)
        predictions = argmax(self.model.predict(img))
        print(f"\nclassified as {predictions}")
        return predictions

if __name__ == "__main__":
    img_path = os.path.join("img", "2.png")
    model_path = os.path.join("model", "mnist_cnn_model.h5")

    mnist = MNISTModel(model_path)
    mnist.predict(img_path)





