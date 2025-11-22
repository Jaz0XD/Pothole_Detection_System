from torchvision import transforms

def normalize_image(image):
    normalization = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    return normalization(image)

def resize_image(image, size=(640, 480)):
    resize = transforms.Resize(size)
    return resize(image)

def preprocess_image(image):
    image = resize_image(image)
    image = normalize_image(image)
    return image

def apply_transforms(image):
    return preprocess_image(image)