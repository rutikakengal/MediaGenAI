# MediaGenAI

English-Hindi Live Commentary Dataset

This repository contains a manually created English-Hindi live commentary dataset along with a Python script to generate Hindi translations. This dataset is intended for projects involving English ↔ Hindi translation, NLP, or live commentary analysis.

Dataset

data/english.txt – 200 English live commentary sentences

data/hindi.txt – Hindi translations generated using Google Translate

⚠️ Note: No freely available English-Hindi live commentary dataset was found online or on Hugging Face. This dataset was manually created for demonstration purposes.

Python Script

```1_download_dataset.py``` – This script:

Reads English commentary from ```english.txt```

Translates each line into Hindi using Google Translate

Saves the Hindi commentary into hindi.txt

Instructions

Clone this repository:
```
git clone <https://github.com/rutikakengal/MediaGenAI>
cd <your-repo-folder>
```

Create a virtual environment (optional but recommended):
```
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac
```

Install dependencies:
```
pip install googletrans==4.0.0-rc1
```

Run the script:
```
python 1_download_dataset.py
```

The translated Hindi commentary will be saved in ```data/hindi.txt.```
