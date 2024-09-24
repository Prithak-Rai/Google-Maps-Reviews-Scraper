import serpapi
import os
from dotenv import load_dotenv
import time
import csv

load_dotenv()

api_key = os.getenv('SERPAPI_KEY')

client = serpapi.Client(api_key=api_key)

def fetch_all_reviews(place_id):
    all_reviews = []  
    next_page_token = None

    while True:

        search_params = {
            'engine': 'google_maps_reviews',
            'type': 'search',
            'place_id': place_id,
        }
        
        if next_page_token:
            search_params['next_page_token'] = next_page_token

        results = client.search(search_params)

        pagination = results.get('serpapi_pagination', {})
        next_page_url = pagination.get('next')
        next_page_token = pagination.get('next_page_token')
        reviews = results.get('reviews', [])

        print("Next Page URL:", next_page_url)
        print("Next Page Token:", next_page_token)

        for review in reviews:
            user_rating = review.get('rating')
            review_text = review.get('snippet')
            user_name = review.get('user', {}).get('name')
            user_link = review.get('user', {}).get('link')

            print(f"User: {user_name} ({user_link})")
            print(f"Rating: {user_rating}, Snippet: {review_text}")
            print("-" * 40)  

            all_reviews.append({
                'user': user_name,
                'link': user_link,
                'rating': user_rating,
                'snippet': review_text
            })

        if not next_page_token:
            break

        time.sleep(2)

    return all_reviews

def write_reviews_to_csv(reviews, filename='reviews.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['user', 'link', 'rating', 'snippet'])
        writer.writeheader() 
        writer.writerows(reviews) 

place_id = 'Place_ID'
all_reviews = fetch_all_reviews(place_id)

write_reviews_to_csv(all_reviews)

print(f"Total Reviews Fetched: {len(all_reviews)}")
