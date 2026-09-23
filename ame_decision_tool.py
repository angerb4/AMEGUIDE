import streamlit as st
from datetime import date
from urllib.parse import quote_plus

st.set_page_config(page_title="FAA AME Decision Tool", page_icon="✈️", layout="wide")

FAA = {
    "AME Guide home": "https://www.faa.gov/ame_guide",
    "Decision considerations / disposition tables": "https://www.faa.gov/ame_guide/dec_cons/disp",
    "CACI conditions and worksheets": "https://www.faa.gov/ame_guide/certification_ws",
    "Special Issuance / AASI": "https://www.faa.gov/ame_guide/special_iss",
    "AASI — all classes": "https://www.faa.gov/ame_guide/special_iss/all_classes",
    "14 CFR Part 67": "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-67",
    "FAA medical certification": "https://www.faa.gov/licenses_certificates/medical_certification",
    "FAA Form 8500-8 / MedXPress": "https://medxpress.faa.gov/",
    "Medication guidance search": "https://www.faa.gov/ame_guide/pharm",
    "Substances of dependence or abuse": "https://www.faa.gov/ame_guide/dec_cons/add",
}

# Routing labels are intentionally conservative. The current FAA table/worksheet controls.
CONDITIONS = {
    "None reported": {"route": "Routine review", "risk": "low", "note": "Continue the full history, examination, and certificate-class review."},
    "Hypertension": {"route": "Disposition table / possible CACI", "risk": "moderate", "note": "Check current blood pressure, treatment, symptoms, target-organ disease, and the current hypertension disposition/CACI worksheet."},
    "Diabetes mellitus": {"route": "Disposition table / possible Special Issuance", "risk": "high", "note": "Determine type, treatment, control, complications, hypoglycemia risk, and applicable FAA pathway."},
    "Obstructive sleep apnea": {"route": "Disposition table / Special Issuance or AASI", "risk": "high", "note": "Assess diagnosis, treatment adherence, effectiveness, daytime sleepiness, and required treating-provider documentation."},
    "Coronary artery disease / myocardial infarction": {"route": "Defer / Special Issuance pathway", "risk": "high", "note": "Do not issue solely from this screen; review the current cardiovascular disposition table and required testing."},
    "Arrhythmia / atrial fibrillation": {"route": "Disposition table / possible Special Issuance", "risk": "high", "note": "Assess symptoms, rhythm, treatment, anticoagulation, recurrence, and current FAA requirements."},
    "Stroke / TIA": {"route": "Defer / Special Issuance pathway", "risk": "high", "note": "Neurologic events require current FAA disposition guidance and supporting records."},
    "Seizure / epilepsy": {"route": "Defer / Special Issuance pathway", "risk": "high", "note": "Obtain neurologic history and records; do not issue without applying the current FAA pathway."},
    "Depression / anxiety / psychiatric condition": {"route": "Disposition table / medication pathway / possible Special Issuance", "risk": "high", "note": "Assess diagnosis, symptoms, stability, treatment, functional effect, suicidality, substance use, and current FAA requirements."},
    "Substance use disorder or dependence": {"route": "Defer / HIMS or Special Issuance pathway", "risk": "high", "note": "Use the current FAA substance guidance and obtain required monitoring/treatment documentation."},
    "Vision disorder": {"route": "Vision standards / disposition table", "risk": "moderate", "note": "Record acuity, correction, fields, color, ocular motility, and disease-specific findings by certificate class."},
    "Hearing disorder": {"route": "Hearing standards / disposition table", "risk": "moderate", "note": "Apply the certificate-class hearing standard and document test method and results."},
    "Neurologic disorder": {"route": "Disposition table / possible Special Issuance", "risk": "high", "note": "Screen for sudden or subtle incapacitation, cognitive effects, episodes, and treatment effects."},
    "Pulmonary disease / asthma / COPD": {"route": "Disposition table / possible CACI or Special Issuance", "risk": "moderate", "note": "Assess symptoms, exacerbations, spirometry or other required testing, medications, and functional capacity."},
    "Cancer / malignancy": {"route": "Disposition table / CACI or Special Issuance", "risk": "high", "note": "Identify cancer type, treatment, recurrence, complications, and the current disease-specific pathway."},
    "Kidney disease / renal stone": {"route": "Disposition table / CACI or Special Issuance", "risk": "moderate", "note": "Assess renal function, recurrence, obstruction, treatment, and current FAA criteria."},
    "Musculoskeletal limitation": {"route": "Examination / functional assessment / disposition table", "risk": "moderate", "note": "Assess range of motion, strength, pain, medication effects, and ability to safely operate controls."},
    "Other potentially aeromedically significant condition": {"route": "Condition-not-listed guidance / AMCD or RFS consultation", "risk": "high", "note": "A condition not listed may still require deferral if it can cause subtle or sudden incapacitation."},
}

MEDICATION_FLAGS = {
    "No medications": ("Routine medication review", "Confirm no undisclosed prescription, OTC, supplement, or adverse-effect issue."),
    "Stable medication with no apparent aeromedical effect": ("Review medication-specific FAA guidance", "Confirm indication, dose, stability, side effects, and whether the medication is specifically addressed by the current FAA guidance."),
    "Sedating medication / sleep aid / opioid": ("Do not issue until reviewed", "Assess sedation, cognition, reaction time, dependence risk, timing, and the current FAA pharmaceutical guidance."),
    "Antidepressant / psychiatric medication": ("Medication pathway / possible Special Issuance", "Apply the current FAA antidepressant and psychiatric guidance; evaluate diagnosis, stability, dose, symptoms, and treating-provider records."),
    "Anticoagulant / antiplatelet medication": ("Evaluate indication and underlying condition", "The medication may be less important than the condition being treated; assess bleeding risk and disease-specific FAA guidance."),
    "Diabetes medication": ("Diabetes pathway", "Identify drug, control, hypoglycemia risk, complications, and the current FAA diabetes guidance."),
    "Weight-loss medication": ("Medication-specific FAA guidance", "Review drug, indication, adverse effects, stability, and current FAA weight-management guidance."),
    "Multiple medications or unclear regimen": ("Defer/obtain clarification before issue", "Reconcile all medications and evaluate interactions, side effects, adherence, and underlying conditions."),
}

EXAM_ITEMS = [
    ("Items 21–24", "Height, weight, SODA, and SODA serial number"),
    ("Items 25–30", "Head, face, neck, scalp, nose, sinuses, mouth, throat, ears, and tympanic membranes"),
    ("Items 31–34", "Eyes, ophthalmoscopy, pupils, and ocular motility"),
    ("Item 35", "Lungs and chest"),
    ("Items 36–37", "Heart and vascular system"),
    ("Items 38–41", "Abdomen/viscera, anus, skin, and genitourinary system"),
    ("Items 42–45", "Extremities, spine/musculoskeletal, marks/scars/tattoos, and lymphatics"),
    ("Items 46–48", "Neurologic, psychiatric, and general systemic findings"),
    ("Item 49", "Hearing"),
    ("Items 50–54", "Distant, near/intermediate, color, field, and heterophoria vision"),
    ("Items 55–58", "Blood pressure, pulse, urinalysis, and ECG when required"),
]


def link(label, url):
    return f"[{label}]({url})"


def add_issue(label, detail):
    st.session_state.setdefault("issues", []).append((label, detail))


def reset():
    st.session_state.clear()

st.title("✈️ FAA AME Aeromedical Decision Tool")
st.warning("Decision support only. This app does not issue a certificate, replace the current FAA AME Guide, or establish a diagnosis. The AME remains responsible for applying current FAA guidance, 14 CFR Part 67, disposition tables, CACI worksheets, authorizations, and FAA instructions.")

with st.sidebar:
    st.header("Applicant / exam")
    applicant = st.text_input("Applicant identifier", help="Use an internal identifier rather than unnecessary personal health information.")
    exam_date = st.date_input("Exam date", value=date.today())
    cert_class = st.selectbox("Certificate class", ["First", "Second", "Third", "BasicMed / not a medical certificate"])
    prior_cert = st.selectbox("Prior FAA certification", ["No prior certificate", "Previously issued without limitation", "Previously deferred", "Special Issuance / AASI", "SODA or other authorization"])
    st.button("Start new assessment", on_click=reset)
    st.divider()
    st.subheader("Official references")
    for name, url in FAA.items():
        st.markdown(link(name, url))

if "issues" not in st.session_state:
    st.session_state.issues = []

st.caption(f"Assessment date: {exam_date}  |  Class: {cert_class}  |  Applicant: {applicant or 'not entered'}")

# Step 1: applicant history
st.header("1. Applicant history and records")
col1, col2 = st.columns(2)
with col1:
    history_complete = st.checkbox("Items 1–20 reviewed and complete")
    signed = st.checkbox("Applicant certification/signature requirements verified")
    records_available = st.checkbox("Relevant prior FAA, specialist, hospital, and treatment records reviewed")
with col2:
    new_changes = st.multiselect("Reported changes since last exam", ["New diagnosis", "New medication", "Surgery/procedure", "Hospitalization/ER visit", "New symptoms", "Change in function", "No changes reported"])
    disclosure_concerns = st.checkbox("Potential inconsistency, omission, or unresolved disclosure concern")
if not history_complete or not signed:
    add_issue("History incomplete", "Do not finalize the certification decision until Items 1–20 and required applicant certification are complete.")
if disclosure_concerns:
    add_issue("Disclosure concern", "Resolve the discrepancy and document the source and disposition before proceeding.")

# Step 2: medical conditions
st.header("2. Conditions and diagnoses")
selected_conditions = st.multiselect("Select all reported or discovered conditions", list(CONDITIONS), default=["None reported"])
condition_rows = []
for condition in selected_conditions:
    if condition == "None reported":
        continue
    c = CONDITIONS[condition]
    condition_rows.append({"Condition": condition, "Suggested route": c["route"], "Risk screen": c["risk"], "FAA-focused note": c["note"]})
    add_issue(condition, f"{c['route']}: {c['note']}")
if condition_rows:
    st.dataframe(condition_rows, use_container_width=True, hide_index=True)
else:
    st.success("No condition selected. Continue with the routine examination and full history review.")

# Step 3: medications
st.header("3. Medication and substance review")
medication_category = st.selectbox("Medication status", list(MEDICATION_FLAGS))
med_name = st.text_input("Medication(s), dose, indication, start date, and stability", placeholder="Document exact drug names and doses; include OTC drugs and supplements.")
med_route, med_note = MEDICATION_FLAGS[medication_category]
st.info(f"**Routing:** {med_route}\n\n{med_note}")
if medication_category not in ("No medications", "Stable medication with no apparent aeromedical effect"):
    add_issue("Medication review", f"{med_route}: {med_note}")

substance = st.selectbox("Alcohol, cannabis, tobacco, or other substance concern", ["No concern identified", "Use disclosed; assess aeromedical relevance", "Possible misuse/dependence", "Prior substance-related diagnosis or treatment"])
if substance != "No concern identified":
    add_issue("Substance review", "Apply current FAA substance guidance; evaluate diagnosis, impairment, treatment, monitoring, and required records.")

# Step 4: physical exam
st.header("4. Physical examination — FAA Form 8500-8 Items 21–58")
st.caption("Mark each area only after the examination is personally performed and documented.")
exam_status = {}
for group, description in EXAM_ITEMS:
    exam_status[group] = st.checkbox(f"{group}: {description}", key=f"exam_{group}")
exam_abnormal = st.checkbox("One or more examination findings are abnormal or potentially aeromedically significant")
if exam_abnormal:
    add_issue("Abnormal examination", "Document specific finding, laterality/severity, functional effect, records obtained, and the applicable FAA disposition pathway.")

# Step 5: red flags
st.header("5. Aeromedical risk screen")
red_flags = st.multiselect("Select any present red flag", [
    "Sudden or subtle incapacitation risk", "Unexplained syncope or near-syncope", "Seizure or loss of consciousness", "Active chest pain or exertional symptoms", "Uncontrolled blood pressure", "Significant cognitive or psychiatric symptoms", "Unsafe medication adverse effects", "Unresolved neurologic deficit", "Uncorrected vision/hearing issue", "Unresolved substance concern", "Insufficient records for a known condition", "None identified"
], default=["None identified"])
for flag in red_flags:
    if flag != "None identified":
        add_issue("Red flag", flag)

# Step 6: decision engine
st.header("6. Suggested workflow disposition")
issue_labels = {x[0] for x in st.session_state.issues}
high_risk = any(CONDITIONS.get(c, {}).get("risk") == "high" for c in selected_conditions)
has_red_flag = any(x != "None identified" for x in red_flags)
exam_incomplete = not all(exam_status.values())

if has_red_flag or high_risk or disclosure_concerns:
    decision = "DEFER / obtain FAA guidance before issuing"
    color = "🔴"
elif issue_labels or exam_incomplete or not records_available:
    decision = "HOLD — complete evaluation, records, and disposition review"
    color = "🟠"
else:
    decision = "POTENTIALLY ISSUEABLE ONLY AFTER FINAL FAA GUIDE CHECK"
    color = "🟢"

st.subheader(f"{color} {decision}")
st.write("This label is a workflow prompt, not a certification determination. Apply the current certificate-class standards and the exact FAA table or worksheet before taking action.")

if st.session_state.issues:
    st.subheader("Open items")
    for label, detail in st.session_state.issues:
        st.markdown(f"- **{label}:** {detail}")
else:
    st.success("No automated issue was generated from the selected inputs.")

# Explicit FAA routing
st.header("7. FAA pathway selector")
pathway = st.radio("Select the pathway requiring review", ["Routine certification review", "Disposition table", "CACI worksheet", "AME-Assisted Special Issuance (AASI)", "Initial Special Issuance / AMCD or RFS", "Condition not listed / consult AMCD or RFS"], horizontal=True)
if pathway == "Disposition table":
    st.markdown(link("Open FAA Aerospace Medical Disposition Tables", FAA["Decision considerations / disposition tables"]))
elif pathway == "CACI worksheet":
    st.markdown(link("Open FAA CACI Conditions and Worksheets", FAA["CACI conditions and worksheets"]))
elif pathway == "AME-Assisted Special Issuance (AASI)":
    st.markdown(link("Open FAA AASI guidance", FAA["AASI — all classes"]))
elif pathway == "Initial Special Issuance / AMCD or RFS":
    st.markdown(link("Open FAA Special Issuance guidance", FAA["Special Issuance / AASI"]))
elif pathway == "Condition not listed / consult AMCD or RFS":
    st.markdown(link("Open FAA disposition-table guidance", FAA["Decision considerations / disposition tables"]))

# Documentation builder
st.header("8. Documentation and final review")
notes = st.text_area("AME notes / Block 60 draft", height=160, placeholder="Summarize history, exam findings, condition status, medications, records reviewed, applicable FAA guidance, and final action.")
final_checks = st.multiselect("Final checks completed", [
    "Certificate class standards applied", "Current disposition table checked", "CACI criteria checked when applicable", "Special Issuance/AASI authorization checked when applicable", "Medication guidance checked", "Required records attached or retained", "Limitations entered correctly", "Applicant advised of next steps", "AMCS entry reviewed"
])

with st.expander("Direct FAA references"):
    for name, url in FAA.items():
        st.markdown(f"- {link(name, url)}")

st.divider()
st.caption("Version 1.0 — review and update this app whenever the FAA AME Guide changes. It is not an official FAA application and must not be used as the sole basis for certification.")

# Optional query helper for a condition or drug not represented above.
st.sidebar.divider()
st.sidebar.subheader("Find current FAA guidance")
search_term = st.sidebar.text_input("Condition or medication")
if search_term:
    st.sidebar.markdown(link("Search the FAA AME Guide", "https://www.google.com/search?q=" + quote_plus("site:faa.gov/ame_guide " + search_term)))
