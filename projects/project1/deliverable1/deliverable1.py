import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

def rate_url_validity(user_query: str, url: str) -> dict:
    """
    Evaluates the validity of a given URL by computing various metrics including
    domain trust, content relevance, fact-checking, bias, and citation scores.

    Args:
        user_query (str): The user's original query.
        url (str): The URL to evaluate.

    Returns:
        dict: A dictionary containing the overall validity score and explanation.
    """

    # === Step 1: Fetch Page Content ===
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = " ".join([p.text for p in soup.find_all("p")])  # Extract paragraph text
    except Exception as e:
        return {"error": f"Failed to fetch content: {str(e)}"}

    # === Step 2: Domain Authority Check (Moz API Placeholder) ===
    domain_trust = 60  # Placeholder value (Scale: 0-100)

    # === Step 3: Content Relevance (Semantic Similarity using SentenceTransformer) ===
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    similarity_score = util.pytorch_cos_sim(
        model.encode(user_query),
        model.encode(page_text)
    ).item() * 100  # Convert similarity score to percentage
    relevance_explanation = f"Computed semantic similarity between the user query and page content."

    # === Step 4: Fact-Checking (Google Fact Check API) ===
    fact_check_score = check_facts(page_text)
    fact_check_explanation = f"Fact-checking score: {fact_check_score} based on Google Fact Check API."

    # === Step 5: Bias Detection (NLP Sentiment Analysis) ===
    sentiment_pipeline = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")
    sentiment_result = sentiment_pipeline(page_text[:512])[0]  # Process first 512 characters

    # Calculate bias score based on sentiment label
    bias_score = (
        100 if sentiment_result["label"] == "POSITIVE" else
        50 if sentiment_result["label"] == "NEUTRAL" else
        0
    )
    bias_explanation = f"Detected sentiment: {sentiment_result['label']} with score of {sentiment_result['score']:.2f}."

    # === Step 6: Citation Check (Google Scholar via SerpAPI) ===
    citation_count = check_google_scholar(url)
    citation_score = min(citation_count * 10, 100)  # Normalize to max 100
    citation_explanation = f"Citation count: {citation_count}, normalized score: {citation_score}."

    # === Step 7: Compute Final Validity Score ===
    final_score = (
        (0.3 * domain_trust) +
        (0.3 * similarity_score) +
        (0.2 * fact_check_score) +
        (0.1 * bias_score) +
        (0.1 * citation_score)
    )

    # Return the results
    return {
        "Domain Trust": domain_trust,
        "Content Relevance": similarity_score,
        "Fact-Check Score": fact_check_score,
        "Bias Score": bias_score,
        "Citation Score": citation_score,
        "Final Validity Score": round(final_score, 2)
    }

# === Helper Function: Fact-Checking via Google Fact Check API ===
def check_facts(text: str) -> int:
    """
    Cross-checks text against Google Fact Check API.
    Returns a score between 0-100 indicating factual reliability.
    """
    api_url = f"https://toolbox.google.com/factcheck/api/v1/claims:search?query={text[:200]}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if "claims" in data and data["claims"]:
            return 80  # If found in fact-checking database
        return 40  # No verification found
    except:
        return 50  # Default uncertainty score

# === Helper Function: Citation Count via Google Scholar API ===
def check_google_scholar(url: str) -> int:
    """
    Checks Google Scholar citations using SerpAPI.
    Returns the count of citations found.
    """
    serpapi_key = "YOUR_SERPAPI_KEY"
    params = {
        "q": url,
        "engine": "google_scholar",
        "api_key": serpapi_key
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        return len(data.get("organic_results", []))
    except:
        return 0  # Assume no citations found


# User input prompt and URL to check
user_prompt = "Is it a bad investment to buy a house as a single male under the age of 30?"
url_to_check = "https://www.quickenloans.com/learn/homes-for-single-people"

# Evaluate the validity of the given URL
result = rate_url_validity(user_prompt, url_to_check)

# Display the results
print(result)


