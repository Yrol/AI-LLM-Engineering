import torch
from transformers import pipeline
import sentencepiece

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
    
    def question_answering(self, question:str, context:str):
        question_answerer = pipeline("question-answering", device=-1 if self.device == "cpu" else 0)
        return question_answerer(question=question, context=context)
    
    def translator(self, translation_type:str, text:str):
        
        device_id = -1 if self.device == "cpu" else 0

        if translation_type == "translation_en_to_es":
            translator = pipeline(
                "translation_en_to_es",
                model="Helsinki-NLP/opus-mt-en-es",
                device=0  # force GPU here, or -1 for CPU if needed
            )
        else:
            translator = pipeline(
                translation_type,
                device=device_id
        )
        return translator(text)
    
    def classification(self, classificationText:str):
        classifier = pipeline("zero-shot-classification", device=-1 if self.device == "cpu" else 0)
        return classifier(classificationText, candidate_labels=["technology", "sports", "politics"])
    
    def text_generation(self, inputText:str):
        text_generation = pipeline("text-generation", device=-1 if self.device == "cpu" else 0)
        return text_generation(inputText)