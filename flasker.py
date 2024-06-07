## In the terminal, "export FLASK_APP=flask_demo" (without .py)
## flask run -h 0.0.0.0 -p 8888

import lucene
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query, BooleanClause, BooleanQuery
from org.apache.lucene.search.similarities import BM25Similarity
from flask import request, Flask, render_template

app = Flask(__name__)

sample_doc = [
    {
        'title' : 'A',
        'context' : 'lucene is a useful tool for searching and information retrieval'
        },
    {
        'title' : 'B',
        'context' : 'Bert is a deep learning transformer model for encoding textual data'
    },
    {
        'title' : 'C',
        'context' : 'Django is a python web framework for building backend web APIs'
    }
]      

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    # parser = QueryParser('Body', StandardAnalyzer())
    # parsed_query = parser.parse(query)

    title_parser = QueryParser('Title', StandardAnalyzer())
    parsed_title = title_parser.parse(query)
    boosted_title = BoostQuery(parsed_title, 2.0) # boost title query x2

    body_parser = QueryParser('Body', StandardAnalyzer())
    parsed_body = body_parser.parse(query)

    boolean_query = BooleanQuery.Builder()
    boolean_query.add(boosted_title, BooleanClause.Occur.SHOULD)
    boolean_query.add(parsed_body, BooleanClause.Occur.SHOULD)

    combined_query = boolean_query.build()

    topDocs = searcher.search(combined_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "post_id": doc.get("Post ID"),
            "author": doc.get("Author"),
            "title": doc.get("Title"),
            "url": doc.get("Url"),
            "post_score": doc.get("Post Score"),
            "num_comments": doc.get("# Comments"),
            "created_utc": doc.get("Created UTC"),
            "body": doc.get("Body"),
        })
    # print(topkdocs)
    return topkdocs

@app.route("/", methods = ['POST', 'GET'])
def input():
    return render_template('input.html')

@app.route('/output', methods = ['POST', 'GET'])
def output():
    if request.method == 'GET':
        return f"Nothing"
    if request.method == 'POST':
        form_data = request.form
        query = form_data['query']
        print(f"this is the query: {query}")
        lucene.getVMEnv().attachCurrentThread()
        docs = retrieve('lucene_index/', str(query))
        print(docs)
        
        return render_template('output.html',lucene_output = docs)
    
lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    
if __name__ == "__main__":
    app.run(debug=True)

# create_index('sample_lucene_index/')
# retrieve('sample_lucene_index/', 'web data')


#search == home page
#button that redirects back to home page after searching