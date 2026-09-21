import streamlit as st

LAST_VERIFIED = "August 26, 2026"  # Update this date whenever you sync with the official FAA AME Guide

# Official FAA links (update if URLs change)
CACI_MAIN = "https://www.faa.gov/ame_guide/certification_ws"
AME_GUIDE = "https://www.faa.gov/ame_guide"
# Individual CACI worksheets (PDF links – verify if FAA renames files)
ASTHMA_CACI = "https://www.faa.gov/ame_guide/media/C-CACIAsthma.pdf"
HYPERTENSION_CACI = "https://www.faa.gov/ame_guide/media/CACI_Hypertension.pdf"
GLAUCOMA_CACI = "https://www.faa.gov/ame_guide/media/C-CACIGlaucoma.pdf"
MIGRAINE_CACI = "https://www.faa.gov/ame_guide/media/C-CACIMigraine.pdf"
PREDIABETES_CACI = "https://www.faa.gov/ame_guide/media/CACI-Pre-Diabetes_Worksheet.pdf"
CKD_CACI = "https://www.faa.gov/ame_guide/media/C-CACIChronicKidneyDisease.pdf"
COLITIS_CACI = "https://www.faa.gov/ame_guide/media/C-CACIColitis.pdf"
ARTHRITIS_CACI = "https://www.faa.gov/ame_guide/media/C-CACIArthritis.pdf"  # verify exact filename
HYPOTHYROIDISM_CACI = "https://www.faa.gov/ame_guide/certification_ws"  # often listed on main CACI page
ESSENTIAL_TREMOR_CACI = "https://www.faa.gov/ame_guide/certification_ws"
RETAINED_STONE_CACI = "https://www.faa.gov/ame_guide/certification_ws"
MASH_NASH_CACI = "https://www.faa.gov/ame_guide/certification_ws"


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
st.markdown(f'<p class="sub-header">Abbreviated interactive clinical reference aid based on the Guide for Aviation Medical Examiners.<br><strong>Last verified against FAA AME Guide revision: {LAST_VERIFIED}</strong></p>', unsafe_allow_html=True)

st.error("""
**IMPORTANT LEGAL & LIABILITY DISCLAIMER — READ CAREFULLY**

This tool is an **unofficial, abbreviated educational and clinical reference aid only**.  
It is **NOT** an official FAA publication, **NOT** a substitute for the current Guide for Aviation Medical Examiners, **NOT** a substitute for the official CACI worksheets, disposition tables, or AASI protocols, and **NOT** a substitute for the AME’s independent professional medical judgment.

- The AME (not this tool) is solely responsible for every certification decision.
- Criteria, worksheets, and policies change. Always verify the latest versions directly on the official FAA AME Guide website (faa.gov/ame_guide) before issuing or deferring.
- Use of this tool does not create any doctor-patient relationship, does not constitute medical or legal advice, and does not shift any liability from the AME to the tool’s creators or distributors.
- By using this tool you acknowledge that you remain fully responsible for compliance with 14 CFR Part 67, FAA orders, and all applicable standards of care.
""")

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
    st.header("Official FAA Links")
    st.markdown(f"""
    **Main pages**
    - [All CACI Conditions]({CACI_MAIN})
    - [Full AME Guide]({AME_GUIDE})

    **Common CACI PDFs**
    - [Asthma]({ASTHMA_CACI})
    - [Hypertension]({HYPERTENSION_CACI})
    - [Glaucoma]({GLAUCOMA_CACI})
    - [Migraine & Chronic Headache]({MIGRAINE_CACI})
    - [Prediabetes]({PREDIABETES_CACI})
    - [Chronic Kidney Disease]({CKD_CACI})
    - [Colitis]({COLITIS_CACI})

    **Other CACIs** (open main CACI page and select the condition)
    - Arthritis, Hypothyroidism, Essential Tremor, Retained Kidney Stone, MASH/NASH, Cancers, etc. → [All CACI Conditions]({CACI_MAIN})
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
    st.markdown("""
    **Official structure (approximate):**
    - Mild stress/tension headache controlled with OTC → often Issue if clearly mild and controlled.
    - Migraine / cluster / chronic headache → use **CACI – Migraine and Chronic Headache Worksheet**.
    - Complicated features, high frequency, or unacceptable medications → Defer.
    """)
    
    headache_type = st.radio("Which best describes the headaches?", 
        [
            "Simple / occasional tension or stress headaches controlled with OTC medication only",
            "Migraine (with or without aura), tension, or cluster headache – evaluate for CACI",
            "Complicated features (neurological impairment, TIA-type symptoms, auras without headache, significant visual impairment, vertigo, syncope, mental status change) or very frequent / incapacitating"
        ],
        key="ha_type")
    
    if headache_type.startswith("Simple"):
        mild = st.radio("Can you determine the condition is mild and under control with no interference with flight duties?",
            ["Yes", "No / uncertain"], key="ha_mild")
        if mild == "Yes":
            show_result("Issue",
                "Mild controlled tension/stress headaches are usually not disqualifying. Document in Item 60.",
                "History of occasional tension/stress headaches – mild, controlled with OTC, no interference with flight.")
            results["18.a"] = ("Issue", "Mild tension headaches")
        else:
            show_result("Defer", "Unable to confirm mild and controlled. Consider full CACI pathway or defer.")
            results["18.a"] = ("Defer", "Tension – uncertain")
    
    elif headache_type.startswith("Complicated"):
        show_result("Defer",
            "Complicated migraine features, neurological symptoms, or incapacitating headaches require FAA review. Submit detailed neurology records.",
            "Deferred – complicated / high-risk headache features.")
        results["18.a"] = ("Defer", "Complicated migraine")
    
    else:
        st.markdown(f"**CACI – Migraine and Chronic Headache Worksheet — ALL must be Yes:** ([Official PDF]({MIGRAINE_CACI}) | [All CACI]({CACI_MAIN}))")
        c1 = st.radio("1. Current detailed Clinical Progress Note (≤ 90 days) from treating physician verifies the condition is stable on current regimen and no management changes are recommended?", ["Yes", "No"], key="ha_c1")
        c2 = st.radio("2. Type is Migraine (with or without aura), tension headache, or cluster headache?", ["Yes", "No"], key="ha_c2")
        c3 = st.radio("3. Frequency ≤ 1 episode per month?", ["Yes", "No"], key="ha_c3")
        c4 = st.radio("4. In the last 12 months: ≤ 2 outpatient/urgent care visits for exacerbation AND no inpatient hospitalizations for headache?", ["Yes", "No"], key="ha_c4")
        c5 = st.radio("5. Only mild non-disabling symptoms AND no functional visual impairment?", ["Yes", "No"], key="ha_c5")
        c6 = st.radio("6. NONE of the following are present: neurological impairment or TIA-type symptoms; auras WITHOUT headaches; impairment of central vision or functionally significant peripheral vision loss; vertigo; syncope; or mental status change?", ["Yes", "No"], key="ha_c6")
        c7 = st.radio("7. Preventive medications are acceptable for CACI (none, or ACE-I / ARB / beta-blocker / CCB / CGRP antagonists used only for prevention)?  **NOT acceptable for CACI prevention: TCAs, anticonvulsants.**", ["Yes", "No"], key="ha_c7")
        c8 = st.radio("8. Abortive / rescue medications (if used) are acceptable and any required no-fly / ground trial times are observed?", ["Yes", "No"], key="ha_c8")
        
        if all(x == "Yes" for x in [c1,c2,c3,c4,c5,c6,c7,c8]):
            show_result("CACI Issue",
                "All listed CACI – Migraine and Chronic Headache criteria appear met. You may issue if otherwise qualified. Keep the progress note in your file.",
                "CACI qualified migraine and chronic headaches.")
            results["18.a"] = ("CACI Issue", "Migraine – CACI met")
        else:
            show_result("Defer",
                "One or more CACI Migraine criteria are not met. Defer and submit the Clinical Progress Note plus supporting records.",
                "NOT CACI qualified migraine. Deferred.")
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
        st.markdown(f"**CACI – Glaucoma criteria check:** ([Official PDF]({GLAUCOMA_CACI}) | [All CACI]({CACI_MAIN}))")
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
    st.markdown(f"**Official worksheet:** [CACI – Asthma PDF]({ASTHMA_CACI}) | [All CACI Conditions]({CACI_MAIN})")
    st.markdown("""
    **Official disposition table structure (Item 35 – Asthma):**
    - **Row A**: Childhood asthma (resolved) **OR** asthma from a specific avoidable trigger managed by avoidance + PRN rescue only **OR** exercise-induced bronchoconstriction treated with PRN rescue only → Issue *if* the AME determines there are no symptoms that would interfere with flight or safety duties.
    - **Row B**: Intermittent or mild persistent → Must use **CACI – Asthma Worksheet** (requires current detailed Clinical Progress Note + spirometry).
    - **Row C**: Moderate or severe persistent → Defer (initial Special Issuance).
    """)
    
    ast = st.radio("Which best describes the airman’s asthma?",
        [
            "A. Childhood asthma fully resolved  OR  specific avoidable trigger managed by avoidance + PRN rescue only  OR  exercise-induced treated with PRN rescue inhaler only",
            "B. Intermittent or mild persistent asthma (currently using controller and/or rescue medication)",
            "C. Moderate or severe persistent asthma"
        ],
        key="ast")
    
    if ast.startswith("A."):
        interfere = st.radio("Can you determine that the airman currently has **no symptoms that would interfere with flight or safety-related duties**?",
            ["Yes – no interfering symptoms", "No / uncertain"],
            key="ast_interfere")
        if interfere.startswith("Yes"):
            show_result("Issue", 
                "Per disposition table Row A: Childhood resolved / avoidable-trigger / exercise-induced with PRN only and no interfering symptoms → Issue. Document clearly in Item 60.",
                "History of [childhood resolved / exercise-induced / specific trigger] asthma – currently asymptomatic, PRN rescue only as needed, no interference with flight duties.")
            results["18.f"] = ("Issue", "Row A – resolved / PRN only")
        else:
            show_result("Defer", "Unable to confirm absence of interfering symptoms. Treat as needing further evaluation or use the CACI pathway if it better fits.")
            results["18.f"] = ("Defer", "Row A – symptoms uncertain")
    
    elif ast.startswith("C."):
        show_result("Defer", 
            "Moderate or severe persistent asthma (Row C) requires initial FAA decision / Special Issuance. Submit detailed pulmonology progress note (≤90 days), medication list, PFTs, and all supporting records.",
            "Deferred – moderate/severe persistent asthma for FAA review.")
        results["18.f"] = ("Defer", "Moderate/severe persistent")
    
    else:  # Row B – Intermittent or mild persistent → full CACI
        st.markdown("**This falls under CACI – Asthma Worksheet. ALL of the following criteria must be met:**")
        a1 = st.radio("1. Treating physician finds the condition stable on current regimen and no changes recommended?", ["Yes", "No"], key="a1")
        a2 = st.radio("2. Symptoms are stable and well-controlled: frequency of symptoms ≤ 2 days per week?", ["Yes", "No"], key="a2")
        a3 = st.radio("3. Use of inhaled short-acting beta agonist (rescue inhaler) ≤ 2 times per week?", ["Yes", "No"], key="a3")
        a4 = st.radio("4. Use of oral corticosteroids for exacerbations ≤ 2 times per year?", ["Yes", "No"], key="a4")
        a5 = st.radio("5. In the last year: No inpatient hospitalizations AND no more than 2 outpatient/urgent care visits for exacerbations (symptoms fully resolved)?", ["Yes", "No"], key="a5")
        a6 = st.radio("6. Medications are acceptable for CACI? (Inhaled LABA, SABA/albuterol, inhaled corticosteroid, leukotriene receptor antagonist such as montelukast. **Monoclonal antibodies are NOT acceptable for CACI**.)", ["Yes", "No"], key="a6")
        a7 = st.radio("7. Current spirometry (≤ 90 days): FEV1 **and** FVC are both ≥ 80% predicted **before** bronchodilators?", ["Yes", "No"], key="a7")
        a8 = st.radio("8. Current detailed Clinical Progress Note from treating physician (≤ 90 days) is available and reviewed?", ["Yes", "No"], key="a8")
        
        if all(x == "Yes" for x in [a1, a2, a3, a4, a5, a6, a7, a8]):
            show_result("CACI Issue", 
                "All CACI – Asthma Worksheet criteria are met. You may issue (no time limitation) if the airman is otherwise qualified. Keep supporting documents in your file; do not submit to FAA unless requested.",
                "CACI qualified asthma.")
            results["18.f"] = ("CACI Issue", "Intermittent/mild persistent – CACI met")
        else:
            show_result("Defer", 
                "One or more CACI – Asthma criteria are not met. Defer the examination and submit the Clinical Progress Note, spirometry, medication list, and all supporting records to the FAA.",
                "NOT CACI qualified asthma. Deferred.")
            results["18.f"] = ("Defer", "Intermittent/mild persistent – CACI not met")

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
    st.markdown(f"**Official worksheet:** [CACI – Hypertension PDF]({HYPERTENSION_CACI}) | [All CACI Conditions]({CACI_MAIN})")
    st.markdown("""
    **Official guidance summary:**
    - Office BP must not exceed **155 systolic / 95 diastolic**.
    - No medication + BP within limits → usually Issue.
    - On ≤ 3 acceptable medication classes + meets all CACI criteria → CACI Issue.
    - 4+ meds, uncontrolled BP, end-organ damage, unacceptable meds (e.g. clonidine), or side effects → Defer.
    """)
    
    bp = st.radio("Current status?",
        [
            "A. Not currently on antihypertensive medication",
            "B. Currently treated with antihypertensive medication(s)",
            "C. BP today remains > 155/95 after rest, or known end-organ damage, or using unacceptable medication"
        ],
        key="bp")
    
    if bp.startswith("A."):
        bp_ok = st.radio("Is today’s seated office blood pressure ≤ 155 systolic AND ≤ 95 diastolic?",
            ["Yes", "No / still elevated after recheck"], key="bp_a")
        if bp_ok == "Yes":
            show_result("Issue",
                "No medication and BP within FAA limits. Summarize history in Item 60. Refer the airman to their physician if the reading is above usual clinical targets even if still ≤ 155/95.",
                "History of elevated blood pressure – currently normotensive off medication. Office BP today within limits.")
            results["18.h"] = ("Issue", "Off medication – BP OK")
        else:
            show_result("Defer", "BP remains elevated. Recheck, treat, or defer. Do not issue while BP exceeds 155/95.")
            results["18.h"] = ("Defer", "Elevated BP off meds")
    
    elif bp.startswith("C."):
        show_result("Defer",
            "Uncontrolled blood pressure, evidence of end-organ damage, or use of unacceptable antihypertensive medication requires deferral and FAA review.",
            "Deferred – uncontrolled hypertension / end-organ damage / unacceptable medication.")
        results["18.h"] = ("Defer", "Uncontrolled or complex HTN")
    
    else:  # On medication → full CACI
        st.markdown("**CACI – Hypertension Worksheet criteria (ALL must be Yes):**")
        h1 = st.radio("1. Treating physician **or** AME finds the condition stable on the current regimen for at least 7 days and no changes are recommended?", ["Yes", "No"], key="h1")
        h2 = st.radio("2. Airman is asymptomatic (no headaches, neurological changes, visual problems, or other hypertension-attributed symptoms)?", ["Yes", "No"], key="h2")
        h3 = st.radio("3. Today’s seated office blood pressure is ≤ 155 systolic AND ≤ 95 diastolic?", ["Yes", "No"], key="h3")
        h4 = st.radio("4. Medications: using a combination of **no more than 3** acceptable classes (alpha blockers, beta-blockers, ACE inhibitors, ARBs, calcium channel blockers, direct renin inhibitors, direct vasodilators, diuretics)? **Centrally acting agents (clonidine, etc.) are NOT acceptable.**", ["Yes", "No"], key="h4")
        h5 = st.radio("5. No medication side effects?", ["Yes", "No"], key="h5")
        h6 = st.radio("6. (Optional but recommended) Current status information is adequate; if the airman is new to you or control is uncertain, have you reviewed a recent progress note?", ["Yes / not required", "No – need more information"], key="h6")
        
        if all(x == "Yes" for x in [h1, h2, h3, h4, h5]) and h6.startswith("Yes"):
            show_result("CACI Issue",
                "All CACI – Hypertension criteria appear met. You may issue if otherwise qualified. Document “CACI qualified hypertension” in Item 60. Supporting documents stay in your file.",
                "CACI qualified hypertension.")
            results["18.h"] = ("CACI Issue", "HTN – CACI met")
        else:
            show_result("Defer",
                "One or more CACI – Hypertension criteria are not clearly met. Defer and submit current status report, medication list, and any evidence regarding end-organ damage or secondary causes.",
                "NOT CACI qualified hypertension. Deferred.")
            results["18.h"] = ("Defer", "HTN – CACI not met")

# ========== 18.i GI ==========
if "18.i" in selected:
    st.subheader("18.i — Stomach, liver, or intestinal trouble")
    st.markdown('<div class="info-box">Many GI/liver conditions have individual CACI worksheets (Colitis, MASH/NASH, Eosinophilic Esophagitis, Hepatitis C, etc.). See the All CACI Conditions link in the sidebar for the current list and PDFs.</div>', unsafe_allow_html=True)
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
        show_result("CACI Issue", "Check the specific CACI worksheet (Retained Kidney Stone or CKD). Official list: see All CACI Conditions link in the sidebar.. If all criteria met → Issue; otherwise Defer.",
                    "CACI qualified [Retained Kidney Stone / CKD].")
        results["18.j"] = ("CACI Issue", "Possible kidney CACI")

# ========== 18.k DIABETES ==========
if "18.k" in selected:
    st.subheader("18.k — Diabetes")
    st.markdown("""
    **High-level guidance:**
    - Prediabetes → possible CACI (check current worksheet).
    - Type 2 treated with oral agents or non-insulin injectables → usually initial Defer / AASI pathway.
    - Insulin-treated (Type 1 or Type 2) → Special Issuance required; first presentation is almost always Deferred.
    """)
    dia = st.radio("Type / treatment?",
        [
            "Prediabetes / impaired fasting glucose / impaired glucose tolerance",
            "Type 2 diabetes treated with oral medication and/or non-insulin injectables only",
            "Any insulin use (Type 1 or Type 2)"
        ],
        key="dia")
    
    if "Prediabetes" in dia:
        st.info(f"Confirm the current CACI – Prediabetes worksheet. [Official PDF]({PREDIABETES_CACI}) | [All CACI Conditions]({CACI_MAIN})")
        pre = st.radio("Do you have the current detailed clinical information and does the airman appear to meet the published CACI Prediabetes criteria?",
            ["Yes – appears to meet all current CACI Prediabetes criteria", "No / incomplete information / does not meet criteria"],
            key="pre")
        if pre.startswith("Yes"):
            show_result("CACI Issue", "If the official CACI Prediabetes worksheet criteria are fully satisfied, you may issue. Keep documents on file.",
                        "CACI qualified prediabetes.")
            results["18.k"] = ("CACI Issue", "Prediabetes – CACI")
        else:
            show_result("Defer", "Prediabetes does not clearly meet CACI criteria or documentation is incomplete. Defer.")
            results["18.k"] = ("Defer", "Prediabetes – not CACI")
    elif "Type 2 diabetes treated" in dia:
        show_result("Defer",
            "Medication-controlled Type 2 diabetes (non-insulin) is typically handled via Special Issuance / AASI after initial FAA review. First-time reports should be deferred with current status report, HbA1c, medication list, and complication screening.",
            "Deferred – Type 2 diabetes on non-insulin medication for FAA review / possible AASI.")
        results["18.k"] = ("Defer", "Type 2 non-insulin")
    else:
        show_result("Defer",
            "Any insulin use requires Special Issuance. First presentation must be deferred. Subsequent issuances follow the current Insulin AASI protocol only after an Authorization has been granted by the FAA.",
            "Deferred – insulin-treated diabetes for Special Issuance.")
        results["18.k"] = ("Defer", "Insulin-treated")

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
    st.subheader("18.m — Mental disorders of any sort")
    st.markdown("""
    **Important:** Most significant psychiatric conditions require FAA review.  
    There is no broad CACI for psychiatric disease. Selected mild cases on acceptable antidepressants may follow the current Antidepressant / Fast Track / Anxiety-Depression pathway — always verify the latest protocol on the AME Guide.
    """)
    ment = st.radio("Which best describes the history?",
        [
            "Mild, fully resolved condition; no psychotropic medication for the period required by current policy",
            "Depression, anxiety, or related condition currently or recently treated with antidepressant medication",
            "ADHD (with or without medication)",
            "Bipolar disorder, psychosis, schizophrenia, or any history of suicide attempt / psychiatric hospitalization"
        ],
        key="ment")
    
    if ment.startswith("Mild, fully resolved"):
        show_result("Issue",
            "Mild conditions that have fully resolved and meet the medication-free interval in the current protocol may be issuable. Document thoroughly. When any doubt exists, defer.",
            "History of mild [condition] – fully resolved, no medication for required interval, no residual symptoms.")
        results["18.m"] = ("Issue", "Resolved mild psychiatric")
    elif ment.startswith("Depression, anxiety"):
        st.warning("Follow the current official Antidepressant / Anxiety-Depression / Fast Track pathway on the FAA AME Guide. Requirements change. Do not rely solely on this tool.")
        show_result("Defer",
            "Most airmen on antidepressants require specific documentation and often FAA review or adherence to the published Fast Track / Special Issuance pathway. Default action is to defer unless you have confirmed the airman meets every current published criterion.",
            "Deferred – depression/anxiety on antidepressant; see current FAA antidepressant protocol.")
        results["18.m"] = ("Defer", "Antidepressant / anxiety pathway")
    elif ment.startswith("ADHD"):
        show_result("Defer",
            "ADHD has a specific FAA protocol that frequently requires neuropsychological testing and Special Issuance. Defer on first presentation or when criteria are not clearly met.",
            "Deferred – ADHD for protocol evaluation.")
        results["18.m"] = ("Defer", "ADHD")
    else:
        show_result("Defer",
            "Bipolar disorder, psychotic disorders, and any history of suicide attempt or psychiatric hospitalization require full evaluation and FAA decision. Do not issue.",
            "Deferred – serious psychiatric history / suicide attempt.")
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
st.header("3. Summary of Decisions (Printable)")

st.markdown("""
<div style="background-color:#FFF8E1; padding:12px; border-radius:6px; border:1px solid #FFD54F;">
<strong>PRINTABLE SUMMARY</strong><br>
Use your browser’s Print function (Ctrl+P / Cmd+P) on this page to save or print the summary below for your records. 
This summary is for the AME’s working notes only and does not replace official documentation in AMCS or the medical file.
</div>
""", unsafe_allow_html=True)

if results:
    import pandas as pd
    summary_data = []
    for k, (decision, note) in results.items():
        summary_data.append({"Item 18": k, "Decision": decision, "Brief Note": note})
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    defer_count = sum(1 for d, _ in results.values() if d == "Defer")
    issue_count = sum(1 for d, _ in results.values() if d in ("Issue", "CACI Issue"))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Issue / CACI Issue", issue_count)
    with col2:
        st.metric("Defer", defer_count)
    
    if defer_count > 0:
        st.error("""
**ACTION REQUIRED:** One or more items are marked DEFER.  
Do **not** issue a medical certificate until every deferred condition has been properly addressed (FAA review completed, or all current official CACI/Issue criteria confirmed and documented).  
Transmit the examination via AMCS and submit required records as indicated.
""")
    else:
        st.success("""
All evaluated Item 18 conditions appear consistent with Issue or CACI Issue **provided**:
- The airman is otherwise fully qualified under Part 67,
- All required supporting documents have been reviewed and retained,
- You have verified the latest official FAA worksheets and disposition tables,
- You have exercised independent professional judgment.
""")
    
    st.markdown("---")
    st.subheader("Suggested Item 60 documentation reminders")
    for k, (decision, note) in results.items():
        st.markdown(f"- **{k}**: {decision} — {note}")
else:
    st.info("No decisions recorded yet. Select Item 18 conditions above and complete the guided questions.")

st.divider()

# Final strong liability block
st.markdown("""
---
### FINAL LIABILITY & USE DISCLAIMER

**This tool is provided solely as an unofficial educational and clinical reference aid.**

- It is **not** published, endorsed, or approved by the Federal Aviation Administration.
- It does **not** replace the current *Guide for Aviation Medical Examiners*, official CACI worksheets, disposition tables, AASI protocols, or any FAA order or regulation.
- Criteria and forms change. The AME must always consult the live FAA AME Guide (faa.gov/ame_guide) before making a certification decision.
- The Aviation Medical Examiner remains solely and fully responsible for every medical certification decision, for the accuracy of entries in AMCS, and for compliance with 14 CFR Part 67 and applicable standards of care.
- Use of this tool does not create a physician-patient relationship with any third party, does not constitute medical, legal, or regulatory advice, and does not transfer or share any liability.
- By continuing to use this tool, the user acknowledges and accepts full professional responsibility for all decisions made.

**When in doubt, DEFER.**
""")

st.caption("Tool version: Abbreviated interactive reference – always verify against current FAA AME Guide before use in certification decisions.")
