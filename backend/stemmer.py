from pathlib import Path
from porter2stemmer import Porter2Stemmer
from nltk.corpus import stopwords

if __name__ == "__main__":
    entries = Path('../crawler/articles/')
    stemmer = Porter2Stemmer()
    stopWords = set(stopwords.words("english"))
    with_capitals_and_stemmed = set()
    for stop_word in stopWords:
        with_capitals_and_stemmed.add(stemmer.stem(stop_word))
        stop_word = chr(ord(stop_word[0]) - 32) + stop_word[1:]
        with_capitals_and_stemmed.add(stop_word)
        with_capitals_and_stemmed.add(stemmer.stem(stop_word))
    stopWords = with_capitals_and_stemmed.union(stopWords)
    for entry in entries.iterdir():
        no_error = False
        with open(entry.absolute(), "r", encoding='utf-8', errors='ignore') as file:
            text = file.read()
            words = text.split(' ')
            for j in range(len(words)):
                words[j] = stemmer.stem(words[j])

            stemmed_text = ' '.join(word for word in words if word.isalnum() and word not in stopWords)
            no_error = True

        if no_error:
            with open(entry.absolute(), "w", encoding='utf-8', errors='ignore') as file:
                file.write(stemmed_text)
