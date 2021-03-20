import sys
import os
import nltk
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf8") as f:
            text = f.read()
        data[file] = text
    return data

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # Tokenize lowercase document
    raw_data = nltk.word_tokenize(document.lower())
    
    # Filter stopwords and punctuation
    words = []
    for data_point in raw_data:
        if data_point in nltk.corpus.stopwords.words("english") \
            or data_point in string.punctuation:
            continue
        words.append(data_point)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_docs = len(documents)
    idfs = dict()

    # Count words per doc
    for doc in documents.values():
        doc = set(doc)
        for word in doc:
            if word in idfs:
                idfs[word] += 1
            else:
                idfs[word] = 1
    
    # Compute idfs for every word
    for k, v in idfs.items():
        idfs[k] = math.log(num_docs / v)
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = []
    for file, words in files.items():
        tfidf = 0
        for q_word in query:
            
            if q_word not in words:
                continue
            
            # Count words for tf
            tf = words.count(q_word)

            # Add tf-idf of word to compound tf-idf of the file
            tfidf += tf * idfs[q_word]
        
        # Keep track of tf-idfs for each file
        tfidfs.append((file, tfidf))

    # Sort results by tf-idf and create list to return
    tfidfs.sort(key=lambda x: -x[1])
    top_matches = [tfidfs[i][0] for i in range(n)]
    
    return top_matches


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idfs = []
    for sentence, words in sentences.items():
        
        # Skip headers
        if sentence[0] == '=':
            continue
        
        sum_idfs = 0
        count = 0
        for q_word in query:
            
            # Count query term density and add to sum of idfs
            if q_word in words:
                count += 1
                sum_idfs += idfs[q_word]
        
        # Keep track of sum_idfs and query term density for each sentence
        sentence_idfs.append((sentence, sum_idfs, count/len(words)))

    # Sort results by sum_idf values x[1] and query term density x[2] and create list to return
    sentence_idfs.sort(key=lambda x: (-x[1], -x[2]))
    top_matches = [sentence_idfs[i][0] for i in range(n)]
    
    return top_matches


if __name__ == "__main__":
    main()
