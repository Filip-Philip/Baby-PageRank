import operator
import numpy as np
from porter2stemmer import Porter2Stemmer
import scipy
from sklearn.decomposition import TruncatedSVD


def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def vector_correlation(vector1, vector2):
    vector1_norm = np.linalg.norm(vector1)
    vector2_norm = np.linalg.norm(vector2)
    if vector1_norm != 0 and vector2_norm != 0:
        return np.dot(vector1, vector2) / (vector1_norm * vector2_norm)


if __name__ == "__main__":
    stemmer = Porter2Stemmer()
    query_string = input("Enter your search query: ")
    k = int(input("Enter number of search results: "))
    bag_of_words = np.load("feature names.npy")
    text_titles = np.load("text titles.npy")
    words = query_string.split(" ")
    for i in range(len(words)):
        words[i] = stemmer.stem(words[i])

    query_vector = np.zeros(shape=bag_of_words.shape)
    for word in words:
        for i in range(len(bag_of_words)):
            if word == bag_of_words[i]:
                print(f"found word = {word}")
                query_vector[i] += 1

    document_term_matrix = scipy.sparse.load_npz("document-term matrix scipy.npz")

    svd = TruncatedSVD(n_components=k).fit(document_term_matrix)
    svd_matrix = svd.transform(document_term_matrix)
    svd_components = svd.components_

    query_vector = np.array([query_vector]).T
    svd_q = svd_components.dot(query_vector)
    svd_c = svd_matrix.dot(svd_q)
    correlations = {text_titles[document_id]: svd_c[document_id, 0] for document_id in range(len(text_titles))}
    results = sorted(correlations.items(), key=operator.itemgetter(1), reverse=True)

    number_of_results = 10
    for result in results[:number_of_results]:
        print(result)
