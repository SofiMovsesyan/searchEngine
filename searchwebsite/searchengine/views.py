from django.shortcuts import render 
from django.views import generic
from searchindex.query import run_query
from searchengine.models import Document
from searchindex.query_completion import complete_query
from django.http import JsonResponse
import re


# Create your views here.
class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"
    context_object_name = 'searchresults'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET['query']
        doc_ids, words_to_highlight = run_query(query)

        if not doc_ids:
            return ['No Results']
        def format_document(doc):
            return f'<h1><a href="https://travel.stackexchange.com/questions/{doc.doc_no}" target="_blank">{doc.title}</a></h1><br/><p>{doc.text}</p>'
        docs = [format_document(Document.objects.get(doc_no=doc)) for doc in doc_ids]
        
       
        


        md =[]
        for doc in docs:
            small = doc
            for i in words_to_highlight:
                location = re.search(f"([^\\w])({i})([^\\w])", doc, flags=re.IGNORECASE)
                
                if location:
                    doc_n = location.span()[0]
                    # small = doc[doc_n -150 :doc_n +150]
                
                    for i in words_to_highlight:
                        html = f'<span class="query" style="font-weight: bold;">{i}</span>'
                        small = re.sub(f"([^\\w])({i})([^\\w])", f"\\1{html}\\3", small, flags=re.IGNORECASE)
                        # small = small.replace(i, html)
            md.append(small)
                

        if len(md)>=50:
            return md[:50]
        return md

def complete(request):
    # Get the text typed into the textbox
    query = request.GET['q']

    completions = complete_query(query)
    return JsonResponse(completions, safe=False)
