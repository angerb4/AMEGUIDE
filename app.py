import streamlit as st

st.set_page_config(
    page_title="FAA AME Item 18 Decision Tool",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 1.8rem; font-weight: 700; color: #1F4E79; margin-bottom: 0.2rem;}
    .sub-header {font-size: 1.0rem; color: #555; margin-bottom: 1.5rem;}
    .issue-box {background-color: #C6EFCE; padding: 1rem; border-radius: 8px; border-left: 5px solid #006100; margin: 0.8rem 0;}
    .defer-box {background-color: #FFC7CE; padding: 1rem; border-radius: 8px; border-left: 5px solid #9C0006; margin: 0.8rem 0;}
    .caci-box {background-color: #DDEBF7; padding: 1rem; border-radius: 8px; border-left: 5px solid #1F4E79; margin: 0.8rem 0;}
    .info-box {background-color: #FFF2CC; padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0;}
    .stRadio > label {font-weight: 500;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">✈️ FAA AME Item 18 Decision Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Abbreviated interactive protocol based on the Guide for Aviation Medical Examiners. For clinical reference only — always verify current FAA worksheets.</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("How to use")
    st.markdown("""
    1. Select every Item 18 item the airman marked **Yes**.
    2. Answer the radio-button questions for each selected condition.
    3. Review the disposition, CACI status, and Item 60 wording.
    4. When finished, scroll to the **Summary** at the bottom.
    """)
    st.divider()
    st.caption("This tool is an abbreviated clinical aid. It does not replace the official FAA AME Guide or current CACI worksheets.")
    st.caption("Always confirm the latest criteria at faa.gov/ame_guide before issuing.")

# ========== ITEM 18 SELECTION ==========
st.header("1. Select Item 18 Yes Answers")

item18_options = {
    "18.a": "Frequent or severe headaches",
    "18.b": "Dizziness or fainting spell",
    "18.c": "Unconsciousness for any reason",
    "18.d": "Eye or vision trouble except glasses",
    "18.e": "Hay fever or allergy",
    "18.f": "Asthma or lung disease",
    "18.g": "Heart or vascular trouble",
    "18.h": "High or low blood pressure",
    "18.i": "Stomach, liver, or intestinal trouble",
    "18.j": "Kidney stone or blood in urine",
    "18.k": "Diabetes",
    "18.l": "Neurological disorders (epilepsy, seizures, stroke, paralysis, etc.)",
    "18.m": "Mental disorders of any sort (depression, anxiety, etc.)",
    "18.n": "Substance dependence / failed drug test / substance abuse (last 2 years)",
    "18.o": "Alcohol dependence or abuse",
    "18.p": "Suicide attempt",
    "18.q": "Motion sickness requiring medication",
    "18.r": "Military medical discharge",
    "18.s": "Medical rejection by military service",
    "18.t": "Rejection for life or health insurance",
    "18.u": "Admission to hospital",
    "18.v": "Arrests / convictions / administrative actions (especially DUI-related)",
    "18.w": "History of nontraffic convictions",
    "18.x": "Other illness, disability, or surgery",
    "18.y": "Medical Disability Benefits",
}

selected = st.multiselect(
    "Select all items the airman marked YES on Item 18:",
    options=list(item18_options.keys()),
    format_func=lambda x: f"{x} — {item18_options[x]}",
    help="Hold Ctrl/Cmd to select multiple"
)

results = {}  # store decisions

if not selected:
    st.info("Select one or more Item 18 items above to begin the guided evaluation.")
    st.stop()

st.divider()
st.header("2. Guided Evaluation by Condition")

# ========== HELPER ==========
def show_result(decision, message, item60=""):
    if decision == "Issue":
        st.markdown(f'<div class="issue-box"><strong>✅ DECISION: ISSUE</strong><br>{message}</div>', unsafe_allow_html=True)
    elif decision == "CACI Issue":
        st.markdown(f'<div class="caci-box"><strong>✅ DECISION: ISSUE under CACI</strong><br>{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="defer-box"><strong>⚠️ DECISION: DEFER</strong><br>{message}</div>', unsafe_allow_html=True)
    if item60:
        st.markdown(f"**Suggested Item 60 wording:** `{item60}`")

# ========== 18.a HEADACHES ==========
if "18.a" in selected:
    st.subheader("18.a — Frequent or severe headaches")
    headache_type = st.radio("Type of headache?", 
        ["Simple / occasional tension headaches", "Migraine, cluster, or chronic headaches", "Complicated migraine or neurological features"],
        key="ha_type")
    
    if headache_type == "Simple / occasional tension headaches":
        show_result("Issue", "Simple tension headaches without sequelae are usually not disqualifying.", 
                    "History of occasional tension headaches – no sequelae, no regular medication.")
        results["18.a"] = ("Issue", "Simple tension headaches")
    elif headache_type == "Complicated migraine or neurological features":
        show_result("Defer", "Complicated migraine or headaches with neurological features require FAA review.")
        results["18.a"] = ("Defer", "Complicated migraine")
    else:
        st.markdown("**CACI – Migraine and Chronic Headache criteria check:**")
        c1 = st.radio("Treating physician confirms condition is stable on current regimen and no changes recommended?", ["Yes", "No"], key="ha_c1")
        c2 = st.radio("Frequency ≤ 1 episode per month?", ["Yes", "No"], key="ha_c2")
        c3 = st.radio("Last 12 months: ≤ 2 outpatient/urgent care visits AND no hospitalizations for headache?", ["Yes", "No"], key="ha_c3")
        c4 = st.radio("Only mild, non-disabling symptoms (no functional visual impairment, no neuro deficits, vertigo, syncope, or mental status change)?", ["Yes", "No"], key="ha_c4")
        c5 = st.radio("Using only acceptable preventive/abortive medications (no narcotics or injectables for CACI)?", ["Yes", "No"], key="ha_c5")
        c6 = st.radio("Current detailed clinical progress note ≤ 90 days available?", ["Yes", "No"], key="ha_c6")
        
        if all(x == "Yes" for x in [c1, c2, c3, c4, c5, c6]):
            show_result("CACI Issue", "All CACI Migraine criteria appear met. You may issue if otherwise qualified.",
                        "CACI qualified migraine and chronic headaches.")
            results["18.a"] = ("CACI Issue", "Migraine – CACI met")
        else:
            show_result("Defer", "One or more CACI Migraine criteria not met. Defer and submit records.")
            results["18.a"] = ("Defer", "Migraine – CACI not met")

# ========== 18.b DIZZINESS ==========
if "18.b" in selected:
    st.subheader("18.b — Dizziness or fainting spell")
    diz = st.radio("Nature of the episode(s)?",
        ["Single, clearly explained episode (e.g., vasovagal) with full recovery and no recurrence",
         "Recurrent episodes or unexplained cause"],
        key="diz")
    if "Single" in diz:
        show_result("Issue", "Single explained episode with full recovery may be issuable with good documentation.",
                    "History of single [vasovagal] episode – fully recovered, no recurrence.")
        results["18.b"] = ("Issue", "Single explained episode")
    else:
        show_result("Defer", "Recurrent or unexplained dizziness/fainting requires further evaluation and FAA review.")
        results["18.b"] = ("Defer", "Recurrent/unexplained")

# ========== 18.c UNCONSCIOUSNESS ==========
if "18.c" in selected:
    st.subheader("18.c — Unconsciousness for any reason")
    unc = st.radio("Nature of unconsciousness?",
        ["Clearly explained (e.g., trauma) with full recovery and no residual issues",
         "Unexplained or recurrent loss of consciousness"],
        key="unc")
    if "Clearly explained" in unc:
        show_result("Defer", "Even explained unconsciousness often needs neurological review. Evaluate under head-injury / neurological protocols. When in doubt, defer.")
        results["18.c"] = ("Defer", "Explained LOC – still review")
    else:
        show_result("Defer", "Unexplained or recurrent loss of consciousness is almost always deferred.")
        results["18.c"] = ("Defer", "Unexplained LOC")

# ========== 18.d EYE ==========
if "18.d" in selected:
    st.subheader("18.d — Eye or vision trouble except glasses")
    eye = st.radio("Primary eye issue?",
        ["Simple refractive error (glasses/contacts) or stable post-refractive surgery (LASIK/PRK etc.)",
         "Glaucoma or ocular hypertension",
         "Other significant pathology (keratoconus, retinal disease, diplopia, field loss, etc.)"],
        key="eye")
    
    if "Simple refractive" in eye:
        show_result("Issue", "Meets visual standards with or without correction. Add corrective lens limitation if required.",
                    "Refractive error corrected to standards. Limitation added if needed.")
        results["18.d"] = ("Issue", "Refractive / post-surgery")
    elif "Glaucoma" in eye:
        st.markdown("**CACI – Glaucoma criteria check:**")
        g1 = st.radio("Treating ophthalmologist confirms stable on current regimen, no changes recommended?", ["Yes", "No"], key="g1")
        g2 = st.radio("Age at diagnosis ≥ 40?", ["Yes", "No"], key="g2")
        g3 = st.radio("Acceptable type only (open-angle, OHTN, glaucoma suspect, or previously treated narrow-angle now stable)?", ["Yes", "No"], key="g3")
        g4 = st.radio("No nerve damage and no trabeculectomy?", ["Yes", "No"], key="g4")
        g5 = st.radio("Acceptable topical meds only (no pilocarpine/miotics, no oral meds)?", ["Yes", "No"], key="g5")
        g6 = st.radio("IOP ≤ 23 mmHg in both eyes AND no visual field defects?", ["Yes", "No"], key="g6")
        g7 = st.radio("Current Form 8500-14 or equivalent ophthalmology report ≤ 90 days?", ["Yes", "No"], key="g7")
        
        if all(x == "Yes" for x in [g1,g2,g3,g4,g5,g6,g7]):
            show_result("CACI Issue", "All CACI Glaucoma criteria appear met.",
                        "CACI qualified glaucoma.")
            results["18.d"] = ("CACI Issue", "Glaucoma – CACI met")
        else:
            show_result("Defer", "One or more CACI Glaucoma criteria not met. Defer with full ophthalmology records.")
            results["18.d"] = ("Defer", "Glaucoma – CACI not met")
    else:
        show_result("Defer", "Significant eye pathology generally requires FAA decision. Obtain Form 8500-7 or specialist report.")
        results["18.d"] = ("Defer", "Significant eye pathology")

# ========== 18.e ALLERGY ==========
if "18.e" in selected:
    st.subheader("18.e — Hay fever or allergy")
    allg = st.radio("Severity and treatment?",
        ["Mild/seasonal, controlled by avoidance or non-sedating antihistamines",
         "Severe, poorly controlled, or requiring sedating medication"],
        key="allg")
    if "Mild" in allg:
        show_result("Issue", "Mild controlled allergies are usually not disqualifying.",
                    "Seasonal allergies – controlled with non-sedating medication / avoidance.")
        results["18.e"] = ("Issue", "Mild allergy")
    else:
        show_result("Defer", "Severe or uncontrolled allergies, or use of sedating medications, may require deferral.")
        results["18.e"] = ("Defer", "Severe allergy")

# ========== 18.f ASTHMA ==========
if "18.f" in selected:
    st.subheader("18.f — Asthma or lung disease")
    ast = st.radio("Asthma severity / type?",
        ["Childhood resolved, exercise-induced, or mild intermittent (PRN rescue only)",
         "Intermittent or mild persistent (candidate for CACI)",
         "Moderate or severe persistent"],
        key="ast")
    
    if "Childhood" in ast:
        show_result("Issue", "Resolved childhood or mild exercise-induced asthma with infrequent PRN use is often issuable.",
                    "History of [childhood/exercise-induced] asthma – resolved / infrequent PRN use only.")
        results["18.f"] = ("Issue", "Mild/resolved asthma")
    elif "Moderate" in ast:
        show_result("Defer", "Moderate or severe persistent asthma requires initial FAA review (Special Issuance pathway).")
        results["18.f"] = ("Defer", "Moderate/severe asthma")
    else:
        st.markdown("**CACI – Asthma criteria check:**")
        a1 = st.radio("Treating physician confirms stable on current regimen, no changes recommended?", ["Yes", "No"], key="a1")
        a2 = st.radio("Symptoms ≤ 2 days per week?", ["Yes", "No"], key="a2")
        a3 = st.radio("Rescue inhaler (SABA) use ≤ 2 times per week?", ["Yes", "No"], key="a3")
        a4 = st.radio("Oral corticosteroids for exacerbations ≤ 2 times per year?", ["Yes", "No"], key="a4")
        a5 = st.radio("Last 12 months: no inpatient hospitalizations AND ≤ 2 outpatient/urgent care visits for exacerbations?", ["Yes", "No"], key="a5")
        a6 = st.radio("Only acceptable medications (inhaled LABA/SABA/ICS/LTRA – no monoclonal antibodies)?", ["Yes", "No"], key="a6")
        a7 = st.radio("Spirometry ≤ 90 days: FEV1 AND FVC both ≥ 80% predicted before bronchodilators?", ["Yes", "No"], key="a7")
        a8 = st.radio("Current detailed clinical progress note ≤ 90 days available?", ["Yes", "No"], key="a8")
        
        if all(x == "Yes" for x in [a1,a2,a3,a4,a5,a6,a7,a8]):
            show_result("CACI Issue", "All CACI Asthma criteria appear met. You may issue if otherwise qualified.",
                        "CACI qualified asthma.")
            results["18.f"] = ("CACI Issue", "Asthma – CACI met")
        else:
            show_result("Defer", "One or more CACI Asthma criteria not met. Defer and submit records + spirometry.")
            results["18.f"] = ("Defer", "Asthma – CACI not met")

# ========== 18.g HEART ==========
if "18.g" in selected:
    st.subheader("18.g — Heart or vascular trouble")
    heart = st.radio("Nature of cardiac/vascular history?",
        ["Significant condition (CAD, MI, stent, CABG, valve disease, arrhythmia, cardiomyopathy, pacemaker, etc.)",
         "Minor or remote issue that appears fully resolved with excellent documentation"],
        key="heart")
    if "Significant" in heart:
        show_result("Defer", "Most significant cardiac conditions require initial FAA review (Defer). Follow-up may use AASI protocols if previously authorized.")
        results["18.g"] = ("Defer", "Significant cardiac history")
    else:
        show_result("Defer", "Even apparently minor cardiac history is usually deferred on first presentation for FAA review. When in doubt, defer.")
        results["18.g"] = ("Defer", "Cardiac history – defer")

# ========== 18.h BLOOD PRESSURE ==========
if "18.h" in selected:
    st.subheader("18.h — High or low blood pressure")
    bp = st.radio("Current status?",
        ["Not on medication and office BP ≤ 155/95",
         "On medication – evaluate for CACI Hypertension",
         "BP remains > 155/95 or evidence of end-organ damage / unacceptable medication"],
        key="bp")
    
    if "Not on medication" in bp:
        show_result("Issue", "BP within limits and no medication – usually issuable.",
                    "History of elevated BP – currently normotensive off medication.")
        results["18.h"] = ("Issue", "BP controlled off meds")
    elif "BP remains" in bp:
        show_result("Defer", "Uncontrolled BP, end-organ damage, or unacceptable medication → Defer.")
        results["18.h"] = ("Defer", "Uncontrolled BP")
    else:
        st.markdown("**CACI – Hypertension criteria check:**")
        h1 = st.radio("Condition stable ≥ 7 days on current regimen and no changes recommended?", ["Yes", "No"], key="h1")
        h2 = st.radio("Asymptomatic (no headache, neuro, visual, or other HTN-related symptoms)?", ["Yes", "No"], key="h2")
        h3 = st.radio("Office blood pressure ≤ 155 systolic AND ≤ 95 diastolic?", ["Yes", "No"], key="h3")
        h4 = st.radio("Using ≤ 3 acceptable medication classes (alpha/beta blockers, ACEI, CCB, ARB, diuretics, etc.) and NO centrally acting agents (e.g. clonidine)?", ["Yes", "No"], key="h4")
        h5 = st.radio("No medication side effects?", ["Yes", "No"], key="h5")
        
        if all(x == "Yes" for x in [h1,h2,h3,h4,h5]):
            show_result("CACI Issue", "All CACI Hypertension criteria appear met.",
                        "CACI qualified hypertension.")
            results["18.h"] = ("CACI Issue", "Hypertension – CACI met")
        else:
            show_result("Defer", "One or more CACI Hypertension criteria not met. Defer.")
            results["18.h"] = ("Defer", "Hypertension – CACI not met")

# ========== 18.i GI ==========
if "18.i" in selected:
    st.subheader("18.i — Stomach, liver, or intestinal trouble")
    st.markdown('<div class="info-box">Many GI/liver conditions have individual CACI worksheets (Colitis, MASH/NASH, Eosinophilic Esophagitis, Hepatitis C, etc.). Check the specific current worksheet.</div>', unsafe_allow_html=True)
    gi = st.radio("Does the condition appear stable and potentially CACI-eligible, or is it significant/complicated?",
        ["Appears stable and likely meets a CACI worksheet",
         "Significant, active, or complicated disease"],
        key="gi")
    if "Appears stable" in gi:
        show_result("CACI Issue", "If the specific CACI worksheet criteria are fully met you may issue. Otherwise defer.",
                    "CACI qualified [specific condition].")
        results["18.i"] = ("CACI Issue", "Possible GI CACI")
    else:
        show_result("Defer", "Significant or complicated GI/liver disease → Defer with specialist records.")
        results["18.i"] = ("Defer", "Significant GI disease")

# ========== 18.j KIDNEY ==========
if "18.j" in selected:
    st.subheader("18.j — Kidney stone or blood in urine")
    kid = st.radio("Primary issue?",
        ["Single resolved stone with no residual",
         "Retained or recurrent stones – possible CACI",
         "Chronic kidney disease – possible CACI",
         "Active bleeding or significant renal disease"],
        key="kid")
    if "Single resolved" in kid:
        show_result("Issue", "Single resolved stone with no residual is often issuable.",
                    "History of single kidney stone – resolved, no residual.")
        results["18.j"] = ("Issue", "Resolved stone")
    elif "Active" in kid:
        show_result("Defer", "Active issues require deferral.")
        results["18.j"] = ("Defer", "Active renal issue")
    else:
        show_result("CACI Issue", "Check the specific CACI worksheet (Retained Kidney Stone or CKD). If all criteria met → Issue; otherwise Defer.",
                    "CACI qualified [Retained Kidney Stone / CKD].")
        results["18.j"] = ("CACI Issue", "Possible kidney CACI")

# ========== 18.k DIABETES ==========
if "18.k" in selected:
    st.subheader("18.k — Diabetes")
    dia = st.radio("Type / treatment?",
        ["Prediabetes",
         "Type 2 on oral medication or non-insulin injectables",
         "Insulin-treated (Type 1 or Type 2)"],
        key="dia")
    if dia == "Prediabetes":
        show_result("CACI Issue", "Check current CACI Prediabetes worksheet. If all criteria met → Issue; otherwise Defer.",
                    "CACI qualified prediabetes.")
        results["18.k"] = ("CACI Issue", "Prediabetes")
    elif "Type 2 on oral" in dia:
        show_result("Defer", "Medication-controlled Type 2 usually follows AASI pathway. First-time presentations are typically deferred for FAA review.")
        results["18.k"] = ("Defer", "Type 2 diabetes")
    else:
        show_result("Defer", "Insulin-treated diabetes requires Special Issuance (AASI protocol after initial FAA authorization).")
        results["18.k"] = ("Defer", "Insulin-treated diabetes")

# ========== 18.l NEURO ==========
if "18.l" in selected:
    st.subheader("18.l — Neurological disorders")
    neuro = st.radio("Primary neurological condition?",
        ["Seizure / epilepsy",
         "Stroke / TIA",
         "Significant head injury / TBI",
         "Essential tremor (possible CACI)",
         "Migraine (see 18.a)",
         "Other progressive or high-risk neurological condition"],
        key="neuro")
    if neuro in ["Seizure / epilepsy", "Stroke / TIA", "Significant head injury / TBI", "Other progressive or high-risk neurological condition"]:
        show_result("Defer", f"{neuro} almost always requires FAA decision on first presentation.")
        results["18.l"] = ("Defer", neuro)
    elif "Essential tremor" in neuro:
        show_result("CACI Issue", "Check CACI Essential Tremor worksheet. If criteria met → Issue; otherwise Defer.",
                    "CACI qualified essential tremor.")
        results["18.l"] = ("CACI Issue", "Essential tremor")
    else:
        show_result("Defer", "See 18.a for migraine pathway.")
        results["18.l"] = ("Defer", "See migraine")

# ========== 18.m MENTAL ==========
if "18.m" in selected:
    st.subheader("18.m — Mental disorders")
    ment = st.radio("Primary mental health issue?",
        ["Mild, fully resolved condition with no medication for the required period",
         "Depression or anxiety currently treated with acceptable SSRI (possible Fast Track)",
         "Bipolar, psychosis, schizophrenia, or history of suicide attempt",
         "ADHD"],
        key="ment")
    if "Mild, fully resolved" in ment:
        show_result("Issue", "Mild resolved conditions without recent medication may be issuable with good documentation.")
        results["18.m"] = ("Issue", "Resolved mild mental health")
    elif "Depression or anxiety" in ment:
        show_result("Defer", "Follow current Antidepressant / Fast Track policy. Many cases still require FAA review or specific documentation. When criteria are clearly met some AMEs can issue; otherwise defer.")
        results["18.m"] = ("Defer", "Depression/anxiety on SSRI")
    elif "ADHD" in ment:
        show_result("Defer", "ADHD has a specific protocol and often requires testing / Special Issuance.")
        results["18.m"] = ("Defer", "ADHD")
    else:
        show_result("Defer", "Bipolar, psychosis, or suicide attempt history requires full psychiatric evaluation and FAA review.")
        results["18.m"] = ("Defer", "Serious psychiatric history")

# ========== 18.n / 18.o SUBSTANCE ==========
if "18.n" in selected or "18.o" in selected:
    st.subheader("18.n / 18.o — Substance or Alcohol dependence / abuse")
    show_result("Defer", "Any history of substance dependence, recent abuse, or failed drug test almost always requires deferral and formal evaluation (frequently HIMS for professional pilots).")
    results["18.n/o"] = ("Defer", "Substance/Alcohol history")

# ========== 18.p SUICIDE ==========
if "18.p" in selected:
    st.subheader("18.p — Suicide attempt")
    show_result("Defer", "Any history of suicide attempt requires full psychiatric evaluation and FAA review.")
    results["18.p"] = ("Defer", "Suicide attempt history")

# ========== 18.q MOTION SICKNESS ==========
if "18.q" in selected:
    st.subheader("18.q — Motion sickness requiring medication")
    ms = st.radio("Medication and impact?",
        ["Non-sedating medication and condition not incapacitating",
         "Sedating medication or severe/incapacitating symptoms"],
        key="ms")
    if "Non-sedating" in ms:
        show_result("Issue", "Non-sedating treatment for motion sickness is usually acceptable.",
                    "Motion sickness – controlled with non-sedating medication.")
        results["18.q"] = ("Issue", "Motion sickness controlled")
    else:
        show_result("Defer", "Sedating medication or incapacitating symptoms may require deferral.")
        results["18.q"] = ("Defer", "Motion sickness – problematic")

# ========== 18.r–y CONTEXT DEPENDENT ==========
for code, label in [("18.r", "Military medical discharge"),
                   ("18.s", "Medical rejection by military service"),
                   ("18.t", "Rejection for life or health insurance"),
                   ("18.u", "Admission to hospital"),
                   ("18.w", "History of nontraffic convictions"),
                   ("18.x", "Other illness, disability, or surgery"),
                   ("18.y", "Medical Disability Benefits")]:
    if code in selected:
        st.subheader(f"{code} — {label}")
        st.markdown('<div class="info-box">Disposition depends entirely on the underlying medical reason. Identify the condition and apply the most specific protocol (many cancers, arthritis, etc. have CACI worksheets).</div>', unsafe_allow_html=True)
        ctx = st.radio(f"Does the underlying condition appear to meet a known CACI or clear Issue pathway?",
            ["Yes – appears to meet a specific CACI or clear Issue criteria",
             "No / unclear / significant condition"],
            key=f"ctx_{code}")
        if "Yes" in ctx:
            show_result("CACI Issue", "If the specific CACI or Issue criteria are fully met you may issue. Document the underlying condition clearly.",
                        f"CACI qualified / resolved [underlying condition].")
            results[code] = ("CACI Issue", "Context – possible CACI")
        else:
            show_result("Defer", "Underlying condition requires FAA review or does not clearly meet Issue/CACI criteria.")
            results[code] = ("Defer", "Context – defer")

# ========== 18.v DUI ==========
if "18.v" in selected:
    st.subheader("18.v — Arrests / convictions / administrative actions (especially DUI)")
    show_result("Defer", "Must be reported. Recent or multiple actions, or any suggestion of substance issues, usually require deferral and possible substance evaluation. Remind airman of 14 CFR 61.15 reporting requirements.")
    results["18.v"] = ("Defer", "Motor vehicle action history")

# ========== SUMMARY ==========
st.divider()
st.header("3. Summary of Decisions")

if results:
    import pandas as pd
    summary_data = []
    for k, (decision, note) in results.items():
        summary_data.append({"Item": k, "Decision": decision, "Notes": note})
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    defer_count = sum(1 for d, _ in results.values() if d == "Defer")
    issue_count = sum(1 for d, _ in results.values() if d in ("Issue", "CACI Issue"))
    
    st.markdown(f"**Totals:** {issue_count} Issue / CACI Issue  |  {defer_count} Defer")
    
    if defer_count > 0:
        st.warning("One or more items require deferral. Do not issue a medical certificate until the FAA has reviewed the deferred conditions (or all CACI/Issue criteria are clearly met and documented).")
    else:
        st.success("All evaluated items appear eligible for Issue or CACI Issue (assuming the airman is otherwise qualified and all supporting documents are present).")
else:
    st.info("No decisions recorded yet.")

st.divider()
st.caption("Disclaimer: This is an abbreviated interactive reference tool based on the FAA Guide for Aviation Medical Examiners. It does not replace the official AME Guide, current CACI worksheets, or clinical judgment. Always verify the latest criteria at faa.gov/ame_guide before making a certification decision. The AME remains responsible for the final determination.")
