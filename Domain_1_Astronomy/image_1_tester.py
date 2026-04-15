from Domain_1_Astronomy.image_module.preprocessing import ImagePreprocessor
from Domain_1_Astronomy.image_module.ml.backbone import BackboneFeatureExtractor

image_url = "https://apod.nasa.gov/apod/image/2602/Wierzchos_Chabo_1080.jpg"

pre = ImagePreprocessor()
image, tensor = pre.process(image_url)

backbone = BackboneFeatureExtractor()
features = backbone.extract_features(tensor)

print("Feature vector shape:", features.shape)
""" Common Tester for backbone.py and preprocessing.py"""