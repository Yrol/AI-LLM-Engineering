import torch
from transformers import pipeline

class HuggingFacePipelineService:
    
    def __init__(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"       
    
    def named_entity_analysis(self, prompt:str):
        ner = pipeline("ner", grouped_entities=True, device=-1 if self.device == "cpu" else 0)
        print(self.device)
        return ner(prompt)
    
    def sentiment_analysis(self, prompt:str):
        classifier = pipeline("sentiment-analysis", device=-1 if self.device == "cpu" else 0)
        return classifier(prompt)
        