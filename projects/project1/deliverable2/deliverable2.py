import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

class URLValidator:
    """
    A URL validation class evaluating credibility based on multiple factors:
    domain trust, content relevance, fact-checking, bias detection, and citations.
    """

    def __init__(self):
        self.similarity_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        self.fake_news_classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")
        self.sentiment_analyzer = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

    def fetch_page_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return " ".join([p.text for p in soup.find_all("p")])
        except:
            return ""

    def compute_similarity_score(self, user_query, content):
        if not content:
            return 0
        return int(util.pytorch_cos_sim(
            self.similarity_model.encode(user_query), 
            self.similarity_model.encode(content)
        ).item() * 100)

    def detect_bias(self, content):
        if not content:
            return 50
        sentiment_result = self.sentiment_analyzer(content[:512])[0]
        return 100 if sentiment_result["label"] == "POSITIVE" else 50 if sentiment_result["label"] == "NEUTRAL" else 30

    def get_star_rating(self, score: float):
        """ Converts a score (0-100) into a 1-5 star rating. """
        stars = max(1, min(5, round(score / 20)))  # Normalize 100-scale to 5-star scale
        return stars, "⭐" * stars

    def generate_explanation(self, domain_trust, similarity_score, fact_check_score, bias_score, citation_score, final_score):
        """ Generates a human-readable explanation for the score. """
        reasons = []
        if domain_trust < 50:
            reasons.append("The source has low domain authority.")
        if similarity_score < 50:
            reasons.append("The content is not highly relevant to your query.")
        if fact_check_score < 50:
            reasons.append("Limited fact-checking verification found.")
        if bias_score < 50:
            reasons.append("Potential bias detected in the content.")
        if citation_score < 30:
            reasons.append("Few citations found for this content.")

        return " ".join(reasons) if reasons else "This source is highly credible and relevant."

    def rate_url_validity(self, user_query, url):
        content = self.fetch_page_content(url)
        similarity_score = self.compute_similarity_score(user_query, content)
        bias_score = self.detect_bias(content)

        domain_trust = 60  # Placeholder
        fact_check_score = 70  # Placeholder
        citation_score = 50  # Placeholder

        final_score = (0.3 * domain_trust) + (0.3 * similarity_score) + (0.2 * fact_check_score) + (0.1 * bias_score) + (0.1 * citation_score)

        stars, icon = self.get_star_rating(final_score)
        explanation = self.generate_explanation(domain_trust, similarity_score, fact_check_score, bias_score, citation_score, final_score)

        return {
            "raw_score": {
                "Domain Trust": domain_trust,
                "Content Relevance": similarity_score,
                "Fact-Check Score": fact_check_score,
                "Bias Score": bias_score,
                "Citation Score": citation_score,
                "Final Validity Score": final_score
            },
            "stars": {
                "score": stars,
                "icon": icon
            },
            "explanation": explanation
        }
# Example usage
user_query = "Is it a bad investment to buy a house as a single male under the age of 30?"
url_to_check = "https://www.quickenloans.com/learn/homes-for-single-people"

validator = URLValidator()
result = validator.rate_url_validity(user_query, url_to_check)

# Display the results
import json
print(json.dumps(result, indent=4))
