import torch
import os
from PIL import Image
from torchvision.models.detection import maskrcnn_resnet50_fpn

def load_img(path): # load images from a folder, which is the input of the model
    img_list = []
    for f in os.listdir(path):
        if f.endswith(".jpg"):
            img = Image.open(os.path.join(path, f))
            img_list.append(img)
    return img_list

def main():
    model = maskrcnn_resnet50_fpn(pretrained=True) # load pretrained model from torchvision
    model.eval()
    img = load_img("img_datafolder")
    predictions = model(img) # get predictions from the model
    print(predictions)

if __name__ == "__main__":
    main()