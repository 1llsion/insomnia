import requests
import json
import os
import urllib.parse
from assets.colors import *

class GoogleSuggestion:
    def __init__(self):
        self.base_url = "http://suggestqueries.google.com/complete/search?client=firefox&q="

    def get_suggestions(self, keyword):
        encoded_keyword = urllib.parse.quote(keyword)
        url = self.base_url + encoded_keyword
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                suggestions = self.parse_suggestions(response.text)
                if suggestions:
                    print(f"[{green}+{white}] Found {cyan}{len(suggestions)}{white} keyword suggestions for '{keyword}'.")
                    self.save_keywords(keyword, suggestions)
                else:
                    print(f"[{red}!{white}] No suggestions found for '{keyword}'.")
            else:
                print(f"[{red}!{white}] Failed to fetch data from Google Suggest.")
        except Exception as e:
            print(f"[{red}!{white}] An error occurred: {e}")

    def parse_suggestions(self, response_text):
        try:
            json_part = response_text[response_text.find('['):response_text.rfind(']') + 1]
            suggestions_data = json.loads(json_part)
            suggestions = suggestions_data[1]
            return suggestions
        except Exception as e:
            print(f"[{red}!{white}] Error parsing suggestions: {e}")
            return []

    def save_keywords(self, keyword, suggestions):
        filename = f"results/google_suggestions_{self.clean_filename(keyword)}.txt"
        os.makedirs("results", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            for suggestion in suggestions:
                file.write(suggestion + "\n")

        print(f"[{green}+{white}] Keywords saved to {magenta}{filename}{white}")

    def clean_filename(self, keyword):
        return "".join(c if c.isalnum() or c in ['.', '_'] else '_' for c in keyword)
