import streamlit as st
from datetime import date
from urllib.parse import quote_plus

st.set_page_config(page_title="FAA AME Decision Tool", page_icon="✈️", layout="wide")

FAA = {
    "AME Guide home": "https://www.faa.gov/ame_guide",
    "Decision considerations / disposition tables": "https://www.faa.gov/ame_guide/dec_cons/disp",
    "CACI conditions and worksheets": "https://www.faa.gov/ame_guide/certification_ws",
    "DNI/DNF medications and no-fly times": "https://www.faa.gov/ame_guide/pharm/dni_dnf",
    "Pharmaceuticals home": "https://www.faa.gov/ame_guide/pharm",
    "Special Issuance / AASI": "https://www.faa.gov/ame_guide/special_iss",
    "AASI — all classes": "https://www.faa.gov/ame_guide/special_iss/all_classes",
    "14 CFR Part 67": "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-67",
    "FAA medical certification": "https://www.faa.gov/licenses_certificates/medical_certification",
    "FAA Form 8500-8 / MedXPress": "https://medxpress.faa.gov/",
    "Substances of dependence or abuse": "https://www.faa.gov/ame_guide/dec_cons/add",
}

# This is a routing aid, not a reproduction of the FAA's legally controlling tables.
CONDITIONS = {
    "Hypertension": "CACI / disposition table",
    "Diabetes mellitus": "Disposition table / Special Issuance",
    "Obstructive sleep apnea": "Disposition table / Special Issuance or AASI",
    "Coronary artery disease / myocardial infarction": "Defer / Special Issuance",
    "Arrhythmia / atrial fibrillation": "Disposition table / possible Special Issuance",
    "Stroke / TIA": "Defer / Special Issuance",
    "Seizure / epilepsy": "Defer / Special Issuance",
    "Depression / anxiety / psychiatric condition": "Medication pathway / disposition table",
    "Substance use disorder or dependence": "Defer / HIMS or Special Issuance",
    "Vision disorder": "Vision standards / disposition table",
    "Hearing disorder": "Hearing standards / disposition table",
    "Neurologic disorder": "Disposition table / possible Special Issuance",
    "Pulmonary disease / asthma / COPD": "CACI / disposition table / Special Issuance",
    "Cancer / malignancy": "CACI / disposition table / Special Issuance",
    "Kidney disease / renal stone": "CACI / disposition table / Special Issuance",
    "Musculoskeletal limitation": "Functional assessment / disposition table",
    "Other potentially aeromedically significant condition": "Consult AMCD/RFS",
}

CACI_CONDITIONS = [
    "Arthritis", "Asthma", "Bladder Cancer", "Breast Cancer",
    "Carotid / Vertebral Artery Stenosis", "C-ITP", "Chronic Kidney Disease",
    "CLL / SLL", "Colitis", "Colon / Colorectal Cancer", "Eosinophilic Esophagitis",
    "Essential Tremor", "Glaucoma", "Hepatitis C — Chronic", "Hypertension",
    "Hypothyroidism", "Low Testosterone / Hypogonadism", "MASH / NASH",
    "Migraine and Chronic Headache", "Mitral Valve Repair", "PCOS", "Prediabetes",
    "Primary Hemochromatosis", "Prostate Cancer", "Psoriasis", "Renal Cancer",
    "Retained Kidney Stone(s)", "Testicular Cancer", "Weight Loss Management",
]

# The FAA page states that the DNI/DNF lists are not all-inclusive. These keywords only trigger review.
DNI_KEYWORDS = {
    "investigational", "experimental", "clinical trial",
    "new drug", "new medication", "less than 12 months",
}
DNF_KEYWORDS = {
    "zolpidem", "ambien", "eszopiclone", "lunesta", "zaleplon", "sonata",
    "temazepam", "restoril", "diphenhydramine", "benadryl", "doxylamine",
    "opioid", "hydrocodone", "oxycodone", "codeine", "tramadol", "morphine",
    "muscle relaxant", "benzodiazepine", "alprazolam", "lorazepam", "diazepam",
    "clonazepam", "sedative", "sleep aid",
}

EXAM_ITEMS = [
    ("Items 21–24", "Height, weight, SODA, and SODA serial number"),
    ("Items 25–30", "Head, face, neck, scalp, nose, sinuses, mouth, throat, ears, and tympanic membranes"),
    ("Items 31–34", "Eyes, ophthalmoscopy, pupils, and ocular motility"),
    ("Item 35", "Lungs and chest"), ("Items 36–37", "Heart and vascular system"),
    ("Items 38–41", "Abdomen/viscera, anus, skin, and genitourinary system"),
    ("Items 42–45", "Extremities, spine/musculoskeletal, marks/scars/tattoos, and lymphatics"),
    ("Items 46–48", "Neurologic, psychiatric, and general systemic findings"),
    ("Item 49", "Hearing"), ("Items 50–54", "Distant, near/intermediate, color, field, and heterophoria vision"),
    ("Items 55–58", "Blood pressure, pulse, urinalysis, and ECG when required"),
]

DECISIONS = [
    "Not applicable / no finding", "Issue under routine standards", "Issue under CACI",
    "Defer — FAA decision required", "Special Issuance / AASI pathway", "Consult AMCD/RFS before action",
]

def link(label, url):
    return f"[{label}]({url})"

def add_issue(label, detail):
    st.session_state.setdefault("issues", []).append((label, detail))

def reset():
    st.session_state.clear()

st.title("✈️ FAA AME Aeromedical Decision Tool")
st.warning("Decision support only. This app does not issue a certificate, replace the current FAA AME Guide, or establish a diagnosis. The AME remains responsible for applying current FAA guidance, the certificate-class standards, disposition tables, CACI worksheets, authorizations, and FAA instructions.")

with st.sidebar:
    st.header("Applicant / exam")
    applicant = st.text_input("Applicant identifier", help="Use an internal identifier rather than unnecessary personal health information.")
    exam_date = st.date_input("Exam date", value=date.today())
    cert_class = st.selectbox("Certificate class", ["First", "Second", "Third"])
    prior_cert = st.selectbox("Prior FAA certification", ["No prior certificate", "Previously issued", "Previously deferred", "Special Issuance / AASI", "SODA or other authorization"])
    st.button("Start new assessment", on_click=reset)
    st.divider()
    st.subheader("Official references")
    for name, url in FAA.items():
        st.markdown(link(name, url))

if "issues" not in st.session_state:
    st.session_state.issues = []
st.caption(f"Assessment date: {exam_date}  |  Class: {cert_class}  |  Applicant: {applicant or 'not entered'}")

# 1. History
st.header("1. Applicant history and records")
h1, h2 = st.columns(2)
with h1:
    history_complete = st.checkbox("Items 1–20 reviewed and complete")
    signed = st.checkbox("Applicant certification/signature requirements verified")
    records_available = st.checkbox("Relevant prior FAA, specialist, hospital, and treatment records reviewed")
with h2:
    st.multiselect("Reported changes since last exam", ["New diagnosis", "New medication", "Surgery/procedure", "Hospitalization/ER visit", "New symptoms", "Change in function", "No changes reported"])
    disclosure_concerns = st.checkbox("Potential inconsistency, omission, or unresolved disclosure concern")
if not history_complete or not signed:
    add_issue("History incomplete", "Complete Items 1–20 and required applicant certification before final action.")
if disclosure_concerns:
    add_issue("Disclosure concern", "Resolve the discrepancy and document the source and disposition.")

# 2. Conditions and determination tables
st.header("2. Conditions and FAA determination tables")
selected_conditions = st.multiselect("Select all reported or discovered conditions", list(CONDITIONS))
if selected_conditions:
    st.markdown(link("Open current FAA Aerospace Medical Disposition Tables", FAA["Decision considerations / disposition tables"]))
    st.caption("Use the radio button for the current FAA table result after reviewing the exact condition, certificate class, and disposition criteria.")
    for condition in selected_conditions:
        c1, c2 = st.columns([1.35, 2])
        with c1:
            st.subheader(condition)
            st.caption(f"Initial routing aid: {CONDITIONS[condition]}")
        with c2:
            result = st.radio(f"Determination-table result — {condition}", DECISIONS, key=f"decision_{condition}")
            if result in ("Defer — FAA decision required", "Special Issuance / AASI pathway", "Consult AMCD/RFS before action"):
                add_issue(condition, result)
            if result == "Issue under CACI":
                st.session_state.setdefault("caci_selected", []).append(condition)
        st.divider()
else:
    st.info("Select conditions to open the determination-table decision controls.")

# 3. Medication review, with explicit DNI/DNF screening
st.header("3. Medication and substance review")
medications = st.text_area("List every prescription, OTC medication, supplement, dose, indication, and timing", height=110, placeholder="Example: medication — dose — indication — time taken — stable since")
med_lower = medications.lower()
auto_dni = sorted([k for k in DNI_KEYWORDS if k in med_lower])
auto_dnf = sorted([k for k in DNF_KEYWORDS if k in med_lower])

m1, m2 = st.columns(2)
with m1:
    known_status = st.radio("Medication status after checking the current FAA pharmaceutical guidance", ["No medications", "No DNI/DNF identified", "DNI medication identified", "DNF medication identified", "Both DNI and DNF concerns", "Unable to classify — consult FAA"], key="med_status")
with m2:
    st.markdown(link("Open FAA DNI/DNF medication guidance", FAA["DNI/DNF medications and no-fly times"]))
    st.markdown(link("Open FAA pharmaceuticals guidance", FAA["Pharmaceuticals home"]))

if auto_dni or auto_dnf:
    st.error("Potential DNI/DNF medication keyword detected — verify the exact medication and current FAA guidance before issuing.")
    if auto_dni:
        st.write("Potential DNI-related terms:", ", ".join(auto_dni))
    if auto_dnf:
        st.write("Potential DNF-related terms:", ", ".join(auto_dnf))
    add_issue("Potential DNI/DNF medication", "Verify the exact drug, indication, dose, timing, stability, adverse effects, and current FAA wait-time or clearance requirements.")

if known_status in ("DNI medication identified", "Both DNI and DNF concerns", "Unable to classify — consult FAA"):
    add_issue("DNI medication", "Do not issue based on this tool; review the current FAA DNI guidance and obtain FAA clearance or direction as required.")
if known_status in ("DNF medication identified", "Both DNI and DNF concerns"):
    add_issue("DNF medication", "Provide the applicant the current FAA no-fly interval and document last dose, required waiting period, symptoms, and return-to-fly instructions.")

with st.expander("Manual medication safety screen"):
    medication_flags = st.multiselect("Additional medication concerns", ["Sedation or impaired cognition", "New medication or dose change", "Unstable regimen", "Antidepressant / psychiatric medication", "Anticoagulant / antiplatelet", "Diabetes medication", "Weight-loss medication", "Medication interaction or duplicate therapy", "OTC or supplement not yet reviewed"])
    if medication_flags:
        add_issue("Medication safety review", "; ".join(medication_flags))
    no_fly_period = st.text_input("FAA-specified no-fly interval / clearance detail", placeholder="Enter the current FAA interval or 'not applicable' after verification")

# 4. CACI worksheets
st.header("4. CACI worksheet workflow")
st.markdown(link("Open FAA CACI Conditions and Worksheets", FAA["CACI conditions and worksheets"]))
caci_candidates = [c for c in CACI_CONDITIONS if c.lower() in " ".join(selected_conditions).lower()]
if caci_candidates:
    st.info("Potential CACI matches detected: " + ", ".join(caci_candidates))
selected_caci = st.multiselect("Select the exact CACI worksheet(s) being applied", CACI_CONDITIONS, default=caci_candidates)
for caci in selected_caci:
    with st.expander(f"CACI worksheet — {caci}", expanded=True):
        st.caption("Enter the worksheet data from the current FAA worksheet. The fields below are a documentation aid and do not reproduce or replace FAA criteria.")
        w1, w2 = st.columns(2)
        with w1:
            st.checkbox("Current diagnosis and treating-provider documentation verified", key=f"caci_dx_{caci}")
            st.checkbox("Required stability / observation period verified", key=f"caci_stable_{caci}")
            st.checkbox("Required tests, labs, imaging, or specialist report reviewed", key=f"caci_tests_{caci}")
        with w2:
            st.checkbox("No disqualifying symptoms, complications, or adverse effects identified", key=f"caci_clear_{caci}")
            st.checkbox("Certificate-class criteria reviewed", key=f"caci_class_{caci}")
            st.checkbox("Supporting documents retained in AME file", key=f"caci_docs_{caci}")
        st.text_area("CACI-specific findings / worksheet notes", key=f"caci_notes_{caci}", height=90)
        caci_complete = all(st.session_state.get(f"caci_{x}_{caci}", False) for x in ["dx", "stable", "tests", "clear", "class", "docs"])
        if not caci_complete:
            add_issue(f"CACI incomplete — {caci}", "Complete the exact current FAA worksheet and defer if its requirements are not met.")
        else:
            st.success("Documentation fields completed. Confirm every current FAA worksheet criterion before issuing.")

# 5. Physical exam
st.header("5. Physical examination — FAA Form 8500-8 Items 21–58")
st.caption("Mark each area only after it is personally performed and documented.")
exam_status = {group: st.checkbox(f"{group}: {description}", key=f"exam_{group}") for group, description in EXAM_ITEMS}
if not all(exam_status.values()):
    add_issue("Physical examination incomplete", "Complete and document all required examination items for the certificate class.")
if st.checkbox("One or more examination findings are abnormal or potentially aeromedically significant"):
    add_issue("Abnormal examination", "Document the specific finding, severity, function, records, and FAA pathway.")

# 6. Red flags
st.header("6. Aeromedical risk screen")
red_flags = st.multiselect("Select any present red flag", ["Sudden or subtle incapacitation risk", "Unexplained syncope or near-syncope", "Seizure or loss of consciousness", "Active chest pain or exertional symptoms", "Uncontrolled blood pressure", "Significant cognitive or psychiatric symptoms", "Unsafe medication adverse effects", "Unresolved neurologic deficit", "Uncorrected vision/hearing issue", "Unresolved substance concern", "Insufficient records", "None identified"], default=["None identified"])
for flag in red_flags:
    if flag != "None identified":
        add_issue("Red flag", flag)

# 7. Workflow disposition
st.header("7. Suggested workflow disposition")
unique_issues = list(dict.fromkeys(st.session_state.issues))
high_priority = any(label.startswith(("DNI", "DNF", "Potential DNI/DNF", "Red flag", "CACI incomplete")) for label, _ in unique_issues)
if high_priority or disclosure_concerns:
    decision, icon = "DEFER / obtain FAA guidance before issuing", "🔴"
elif unique_issues or not records_available:
    decision, icon = "HOLD — complete evaluation, records, and disposition review", "🟠"
else:
    decision, icon = "POTENTIALLY ISSUEABLE ONLY AFTER FINAL FAA GUIDE CHECK", "🟢"
st.subheader(f"{icon} {decision}")
st.write("This is a workflow prompt, not a certification determination. A DNI finding, unmet CACI criterion, unresolved DNF interval, or applicable FAA table instruction controls over this screen.")

if unique_issues:
    st.subheader("Open items")
    for label, detail in unique_issues:
        st.markdown(f"- **{label}:** {detail}")
else:
    st.success("No automated issue was generated from the selected inputs.")

# 8. Pathway and documentation
st.header("8. Pathway and documentation")
pathway = st.radio("Primary pathway requiring review", ["Routine certification review", "Disposition table", "CACI worksheet", "AASI", "Initial Special Issuance / AMCD or RFS", "Condition or medication not listed / consult AMCD or RFS"], horizontal=True)
pathway_links = {
    "Disposition table": FAA["Decision considerations / disposition tables"],
    "CACI worksheet": FAA["CACI conditions and worksheets"],
    "AASI": FAA["AASI — all classes"],
    "Initial Special Issuance / AMCD or RFS": FAA["Special Issuance / AASI"],
    "Condition or medication not listed / consult AMCD or RFS": FAA["AME Guide home"],
}
if pathway in pathway_links:
    st.markdown(link("Open the applicable FAA guidance", pathway_links[pathway]))
notes = st.text_area("AME notes / Block 60 draft", height=180, placeholder="Summarize history, exam findings, conditions, exact medications, DNI/DNF review, records, table/worksheet criteria, and final action.")
final_checks = st.multiselect("Final checks completed", ["Certificate-class standards applied", "Current disposition table checked", "Exact CACI worksheet checked", "CACI criteria met and documents retained", "DNI/DNF guidance checked", "No-fly interval documented", "Special Issuance/AASI authorization checked", "Required records attached or retained", "Limitations entered correctly", "Applicant advised of next steps", "AMCS entry reviewed"])

with st.expander("Direct FAA references"):
    for name, url in FAA.items():
        st.markdown(f"- {link(name, url)}")

st.divider()
st.caption("Version 2.0 — update this app whenever the FAA AME Guide, medication guidance, disposition tables, or CACI worksheets change. It is not an official FAA application and must not be used as the sole basis for certification.")

st.sidebar.divider()
st.sidebar.subheader("Find current FAA guidance")
search_term = st.sidebar.text_input("Condition or medication")
if search_term:
    st.sidebar.markdown(link("Search FAA AME Guide", "https://www.google.com/search?q=" + quote_plus("site:faa.gov/ame_guide " + search_term)))
