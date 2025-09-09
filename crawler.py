import pickle
import praw
from datetime import datetime, timedelta
from collections import Counter
import re
import os
from dotenv import load_dotenv

def reddit_crawler():
    cwd=""
    # Pfad zur Excel-Datei
    cwd = os.getcwd()        
    # Eindeutige ID generieren (YYMMDD-HHMM)
    run_id = datetime.now().strftime("%y%m%d-%H%M")
    print(f"Crawler-Run ID: {run_id}")
    
    # .env-Datei laden
    load_dotenv(dotenv_path=cwd+"\\secret.env")
    # Reddit-Client mit Umgebungsvariablen erstellen
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    
    blacklist = {
        'BE', 'GO', 'IT', 'OR', 'SO', 'NO', 'UP', 'FOR', 'ON', 'BY', 'AS', 'HE', 'AM', 'AN', 'AI', 'DD', 'OP', 'ALL', 'YOU', 'TV', 'PM', 'HAS', 'ARM' 
        'ARE', 'PUMP', 'EOD', 'DAY', 'WTF', 'HIT', 'NOW'}
        
    pattern_template = r'(?<!\w)(\${symbol}|{symbol})(?!\w)'
    
    # Akronyme laden
    with open(cwd+'\\symbols_list2.pkl', 'rb') as f:
        all_symbols = pickle.load(f)
        
    symbols = [symbol for symbol in all_symbols if symbol not in blacklist]
        
    print(f"Suche nach {len(symbols)} Akronymen in r/wallstreetbets...")
    
    # Treffer-Counter
    symbol_counts = Counter()
    
    # Subreddit laden und neue Posts der letzten 24h abrufen
    subreddit = reddit.subreddit('wallstreetbets')
    cutoff_time = datetime.now() - timedelta(days=1)
    
    post_count = 0
    for post in subreddit.new(limit=100):  # Limit anpassen je nach Bedarf
        post_time = datetime.fromtimestamp(post.created_utc)
        
        if post_time < cutoff_time:
            continue
            
        post_count += 1
        print(f"Durchsuche Post {post_count}: {post.title[:50]}...")
        
        # Text für Suche vorbereiten (Post-Titel + Inhalt)
        search_text = f"{post.title} {post.selftext}"
        
        # Kommentare laden und hinzufügen
        post.comments.replace_more(limit=30)  # Alle Kommentare laden
        for comment in post.comments.list():
            search_text += f" {comment.body}"
        
        # Nach Akronymen suchen (Case-sensitive, ganze Wörter)
        for symbol in symbols:
            # Regex für ganze Wörter: \b für Wortgrenzen
            pattern = pattern_template.format(symbol=re.escape(symbol))

            #pattern = rf'\b{re.escape(symbol)}\b'
            matches = len(re.findall(pattern, search_text))
            if matches > 0:
                symbol_counts[symbol] += matches
                print(f"  → {symbol}: {matches} Treffer")
    
    print(f"\nSuche abgeschlossen. {post_count} Posts durchsucht.")
    # Ergebnisse filtern (>5 Treffer) und speichern
    filtered_results = {symbol: count for symbol, count in symbol_counts.items() if count > 5}
    
    if filtered_results:
        # Als Dictionary mit Run-ID speichern
        result_data = {
            'run_id': run_id,
            'results': filtered_results,
            'total_posts': post_count
        }
        
        # Dateiname mit run_id als Präfix erstellen
        filename = f"{run_id}_crawler-ergebnis.pkl"
        filepath = os.path.join(cwd+'\\pickle', filename)
        
        with open(filepath, 'wb') as f:
            pickle.dump(result_data, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        print(f"\nErgebnisse gespeichert in: {filename}")
        print(f"{len(filtered_results)} Akronyme mit >5 Treffern:")
        for symbol, count in sorted(filtered_results.items(), key=lambda x: x[1], reverse=True):
            print(f"  {symbol}: {count} Treffer")
    else:
        print("\nKeine Akronyme mit >5 Treffern gefunden.")

if __name__ == "__main__":
    reddit_crawler()