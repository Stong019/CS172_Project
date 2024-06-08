## In the terminal, "export FLASK_APP=flask_demo" (without .py)
## flask run -h 0.0.0.0 -p 8888

import lucene
import os
import re
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query, BooleanClause, BooleanQuery
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.search.highlight import SimpleHTMLFormatter, QueryScorer, Highlighter, SimpleFragmenter
from org.apache.lucene.search import Sort, SortField
from flask import request, Flask, render_template
from datetime import datetime

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

def generate_snippet(text, query_terms):
    snippet_length = 200
    highlighted_text = text
    query_terms = query_terms.lower().split()
    
    # Find the first occurrence of any query term
    match = re.search('|'.join(re.escape(term) for term in query_terms), text, re.IGNORECASE)
    if match:
        start = max(match.start() - snippet_length // 2, 0)
        end = min(match.end() + snippet_length // 2, len(text))
        snippet = text[start:end]
        
        # Highlight the query terms
        for term in query_terms:
            snippet = re.sub(f"(?i)({re.escape(term)})", r"<span class='highlight'>\1</span>", snippet)
        return ("..." + snippet + "...")
    return text[:snippet_length]  # Return the first snippet_length characters if no match is found

def retrieve(storedir, query, sort):
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

    if sort == 'votes':
        #sort by post_score
        print("sorting by votes")
        sort_field = SortField("Post Score", SortField.Type.INT, True)
        sort = Sort(sort_field)
        topDocs = searcher.search(combined_query, 10, sort)
    
    elif sort == 'time':
        #sort by time
        print("sorting by time")
        sort_field = SortField("Created UTC", SortField.Type.LONG, True)
        sort = Sort(sort_field)
        topDocs = searcher.search(combined_query, 10, sort)

    else:
        print("sorting by relevance")
        sort = None
        topDocs = searcher.search(combined_query, 10)

    topkdocs = []
    for hit in topDocs.scoreDocs:
        doc = searcher.doc(hit.doc)
        snippet = generate_snippet(doc.get("Body"), query)
        created_utc = int(doc.get("Created UTC"))
        created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M')
        topkdocs.append({
            "score": hit.score,
            "post_id": doc.get("Post ID"),
            "author": doc.get("Author"),
            "title": doc.get("Title"),
            "url": doc.get("Url"),
            "post_score": doc.get("Post Score"),
            "num_comments": doc.get("# Comments"),
            "created_utc": created_date,
            "body": snippet
        })

    return topkdocs

#print

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
        sort = form_data['sort']
        print(f"this is the query: {query}")
        print(f"this is the sort option: {sort}")
        lucene.getVMEnv().attachCurrentThread()
        docs = retrieve('lucene_index/', str(query), str(sort))

        for doc in docs:
            if not doc['body']:
                doc['body'] = "Archived post. New comments cannot be posted and votes cannot be cast."
        # print(docs)
        
        return render_template('output.html',lucene_output = docs)
    
lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    
if __name__ == "__main__":
    app.run(debug=True, port=12345) # CHANGE PORT IF NECESSARY

# create_index('sample_lucene_index/')
# retrieve('sample_lucene_index/', 'web data')


#search == home page
#button that redirects back to home page after searching