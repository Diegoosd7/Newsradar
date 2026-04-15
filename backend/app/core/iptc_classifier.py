from transformers import pipeline

# Se usa el siguiente modelo
# https://huggingface.co/classla/multilingual-IPTC-news-topic-classifier


class IPTCClassifier:
    def __init__(self) -> None:
        # Load a multi-class classification pipeline - if the model runs on CPU, comment out "device"
        self.classifier = pipeline(
            "text-classification",
            model="classla/multilingual-IPTC-news-topic-classifier",
            # device=0,
            max_length=512,
            truncation=True,
        )
        self.iptc_label_en_to_es = {
            "education": "educación",
            "human interest": "interés humano, animales, insólito",
            "society": "sociedad",
            "sport": "deporte",
            "crime, law and justice": "policía y justicia",
            "disaster, accident and emergency incident": "catástrofes y accidentes",
            "arts, culture, entertainment and media": "artes, cultura, entretenimiento y medios",
            "politics": "política",
            "economy, business and finance": "economía, negocios y finanzas",
            "lifestyle and leisure": "Estilo de vida y tiempo libre",
            "science and technology": "	ciencia y tecnología",
            "health": "salud",
            "labour": "mano de obra",
            "religion": "religión y culto",
            "weather": "meteorología",
            "environment": "medio ambiente",
            "conflict, war and peace": "conflicto, guerra y paz",
        }

    def get_news_iptc_label(self, news_content: str) -> str:
        # El output del classifier es una lista de dicts como por ejemplo
        # [{'label': 'sport', 'score': 0.9985264539718628}]
        result = self.classifier(news_content)
        label_en = result[0]["label"]
        label_es = self.iptc_label_en_to_es[label_en]
        return label_es

    def get_multiple_news_iptc_labels(self, news_content: list[str]) -> list[str]:
        # El output del classifier es una lista de dicts como por ejemplo
        # [{'label': 'sport', 'score': 0.9985264539718628}]
        results = self.classifier(news_content)
        labels_en = [result["label"] for result in results]
        labels_es = [self.iptc_label_en_to_es[label_en] for label_en in labels_en]
        return labels_es
