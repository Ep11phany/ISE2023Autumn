from PIL import Image
from langchain.vectorstores import faiss as FAISS
from transformers import CLIPProcessor, CLIPModel

class Retriever(object):
    def __init__(self, args):
        self.model, self.processor = self.__build_model(args.model_name_or_path)
        self.db = self.__load_db(args.db_path, self.model, self.processor)

    def __build_model(self, model_name_or_path):
        model = CLIPModel.from_pretrained(model_name_or_path)
        processor = CLIPProcessor.from_pretrained(model_name_or_path)
        return model, processor

    def __load_db(self, db_path, model, processor):
        pass
        #return FAISS.load_local(db_path, model, processor)

    def search(self, text, image, k=1):
        if not text is None:
            text_vec = self.__text2vec(text)
        if not image is None:
            image_vec = self.__image2vec(image)
        # vec = self.model.encode(text)
        # image_url = self.db.similarity_search_with_score(vec, k=k)
        #return image_url

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

