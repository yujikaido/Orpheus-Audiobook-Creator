import nltk
from nltk.tokenize import sent_tokenize
import logging

# Configure logging (optional, but recommended for feedback)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Start of NLTK Data Download ---
def download_nltk_data():
    """Checks for and downloads required NLTK data if missing."""
    required_data = {
        "punkt": "tokenizers/punkt",
        "punkt_tab": "tokenizers/punkt_tab" # Added the missing resource check
    }
    missing_data = []

    for data_id, data_path in required_data.items():
        try:
            nltk.data.find(data_path)
            logging.info(f"NLTK resource '{data_id}' found.")
        except LookupError:
            logging.warning(f"NLTK resource '{data_id}' not found.")
            missing_data.append(data_id)

    if missing_data:
        logging.info(f"Downloading missing NLTK resources: {missing_data}")
        try:
            for data_id in missing_data:
                nltk.download(data_id, quiet=True)
            logging.info("NLTK resource download successful.")
            for data_id in missing_data:
               nltk.data.find(required_data[data_id])
            logging.info("NLTK resources verified after download.")
        except Exception as e:
            logging.error(f"Failed to download NLTK resources: {e}")
            logging.error("Please try downloading manually in a Python console:")
            logging.error(">>> import nltk")
            for data_id in missing_data:
                logging.error(f">>> nltk.download('{data_id}')")
            raise RuntimeError(f"Failed to download required NLTK data: {missing_data}") from e

# --- Call the download function when the module is imported or script is run ---
download_nltk_data()
# --- End of NLTK Data Download ---

def split_text_into_chunks(text, max_chars=350, overlap_sentences=0):
    if not text:
        logging.warning("Input text is empty or None.")
        return []
    if max_chars <= 0:
        raise ValueError("max_chars must be a positive integer.")
    if overlap_sentences < 0:
        raise ValueError("overlap_sentences cannot be negative.")

    try:
        sentences = sent_tokenize(text)
        logging.info(f"Text length: {len(text)} | Sentences detected: {len(sentences)}")
    except Exception as e:
        logging.error(f"NLTK sentence tokenization failed: {e}")
        logging.warning("Falling back to treating the entire text as a single sentence.")
        sentences = [text]

    if not sentences:
        return []

    # One sentence per chunk by default
    chunks = []
    for i, sentence in enumerate(sentences):
        chunks.append(sentence.strip())

    return chunks
