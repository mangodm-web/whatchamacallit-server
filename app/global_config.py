import logging

from sentence_transformers import SentenceTransformer
from app.core.mongodb_utils import get_mongodb_client, get_collection

from app.settings.constants import MODEL_LOCAL

from huggingface_hub.utils._errors import RepositoryNotFoundError

try:
    model_instance = SentenceTransformer(MODEL_LOCAL)
except RepositoryNotFoundError:
    logging.error(
        "Failed to find the specificed repository. Please check the model name."
    )
except ImportError:
    logging.error("Failed to import model_instance from app.")
except Exception:
    logging.error("An unexpected error occurred.")

try:
    mongodb_client = get_mongodb_client()
    corpus_df = get_collection(mongodb_client, "training_data")
except Exception:
    logging.error("An unexpected error occurred.")

try:
    corpus_embeddings = model_instance.encode(corpus_df.description)
except Exception:
    logging.error("An unexpected error occurred.")
