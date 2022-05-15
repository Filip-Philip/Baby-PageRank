from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import glob
import numpy as np
import scipy


if __name__ == "__main__":
    directory_path = "../crawler/articles/"
    text_files = glob.glob(f"{directory_path}/*.txt")

    text_titles = np.array([Path(text).stem for text in text_files])

    # np.save("text titles.npy", text_titles)

    tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english')
    tfidf_vector = tfidf_vectorizer.fit_transform(text_files)
    # np.save("feature names.npy", tfidf_vectorizer.get_feature_names())

    scipy.sparse.save_npz("document-term matrix scipy.npz", tfidf_vector)
