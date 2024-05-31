from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.stem import PorterStemmer
import re
import nltk
from nltk.corpus import stopwords

from sentence_transformers import util


# Ensure the stopwords are downloaded
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))




# Define custom stopwords to exclude relevant technical terms (adjust based on your needs)
custom_stopwords = set(stopwords.words('english')).union({'framework', 'etc', 'develop', 
                           'implement', 'build', 'system', 'solution', 'approach', 
                           'real-time', 'scalable', 'user-friendly','methodology', 'application',
                             'app', 'web', 'development', 'project', 'create', 'develop',
                           'cost-effective', 'robust'})  # Add/remove words as needed

def preprocess_text(text):
  text = text.lower()
  # Keep essential punctuation for technical terms (hyphens, colons)
  text = re.sub(r'[^\w\s\-:]', '', text)
  text = ' '.join([word for word in text.split() if word not in custom_stopwords])

  # Stemming
  text = ' '.join([PorterStemmer().stem(word) for word in text.split()])

  return text


def calculate_similarity(text1, text2):
    if text1 is None or text2 is None:
        return 0.0
    # Tokenize and lemmatize the texts
    tokens1 = word_tokenize(text1)
    tokens2 = word_tokenize(text2)
    lemmatizer = WordNetLemmatizer()
    tokens1 = [lemmatizer.lemmatize(token) for token in tokens1]
    tokens2 = [lemmatizer.lemmatize(token) for token in tokens2]

    # Remove stopwords
    stop_words = stopwords.words('english')
    tokens1 = [token for token in tokens1 if token not in stop_words]
    tokens2 = [token for token in tokens2 if token not in stop_words]

    # Create the TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vector1 = vectorizer.fit_transform([' '.join(tokens1)])
    vector2 = vectorizer.transform([' '.join(tokens2)])

    # Calculate the cosine similarity
    similarity = cosine_similarity(vector1, vector2)[0][0]

    # Map similarity values from [-1, 1] to [0, 1]
    similarity = round((similarity + 1) / 2, 2)

    return similarity

def check_similarity_with_projects(title, description, projects, threshold):
    for project in projects:
        title_similarity = calculate_similarity(title, project.title)
        description_similarity = calculate_similarity(description, project.description)
        if title_similarity > threshold or description_similarity > threshold:
            return True
    return False


