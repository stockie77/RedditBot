
import requests

client_id="-vo1jgs5tX0-BojGtt6TYg",
client_secret="MI5FfQKYlqcTIQAo9OdxegOMLzji4A",
password="65CA!5K2AGB-U.",
user_agent="firstBot",
username="hanni777",

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