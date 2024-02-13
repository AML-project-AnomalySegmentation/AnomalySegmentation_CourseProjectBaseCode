# Code with dataset loader for VOC12 and Cityscapes (adapted from bodokaiser/piwise code)
# Sept 2017
# Eduardo Romera
#######################

import numpy as np
import os
import torch

from PIL import Image

from torch.utils.data import Dataset

EXTENSIONS = ['.jpg', '.png']

def load_image(file):
    return Image.open(file)

def is_image(filename):
    return any(filename.endswith(ext) for ext in EXTENSIONS)

def is_label(filename):
    return filename.endswith("_labelTrainIds.png")

def image_path(root, basename, extension):
    return os.path.join(root, f'{basename}{extension}')

def image_path_city(root, name):
    return os.path.join(root, f'{name}')

def image_basename(filename):
    return os.path.basename(os.path.splitext(filename)[0])

class VOC12(Dataset):

    def __init__(self, root, input_transform=None, target_transform=None):
        self.images_root = os.path.join(root, 'images/')
        self.labels_root = os.path.join(root, 'labels_masks/')

        self.filenames = [image_basename(f)
            for f in os.listdir(self.labels_root) if is_image(f)]
        self.filenames.sort()

        self.input_transform = input_transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        filename = self.filenames[index]
        image = image_path(self.images_root, filename, '.png')
        #print(image)
        #with open(image_path(self.images_root, filename, '.png'), 'rb') as f:
        #    image = load_image(f).convert('RGB')
        #    print(image)
        #with open(image_path(self.labels_root, filename, '.png'), 'rb') as f:
        #    label = load_image(f).convert('P')
        label =image_path(self.labels_root, filename, '.png')
        if self.input_transform is not None:
            image = self.input_transform(image)
        if self.target_transform is not None:
            label = self.target_transform(label)
        #print(label)
        return image, label

    def __len__(self):
        return len(self.filenames)


class cityscapes(Dataset):

    def __init__(self, root, input_transform=None, target_transform=None, subset='val'):

        self.images_root = os.path.join(root, 'leftImg8bit/' + subset)
        self.labels_root = os.path.join(root, 'gtFine/' + subset)
        print(self.images_root, self.labels_root)
        self.filenames = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.images_root)) for f in fn if is_image(f)]
        self.filenames.sort()

        self.filenamesGt = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.labels_root)) for f in fn if is_label(f)]
        
        self.filenamesGt.sort()

        self.input_transform = input_transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        
        filename = self.filenames[index]
        filenameGt = self.filenamesGt[index]

        #print(filename)

        with open(image_path_city('', filename), 'rb') as f:
            image = load_image(f).convert('RGB')
        with open(image_path_city('', filenameGt), 'rb') as f:
            label = load_image(f).convert('P')

        if self.input_transform is not None:
            image = self.input_transform(image)
        if self.target_transform is not None:
            label = self.target_transform(label)

        return image, label, filename, filenameGt

    def __len__(self):
        return len(self.filenames)

class ValidationDataset(Dataset):

    def __init__(self, root, input_transform=None, target_transform=None):

        self.images_root = os.path.join(root, 'images/')
        self.labels_root = os.path.join(root, 'label_marks/')
        print(self.images_root, self.labels_root)
        self.filenames = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.images_root)) for f in fn if is_image(f)]
        self.filenames.sort()

        self.filenamesGt = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.labels_root)) for f in fn if is_label(f)]
        
        self.filenamesGt.sort()

        self.input_transform = input_transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        
        filename = self.filenames[index]
        filenameGt = self.filenamesGt[index]

        #print(filename)

        with open(image_path_city('', filename), 'rb') as f:
            image = load_image(f).convert('RGB')
        with open(image_path_city('', filenameGt), 'rb') as f:
            label = load_image(f).convert('P')

        if self.input_transform is not None:
            image = self.input_transform(image)
        if self.target_transform is not None:
            label = self.target_transform(label)

        return image, label, filename, filenameGt

    def __len__(self):
        return len(self.filenames)

class cityscapesTemperature(Dataset):

    def __init__(self, root, input_transform=None, target_transform=None, subset='val'):

        self.images_root = os.path.join(root, 'leftImg8bit/' + subset)
        self.labels_root = os.path.join(root, 'gtFine/' + subset)
        print("ROOT: " + root)
        print("IMAGES: " + self.images_root)
        print("LABELS: " + self.labels_root)
        print(self.images_root, self.labels_root)
        self.filenames = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.images_root)) for f in fn if is_image(f)]
        self.filenames.sort()

        self.filenamesGt = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.labels_root)) for f in fn if is_label(f)]
        self.filenamesGt.sort()

        self.input_transform = input_transform
        self.target_transform = target_transform

    def __getitem__(self, index):

        filename = self.filenames[index]
        filenameGt = self.filenamesGt[index]

        with open(image_path_city("", filename), 'rb') as f:
            image = load_image(f).convert('RGB')
        with open(image_path_city("", filenameGt), 'rb') as f:
            label = load_image(f).convert('P')

        if self.input_transform is not None:
            image = self.input_transform(image)
        if self.target_transform is not None:
            label = self.target_transform(label)

        # Converti l'etichetta in un array numpy
        label_np = np.array(label)

        # Assicurati che l'etichetta sia bidimensionale
        if len(label_np.shape) > 2:
            # Riduci la dimensione dell'etichetta a 2 dimensioni
            label_np = label_np.squeeze()

        # Converti l'etichetta in un tensore PyTorch
        label = torch.from_numpy(label_np)

        return image, label



    def __len__(self):
        return len(self.filenames)
