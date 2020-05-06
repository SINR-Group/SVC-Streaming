# modified from https://github.com/desimone/vision/blob/fb74c76d09bcc2594159613d5bdadd7d4697bb11/torchvision/datasets/folder.py

import os
import os.path

import torch
from torchvision import transforms
import torch.utils.data as data
from PIL import Image

IMG_EXTENSIONS = [
    '.jpg',
    '.JPG',
    '.jpeg',
    '.JPEG',
    '.png',
    '.PNG',
    '.ppm',
    '.PPM',
    '.bmp',
    '.BMP',
]


def is_image_file(filename):
    """
    checks if image as an appropriate extension
    """
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def default_loader(path):
    """
    loads image and converts to rgb format
    """
    return Image.open(path).convert('RGB')


class ImageFolder(data.Dataset):
    """ 
    ImageFolder can be used to load images where there are no labels.
    """

    def __init__(self, root, transform=None, loader=default_loader, heirarchy_flag=False):
        images = []
        for filename in os.listdir(root):
            # check if image exists
            if is_image_file(filename):

                img_idx = int(filename[-4].split('_')[-1])

                if ((img_idx % 12) == 1) or (not heirarchy_flag):
                    images.append('{}'.format(filename))

        self.heirarchy_flag = heirarchy_flag
        self.root = root
        self.imgs = images
        self.transform = transform
        self.loader = loader

    def __getitem__(self, index):
        filename = self.imgs[index]
        try:
            img = self.loader(os.path.join(self.root, filename))
        except:
            return torch.zeros((3, 32, 32))

        if self.transform is not None:
            img = self.transform(img)
        return img

    def __len__(self):
        return len(self.imgs)
