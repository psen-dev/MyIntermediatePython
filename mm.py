import re
text = "Visit www.example.com today"
result = re.sub(r'www\.(\w+)\.com', r'https://\1.org', text)
print(result)