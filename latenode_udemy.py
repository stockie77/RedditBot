
import requests

    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    password=os.getenv('REDDIT_CLIENT_SECRET'),,
    user_agent=,
    username=,

print("latenode")

# Make the POST request to obtain the access token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {
    "grant_type": "password",
    "username": username,
    "password": password
}
headers = {"User-Agent": user_agent}
response = requests.post("https://www.reddit.com/api/v1/access_token",
                         auth=auth, data=data, headers=headers)

# Extract the access token from the response
access_token = response.json()["access_token"]