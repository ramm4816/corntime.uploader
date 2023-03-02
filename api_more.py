import requests

url = "https://siren.more.tv/player/config?track_id=714005&partner_id=1796&user_token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIyNTg2NTkyMSwiZXhwIjoxNjc3NzI4MjEwLCJpYXQiOjE2Nzc3MTc0MTAsInBjdCI6MTY3NzcxNjk1OSwicHJvdmlkZXJfaWQiOjEsInByb3ZpZGVyX25hbWUiOiJQYXNzd29yZCIsImFub255bW91cyI6ZmFsc2V9.TKJDJKQmHtgGveIwQmHCcveQX47ne9um_xtpZ6Ti4sAmegNbjQuRT7beiG-dL0GrkWf8j9lMs3iuCOQDZjl1PA&userId=225865921"

payload={}
headers = {
  'TE': 'gzip, deflate; q=0.5',
  'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android S Build/AOSP.MASTER)',
  'Host': 'siren.more.tv',
  'Cookie': '__lhash_=47960c9786b7fca0d858bed7d38ff069'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
