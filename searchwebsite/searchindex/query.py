from searchindex.build_index import index
from searchindex.preprocessing import preprocess_line_en
from searchengine.models import Document
import re
import math

def run_ranked_search(query):
  words = preprocess_line_en(query)
  scores = {}
  for word in words:
      docs = index.get(word, [])
      for doc_id in docs:
          score = (1 + math.log10(docs[doc_id].freq)) * math.log10(index.docCount / docs.docFreq)
          if (doc_id in scores):
              scores[doc_id] += score
          else:
              scores[doc_id] = score
  sorted_scores_ids = sorted(scores, key=scores.get, reverse=True)
  sorted_scores = {doc_id:scores[doc_id] for doc_id in sorted_scores_ids}
#   print(sorted_scores)

  return sorted_scores


def run_query(query):
  
   words_to_highlight = query.split(' ')
   words = preprocess_line_en(query)
#    Remove empty items from words_to_highlight
#   suppose words_to_higlight = ['', 'word1', '']
   for word in words_to_highlight:
       if word == '':

            words_to_highlight.remove(word)

   if not words:
       return [],words
   nums = []
   
   
   
    

   if ' and not ' in query:
       words_to_highlight.remove("and")
       words_to_highlight.remove("not")
       res1 = set(index.get(words[0], []))
       res2 = set(index.get(words[1], []))
      
       all_doc_ids = set([str(doc.doc_no) for doc in Document.objects.all()])
       not_res2 = all_doc_ids.difference(res2)


       nums = res1.intersection(not_res2)
       nums = [int(i) for i in nums]

    #    print(nums)


   # and search
   elif ' and ' in query:
       words_to_highlight.remove("and")

   #    words.remove("and")
    #    print('and query')
       res1 = set(index.get(words[0], []))
       res2 = set(index.get(words[1], []))
      
       nums = res1.intersection(res2)


   elif ' or not ' in query:
    #    print('or not query')
       words_to_highlight.remove("or")
       words_to_highlight.remove("not")
       

       print(words)
       res1 = set(index.get(words[0], []))
       res2 = set(index.get(words[1], []))
      
       all_doc_ids = set([str(doc.doc_no) for doc in Document.objects.all()])

       not_res2 = all_doc_ids.difference(res2)

       nums = res1.union(not_res2)
       nums = [int(i) for i in nums]
       print(nums)


   # or search
   elif ' or ' in query:
       print(words_to_highlight)
       words_to_highlight.remove("or")
        

       res1 = set(index.get(words[0], []))
       res2 = set(index.get(words[1], []))


       nums = res1.union(res2)




   else:
       # one word
       nums = run_ranked_search(query)
    #    words_to_highlight = ["paris"]
       
    
  
   #-----------
   return nums, words_to_highlight
   


   # res = {}
   # for i in nums:
   #     try:
   #         res[str(i)] = index.get(words[0], ["No Results"])[i]
   #     except:
   #         res[str(i)] = index.get(words[1], ["No Results"])[i]


   # return res



