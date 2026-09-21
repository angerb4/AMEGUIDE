# Monthly Update Checklist – FAA AME Item 18 Decision Tool

**Goal:** Keep the tool aligned with the current FAA AME Guide with minimal effort.

FAA usually posts Guide updates on the **last Wednesday of each month** (before ~9 a.m. CT).  
Check: https://www.faa.gov/ame_guide

---

## Quick Monthly Process (15–30 minutes)

### 1. Check for changes
- Open https://www.faa.gov/ame_guide
- Look at the “AME ALERT” / current revision date
- Open the Archives and Updates PDF if a new revision is posted
- Note any changes to:
  - CACI worksheets (Asthma, Hypertension, Glaucoma, Migraine, Prediabetes, etc.)
  - Disposition tables for Item 18-related conditions
  - Medication lists (especially migraine, hypertension, asthma, antidepressants)

### 2. Update the tool (if needed)
Only change what actually moved.

**Easiest method – edit on GitHub:**
1. Go to your GitHub repository
2. Click `app.py` → pencil icon (Edit)
3. Make the specific criterion changes
4. Update the “Last verified” date near the top of the app
5. Commit with a message such as: `Update Migraine CACI criteria – Aug 2026 Guide`
6. Streamlit Cloud will automatically redeploy in 1–2 minutes

**Local method:**
1. Edit `app.py` on your computer
2. Test with `streamlit run app.py`
3. `git add app.py`
4. `git commit -m "Update [condition] to [date] Guide"`
5. `git push`

### 3. Update the “Last verified” date inside the app
Near the top of `app.py` there is a line like:
```python
LAST_VERIFIED = "August 26, 2026"
```
Change it to the new Guide revision date every time you update.

### 4. Quick smoke test
- Open the live Streamlit URL
- Select 18.a, 18.f, 18.h and walk through the radio buttons
- Confirm the new criteria appear correctly

---

## What usually changes
- Medication acceptability lists (most frequent)
- Lab thresholds (A1C, eGFR, FIB-4, etc.)
- New CACI conditions (rare)
- Clarifications to existing worksheets

## What almost never needs monthly work
- Basic branching structure (Issue / CACI / Defer)
- Item 18 letter order
- Liability disclaimer language

---

## Recommended calendar reminder
Set a recurring calendar event for the **last Thursday of each month**:
“Check FAA AME Guide for updates → update ame-item18-tool if needed”

---

## Important
Even after updating, the tool remains an **unofficial abbreviated aid**.  
The AME must still exercise independent judgment and may need the official PDF worksheet for unusual or edge cases.
