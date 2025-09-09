import praw
import re
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

def search_acronym(acronym):
    """Hauptfunktion für Reddit-Crawling"""
    # .env-Datei laden
    cwd = os.getcwd()
    load_dotenv(dotenv_path=cwd+'\\secret.env')
    # Reddit-Client mit Umgebungsvariablen erstellen
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    subreddit = reddit.subreddit('wallstreetbets')
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
    
    # Erweiterte Pattern für Akronym mit und ohne Dollarzeichen
    pattern = re.compile(r'(?<!\w)(\$' + re.escape(acronym) + r'|' + re.escape(acronym) + r')(?!\w)')
    
    total_count = 0
    results = []
    
    for post in subreddit.new(limit=100):
        if datetime.fromtimestamp(post.created_utc, tz=timezone.utc) < one_day_ago:
            continue
            
        # Post durchsuchen
        post_text = post.title + '\n' + (post.selftext or '')
        post_matches = pattern.findall(post_text)
        
        # Kommentare durchsuchen
        comment_matches = []
        try:
            post.comments.replace_more(limit=30)
            for comment in post.comments.list():
                if hasattr(comment, 'body'):
                    comment_matches.extend(pattern.findall(comment.body))
        except:
            pass
        
        total_matches = len(post_matches) + len(comment_matches)
        if total_matches > 0:
            total_count += total_matches
            
            # Varianten sammeln für detaillierte Ausgabe
            all_variants = post_matches + comment_matches
            variant_counts = {}
            for variant in all_variants:
                variant_counts[variant] = variant_counts.get(variant, 0) + 1
            
            results.append({
                'title': post.title,
                'url': f"https://reddit.com{post.permalink}",
                'post_hits': len(post_matches),
                'comment_hits': len(comment_matches),
                'variants': variant_counts,
                'upvotes': post.score,  # Upvotes hinzugefügt
                'num_comments': post.num_comments  # Kommentaranzahl hinzugefügt
            })
    
    return total_count, results

def main():
    while True:
        acronym = input("Akronym eingeben (oder 'quit'): ").strip()
        if acronym.lower() == 'quit':
            break
            
        total, results = search_acronym(acronym)
        
        print(f"\n=== ERGEBNISSE FÜR '{acronym}' ===")
        print(f"Gesamttreffer: {total}")
        print(f"Posts gefunden: {len(results)}")
        
        # Gesamtübersicht der Varianten
        all_variants = {}
        for result in results:
            for variant, count in result['variants'].items():
                all_variants[variant] = all_variants.get(variant, 0) + count
        
        if all_variants:
            print(f"\nGefundene Varianten:")
            for variant, count in sorted(all_variants.items(), key=lambda x: x[1], reverse=True):
                print(f"  '{variant}': {count}x")
        
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] {result['title']}")
            print(f"    📊 Upvotes: {result['upvotes']} | 💬 Kommentare: {result['num_comments']}")  # Neue Zeile
            print(f"    🎯 Treffer - Post: {result['post_hits']} | Kommentare: {result['comment_hits']}")
            
            # Varianten für diesen Post anzeigen
            if result['variants']:
                variant_str = ", ".join([f"'{v}': {c}x" for v, c in result['variants'].items()])
                print(f"    🔍 Varianten: {variant_str}")
            
            print(f"    🔗 {result['url']}")

if __name__ == "__main__":
    main()