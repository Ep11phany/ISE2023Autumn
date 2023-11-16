import numpy as np
import faiss
import os
import pickle
class MYFAISS(object):
    def __init__(self,
                 db_path: str,
                 matedate_path: str,
                 dim: int,
        ):
        self.db_path = db_path
        self.dim = dim
        self.matedata_path = matedate_path
        if os.path.exists(db_path):
            self.index = faiss.read_index(db_path) # 读取索引
        else:
            self.index = faiss.IndexFlatL2(dim)
        if os.path.exists(matedate_path):
            with open(matedate_path, 'rb') as f:
                self.matedatas = pickle.load(f)
        else:
            self.matedatas = {}

    def add_vectors(self, vectors, matedatas):
        try:
            vectors_np = np.array(vectors).astype('float32')
            faiss.normalize_L2(vectors_np)
            self.index.add(vectors_np)
            start_idx = self.index.ntotal - len(vectors)  # 新向量在索引中的起始位置
            for i, string in enumerate(matedatas):
                self.matedatas[start_idx + i] = string
            self.__save_db()
            return f"vectors add success"
        except Exception as e:
            print(e)
            return f"vectors add fail"
    
    def __save_db(self):
        faiss.write_index(self.index, self.db_path)
        with open('vector_to_string_mapping.pkl', 'wb') as f:
            pickle.dump(self.matedata_path, f)
    
    def similarity_search(self, vector, k):
        try:
            query = np.array(vector).astype('float32')
            faiss.normalize_L2(query)
            D, I = self.index.search(query, k)
            matedata_indexs = [i for i in I[0]]  # 最相似向量的索引
            return [self.matedatas[i] for i in matedata_indexs]
        except Exception as e:
            print(e)
            return f"search fail"