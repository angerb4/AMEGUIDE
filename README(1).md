# FAA AME Item 18 Decision Tool (Streamlit)

Interactive abbreviated decision-support tool for Aviation Medical Examiners based on the FAA Guide for Aviation Medical Examiners (Item 18 medical history, CACI criteria, and disposition guidance).

## Features
- Select any combination of Item 18.a–18.y Yes answers
- Radio-button guided questions for each condition
- Full abbreviated CACI criteria checks (Hypertension, Asthma, Glaucoma, Migraine, etc.)
- Clear Issue / CACI Issue / Defer recommendations
- Suggested Item 60 wording
- Summary table of all decisions

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free on Streamlit Community Cloud

1. Create a free account at https://share.streamlit.io
2. Create a new GitHub repository and upload `app.py` + `requirements.txt`
3. In Streamlit Cloud, click "New app", select your repo, and deploy
4. Your tool will have a permanent public URL

## Important Disclaimer
This is an abbreviated clinical reference aid only. It does not replace the official FAA AME Guide or current CACI worksheets. Always verify the latest criteria on the FAA website before issuing a medical certificate.
