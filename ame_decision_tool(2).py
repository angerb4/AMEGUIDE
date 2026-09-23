import streamlit as st
from dataclasses import dataclass
from typing import Optional

st.set_page_config(page_title="FAA AME Disposition Tool", page_icon="✈️", layout="wide")

FAA = {
    "AME Guide home": "https://www.faa.gov/ame_guide",
    "Disposition tables": "https://www.faa.gov/ame_guide/dec_cons/disp",
    "CACI worksheets": "https://www.faa.gov/ame_guide/certification_ws",
    "DNI/DNF medications": "https://www.faa.gov/ame_guide/pharm/dni_dnf",
    "Pharmaceutical guidance": "https://www.faa.gov/ame_guide/pharm",
    "Special Issuance/AASI": "https://www.faa.gov/ame_guide/special_iss",
    "14 CFR Part 67": "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-67",
}

# FAA disposition-table pages. The FAA table controls; links are supplied for verification.
ITEMS = {
    "Item 25 — Head, face, neck, scalp": "https://www.faa.gov/ame_guide/dec_cons/disp/item25",
    "Item 26 — Nose": "https://www.faa.gov/ame_guide/dec_cons/disp/item26",
    "Item 27 — Sinuses": "https://www.faa.gov/ame_guide/dec_cons/disp/item27",
    "Item 28 — Mouth and throat": "https://www.faa.gov/ame_guide/dec_cons/disp/item28",
    "Item 29 — Ear": "https://www.faa.gov/ame_guide/dec_cons/disp/item29",
    "Item 30 — Ear drums": "https://www.faa.gov/ame_guide/dec_cons/disp/item30",
    "Item 31 — Eyes": "https://www.faa.gov/ame_guide/dec_cons/disp/item31",
    "Item 32 — Ophthalmoscopic": "https://www.faa.gov/ame_guide/dec_cons/disp/item32",
    "Item 33 — Pupils": "https://www.faa.gov/ame_guide/dec_cons/disp/item33",
    "Item 34 — Ocular motility": "https://www.faa.gov/ame_guide/dec_cons/disp/item34",
    "Item 35 — Lungs and chest": "https://www.faa.gov/ame_guide/dec_cons/disp/item35",
    "Item 36 — Heart": "https://www.faa.gov/ame_guide/dec_cons/disp/item36",
    "Item 37 — Vascular system": "https://www.faa.gov/ame_guide/dec_cons/disp/item37",
    "Item 38 — Abdomen and viscera": "https://www.faa.gov/ame_guide/dec_cons/disp/item38",
    "Item 39 — Anus": "https://www.faa.gov/ame_guide/dec_cons/disp/item39",
    "Item 40 — Skin": "https://www.faa.gov/ame_guide/dec_cons/disp/item40",
    "Item 41 — Genitourinary system": "https://www.faa.gov/ame_guide/dec_cons/disp/item41",
    "Item 42 — Upper and lower extremities": "https://www.faa.gov/ame_guide/dec_cons/disp/item42",
    "Item 43 — Spine and other musculoskeletal": "https://www.faa.gov/ame_guide/dec_cons/disp/item43",
    "Item 44 — Identifying body marks, scars, tattoos": "https://www.faa.gov/ame_guide/dec_cons/disp/item44",
    "Item 45 — Lymphatics": "https://www.faa.gov/ame_guide/dec_cons/disp/item45",
    "Item 46 — Neurologic": "https://www.faa.gov/ame_guide/dec_cons/disp/item46",
    "Item 47 — Psychiatric conditions": "https://www.faa.gov/ame_guide/dec_cons/disp/item47",
    "Item 48 — General systemic": "https://www.faa.gov/ame_guide/dec_cons/disp/item48",
    "Item 49 — Hearing": "https://www.faa.gov/ame_guide/dec_cons/disp/item49",
    "Item 50 — Distant vision": "https://www.faa.gov/ame_guide/dec_cons/disp/item50",
    "Item 51 — Near and intermediate vision": "https://www.faa.gov/ame_guide/dec_cons/disp/item51",
    "Item 52 — Color vision": "https://www.faa.gov/ame_guide/dec_cons/disp/item52",
    "Item 53 — Field of vision": "https://www.faa.gov/ame_guide/dec_cons/disp/item53",
    "Item 54 — Heterophoria": "https://www.faa.gov/ame_guide/dec_cons/disp/item54",
    "Item 55 — Blood pressure": "https://www.faa.gov/ame_guide/dec_cons/disp/item55",
    "Item 56 — Pulse": "https://www.faa.gov/ame_guide/dec_cons/disp/item56",
    "Item 57 — Urinalysis": "https://www.faa.gov/ame_guide/dec_cons/disp/item57",
    "Item 58 — ECG": "https://www.faa.gov/ame_guide/dec_cons/disp/item58",
}

# These are screening labels, not substitutes for the live FAA table text.
CONDITIONS = {
    "Item 25 — Head, face, neck, scalp": ["No abnormality", "Head/face/neck mass or lesion", "Significant trauma or deformity", "Other finding"],
    "Item 26 — Nose": ["No abnormality", "Chronic obstruction or deformity", "Polyps or significant disease", "Other finding"],
    "Item 27 — Sinuses": ["No abnormality", "Recurrent/chronic sinus disease", "Active infection or significant obstruction", "Other finding"],
    "Item 28 — Mouth and throat": ["No abnormality", "Significant oral/oropharyngeal disease", "Airway-related abnormality", "Other finding"],
    "Item 29 — Ear": ["No abnormality", "Chronic ear disease", "Infection, drainage, or obstruction", "Other finding"],
    "Item 30 — Ear drums": ["Normal", "Perforation/scarring/retraction", "Active middle-ear disease", "Other finding"],
    "Item 31 — Eyes": ["No abnormality", "Diplopia or significant ocular disease", "Recent ocular surgery or unresolved symptoms", "Other finding"],
    "Item 32 — Ophthalmoscopic": ["Normal", "Stable documented finding", "Unexplained or progressive abnormality", "Other finding"],
    "Item 33 — Pupils": ["Normal", "Stable documented anisocoria", "Afferent pupillary or unexplained abnormality", "Other finding"],
    "Item 34 — Ocular motility": ["Normal", "Stable controlled finding", "Diplopia, limitation, or nystagmus affecting function", "Other finding"],
    "Item 35 — Lungs and chest": ["Normal", "Stable asthma/reactive airway disease", "COPD or significant pulmonary disease", "Unexplained symptoms/abnormal exam"],
    "Item 36 — Heart": ["Normal", "Hypertension without red flags", "Coronary disease, infarction, cardiomyopathy, or valve disease", "Arrhythmia or unexplained cardiac finding"],
    "Item 37 — Vascular system": ["Normal", "Stable peripheral vascular condition", "Aneurysm, significant stenosis, thrombosis, or vascular event", "Other finding"],
    "Item 38 — Abdomen and viscera": ["Normal", "Stable non-limiting condition", "Significant liver, gastrointestinal, or abdominal disease", "Unexplained mass or abnormality"],
    "Item 39 — Anus": ["No disposition / no significant finding", "Significant finding", "Unclear or functionally significant finding"],
    "Item 40 — Skin": ["Normal/minor finding", "Stable dermatologic disease", "Malignancy or systemic significance", "Medication/treatment creates aeromedical concern"],
    "Item 41 — Genitourinary system": ["Normal", "Stable condition", "Renal disease, recurrent stone, malignancy, or significant dysfunction", "Unclear finding"],
    "Item 42 — Upper and lower extremities": ["Normal", "Stable limitation with full safe function", "Loss of function, weakness, or unsafe control operation", "Unclear finding"],
    "Item 43 — Spine and other musculoskeletal": ["Normal", "Stable condition without functional impairment", "Limitation, neurologic deficit, or sedating treatment", "Unclear finding"],
    "Item 44 — Body marks, scars, tattoos": ["No aeromedical significance", "Finding requires documentation", "Finding suggests unresolved injury/disease", "Other finding"],
    "Item 45 — Lymphatics": ["Normal", "Stable documented condition", "Lymphadenopathy or hematologic disease requiring evaluation", "Unclear finding"],
    "Item 46 — Neurologic": ["Normal", "Stable condition explicitly addressed by FAA guidance", "Seizure, TIA/stroke, unexplained episode, or significant deficit", "Unclear neurologic finding"],
    "Item 47 — Psychiatric conditions": ["No condition", "Stable condition on an FAA-recognized pathway", "Active symptoms, suicidality, psychosis, impairment, or unclear diagnosis", "Substance-related concern"],
    "Item 48 — General systemic": ["Normal", "Stable condition with applicable pathway", "Cancer, endocrine, metabolic, or systemic disease needing FAA review", "Unexplained symptoms or abnormality"],
    "Item 49 — Hearing": ["Meets standard", "Does not meet standard but formal evaluation may apply", "Hearing loss with no qualifying pathway", "Unclear test/result"],
    "Item 50 — Distant vision": ["Meets applicable class standard", "Does not meet standard; correction/referral may resolve", "Unexplained or progressive visual loss", "Unclear result"],
    "Item 51 — Near/intermediate vision": ["Meets applicable class standard", "Does not meet standard; correction may resolve", "Unexplained or progressive visual loss", "Unclear result"],
    "Item 52 — Color vision": ["Passes applicable test", "Fails screening; alternative testing/SODA pathway may apply", "No qualifying pathway identified", "Unclear test/result"],
    "Item 53 — Field of vision": ["Normal/within standard", "Defect may have an accepted evaluation pathway", "Significant unexplained defect", "Unclear result"],
    "Item 54 — Heterophoria": ["Within standard", "Outside standard but further evaluation may apply", "Diplopia or functionally significant abnormality", "Unclear result"],
    "Item 55 — Blood pressure": ["Within FAA limit and otherwise qualified", "Elevated; repeat/recheck pathway needed", "Uncontrolled, unevaluated, unacceptable medication, or adverse effects", "Unclear status"],
    "Item 56 — Pulse": ["Normal/clinically acceptable", "Stable explained abnormality", "Unexplained significant bradycardia/tachycardia or symptoms", "Unclear status"],
    "Item 57 — Urinalysis": ["Normal/acceptable", "Minor or explainable abnormality", "Significant renal/metabolic finding", "Unclear test/result"],
    "Item 58 — ECG": ["Not required or acceptable", "Abnormality with documented evaluation", "Significant unexplained abnormality", "Unclear result"],
}

# FAA CACI worksheet names from the current CACI index.
CACI = [
    "Arthritis", "Asthma", "Bladder Cancer", "Breast Cancer", "Carotid/Vertebral Artery Stenosis",
    "C-ITP", "Chronic Kidney Disease", "CLL/SLL", "Colitis", "Colon/Colorectal Cancer",
    "Eosinophilic Esophagitis", "Essential Tremor", "Glaucoma", "Chronic Hepatitis C", "Hypertension",
    "Hypothyroidism", "Low Testosterone Hypogonadism", "MASH/NASH", "Migraine and Chronic Headache",
    "Mitral Valve Repair", "PCOS", "Prediabetes", "Primary Hemochromatosis", "Prostate Cancer",
    "Psoriasis", "Renal Cancer", "Retained Kidney Stone(s)", "Testicular Cancer", "Weight Loss Management",
]

# FAA list is intentionally limited to DNI/DNF categories; ordinary medications are not listed here.
DNI_DNF = {
    "Investigational/experimental study drug": "DNI — do not issue; contact RFS/AMCD.",
    "FDA-approved drug class less than 12 months ago": "DNI — generally requires FAA review; contact RFS/AMCD.",
    "Other medication appearing on the FAA DNI/DNF list": "Open the current FAA list and verify the exact drug, dose, indication, and required no-fly interval.",
}


def link(label, url):
    return f"[{label}]({url})"


def add_result(section, result, detail=""):
    st.session_state.setdefault("results", []).append({"section": section, "result": result, "detail": detail})


def reset():
    st.session_state.clear()

st.title("✈️ FAA AME Disposition / CACI Decision Tool")
st.warning("Decision support only. This app does not issue a medical certificate and does not replace the current FAA AME Guide, disposition tables, CACI worksheets, 14 CFR Part 67, or RFS/AMCD instructions. When the live FAA source conflicts with this interface, follow the FAA source.")

with st.sidebar:
    st.header("FAA references")
    for label, url in FAA.items():
        st.markdown(link(label, url))
    st.divider()
    if st.button("Reset assessment", use_container_width=True):
        reset()
        st.rerun()

st.subheader("1. DNI / DNF medication screen")
st.caption("This section intentionally screens only medication categories covered by the FAA Do Not Issue / Do Not Fly guidance. It is not a general medication database.")
med_status = st.radio("Is the applicant prescribed, taking, or recently stopped any medication appearing on the current FAA DNI/DNF list?", ["No", "Yes", "Unknown / list not verified"], horizontal=True, key="med_status")
if med_status == "Yes":
    med_type = st.selectbox("Select the applicable FAA DNI/DNF category", list(DNI_DNF), key="med_type")
    st.error(DNI_DNF[med_type])
    st.markdown(link("Open current FAA DNI/DNF medication list", FAA["DNI/DNF medications"]))
    add_result("Medication", "DEFER / DO NOT ISSUE", f"{med_type}. Verify current FAA list and contact RFS/AMCD as required.")
elif med_status == "Unknown / list not verified":
    st.warning("Do not make an issue decision until the exact medication is checked against the current FAA DNI/DNF guidance.")
    add_result("Medication", "HOLD / VERIFY", "Exact medication and current FAA DNI/DNF status not verified.")
else:
    add_result("Medication", "No DNI/DNF medication reported", "Continue with condition review and all other required medication/medical-history evaluation.")

st.subheader("2. Disposition-table condition review")
st.caption("Review every applicable examination/history item. Select the closest FAA disposition-table screening category, then open the live table before making the actual decision.")
selected_items = st.multiselect("Select the FAA items with a reported history or abnormal finding", list(ITEMS), key="selected_items")
for item in selected_items:
    st.markdown(f"### {item}")
    st.markdown(link("Open FAA disposition table", ITEMS[item]))
    choice = st.radio("Finding / pathway", CONDITIONS[item], key=f"condition_{item}")
    if choice.startswith("No ") or choice.startswith("Normal") or choice.startswith("Meets") or choice.startswith("Within") or choice.startswith("Passes") or choice.startswith("Not required") or choice.startswith("No condition"):
        disposition = "POTENTIAL ISSUE — verify all FAA criteria and otherwise-qualified status"
    elif "CACI" in choice or "further evaluation" in choice or "repeat" in choice or "formal" in choice or "Stable" in choice or "Minor" in choice or "correction" in choice or "alternative" in choice:
        disposition = "REVIEW FAA TABLE / CACI OR REQUIRED DOCUMENTATION"
    else:
        disposition = "DEFER / CONSULT FAA"
    st.radio("Tool routing", [disposition], key=f"route_{item}", disabled=True)
    notes = st.text_input("AME notes / required records", key=f"notes_{item}")
    add_result(item, disposition, notes)

st.subheader("3. CACI pathway")
caci_choice = st.selectbox("Is a CACI condition implicated by the disposition table?", ["No CACI implicated", "Yes — select worksheet", "Uncertain — review CACI index"], key="caci_choice")
if caci_choice == "Yes — select worksheet":
    caci = st.selectbox("CACI worksheet", CACI, key="caci")
    st.markdown(link("Open FAA CACI worksheet index", FAA["CACI worksheets"]))
    st.info("Complete the selected FAA worksheet exactly as published. Every required criterion must be satisfied, the condition must be otherwise qualified, and supporting documentation must be retained as required by the worksheet.")
    caci_answers = {}
    for prompt in ["Diagnosis and required history criteria satisfied?", "Required treating-provider records available and current?", "Required testing/results within worksheet parameters?", "No disqualifying symptoms, complications, or adverse medication effects?", "Applicant otherwise qualified for the requested class?"]:
        caci_answers[prompt] = st.radio(prompt, ["Yes", "No", "Unknown / incomplete"], horizontal=True, key=f"caci_{prompt}")
    if all(v == "Yes" for v in caci_answers.values()):
        st.success("CACI pathway appears complete for tool purposes. Verify the live worksheet and document the FAA-required findings before issuing.")
        add_result("CACI", "POTENTIAL ISSUE UNDER CACI — VERIFY LIVE WORKSHEET", caci)
    else:
        st.error("CACI criteria are not all satisfied or are incomplete: defer and submit/review supporting documentation according to the FAA pathway.")
        add_result("CACI", "DEFER — CACI CRITERIA NOT COMPLETE", caci)
elif caci_choice == "Uncertain — review CACI index":
    st.markdown(link("Open FAA CACI worksheet index", FAA["CACI worksheets"]))
    add_result("CACI", "HOLD / REVIEW CACI INDEX", "Determine whether an applicable worksheet exists before deciding.")

st.subheader("4. Assessment summary")
results = st.session_state.get("results", [])
if results:
    for row in results:
        if "DEFER" in row["result"] or "DO NOT ISSUE" in row["result"]:
            st.error(f"**{row['section']}: {row['result']}** — {row['detail']}")
        elif "HOLD" in row["result"] or "REVIEW" in row["result"]:
            st.warning(f"**{row['section']}: {row['result']}** — {row['detail']}")
        else:
            st.success(f"**{row['section']}: {row['result']}** — {row['detail']}")
else:
    st.info("Complete the medication and condition screens to generate a summary.")

st.divider()
st.caption("The FAA states that disposition tables are not all-inclusive and that an AME must consult the FAA when a condition requires deferral or is not listed and may cause subtle or sudden incapacitation. Last verified FAA source pages should be checked at every use.")