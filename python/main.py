import sys
import json
import os
import argparse
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.nltk_config import ensure_nltk_data
from models.scholarScraper import ScholarScraper
from models.scholarComputation import ScholarComputation

def main():
    try:
        ensure_nltk_data()
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--author', type=str, default="", help='Nama Penulis')
    parser.add_argument('-k', '--keyword', type=str, default="", help='Keyword untuk similaritas')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Jumlah data')
    
    args = parser.parse_args()
    
    author_name = args.author
    keyword = args.keyword
    limit_data = args.limit
    search_query = author_name if author_name else keyword

    try:
        # --- A. SCRAPING ---
        scraper = ScholarScraper(query=search_query)
        scraper.config.set_headless(True)
        
        scraper.request_scholar(search_query)
        
        # Scrape data
        raw_papers = scraper.scrape_scholar_papers(count=limit_data, output_format="dict")
        
        if not raw_papers:
            print(json.dumps({"papers": [], "top_keywords": []}))
            return

        # --- B. COMPUTATION ---
        
        documents = [p['title'] if p['title'] else "" for p in raw_papers]
        
        computer = ScholarComputation(language="en")
        
        # Preprocessing Documents
        processed_docs = computer.case_folding(documents)
        processed_docs = computer.stopword_removal(processed_docs)
        processed_docs = computer.lemmatization(processed_docs)
        
        tfidf_matrix = computer.train_tfidf_weighting(processed_docs)
        
        top_keywords = []
        if hasattr(computer, 'top_word'):
            for word, score in computer.top_word:
                top_keywords.append({"word": word, "score": float(score)})

        if keyword:
            processed_query = computer.case_folding([keyword])
            processed_query = computer.stopword_removal(processed_query)
            processed_query = computer.lemmatization(processed_query)
            query_vector = computer.apply_tfidf_weighting(processed_query)
            similarity_scores = computer.calculate_similarity(query_vector, tfidf_matrix)
        else:
            similarity_scores = [0.0] * len(raw_papers)

        # --- C. OUTPUT ---
        final_papers = []
        for i, paper in enumerate(raw_papers):
            paper['similarity'] = float(similarity_scores[i])
            final_papers.append(paper)
        
        final_papers.sort(key=lambda x: x['similarity'], reverse=True)

        print(json.dumps({
            "papers": final_papers,
            "top_keywords": top_keywords
        }))
        
    except Exception as e:
        print(json.dumps({"error": str(e), "details": traceback.format_exc()}))
    finally:
        if 'scraper' in locals():
            scraper._close_webdriver()

if __name__ == "__main__":
    main()