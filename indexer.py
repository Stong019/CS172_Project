import logging, sys
logging.disable(sys.maxsize)

import lucene
import os
import json

from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField

'''
For each JSON file, extract relevant fields (e.g., post_id, author, title,
    url, score, num_comments, created_utc, selftext, permalink, comments)
    and index them.

Ensure you handle the text fields correctly for search indexing

IndexWriter: main class for creating and managing the index; allows you
    to add, update, and delete documents in the index

Directory: represents the location where the index is stored; either disk
    (SimpleFSDirectory) or memory (RAMDirectory)

Analyzer: breaks text into tokens; different analyzers handle text
    differently (e.g. StandardAnalyzer splits text on whitespace &
    punctuation)

Field: piece of data w/in a document. Fields can be indexed (to search)
    and/or stored (for retrieval)

Document: a container for fields lol
'''

def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    posts_dir = os.path.join(os.getcwd(), "crawled_posts")

    for filename in os.listdir(posts_dir):
        with open(os.path.join(posts_dir, filename), 'r') as f: # open in readonly mode
            data = json.load(f)
            for post in data:
                title = post['title']
                author = post['author']
                body = post['selftext']

                print(title, body)
                
                doc = Document()
                doc.add(Field('Title', str(title), metaType))
                doc.add(Field('Author', str(author), contextType))
                doc.add(Field('Body', str(body), contextType))
                writer.addDocument(doc)
    
    writer.close()

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Body', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "text": doc.get("Title"),
            "author": doc.get("Author"),
            "body": doc.get("Body")
        })
    
    print(topkdocs)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# create_index('sample_lucene_index/')
search_term = input("Enter a query term: ")
retrieve('sample_lucene_index/', search_term)
