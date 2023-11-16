from PIL import Image
from utils.vecstore import MYFAISS
from transformers import CLIPProcessor, CLIPModel

class Retriever(MYFAISS):
    def __init__(self, args):
        super().__init__(args.db_path, args.matedata_path, args.dim)
        self.model, self.processor = self.__build_model(args.model_name_or_path)

    def __build_model(self, model_name_or_path):
        model = CLIPModel.from_pretrained(model_name_or_path)
        processor = CLIPProcessor.from_pretrained(model_name_or_path)
        return model, processor

    def search(self, text, image, k=1):
        image_urls = []
        if not text is None:
            text_vec = self.__text2vec(text)
            image_urls += self.similarity_search(text_vec, k=k)
        if not image is None:
            image_vec = self.__image2vec(image)
            image_urls += self.similarity_search(image_vec, k=k)
        return image_urls

    def __text2vec(self, text):
        inputs = self.processor(text=text, return_tensors="pt")
        inputs = inputs.to(self.device)
        text_vec = self.model.get_text_features(**inputs)
        return text_vec


    def __image2vec(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = inputs.to(self.device)
        image_vec = self.model.get_image_features(**inputs)
        return image_vec

