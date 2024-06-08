import logging, sys
logging.disable(sys.maxsize)

import lucene
import os
import json
import time

from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader, DocValuesType
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query, BooleanClause, BooleanQuery
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
    start = time.time()

    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer() # 'knows about certain token types, lowercases, removes stopwords...'
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False) # not tokenized

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS) # tokenized

    numericType = FieldType()
    numericType.setStored(True)
    numericType.setTokenized(False)
    numericType.setDocValuesType(DocValuesType.NUMERIC)

    posts_dir = os.path.join(os.getcwd(), "crawled_posts")

    for root, _, files in os.walk(posts_dir):
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r') as f: # open in readonly mode
                    data = json.load(f)
                    for post in data:
                        
                        post_id = post['post_id']
                        author = post['author']
                        title = post['title']
                        url = post['url']
                        post_score = post['score']
                        num_comments = post['num_comments']
                        created_utc = post['created_utc']
                        body = post['selftext']
                        # permalink = post['permalink']
                        # comments = post['comments']
                        
                        doc = Document()
                        doc.add(Field('Post ID', str(post_id), metaType)) # metaType not tokenized
                        doc.add(Field('Author', str(author), metaType))
                        doc.add(Field('Title', str(title), contextType))
                        doc.add(Field('Url', str(url), metaType))
                        doc.add(Field('Post Score', int(post_score), numericType))
                        doc.add(Field('# Comments', int(num_comments), numericType))
                        doc.add(Field('Created UTC', int(created_utc), numericType))
                        doc.add(Field('Body', str(body), contextType))

                        writer.addDocument(doc)
    
    writer.close()
    end = time.time()
    print("Total indexing time: ", (end-start), "s")

# def retrieve(storedir, query):
#     searchDir = NIOFSDirectory(Paths.get(storedir))
#     searcher = IndexSearcher(DirectoryReader.open(searchDir))

#     # parser = QueryParser('Body', StandardAnalyzer())
#     # parsed_query = parser.parse(query)

#     title_parser = QueryParser('Title', StandardAnalyzer())
#     parsed_title = title_parser.parse(query)
#     boosted_title = BoostQuery(parsed_title, 2.0) # boost title query x2

#     body_parser = QueryParser('Body', StandardAnalyzer())
#     parsed_body = body_parser.parse(query)

#     boolean_query = BooleanQuery.Builder()
#     boolean_query.add(boosted_title, BooleanClause.Occur.SHOULD)
#     boolean_query.add(parsed_body, BooleanClause.Occur.SHOULD)

#     combined_query = boolean_query.build()

#     topDocs = searcher.search(combined_query, 10).scoreDocs
#     topkdocs = []
#     for hit in topDocs:
#         doc = searcher.doc(hit.doc)
#         topkdocs.append({
#             "score": hit.score,
#             "post_id": doc.get("Post ID"),
#             "author": doc.get("Author"),
#             "title": doc.get("Title"),
#             "url": doc.get("Url"),
#             "post_score": doc.get("Post Score"),
#             "num_comments": doc.get("# Comments"),
#             "created_utc": doc.get("Created UTC"),
#             "body": doc.get("Body"),
#         })
    
#     print(topkdocs)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index('lucene_index/')
# search_term = input("Enter a query term: ")
# retrieve('lucene_index/', search_term)
