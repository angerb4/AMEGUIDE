import re
from datetime import date
import streamlit as st

st.set_page_config(page_title="FAA AME Decision Tool", page_icon="✈️", layout="wide")

# FAA source links from the supplied 2026 Guide for Aviation Medical Examiners.
FAA = {
    "AME Guide home": "https://www.faa.gov/go/ameguide",
    "Aerospace Medical Disposition Tables": "https://www.faa.gov/ame_guide/dec_cons/disp",
    "CACI worksheets": "https://www.faa.gov/go/caci",
    "DNI/DNF medications": "https://www.faa.gov/go/dni",
    "Pharmaceuticals": "https://www.faa.gov/go/meds",
    "Antidepressant guidance": "https://www.faa.gov/go/ssri",
    "OSA protocol": "https://www.faa.gov/go/osa",
    "Diabetes—medication controlled": "https://www.faa.gov/go/diabetic",
    "Insulin / ITDM": "https://www.faa.gov/go/ITDM",
    "HIMS drug/alcohol monitoring": "https://www.faa.gov/go/hims-da",
    "14 CFR Part 67": "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-67",
    "14 CFR 61.53": "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-61#61.53",
    "MedXPress": "https://medxpress.faa.gov/",
    "FAA medical certification": "https://www.faa.gov/licenses_certificates/medical_certification",
}

# Exact medication examples and classes transcribed from the supplied Guide pages 625–628.
DNI = {
    "Angina medications": ["nitroglycerin", "isosorbide", "imdur", "ranolazine", "ranexa"],
    "Oral anticholinergics": ["atropine", "tolterodine", "detrol", "oxybutynin", "ditropan", "solifenacin", "vesicare", "benztropine", "cogentin"],
    "Cancer treatments": ["chemotherapy", "radiation therapy", "immunotherapy", "oncology treatment"],
    "Controlled substances": ["medical marijuana", "marijuana", "cannabis", "schedule i", "schedule ii", "schedule iii", "schedule iv", "schedule v"],
    "Diabetes medication—specific DNI": ["pramlintide", "symlin"],
    "Dopamine agonists": ["bromocriptine", "parlodel", "pramipexole", "mirapex", "ropinirole", "requip", "rotigotine", "neupro"],
    "Centrally acting antihypertensives": ["clonidine", "guanabenz", "methyldopa", "reserpine", "guanfacine"],
    "Mefloquine": ["mefloquine", "lariam"],
    "Psychiatric/psychotropic medication classes": ["antipsychotic", "mood stabilizer", "adhd medication", "stimulant", "tranquilizer", "antidepressant"],
    "Seizure medications": ["antiepileptic", "anticonvulsant", "seizure medication"],
    "High-dose steroids": ["prednisone >20", "prednisone 20 mg", "high dose steroid"],
    "Weight-loss medications—specific DNI": ["phentermine", "adipex", "fastin", "contrave", "bupropion + naltrexone"],
}
DNF = {
    "Sedating antihistamines": {"diphenhydramine": "60 hours", "benadryl": "60 hours", "doxylamine": "60 hours", "unisom": "60 hours", "chlorpheniramine": "5 days", "coricidin": "5 days", "clemastine": "5 days", "cetirizine": "48 hours", "levocetirizine": "48 hours"},
    "Anti-anxiety medications": {"alprazolam": "Verify current FAA guidance / defer if routine use", "xanax": "Verify current FAA guidance / defer if routine use", "lorazepam": "Verify current FAA guidance / defer if routine use", "ativan": "Verify current FAA guidance / defer if routine use", "temazepam": "72 hours", "restoril": "72 hours", "triazolam": "Verify current FAA guidance / defer if routine use"},
    "Muscle relaxants": {"carisoprodol": "Verify half-life / defer if routine use", "soma": "Verify half-life / defer if routine use", "cyclobenzaprine": "Verify half-life / defer if routine use", "flexeril": "Verify half-life / defer if routine use"},
    "Kava/kratom/valerian": {"kava": "Use general 5x half-life rule; consult FAA", "kratom": "Consult FAA", "valerian": "Consult FAA"},
    "Narcotic or non-narcotic pain medication": {"morphine": "Use general 5x half-life rule", "codeine": "Use general 5x half-life rule", "oxycodone": "Use general 5x half-life rule", "hydrocodone": "Use general 5x half-life rule", "tramadol": "Use general 5x half-life rule"},
    "Sleep aids": {"zolpidem": "24 hours", "ambien": "24 hours", "eszopiclone": "30 hours", "lunesta": "30 hours", "zaleplon": "12 hours", "sonata": "12 hours", "ramelteon": "24 hours", "rozerem": "24 hours", "zolpidem er": "24 hours", "zolpimist": "48 hours"},
    "Pre-medication/procedure drugs": {"pre-medication": "Do not fly until applicable recovery interval has elapsed", "sedation": "Do not fly until applicable recovery interval has elapsed", "anesthesia": "Do not fly until applicable recovery interval has elapsed"},
}

# 2026 CACI list from Guide page 502. Criteria are entered as editable worksheet rows.
CACI = {
    "Arthritis": ["Current detailed clinical progress note reviewed", "Stable; no changes recommended", "No significant functional limitation", "Acceptable diagnosis and medication", "HCQ/CQ status report reviewed if applicable"],
    "Asthma": ["Current detailed clinical progress note reviewed", "Symptoms ≤2 days/week", "Rescue inhaler ≤2 times/week", "Oral steroid exacerbations ≤2/year", "No inpatient hospitalization in last year", "Spirometry current and FEV1/FVC criteria met when required", "No monoclonal antibody for CACI"],
    "Bladder Cancer": ["Stable; no metastatic disease or muscle invasion", "Active treatment completed", "No concerning symptoms", "Surgery recovery complete if applicable", "No current chemotherapy/radiation; maintenance BCG/mitomycin timing addressed"],
    "Breast Cancer": ["DCIS/LCIS/Tis/Paget or other CACI-eligible pathology", "No invasive/metastatic disease", "No chemotherapy ever", "Treatment completed or stable", "Approved hormone medication tolerated without side effects"],
    "Carotid/Vertebral Artery Stenosis": ["Stable with no symptoms", "No clinically significant progression", "Bilateral stenosis ≤79%", "No DOAC/NOAC/warfarin for this condition", "Imaging within prior year", "ASA/Plavix/Brilinta regimen documented if used"],
    "Chronic Immune Thrombocytopenia (cITP)": ["Chronic >12 months", "Platelets stable ≥50,000/microL", "No bleeding requiring medical attention", "No splenectomy", "No antiplatelet/anticoagulant use", "CBC current and no anemia/leukopenia", "No treatment change"],
    "Chronic Kidney Disease": ["Two functioning kidneys", "Asymptomatic and stable", "eGFR ≥35", "Albumin trace/negative or ACR ≤29", "Hgb ≥10 and Hct ≥30%", "No dialysis/transplant anticipated", "Allowed hypertension medication only if applicable"],
    "CLL/SLL": ["Oncology follow-up ≥5 years", "Age at diagnosis ≥40", "Rai 0–1 and/or Binet A", "Asymptomatic with no active disease", "Observation only", "Hgb ≥11", "Platelets ≥100,000/microL", "Lymphocyte doubling time >6 months"],
    "Colitis/IBS": ["Stable with no flight-interfering effects", "No surgery in last 6 weeks", "None or mild symptoms", "No severe fatigue or activity limitation", "Acceptable diagnosis", "Medication and biologic observation/no-fly time documented"],
    "Colon/Colorectal Cancer": ["Stable and back to full activities", "No high-risk features", "No recurrence", "No metastatic disease", "TNM 0–III", "CEA criteria met", "CBC current and acceptable"],
    "Eosinophilic Esophagitis": ["Compliant and well-controlled", "Histologic remission <15 eos/hpf", "No fibrostenotic disease", "No food impaction in last 12 months or while treated", "Acceptable treatment and post-dose time documented"],
    "Essential Tremor": ["Diagnosis is essential tremor", "Stable with no progression", "No disabling tremor", "Not dependent on medication to function", "No medication or beta-blocker only"],
    "Glaucoma": ["Stable on current regimen", "Age at diagnosis ≥40", "Eligible glaucoma type", "No nerve damage or trabeculectomy", "CACI-eligible drops only", "No medication side effects", "IOP ≤23 mmHg both eyes", "Reliable formal visual fields with no defect"],
    "Hepatitis C—Chronic": ["Stable with no changes recommended", "No complications or symptoms", "No medication for condition", "Current labs", "AST, ALT, albumin and PT within 10% of normal"],
    "Hypertension": ["Stable ≥7 days; no changes recommended", "No symptoms", "BP ≤155/95", "No more than 3 acceptable medication components", "No medication side effects"],
    "Hypothyroidism": ["Stable", "No fatigue or mental-status impairment", "Acceptable thyroid medication", "TSH <10 within past year"],
    "Low Testosterone/Hypogonadism": ["Stable; no changes or flight-interfering side effects", "No phlebotomy required", "No VTE", "Hct ≤54%", "Acceptable medication and required ground trial completed"],
    "MASH/NASH": ["Controlled; no flight-interfering symptoms", "No cirrhosis", "Fibrosis criterion met: FIB-4 <2.68 or VCTE <8 kPa or MRE <2.55 kPa", "Acceptable medications only"],
    "Migraine/Chronic Headache": ["Stable; no management changes", "No more than 1 episode/month", "No more than 2 outpatient exacerbation visits/year", "No inpatient headache hospitalization", "Mild, non-disabling symptoms", "No neurologic impairment, vertigo, syncope, cognitive change or functionally significant visual symptoms", "Medication and no-fly times documented"],
    "Mitral Valve Repair": ["Repair ≥5 years ago for primary mitral disease", "Asymptomatic and stable", "No other cardiac condition", "No connective-tissue disorder/COPD/pulmonary HTN", "Echo within 24 months shows mild/no disqualifying findings"],
    "PCOS": ["Stable; no medication side effects", "Cardiovascular risk factors controlled", "OSA absent or adequately treated", "No depression/anxiety concern", "No diabetes or prolactinoma", "Acceptable medications"],
    "Prediabetes": ["Medication is for prediabetes, not diabetes", "Stable with no side effects", "No hypoglycemia requiring intervention", "One eligible medication only", "A1C ≤6.4% within 90 days and never ≥6.5%", "Required observation period completed"],
    "Primary Hemochromatosis": ["Stable and asymptomatic", "No end-organ or major comorbid disease", "Hgb ≥11", "Ferritin ≤150", "Dietary treatment or phlebotomy no more than monthly"],
    "Prostate Cancer": ["Stable with no spread or recurrence", "No metastatic disease", "Treatment complete or eligible surveillance", "PSA ≤20 without prostatectomy or ≤0.2 after prostatectomy", "No symptoms"],
    "Psoriasis": ["Stable, mild/moderate, no systemic symptoms or functional limitation", "Eligible subtype", "Acceptable medication", "Required biologic ground trial and post-dose time completed"],
    "Renal Cancer": ["Stable with no recurrence", "No chemotherapy, extracapsular extension, metastasis, stage 4, or paraneoplastic syndrome", "Surgery recovery complete", "No symptoms", "Full unrestricted activity"],
    "Retained Kidney Stone(s)": ["Asymptomatic and stable", "No increase in number/size", "Unlikely sudden incapacitation", "No complications", "No underlying recurrent-stone cause requiring disqualifying monitoring", "Treatment and imaging reviewed"],
    "Testicular Cancer": ["Stable with no spread or recurrence", "No metastatic disease", "Active treatment complete", "Surgery recovery complete", "No symptoms", "No current chemotherapy/radiation"],
    "Weight Loss Management": ["Medication is for weight loss, not diabetes", "Stable with no side effects", "No hypoglycemia requiring intervention", "One eligible medication only", "No history A1C ≥6.5%", "Required observation period completed"],
}

# Condition index derived from the supplied Guide contents and disposition sections.
CONDITIONS = {
    "Condition not listed": "Assess sudden/subtle incapacitation risk. Issue only if risk is not increased and rationale is documented; otherwise defer.",
    "Allergies/anaphylaxis": "Controlled acceptable treatment may issue; severe/recurrent reaction or anaphylaxis requires FAA review.",
    "Asthma": "Resolved/trigger-specific may issue; intermittent/mild persistent may use CACI; moderate/severe requires FAA review.",
    "COPD/emphysema/chronic bronchitis": "Disposition depends on GOLD stage, SpO2, FEV1, 6MWT, medication burden and steroids; generally defer.",
    "Obstructive sleep apnea": "Use OSA triage/protocol; treated OSA may issue when criteria are met; initial SI requires FAA decision.",
    "Coronary heart disease/MI/stent/CABG": "Specifically disqualifying history; defer for FAA Special Issuance review after required recovery and testing.",
    "Arrhythmia/AFib/flutter/pacemaker": "Use the exact cardiac disposition table and current monitor/echo/protocol requirements.",
    "Hypertension": "No medication or ≤3 acceptable medications may qualify for CACI; otherwise defer.",
    "Stroke/TIA/syncope/ULOC": "Recovery periods and neurologic/cardiac evaluation requirements apply; unexplained events require FAA review.",
    "Seizure/epilepsy": "Defer for FAA review; recovery period, MRI, EEG and seizure questionnaire may be required.",
    "Psychiatric/antidepressant/ADHD": "Use the specific psychiatric table, antidepressant protocol, ADHD fast/standard track and HIMS requirements.",
    "Substance abuse/dependence/DUI": "Defer when required; use the drug/alcohol tables and HIMS pathway.",
    "Diabetes/prediabetes/weight loss medication": "Diet-controlled diabetes may issue; medication-treated diabetes and insulin require FAA protocol/SI; prediabetes/weight loss may use CACI.",
    "Vision/eye conditions": "Apply class-specific acuity, color, field and ocular disposition tables; use eye forms/status summaries as specified.",
    "Hearing/ENT/vertigo": "Apply hearing standards and the ENT/vestibular disposition tables; current symptoms generally preclude issuance.",
    "Neurologic conditions": "Most require FAA neurologic evaluation and deferral; use condition-specific table.",
    "Cancer/neoplasm": "Use the exact cancer table; eligible low-risk cases may use CACI, while metastatic/high-risk disease requires FAA review.",
    "Kidney/renal disease/stones": "Use CKD, renal stone, transplant and renal cancer tables/CACI worksheets.",
    "Musculoskeletal/functional limitation": "Assess strength, range of motion, pain, dexterity and functional ability; MFT/SODA may be needed.",
}

EXAM_ITEMS = [
    ("Items 21–24", "Height, weight, SODA and SODA serial number"),
    ("Items 25–30", "Head/face/neck/scalp, nose, sinuses, mouth/throat, ears and tympanic membranes"),
    ("Items 31–34", "Eyes, ophthalmoscopy, pupils and ocular motility"),
    ("Item 35", "Lungs and chest"), ("Items 36–37", "Heart and vascular system"),
    ("Items 38–41", "Abdomen/viscera, anus, skin and genitourinary system"),
    ("Items 42–45", "Extremities, spine/musculoskeletal, marks/scars/tattoos and lymphatics"),
    ("Items 46–48", "Neurologic, psychiatric and general systemic findings"),
    ("Item 49", "Hearing"), ("Items 50–54", "Distant, near/intermediate, color, field and heterophoria vision"),
    ("Items 55–58", "Blood pressure, pulse, urine test and ECG when required"),
]
DECISIONS = ["Not applicable / no finding", "Issue—routine standards", "Issue—CACI criteria met", "Defer—FAA decision required", "Special Issuance/AASI pathway", "Deny—clear failure to meet standards"]


def issue(label, detail):
    st.session_state.setdefault("issues", []).append((label, detail))


def clear_state():
    st.session_state.clear()


def yes_no(label, key):
    return st.radio(label, ["Not assessed", "Yes", "No"], horizontal=True, key=key)


def medication_matches(text):
    t = text.lower()
    dni_hits = [(group, term) for group, terms in DNI.items() for term in terms if term in t]
    dnf_hits = [(group, term, wait) for group, terms in DNF.items() for term, wait in terms.items() if term in t]
    return sorted(set(dni_hits)), sorted(set(dnf_hits))


if "issues" not in st.session_state:
    st.session_state.issues = []

st.title("✈️ FAA AME Aeromedical Decision Tool")
st.warning("Decision support only. This is not an FAA application and cannot replace the current AME Guide, 14 CFR Part 67, AMCD/RFS instructions, disposition tables, CACI worksheets, AASI authorization letters or professional judgment.")

with st.sidebar:
    st.header("Applicant / exam")
    applicant = st.text_input("Applicant identifier")
    exam_date = st.date_input("Exam date", value=date.today())
    cert_class = st.selectbox("Certificate class", ["First", "Second", "Third"])
    prior_status = st.selectbox("Prior FAA status", ["No prior certificate", "Previously issued", "Previously deferred", "Current/previous SI or AASI", "SODA/LOE/other authorization"])
    st.button("Start new assessment", on_click=clear_state)
    st.divider()
    st.subheader("Official references")
    for name, url in FAA.items():
        st.markdown(f"[{name}]({url})")

st.caption(f"Assessment date: {exam_date}  |  Class: {cert_class}  |  Applicant: {applicant or 'not entered'}")

st.header("1. Application and history review")
h1, h2 = st.columns(2)
with h1:
    history_complete = st.checkbox("Items 1–20 reviewed and complete")
    applicant_certified = st.checkbox("Applicant certification/declaration verified")
    identity_verified = st.checkbox("Identity and MedXPress information verified")
with h2:
    records_available = st.checkbox("Relevant FAA, specialist, hospital and treatment records reviewed")
    disclosure_concern = st.checkbox("Potential omission, inconsistency or unresolved disclosure concern")
    st.multiselect("Reported changes since last exam", ["New diagnosis", "New medication", "Dose change", "Surgery/procedure", "Hospitalization/ER", "New symptoms", "Functional change", "No changes"])
if not history_complete or not applicant_certified or not identity_verified:
    issue("Application incomplete", "Complete and verify the applicable Items 1–20 workflow before final action.")
if disclosure_concern:
    issue("Disclosure concern", "Resolve the discrepancy and document source, clarification and disposition.")

st.header("2. Medication review — DNI/DNF flagging")
medications = st.text_area("List every prescription, OTC medication, supplement, dose, indication, last dose and recent changes", height=120, placeholder="Example: medication — dose — indication — last dose — stable since")
manual_med_status = st.selectbox("Manual status after checking the current FAA medication page", ["Not yet reviewed", "No DNI/DNF identified", "DNI identified", "DNF identified", "Both DNI and DNF identified", "Unlisted/new medication—consult FAA"])
dni_hits, dnf_hits = medication_matches(medications)
if dni_hits:
    st.error("DNI FLAG: a possible Do Not Issue medication or class was detected. The AME must not issue until the exact drug, indication and current FAA direction are verified.")
    for group, term in dni_hits:
        st.write(f"• **{group}:** `{term}`")
    issue("DNI medication", "Defer or obtain FAA direction/clearance as required. Do not issue solely from this tool.")
if dnf_hits:
    st.warning("DNF FLAG: a possible Do Not Fly medication was detected. Document the last dose, required post-dose interval, symptoms and return-to-flying instructions.")
    for group, term, wait in dnf_hits:
        st.write(f"• **{group}:** `{term}` — Guide interval/reference: **{wait}**")
    issue("DNF medication", "Counsel no flight/safety-related duties until the applicable FAA no-fly interval has elapsed and symptoms/side effects have resolved.")
if manual_med_status in ["DNI identified", "Both DNI and DNF identified", "Unlisted/new medication—consult FAA"]:
    issue("Medication status", "Manual review indicates FAA clearance or additional guidance is needed.")
if manual_med_status in ["DNF identified", "Both DNI and DNF identified"]:
    issue("No-fly interval", "Enter the exact current FAA interval and last-dose calculation in the AME notes.")
st.markdown(f"[{('Open current FAA DNI/DNF medication guidance')}]({FAA['DNI/DNF medications']})")
with st.expander("Medication documentation checklist"):
    for item in ["Exact generic and brand name verified", "Indication and underlying condition reviewed", "Dose/frequency/route documented", "Start/stop/change dates documented", "Side effects and functional impact assessed", "Initial ground trial/post-dose interval checked", "Current FAA guidance checked", "Applicant counseled under 14 CFR 61.53"]:
        st.checkbox(item, key=f"med_{item}")

st.header("3. Conditions and determination tables")
selected_conditions = st.multiselect("Select all reported, historical or discovered conditions", list(CONDITIONS))
for condition in selected_conditions:
    with st.expander(condition, expanded=True):
        st.caption(CONDITIONS[condition])
        result = st.radio("Disposition-table result", DECISIONS, key=f"disp_{condition}")
        st.text_area("Condition-specific evidence, table row, records and Item 60 notes", key=f"notes_{condition}", height=100)
        if result in ["Defer—FAA decision required", "Special Issuance/AASI pathway", "Deny—clear failure to meet standards"]:
            issue(condition, result)
        st.markdown(f"[{condition} — open current FAA Guide/disposition tables]({FAA['Aerospace Medical Disposition Tables']})")
if not selected_conditions:
    st.info("Select conditions to open radio-button disposition controls and direct FAA references.")

st.header("4. CACI worksheet workspace")
st.caption("Use the disposition table first. A CACI can be used only when every applicable current FAA worksheet criterion is satisfied and the applicant is otherwise qualified. Keep required supporting documents in the AME file as directed.")
selected_caci = st.multiselect("Select CACI worksheet(s) to complete", list(CACI))
for name in selected_caci:
    with st.expander(f"CACI — {name}", expanded=True):
        st.markdown(f"[Open the current FAA CACI worksheet index]({FAA['CACI worksheets']})")
        all_yes = True
        for i, criterion in enumerate(CACI[name]):
            answer = st.radio(criterion, ["Not assessed", "Yes", "No", "N/A—document rationale"], horizontal=True, key=f"caci_{name}_{i}")
            if answer in ["Not assessed", "No"]:
                all_yes = False
        st.text_area("Provider/report values, dates, tests, medication timing and worksheet notes", key=f"caci_notes_{name}", height=130)
        st.radio("Required Block 60 CACI statement", [f"CACI qualified {name}", f"Has current/previous SI/AASI but now CACI qualified {name}", f"NOT CACI qualified {name}; I have deferred"], key=f"caci_statement_{name}")
        if all_yes:
            st.success("All displayed criteria are marked clear. Confirm the exact current FAA worksheet and retain supporting documentation before issuing.")
        else:
            issue(f"CACI incomplete — {name}", "One or more worksheet criteria are missing or not met; do not use CACI issuance pathway until resolved.")

st.header("5. Physical examination — FAA Form 8500-8 Items 21–58")
for group, description in EXAM_ITEMS:
    st.checkbox(f"{group}: {description}", key=f"exam_{group}")
if not all(st.session_state.get(f"exam_{group}", False) for group, _ in EXAM_ITEMS):
    issue("Physical examination incomplete", "Complete and document the AME-performed examination and required ancillary testing.")
if st.checkbox("Abnormal or potentially aeromedically significant physical finding"):
    issue("Abnormal examination", "Document item number, finding, severity, functional effect, supporting records and applicable FAA pathway.")

st.header("6. Focused decision tools")
with st.expander("Syncope decision tool"):
    syncope_questions = ["Uncertain cause", "Incapacitated after event", "Additional unrelated event within 5 years", "History/injury raises aeromedical concern", "Cardiac syncope or cardiac pathology", "AME cannot obtain complete history or has concerns"]
    for i, q in enumerate(syncope_questions):
        if yes_no(q, f"syncope_{i}") == "Yes": issue("Syncope decision tool", q)
with st.expander("Brain injury decision tool"):
    brain_questions = ["Within past 5 years", "LOC/AOC/PTA ≥1 hour", "Seizure ≥24 hours after injury", "High-impact or penetrating mechanism", "Blood/hemosiderin, hematoma, diffuse axonal injury or skull fracture", "Current cognitive/neurologic symptoms or abnormal examination", "AME concerns"]
    for i, q in enumerate(brain_questions):
        if yes_no(q, f"brain_{i}") == "Yes": issue("Brain injury decision tool", q)
with st.expander("Anxiety/depression/related conditions decision tool"):
    psych_questions = ["Additional unacceptable psychiatric diagnosis", "Suicidal/homicidal ideation, attempt or self-harm", "Involuntary evaluation or court-ordered treatment", "ECT, TMS, ketamine or psychedelic therapy", "Psychiatric/substance hospitalization", "More than one episode", "Unresolved symptoms impairing safety duties", "Multiple/current mental-health medications within restricted period", "Treating clinician or AME concerns"]
    for i, q in enumerate(psych_questions):
        if yes_no(q, f"psych_{i}") == "Yes": issue("Psychiatric decision tool", q)

st.header("7. Overall workflow result")
unique_issues = list(dict.fromkeys(st.session_state.issues))
if any(label.startswith(("DNI", "DNF", "Medication", "Red flag")) for label, _ in unique_issues):
    decision = "🔴 DEFER / DO NOT ISSUE until medication and FAA requirements are resolved"
elif unique_issues:
    decision = "🟠 HOLD / DEFER or complete required records, tables and worksheets"
else:
    decision = "🟢 POTENTIALLY ISSUEABLE ONLY AFTER FINAL FAA GUIDE CHECK"
st.subheader(decision)
if unique_issues:
    st.subheader("Open items")
    for label, detail in unique_issues:
        st.markdown(f"- **{label}:** {detail}")
else:
    st.success("No automated issue was generated from the completed inputs.")

st.header("8. Final documentation and Item 60 draft")
pathway = st.selectbox("Primary pathway", ["Routine standards", "Disposition table", "CACI", "AASI follow-up", "Initial Special Issuance / FAA decision", "Condition or medication not listed—AMCD/RFS consultation"])
notes = st.text_area("AME notes / Block 60 draft", height=200, placeholder="Include item number, condition, medication name/dose/frequency/indication, records reviewed, exact disposition-table row, CACI status, DNI/DNF review, no-fly interval, counseling and final action.")
for item in ["Certificate class standards applied", "Current disposition table checked", "Exact CACI worksheet checked", "DNI/DNF page checked", "Last dose and no-fly interval documented", "AASI authorization reviewed if applicable", "Required records uploaded/retained", "Limitations entered correctly", "14-day AMCS transmission requirement addressed"]:
    st.checkbox(item, key=f"final_{item}")

with st.expander("All direct FAA references"):
    for name, url in FAA.items():
        st.markdown(f"- [{name}]({url})")

st.divider()
st.caption("Built from the supplied Guide for Aviation Medical Examiners, Version 08/26/2026. The PDF states that DNI/DNF lists and disposition tables are not all-inclusive; verify current FAA guidance before every certification decision.")
