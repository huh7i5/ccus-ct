
import os
from paddlenlp import Taskflow

class Ner:
    def __init__(self):
        # 使用绝对路径确保模型可以正确加载
        current_dir = os.path.dirname(os.path.abspath(__file__))
        server_dir = os.path.dirname(os.path.dirname(current_dir))
        model_path = os.path.join(server_dir, "weights", "model_41_100")
        self.model = Taskflow("ner", task_path=model_path)

    def predict(self, text):
        return self.model(text)

    def get_entities(self, text, etypes=None):
        '''获取句子中指定类型的实体

        Args:
            text: 句子
            etype: 实体类型
        Returns:
            entities: 实体列表
        '''
        if etypes is None:
            etypes = [None]

        entities = []
        for etype in etypes:
            for ent, et in self.predict(text):
                if not etype or etype in et:
                    entities.append(ent)
        return entities