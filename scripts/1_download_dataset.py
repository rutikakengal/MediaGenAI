# Step 1: Import required libraries
from googletrans import Translator
import os

# Step 2: Make sure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Step 3: Read English commentary
with open("data/english.txt", "r", encoding="utf-8") as f:
    english_lines = f.readlines()

# Step 4: Translate English to Hindi
translator = Translator()
hindi_lines = []

print("🔁 Translating English commentary to Hindi...")

for line in english_lines:
    line = line.strip()  # remove extra spaces/newlines
    if line:  # only translate non-empty lines
        hindi_text = translator.translate(line, src='en', dest='hi').text
        hindi_lines.append(hindi_text)

# Step 5: Save Hindi commentary
with open("data/hindi.txt", "w", encoding="utf-8") as f:
    for line in hindi_lines:
        f.write(line + "\n")

print("✅ Hindi commentary saved to data/hindi.txt")
