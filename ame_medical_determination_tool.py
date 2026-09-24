import streamlit as st
from datetime import date

st.set_page_config(
    page_title="AME Medical Determination Tool",
    page_icon="✈️",
    layout="wide",
)

GUIDE_VERSION = "FAA Guide for Aviation Medical Examiners — Version 08/26/2026"
GUIDE_URL = "https://www.faa.gov/go/ameguide"

# Decision support only. This app intentionally uses conservative logic:
# uncertainty, incomplete criteria, or "Requires FAA Decision" results in DEFER.

ISSUE = "ISSUE"
DEFER = "DEFER"
LIMIT = "ISSUE WITH LIMITATION"
DENY = "DENY"
INCOMPLETE = "INCOMPLETE"

STATUS_RANK = {ISSUE: 0, LIMIT: 1, INCOMPLETE: 2, DEFER: 3, DENY: 4}
STATUS_COLOR = {
    ISSUE: "#0a9f47",
    LIMIT: "#d97706",
    INCOMPLETE: "#64748b",
    DEFER: "#dc2626",
    DENY: "#7f1d1d",
}


def scenario(label, disposition, evaluation="", item60="", notes="", limitation="", checklist=None):
    return {
        "label": label,
        "disposition": disposition,
        "evaluation": evaluation,
        "item60": item60,
        "notes": notes,
        "limitation": limitation,
        "checklist": checklist or [],
    }


def condition(category, page, scenarios, aliases=""):
    return {"category": category, "page": page, "scenarios": scenarios, "aliases": aliases}


def caci(label, page, criteria, notes=""):
    return condition(
        "CACI",
        page,
        [
            scenario(
                label,
                ISSUE,
                evaluation="Review the current detailed Clinical Progress Note and all condition-specific supporting data.",
                item60="Use the exact applicable CACI statement from the FAA worksheet.",
                notes=notes,
                checklist=criteria,
            )
        ],
    )


DCPN = (
    "Current detailed Clinical Progress Note, generally from a clinic visit no more than 90 days "
    "before the AME exam, including history, medications/doses/side effects, exam findings, testing, "
    "diagnosis, assessment/plan, prognosis, and follow-up."
)

DATA = {
    "Condition not listed": condition("General", 60, [
        scenario(
            "AME determines no increased risk for sudden or subtle incapacitation",
            ISSUE,
            "Review the condition, treatment, pertinent reports, and any recent testing. Upload supporting documentation when appropriate.",
            "Explain the rationale for issuance in Item 60.",
            "If uncertain, contact AMCD or the RFS before issuing.",
        ),
        scenario(
            "Condition or treatment may cause sudden or subtle incapacitation, or risk is uncertain",
            DEFER,
            f"Submit {DCPN}; recent pertinent testing; and related treatment records.",
            "Explain the specific concern that caused deferral.",
        ),
    ]),

    # ENT
    "Allergies / allergic rhinitis / anaphylaxis": condition("ENT", 65, [
        scenario("Controlled with acceptable medication; no flight-interfering symptoms", ISSUE,
                 "Verify control, acceptable medication, and required no-fly intervals.",
                 "Document control, medication review, and counseling in Item 60."),
        scenario("Chronic/repeated steroid treatment or urgent intervention, airway closure, or treated urticaria", DEFER,
                 f"{DCPN} from the treating allergist, ENT, or pulmonologist.", "Describe severity and concern."),
        scenario("History of anaphylaxis or reaction requiring epinephrine", DEFER,
                 f"{DCPN} addressing cause, recurrence likelihood, and expected severity.", "Describe the reaction history."),
    ]),
    "Anosmia": condition("ENT", 67, [
        scenario("Known benign etiology; no other flight-interfering condition", ISSUE,
                 "No additional evaluation is needed when the benign cause is established.",
                 "Document etiology and counseling regarding fuel/exhaust/fire detection and use of a CO detector."),
        scenario("Unknown or uncertain etiology", DEFER,
                 f"Most recent {DCPN} from an ENT; it must address etiology if found.", "Document uncertain etiology."),
    ]),
    "Sinusitis / sinus obstruction": condition("ENT", 68, [
        scenario("Acute infection resolved, or non-obstructing deviated septum", ISSUE,
                 "Verify symptoms have resolved, treatment is complete, and medications are acceptable.",
                 "Document resolution in Item 60."),
        scenario("Chronic, severe, barometric symptoms, polyps/cysts/tumor, or anatomic obstruction", DEFER,
                 f"{DCPN} from ENT/allergist; personal statement; available sinus CT; and evaluation for underlying causes.",
                 "Document chronicity, obstruction, or barometric concern."),
    ]),
    "Speech impediment / stuttering": condition("ENT", 70, [
        scenario("Resolved or does not impair required voice communication", ISSUE,
                 "Assess emergency, ATC, and crew communication.", "Document adequate communication."),
        scenario("Impairs voice communication", DEFER,
                 f"{DCPN} from a speech-language pathologist, including cause, intelligibility, and appropriate severity/fluency testing.",
                 "Describe how well the applicant communicates."),
    ]),
    "Cochlear implant": condition("ENT", 71, [
        scenario("Adult implant/SSD and applicant passes hearing requirements with implant OFF", ISSUE,
                 "Verify no flight-interfering symptoms.", "Document age/reason for implant and whether testing was passed with implant on or off."),
        scenario("Implanted for childhood/teen hearing loss, or cannot pass with implant off", DEFER,
                 f"{DCPN} from ENT/audiologist plus current audiogram.", "Document hearing findings."),
    ]),
    "Benign paroxysmal positional vertigo (BPPV)": condition("ENT", 73, [
        scenario("Resolved; total symptomatic period 1 year or less; off medication; no hearing loss", ISSUE,
                 "Verify complete resolution without sequelae.", "Document resolution."),
        scenario("Multiple/intermittent episodes with combined symptoms for 1 year or more", DEFER,
                 f"{DCPN} from ENT/PCP and clinically indicated vestibular testing.", "Document episode history."),
        scenario("Severe, persistent, recurrent/refractory, or required surgery", DEFER,
                 f"{DCPN} from ENT/neurotologist; if surgery occurred, operative and hospital records plus imaging.", "Document severity or surgery."),
    ]),
    "Labyrinthitis / vestibular neuritis": condition("ENT", 75, [
        scenario("Single episode completely resolved; no medication or hearing loss", ISSUE,
                 "Verify complete resolution.", "Document resolution."),
        scenario("Current symptoms", DEFER, "Do not issue while symptomatic; submit pertinent information.", "Document current symptoms."),
        scenario("Multiple episodes separated by weeks to months", DEFER,
                 f"{DCPN} from ENT/neurotologist; treatment records; vestibular testing; current audiogram; and personal statement.",
                 "Document recurrence."),
    ]),
    "Meniere disease": condition("ENT", 77, [
        scenario("Previously reviewed by FAA; remains asymptomatic with no further vertigo", ISSUE,
                 "Review prior FAA disposition and current history.", "Document continued absence of symptoms."),
        scenario("First report to FAA after at least 6 months control", DEFER,
                 f"Current ENT evaluation, audiogram, personal statement, clinically indicated testing, and treatment records.",
                 "Document control period and hearing status."),
        scenario("Associated hearing loss", DEFER, "Evaluate against FAA hearing standards and submit information.", "Document hearing loss."),
    ]),
    "Middle ear abnormality / otitis media / ear tubes": condition("ENT", 85, [
        scenario("Myringotomy or pressure-equalizing tubes; controlled and asymptomatic", ISSUE,
                 "No mandatory recovery period other than anesthesia recovery.", "Document status."),
        scenario("Resolved otitis media, dry perforation, or serous otitis; passes hearing", ISSUE,
                 "Verify resolution and hearing.", "Document resolution and hearing."),
        scenario("Active/chronic/recurrent disease, wet perforation, ETD, or associated pathology", DEFER,
                 f"{DCPN} from ENT or PCP.", "Document active or chronic pathology."),
    ]),

    # EYES
    "Amblyopia": condition("Eyes", 95, [
        scenario("Simple unilateral refractive/strabismic amblyopia with normal fellow eye", DEFER,
                 "Amblyopia Status Summary or equivalent current eye progress note; associated records.",
                 "Summarize findings and preferred FSDO if an MFT may be required."),
        scenario("Both eyes, other eye disease, medication, instability, or vision criteria not met", DEFER,
                 "Amblyopia Status Summary; board-certified ophthalmology evaluation; associated notes and testing.",
                 "Summarize findings and preferred FSDO if an MFT may be required."),
    ]),
    "Blepharitis / conjunctivitis": condition("Eyes", 97, [
        scenario("Resolved or controlled; meets vision standards; no impairing symptoms", ISSUE,
                 "Verify treatment is acceptable and vision is not impaired.", "Document status and counsel regarding transient blur from drops/ointments."),
        scenario("Active infectious conjunctivitis", INCOMPLETE,
                 "Applicant should not fly until discharge, tearing, irritation, and redness resolve; then use the resolved pathway.",
                 "Document active infection if exam is completed."),
        scenario("Does not meet vision standards or symptoms impair safety duties", DEFER,
                 f"{DCPN} from optometrist/ophthalmologist, best-corrected acuity, and pertinent testing.", "Document visual impairment."),
    ]),
    "Cataract": condition("Eyes", 99, [
        scenario("Meets class vision standards and quality of vision is unaffected", ISSUE,
                 "Confirm no significant glare, halos, contrast loss, or poor night vision.",
                 "Document findings; apply limitation 102 if correction is required."),
        scenario("Does not meet standards, quality affected, or eye professional/AME has concerns", DEFER,
                 f"{DCPN}; best-corrected acuity; visual testing; Quality of Vision Questionnaire.", "Document the concern."),
        scenario("Cataract surgery performed", INCOMPLETE, "Use the Lens implant pathway.", ""),
    ]),
    "Diplopia": condition("Eyes", 100, [
        scenario("Any history or current persistent/intermittent diplopia", DEFER,
                 f"{DCPN} from ophthalmology/neurology/neuro-ophthalmology identifying cause, stability/resolution, treatment, acuity, and testing.",
                 "Summarize findings."),
    ]),
    "Lens implant / cataract surgery": condition("Eyes", 104, [
        scenario("Surgery 3 or more months ago; fully recovered; off medication; meets standards", ISSUE,
                 "Verify no glare, halos, contrast loss, or poor night vision.",
                 "Document reason for surgery and apply limitation 102 if needed."),
        scenario("Surgery within 3 months; all Lens Implant Status Summary items YES", ISSUE,
                 "Review signed Lens Implant Status Summary and vision standards.", "Document and submit evaluation for retention."),
        scenario("Complication, vision standard not met, or quality affected", DEFER,
                 f"{DCPN} from ophthalmologist, best-corrected acuity, and pertinent testing.", "Document abnormal findings."),
    ]),
    "Refractive surgery (LASIK / PRK / SMILE)": condition("Eyes", 110, [
        scenario("Surgery 3 or more months ago; recovered; off medication; meets standards", ISSUE,
                 "Verify no glare, halos, contrast loss, or poor night vision.", "Document; apply limitation 102 if needed."),
        scenario("Within 3 months; all Refractive Surgery Status Summary items YES", ISSUE,
                 "Review signed status summary and procedure-specific recovery period.", "Document and submit evaluation for retention."),
        scenario("Complication, standards not met, or quality affected", DEFER,
                 f"{DCPN}, best-corrected acuity, and pertinent testing.", "Document abnormal findings."),
    ]),
    "Chorioretinitis": condition("Eyes", 115, [
        scenario("Single episode at least 5 years ago; no treatment in 5 years; resolved; meets acuity", ISSUE,
                 "Review Chorioretinitis Status Summary or equivalent ophthalmology progress note.",
                 "Explain in Item 60 and submit supporting material for retention."),
        scenario("All other chorioretinitis", DEFER,
                 f"Retinal specialist/ophthalmology {DCPN}; acuity; visual fields; OCT.", "Summarize findings; note FSDO if MFT may be required."),
    ]),
    "Glaucoma / ocular hypertension": caci("Evaluate under CACI glaucoma criteria", 119, [
        "Treating ophthalmologist finds condition stable with no changes recommended",
        "Age at diagnosis was 40 or older",
        "FAA Form 8500-14 or equivalent report is available",
        "Type is CACI eligible: stable open-angle, ocular hypertension/suspect, or treated stable narrow-angle",
        "No documented nerve damage or trabeculectomy",
        "Medication is CACI acceptable",
        "No medication side effects",
        "Intraocular pressure is 23 mm Hg or less in both eyes",
        "No visual-field defect and fields are reliable",
    ]),
    "Lattice degeneration": condition("Eyes", 120, [
        scenario("No flashes, floaters, decreased/blurry vision; meets standards; no laser treatment", ISSUE,
                 "Review symptoms and vision standards.", "Document findings."),
        scenario("Symptoms, standards not met, quality affected, or treated with laser", DEFER,
                 f"{DCPN} from ophthalmology/optometry, acuity, and testing.", "Document concern."),
    ]),
    "Optic neuritis": condition("Eyes / Neurologic", 121, [
        scenario("Any history", DEFER,
                 f"Ophthalmology {DCPN}; acuity; visual fields; MRI brain/orbits; neurologic evaluation; separate-eye computerized color testing; other testing.",
                 "Document findings."),
    ]),
    "Retinal dystrophy / retinitis pigmentosa": condition("Eyes", 123, [
        scenario("Any history", DEFER,
                 f"{DCPN} from board-certified retinal specialist; reliable fields; ERG/OCT/fundus imaging; current acuity.",
                 "Submit to FAA. In most cases these conditions are incompatible with certification."),
    ]),
    "Retinoschisis": condition("Eyes", 124, [
        scenario("Any history", DEFER,
                 f"Retina specialist {DCPN}; acuity; 30-2 visual fields; ERG/OCT or other testing already performed.", "Summarize findings."),
    ]),

    # PULMONARY
    "Alpha-gal syndrome": condition("Pulmonary / Allergy", 129, [
        scenario("Mild reactions resolved with dietary modification", ISSUE,
                 "Verify control and no flight-interfering symptoms.", "Document control."),
        scenario("Severe reaction or currently symptomatic", DEFER,
                 f"{DCPN} from allergist/GI/treating physician; severity/frequency/recurrence risk; alpha-gal IgE or indicated testing.",
                 "Document severity."),
    ]),
    "Asthma": caci("Intermittent or mild persistent asthma — CACI evaluation", 132, [
        "Treating physician finds condition stable with no changes recommended",
        "Symptoms occur no more than 2 days per week",
        "Rescue inhaler is used no more than 2 times per week",
        "Oral steroid exacerbation treatment is no more than 2 times per year",
        "No inpatient hospitalization in the last year",
        "No more than 2 outpatient/urgent-care exacerbation visits in the last year, fully resolved",
        "Medication is CACI acceptable and not a monoclonal antibody",
        "Required spirometry is current and both FEV1 and FVC are at least 80% predicted pre-bronchodilator",
    ], "Spirometry is not required when the only treatment is PRN short-acting beta agonist on one or two days per week."),
    "COPD / emphysema / chronic bronchitis": condition("Pulmonary", 134, [
        scenario("Any COPD diagnosis — initial FAA review", DEFER,
                 f"COPD Status Summary; {DCPN}; PFT; 6-minute walk test; CBC; imaging/testing. More severe cases require pulmonologist and DLCO.",
                 "Document severity, SpO2, FEV1, walk distance/desaturation, medications, and steroid use."),
    ]),
    "Pulmonary fibrosis": condition("Pulmonary", 138, [
        scenario("Idiopathic pulmonary fibrosis", DEFER,
                 f"Pulmonologist {DCPN}; severity/GAP; PFT with DLCO; 6MWT; available imaging/ABG.", "Document findings."),
        scenario("Secondary pulmonary fibrosis", DEFER,
                 "All idiopathic-fibrosis evaluation data plus documentation for the underlying cause.", "Document underlying condition."),
    ]),
    "Pneumothorax": condition("Pulmonary", 139, [
        scenario("Traumatic pneumothorax resolved at least 3 months", ISSUE,
                 "Review pertinent records and current status.", "Document resolution."),
        scenario("Spontaneous pneumothorax", DEFER,
                 "Submit documentation of resolution and evaluation for recurrence risk/residual blebs; repeat cases generally require corrective surgery.",
                 "Document history and recurrence risk."),
    ]),
    "Sarcoidosis": condition("Pulmonary / Systemic", 140, [
        scenario("Pulmonary stage 1 only; all Status Summary items favorable", ISSUE,
                 "Review signed Sarcoid Status Summary or equivalent progress note.", "Document and submit evaluation for retention."),
        scenario("Stage 2+, other organ involvement, or hypercalcemia", DEFER,
                 f"Specialist {DCPN}; CBC/CMP/calcium/urinalysis; chest imaging; biopsy; TB test; PFT/DLCO; 6MWT; eye exam; ECG; Holter; brain MRI.",
                 "Document affected systems."),
        scenario("Cardiac or neurologic sarcoidosis", DEFER,
                 "All stage 2+ data plus condition-specific cardiology or neurologic evaluation/testing.", "Document organ involvement."),
    ]),
    "Obstructive sleep apnea": condition("Sleep", 590, [
        scenario("Known OSA; treated; all OSA Treated Status Report items favorable", ISSUE,
                 "Review authorization when present, treated status report, and PAP/dental/surgical compliance data as required.",
                 "Document OSA group and treatment status; apply authorization time limit when required."),
        scenario("At risk but not an immediate safety risk — Group 5", ISSUE,
                 "Provide Specification Sheet B; applicant has 90 days for AASM assessment. Issue if otherwise qualified.",
                 "Document OSA risk triage Group 5."),
        scenario("Severe symptoms representing immediate aviation safety risk — Group 6", DEFER,
                 "Immediate AASM sleep evaluation/assessment is required.", "Document severe symptoms and Group 6."),
        scenario("Other sleep disorder, central apnea, narcolepsy, or unclear diagnosis", DEFER,
                 "Use the condition-specific disposition and submit pertinent sleep records.", "Document the non-OSA concern."),
    ]),

    # CARDIAC
    "Premature atrial contractions (PACs)": condition("Cardiac", 152, [
        scenario("Asymptomatic and no treatment/medication required", ISSUE,
                 "Incidental PACs may be a normal variant.", "Summarize history."),
        scenario("Symptomatic or requires treatment", DEFER,
                 f"{DCPN}; ECG; 24-hour monitor; echocardiogram; other indicated testing.", "Document symptoms/testing."),
    ]),
    "Atrial fibrillation / atrial flutter": condition("Cardiac", 154, [
        scenario("Previously reported; FAA letter says monitoring not required; no recurrence", ISSUE,
                 "Review FAA letter and current history/exam.", "Summarize history."),
        scenario("Any untreated/treated non-valvular AFib or atypical/symptomatic flutter", DEFER,
                 "AFib/A-Flutter Status Summary; detailed progress notes; hospital records if applicable; current 24-hour monitor; TSH; qualifying sleep study; echo; stress test; anticoagulation data if used.",
                 "Document rhythm history and treatment."),
        scenario("Typical flutter successfully ablated at least 2 years ago; Status Summary all YES", ISSUE,
                 "Review cardiologist-completed Typical Atrial Flutter Status Summary.", "Document and submit for retention."),
        scenario("Typical flutter ablated within 2 years or treated with antiarrhythmic", DEFER,
                 f"After 90-day recovery: {DCPN}; echo; cardiac monitor performed at least 90 days after procedure.", "Document status."),
    ]),
    "Pacemaker": condition("Cardiac", 160, [
        scenario("Initial pacemaker review after 2-month recovery", DEFER,
                 "All Pacemaker Protocol items and Pacemaker Status Summary; testing after recovery period.", "Document pacemaker history."),
        scenario("Lead replacement after 2-month recovery", DEFER,
                 "Procedure note; Pacemaker Status Summary; surgeon status report verifying function and no complications.", "Document lead replacement."),
        scenario("Battery/generator replacement; at least 14 days; healing well; off pain meds; no complications", ISSUE,
                 "Procedure note and Pacemaker Status Summary.", "Document and submit for retention."),
        scenario("Pacemaker with active ICD circuit", DENY,
                 "An active ICD is disqualifying. FAA consideration requires documentation that the ICD circuit is deactivated.",
                 "Document ICD status and defer/deny per FAA guidance."),
    ]),
    "Coronary heart disease / MI / stent / CABG": condition("Cardiac", 166, [
        scenario("First or second class / ATCS after applicable recovery period", DEFER,
                 "Follow CHD 1st/2nd Class protocol: cardiology evaluation, A1c/lipids, radionuclide stress test, hospital records, CAMI petition, and post-event cath when required.",
                 "Document event/procedure and recovery period."),
        scenario("Third class; released by treating physician", DEFER,
                 "Follow CHD 3rd Class protocol: cardiology evaluation, A1c/lipids, post-event EST with tracings, and hospital records.",
                 "Document event/procedure."),
        scenario("Current valid AASI and CHD/CAD Recertification Status Summary all favorable", ISSUE,
                 "Follow Authorization and AASI requirements.", "Document AASI issuance and required limitation."),
    ]),
    "Hypertension": caci("Treated hypertension with 3 or fewer acceptable medication components", 173, [
        "Condition stable on current regimen for at least 7 days with no change recommended",
        "No symptoms",
        "Office blood pressure is 155/95 or lower",
        "Medication combination contains no more than 3 acceptable components",
        "No medication side effects",
    ]),
    "Syncope": condition("Cardiac / Neurologic", 176, [
        scenario("Simple known cause, completely resolved, all Syncope Decision Tool answers NO", ISSUE,
                 "Review event, trigger, recurrence, injury, cardiac findings, and AME concerns.",
                 'Document: "Discussed the history of SYNCOPE, no positives to screening questions, and no concerns."'),
        scenario("Unknown/unexplained cause or multiple unrelated events", DEFER,
                 "Current cardiac evaluation, echo, EST, 14-day monitor, A1c, lipids, CBC, EMS/ED records, and carotid duplex if age 40+ at event.",
                 "Document the unexplained feature."),
        scenario("Unexplained after negative cardiac evaluation", DEFER,
                 "All cardiac-row data plus FAA-compliant neurologic evaluation. A 2-year recovery period applies when no definitive cause is found.",
                 "Document unresolved etiology."),
    ]),
    "Heart murmur": condition("Cardiac", 179, [
        scenario("Systolic grade 1/6 or 2/6, or innocent/flow murmur; asymptomatic and nonpathologic", ISSUE,
                 "Confirm nonpathologic status and absence of symptoms.", "Summarize murmur."),
        scenario("Systolic grade 3+, any diastolic murmur, or symptomatic", DEFER,
                 f"Cardiologist {DCPN} with clinical correlation and current 2-D/Doppler echo.", "Document murmur and symptoms."),
    ]),
    "Mitral valve disease": condition("Cardiac", 182, [
        scenario("Mild/trace regurgitation, insufficiency, or MVP; asymptomatic", ISSUE,
                 "Review most recent echo or progress note documenting mild disease.", "Document mild asymptomatic disease."),
        scenario("Moderate and asymptomatic", DEFER,
                 f"{DCPN}; current echo; current 24-hour cardiac monitor.", "Document severity."),
        scenario("Severe or symptomatic at any severity", DEFER,
                 f"{DCPN}; echo within 12 months; use valve surgery pathway if applicable.", "Document symptoms/severity."),
    ]),
    "Hypertrophic cardiomyopathy (HCM/HOCM/IHSS)": condition("Cardiac", 192, [
        scenario("Any history or suspected history", DEFER,
                 f"Cardiology {DCPN}; 5-year SCD risk score; Valsalva echo with images; at least 72-hour monitor; maximal EST; resting ECG; cardiac MRI; historical records.",
                 "Summarize findings."),
    ]),

    # VASCULAR
    "Peripheral arteriovenous malformation (AVM)": condition("Vascular", 199, [
        scenario("Incidental finding; no surveillance required; asymptomatic", ISSUE,
                 "Confirm no treatment or surveillance requirement.", "Summarize findings."),
        scenario("Symptomatic, requires surveillance, or treatment recommended", DEFER,
                 f"{DCPN}; available imaging; hospital/operative records if treated.", "Summarize findings."),
    ]),
    "Buerger disease / thromboangiitis obliterans": condition("Vascular", 200, [
        scenario("Controlled; no complications; no medication; not smoking", ISSUE,
                 "Confirm absence of symptoms and tobacco use.", "Summarize findings."),
        scenario("Complications or continued smoking", DEFER,
                 f"{DCPN}; typed tobacco history; available testing.", "Document complications/tobacco use."),
    ]),
    "Postural tachycardia syndrome (POTS)": condition("Vascular / Neurologic", 201, [
        scenario("Any history", DEFER,
                 f"Cardiology/neurology {DCPN} stating whether diagnosis is confirmed, equivocal, or not confirmed; all related records/testing.",
                 "Submit to FAA. Most confirmed POTS cases are not acceptable for certification."),
    ]),
    "Raynaud syndrome": condition("Vascular", 202, [
        scenario("Primary Raynaud disease; no underlying cause; no functional impairment; acceptable medication", ISSUE,
                 "Assess symptoms, underlying disease, and medication.", "Document findings."),
        scenario("Secondary Raynaud or any impairment/disability", DEFER,
                 f"{DCPN} and testing for the underlying condition.", "Document functional impact/underlying cause."),
    ]),

    # GI / ENDO / GU / MSK / NEURO / PSYCH
    "GERD": condition("Gastrointestinal", 217, [
        scenario("Controlled with lifestyle or acceptable medication", ISSUE,
                 "Verify no flight-interfering symptoms.", "Document medication and complications, if any."),
        scenario("Surgery at least 2 months ago; resolved; no complications/bleed/cancer", ISSUE,
                 "Review surgical history.", "Document surgery and complications or absence thereof."),
        scenario("Severe, recent surgery, or recurrent procedures", DEFER,
                 f"GI/surgeon {DCPN} addressing etiology, outcomes, complications, and testing.", "Summarize findings."),
    ]),
    "Chronic hepatitis C": caci("Chronic hepatitis C — CACI evaluation", 219, [
        "Treating physician finds condition stable with no changes recommended",
        "No complications or symptoms",
        "No medication for the condition",
        "Current AST, ALT, albumin, and PT are within 10% of the normal laboratory scale",
    ]),
    "MASH / NASH": caci("MASH/NASH — CACI evaluation", 224, [
        "Condition is controlled with no flight-interfering fatigue or malaise",
        "No clinical evidence or diagnosis of cirrhosis",
        "At least one acceptable fibrosis assessment is current and below the FAA threshold",
        "Medication is limited to none, vitamin E, or acceptable weight-loss medication",
    ]),
    "Pancreatitis": condition("Gastrointestinal", 226, [
        scenario("Single resolved gallstone pancreatitis; 1-month recovery; definitive treatment; off pain meds", ISSUE,
                 "Verify alcohol was not contributory, CBD cleared, cholecystectomy completed, and applicant released.", "Summarize history."),
        scenario("Alcohol-related, chronic/recurrent, retained stone, stricture, hypertriglyceridemia, unknown/other cause", DEFER,
                 "After 3-month recovery: GI progress note, medications, amylase/lipase, hospital/operative records, imaging.", "Document cause and stability."),
    ]),
    "Chronic kidney disease": caci("CKD with eGFR 35–44 and two functioning kidneys — CACI evaluation", 242, [
        "Asymptomatic and stable with no new complications",
        "Two functioning kidneys",
        "Underlying conditions are well controlled",
        "Dialysis or transplant is not recommended or anticipated",
        "Current eGFR is 35 or higher",
        "Urine albumin is trace/negative or ACR is 29 or less",
        "Hemoglobin is at least 10 g/dL and hematocrit at least 30%",
        "Treatment is limited to allowed antihypertensive medication",
    ]),
    "Kidney stones / retained renal calculi": caci("Retained asymptomatic kidney stones — CACI evaluation", 249, [
        "Asymptomatic and stable with no increase in number or size",
        "Unlikely to cause a sudden incapacitating event",
        "If surgery occurred: full recovery, off pain medication, and released",
        "No chronic hydronephrosis, recurrent UTI/sepsis, renal obstruction/failure, or 3+ procedures in 5 years",
        "No underlying cause requiring disqualifying treatment/surveillance",
        "No treatment other than hydration or acceptable recurrence-prevention medication without side effects",
    ]),
    "Peripheral neuropathy": condition("Musculoskeletal / Neurologic", 265, [
        scenario("No functional limitations; controlled; acceptable medication", ISSUE,
                 "Assess weakness, numbness, dexterity, and ability to operate controls.", "Document absence of functional limitations."),
        scenario("Weakness, numbness, or functional limitation", DEFER,
                 f"{DCPN} describing etiology and functional limitations; lab/imaging/testing.", "Describe aircraft-control impact."),
    ]),
    "Osteomyelitis": condition("Musculoskeletal", 267, [
        scenario("Single episode fully resolved; no residual sequelae", ISSUE,
                 "Verify complete resolution.", "Summarize findings."),
        scenario("Current antibiotics, recurrent/chronic, functional limitation, or amputation", DEFER,
                 f"Infectious disease/treating physician {DCPN} addressing etiology, recurrence risk, and functional limitations.",
                 "Describe functional impact."),
    ]),
    "Arthritis": caci("Osteoarthritis on additional medication or eligible autoimmune arthritis — CACI evaluation", 270, [
        "Treating physician finds condition stable with no changes recommended",
        "Symptoms are none to mild/moderate without significant range-of-motion or activity limitation",
        "Cause is eligible osteoarthritis, rheumatoid arthritis limited to joints, psoriatic arthritis, or ankylosing spondylitis",
        "Medication and required post-dose observation are CACI acceptable",
        "If taking hydroxychloroquine/chloroquine, the required eye Status Summary is favorable",
    ]),
    "Migraine / chronic headache": caci("Migraine or chronic headache — CACI evaluation", 328, [
        "Condition is stable with no management change recommended",
        "Type is eligible migraine, tension, or cluster headache",
        "No more than one episode per month",
        "No inpatient hospitalization and no more than 2 outpatient/urgent-care exacerbation visits in 12 months",
        "Only mild non-disabling symptoms and no functional visual impairment",
        "No TIA-like symptoms, aura without headache, vertigo, syncope, or mental-status change",
        "Preventive medication is CACI acceptable",
        "Rescue medication is CACI acceptable and required no-fly interval is followed",
    ]),
    "Head injury / concussion / TBI": condition("Neurologic", 320, [
        scenario("Head injury only; no concussion/brain injury/neurologic symptoms; fully resolved", ISSUE,
                 "Verify no brain trauma on imaging if performed and full release.", "Document mechanism and date."),
        scenario("Mild brain injury at least 5 years ago; all Brain Injury Decision Tool answers NO", ISSUE,
                 "Review all injuries, symptoms, seizure history, imaging, disability, and concerns.",
                 'Document: "Discussed the history of BRAIN INJURY, no positives to screening questions, and no concerns."'),
        scenario("Mild brain injury within 5 years", DEFER,
                 "After 6-month recovery: current progress note, detailed event/recovery information, hospital records, and imaging reports/images.",
                 "Document injury severity."),
        scenario("Moderate brain injury", DEFER,
                 "After 12-month recovery: neurologic evaluation, neuropsychological evaluation, MRI, hospital records, and other indicated testing.",
                 "Document severity."),
        scenario("Severe brain injury", DEFER,
                 "After 5-year recovery: all moderate-injury evaluation items.", "Document severity."),
    ]),
    "ADHD / ADHD medication history": condition("Psychiatric", 399, [
        scenario("No medication/treatment/symptoms/instability for 4 years; no other psychiatric condition; favorable Fast Track Summary", ISSUE,
                 "Review FAA ADHD Summary, actual psychologist/neuropsychologist report, and all supporting documents.",
                 'Document: "Meets ADHD Fast Track requirements." Submit supporting documents.'),
        scenario("Symptoms/treatment/instability in 4 years, other psychiatric history, or evaluator concern", DEFER,
                 "Standard Track in-person HIMS neuropsychology evaluation/testing; off ADHD medication at least 90 days before testing.",
                 "Document reason for Standard Track."),
        scenario("Currently taking ADHD medication, stopped within 90 days, or current symptoms", DEFER,
                 "Submit current prescribing-provider progress note. Medication/current symptoms are incompatible with aviation safety.",
                 "Document current status."),
    ]),
    "Anxiety / depression / related condition": condition("Psychiatric", 402, [
        scenario("Eligible uncomplicated condition; up to two diagnoses; all Decision Tool answers NO", ISSUE,
                 "Review diagnosis, episodes, treatment, medication timeline, hospitalization/self-harm history, and clinician/AME concerns.",
                 'Document: "Discussed the history of [diagnosis], no positives to screening questions, and no concerns."'),
        scenario("Recurrent symptoms, MDD/dysthymia, prior SSRI SI, multiple concurrent medications, or any Decision Tool YES", DEFER,
                 f"{DCPN} from treating physician/specialist and condition-specific psychiatric documentation.",
                 "Document deferral trigger."),
        scenario("Currently using a conditionally acceptable antidepressant", DEFER,
                 "Use Antidepressant Protocol and HIMS AME process; initial authorization is an FAA decision.",
                 "Document medication, dose, stability period, diagnosis, and HIMS pathway."),
    ]),
    "Diabetes mellitus — diet controlled": condition("Endocrine", 426, [
        scenario("Diet controlled/in remission; no disqualifying end-organ disease", ISSUE,
                 "Follow Diet-Controlled Diabetes Protocol and document control/end-organ review.", "Summarize history."),
    ]),
    "Diabetes mellitus — non-insulin medication": condition("Endocrine", 540, [
        scenario("Initial authorization", DEFER,
                 "Diabetes/Hyperglycemia on Medications Status Report or equivalent progress note; current A1c; medication combination and observation period review.",
                 "Document medications, control, hypoglycemia, and end-organ disease."),
        scenario("Valid AASI; all authorization criteria met", ISSUE,
                 "Follow Authorization/AASI and acceptable medication combination criteria.", "Document AASI issuance and limitation."),
    ]),
    "Diabetes mellitus — insulin treated": condition("Endocrine", 543, [
        scenario("Initial certification using CGM protocol", DEFER,
                 "At least 6 months stability/CGM data plus endocrinology, labs, ophthalmology, cardiac risk evaluation, ECG, and age-indicated stress test.",
                 "Document use of CGM protocol."),
        scenario("Third-class non-CGM option", DEFER,
                 "Follow insulin-treated diabetes non-CGM third-class protocol.", "Document selected protocol."),
        scenario("Renewal under valid Authorization; all requirements met", ISSUE,
                 "Follow the Authorization letter exactly.", "Document SI/AASI issuance and limitation."),
    ]),
}

# Add a conservative placeholder pathway for several FAA-listed conditions not yet represented
# by a detailed algorithm above. This keeps the tool searchable while preventing unsafe issuance.
PLACEHOLDER_CONDITIONS = {
    "Acoustic neuroma": ("ENT", 72),
    "Perilymph fistula": ("ENT", 79),
    "Persistent postural perceptual dizziness (PPPD)": ("ENT", 81),
    "Superior semicircular canal dehiscence": ("ENT", 82),
    "Ocular histoplasmosis": ("Eyes", 101),
    "Coloboma": ("Eyes", 117),
    "Pectus excavatum": ("Pulmonary", 133),
    "Bronchiectasis": ("Pulmonary", 143),
    "Restless leg syndrome": ("Sleep", 145),
    "Chest pain / angina": ("Cardiac", 170),
    "Mitral valve repair": ("Cardiac", 184),
    "Congenital heart disease": ("Cardiac", 186),
    "Fibromuscular dysplasia": ("Vascular", 189),
    "Heart transplant": ("Cardiac", 190),
    "Barrett esophagus": ("Gastrointestinal", 205),
    "Cholelithiasis": ("Gastrointestinal", 206),
    "Cirrhosis": ("Gastrointestinal", 208),
    "Colitis / Crohn disease / ulcerative colitis / IBS": ("Gastrointestinal", 210),
    "Congenital sucrase-isomaltase deficiency": ("Gastrointestinal", 212),
    "Eosinophilic esophagitis": ("Gastrointestinal", 213),
    "Esophageal varices": ("Gastrointestinal", 215),
    "Liver transplant": ("Gastrointestinal", 220),
    "Colon / colorectal cancer": ("Cancer", 227),
    "Low testosterone / hypogonadism": ("Endocrine", 243),
    "Bladder cancer": ("Cancer", 250),
    "Prostate cancer": ("Cancer", 252),
    "Renal cancer": ("Cancer", 255),
    "Testicular cancer": ("Cancer", 257),
    "Cerebral palsy": ("Neurologic / Musculoskeletal", 271),
    "Gout / pseudogout": ("Musculoskeletal", 273),
    "Brain aneurysm": ("Neurologic", 297),
    "Brain bleed / intracranial hemorrhage": ("Neurologic", 298),
    "Brain tumor": ("Neurologic", 300),
    "Carotid / vertebral artery stenosis": ("Neurologic / Vascular", 303),
    "Central sleep apnea": ("Sleep / Neurologic", 306),
    "Chiari malformation": ("Neurologic", 309),
    "Cognitive impairment / dementia": ("Neurologic", 311),
    "Dystonia": ("Neurologic", 314),
    "Epilepsy": ("Neurologic", 315),
    "Guillain-Barre syndrome": ("Neurologic", 319),
    "Multiple sclerosis": ("Neurologic", 337),
    "Narcolepsy / idiopathic hypersomnia": ("Sleep / Neurologic", 339),
    "Parkinson disease": ("Neurologic", 350),
    "Seizure": ("Neurologic", 355),
    "Stroke / TIA": ("Neurologic", 361),
    "Transient global amnesia": ("Neurologic", 363),
    "Tremor": ("Neurologic", 365),
    "Unexplained loss of consciousness": ("Neurologic", 369),
    "PTSD": ("Psychiatric", 408),
    "Substance dependence / abuse": ("Psychiatric", 721),
    "Prediabetes": ("Endocrine", 424),
    "Hypothyroidism": ("Endocrine", 442),
    "Hyperthyroidism": ("Endocrine", 441),
    "Pituitary adenoma": ("Endocrine", 445),
    "HIV": ("Systemic", 448),
    "Breast cancer": ("Cancer", 450),
    "Polycystic ovarian syndrome": ("Endocrine", 454),
    "Primary hemochromatosis": ("Hematology", 457),
    "Thrombocytopenia": ("Hematology", 420),
}

for name, (cat, page) in PLACEHOLDER_CONDITIONS.items():
    if name not in DATA:
        DATA[name] = condition(cat, page, [
            scenario(
                "Use the current FAA condition-specific disposition table / protocol",
                DEFER,
                f"This condition requires review of the full FAA disposition table beginning near Guide page {page}. "
                "Collect the current detailed Clinical Progress Note and all condition-specific records/testing.",
                "Document the diagnosis, relevant history, current status, and reason for deferral.",
                "This conservative pathway intentionally does not authorize issuance. Open the current FAA Guide and apply the exact table, CACI worksheet, AASI, or Authorization letter.",
            )
        ])


def state_key(condition_name, suffix):
    safe = "".join(ch if ch.isalnum() else "_" for ch in condition_name)
    return f"{safe}_{suffix}"


def status_badge(status):
    color = STATUS_COLOR.get(status, "#64748b")
    return f"<span style='background:{color};color:white;padding:.25rem .65rem;border-radius:.5rem;font-weight:700'>{status}</span>"


def evaluate_scenario(condition_name, selected_scenario):
    result = dict(selected_scenario)
    checklist = selected_scenario.get("checklist", [])
    failures, unknowns = [], []
    for idx, criterion in enumerate(checklist):
        value = st.session_state.get(state_key(condition_name, f"criterion_{idx}"), "Not answered")
        if value == "No":
            failures.append(criterion)
        elif value == "Not answered":
            unknowns.append(criterion)
    if checklist:
        if failures:
            result["disposition"] = DEFER
            result["notes"] = "One or more required CACI criteria are not met. Defer and submit supporting documentation."
        elif unknowns:
            result["disposition"] = INCOMPLETE
            result["notes"] = "Complete every CACI criterion before making a determination."
        else:
            result["disposition"] = ISSUE
    result["failures"] = failures
    result["unknowns"] = unknowns
    return result


def render_condition(name, info):
    st.markdown(f"### {name}")
    st.caption(f"{info['category']} · FAA Guide page {info['page']} · {GUIDE_VERSION}")
    options = [s["label"] for s in info["scenarios"]]
    selected_label = st.selectbox(
        "Choose the disposition-table row that best matches this applicant",
        ["Select a pathway…"] + options,
        key=state_key(name, "scenario"),
    )
    if selected_label == "Select a pathway…":
        st.info("Select the most applicable clinical pathway. If no pathway clearly applies, use **Condition not listed** or defer and consult AMCD/RFS.")
        return None

    selected = next(s for s in info["scenarios"] if s["label"] == selected_label)
    if selected["checklist"]:
        st.markdown("**Required CACI criteria — every item must be Yes**")
        for idx, criterion in enumerate(selected["checklist"]):
            st.radio(
                criterion,
                ["Not answered", "Yes", "No"],
                horizontal=True,
                key=state_key(name, f"criterion_{idx}"),
            )

    result = evaluate_scenario(name, selected)
    st.markdown(status_badge(result["disposition"]), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Evaluation data / records**")
        st.write(result["evaluation"] or "Follow the current FAA disposition table and Authorization letter.")
    with c2:
        st.markdown("**Item 60 / AME action**")
        st.write(result["item60"] or "Document the pertinent history, findings, and determination.")

    if result.get("limitation"):
        st.warning(f"Certificate limitation: {result['limitation']}")
    if result.get("notes"):
        st.info(result["notes"])
    if result.get("failures"):
        st.error("Criteria not met:\n- " + "\n- ".join(result["failures"]))
    if result.get("unknowns"):
        st.warning("Unanswered criteria:\n- " + "\n- ".join(result["unknowns"]))

    ame_note = st.text_area(
        "Case-specific notes",
        placeholder="Dates, symptoms, medication details, test values, authorization language, or rationale…",
        key=state_key(name, "notes"),
    )
    result["case_notes"] = ame_note
    result["condition"] = name
    result["page"] = info["page"]
    return result


st.title("✈️ Interactive AME Medical Determination Tool")
st.warning(
    "Decision support only — not an FAA product and not a substitute for the current AME Guide, AMCS, "
    "an applicant's Authorization letter, or consultation with AMCD/RFS. When uncertain, DEFER."
)

with st.sidebar:
    st.header("Exam context")
    exam_date = st.date_input("AME exam date", value=date.today())
    certificate_class = st.selectbox("Class applied for", ["First", "Second", "Third", "ATCS / other FAA clearance"])
    prior_authorization = st.selectbox("Current FAA Authorization/SODA/AASI?", ["No", "Yes", "Unknown"])
    st.divider()
    st.markdown(f"**Source:** [{GUIDE_VERSION}]({GUIDE_URL})")
    st.caption("The FAA Guide is updated periodically. Confirm the current online version before acting.")

st.subheader("1. Select all applicant conditions")
search = st.text_input("Search conditions", placeholder="e.g., asthma, atrial fibrillation, migraine")
all_names = sorted(DATA)
if search.strip():
    q = search.lower().strip()
    visible = [n for n in all_names if q in n.lower() or q in DATA[n].get("aliases", "").lower() or q in DATA[n]["category"].lower()]
else:
    visible = all_names

selected_conditions = st.multiselect(
    "Applicant conditions",
    options=visible,
    placeholder="Select one or more conditions",
)

st.subheader("2. Complete each interactive disposition pathway")
results = []
if not selected_conditions:
    st.info("Select at least one condition. For an unlisted diagnosis, select **Condition not listed**.")
else:
    for name in selected_conditions:
        with st.expander(name, expanded=True):
            result = render_condition(name, DATA[name])
            if result:
                results.append(result)

st.subheader("3. Consolidated medical determination")
if results:
    overall = max((r["disposition"] for r in results), key=lambda s: STATUS_RANK.get(s, 2))
    st.markdown(status_badge(overall), unsafe_allow_html=True)

    if overall == ISSUE:
        st.success("All completed condition pathways support issuance, subject to all other Part 67 standards, medication review, required limitations, and the current FAA Guide.")
    elif overall == LIMIT:
        st.warning("Issuance may be supported only with the specified limitation(s), if otherwise qualified.")
    elif overall == INCOMPLETE:
        st.warning("The determination is incomplete. Resolve all unanswered criteria before issuing.")
    elif overall == DEFER:
        st.error("At least one condition requires deferral or FAA decision. Do not issue unless current FAA written authorization specifically permits issuance.")
    else:
        st.error("At least one selected pathway is disqualifying. Follow the current FAA denial/deferral and reconsideration procedures.")

    rows = []
    for r in results:
        rows.append({
            "Condition": r["condition"],
            "Guide page": r["page"],
            "Pathway": r["label"],
            "Disposition": r["disposition"],
            "Evaluation data": r["evaluation"],
            "Item 60 / action": r["item60"],
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)

    summary_lines = [
        "INTERACTIVE AME MEDICAL DETERMINATION SUMMARY",
        f"Exam date: {exam_date.isoformat()}",
        f"Class applied for: {certificate_class}",
        f"Current Authorization/SODA/AASI: {prior_authorization}",
        f"Guide source: {GUIDE_VERSION}",
        f"OVERALL: {overall}",
        "",
    ]
    for r in results:
        summary_lines += [
            f"CONDITION: {r['condition']}",
            f"Guide page: {r['page']}",
            f"Pathway: {r['label']}",
            f"Disposition: {r['disposition']}",
            f"Evaluation data: {r['evaluation']}",
            f"Item 60 / AME action: {r['item60']}",
        ]
        if r.get("failures"):
            summary_lines.append("Criteria not met: " + "; ".join(r["failures"]))
        if r.get("unknowns"):
            summary_lines.append("Unanswered criteria: " + "; ".join(r["unknowns"]))
        if r.get("case_notes"):
            summary_lines.append("Case notes: " + r["case_notes"])
        summary_lines.append("")

    summary_lines += [
        "CAUTION: This summary is decision support only. Verify the current FAA AME Guide, AMCS,",
        "medication guidance, all coexisting conditions, and any Authorization letter before acting.",
    ]
    st.download_button(
        "Download determination summary",
        data="\n".join(summary_lines),
        file_name=f"ame_determination_{exam_date.isoformat()}.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "Privacy: This tool does not require applicant identifiers and does not transmit data by itself. "
    "Deployment, hosting, logging, and access controls remain the responsibility of the deploying organization."
)
