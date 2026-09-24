import streamlit as st
from dataclasses import dataclass
from typing import List

st.set_page_config(page_title="FAA AME Medication Flagger", page_icon="✈️", layout="wide")

GUIDE_VERSION = "FAA Guide for Aviation Medical Examiners — Version 08/26/2026"

@dataclass(frozen=True)
class Medication:
    names: tuple
    category: str
    status: str
    guidance: str
    no_fly: str = ""
    notes: str = ""

MEDICATIONS: List[Medication] = [
    Medication(("nitroglycerin", "isosorbide dinitrate", "isosorbide mononitrate", "ranolazine", "ranexa"), "Angina medications", "DNI", "AMEs should defer; FAA clearance is required. Review the underlying cardiac condition, including possible angina or coronary disease.", notes="Do not assess the medication in isolation; the indication is aeromedically significant."),
    Medication(("atropine",), "Oral anticholinergics", "DNI", "AMEs should defer. Review the indication and any cognitive, visual, or cardiovascular effects."),
    Medication(("tolterodine", "detrol", "oxybutynin", "ditropan", "solifenacin", "vesicare", "benztropine", "cogentin"), "Oral anticholinergics", "DNI", "AMEs should defer. These medications may carry sedation or cognitive concerns; review the underlying condition and treatment alternatives."),
    Medication(("mefloquine", "lariam"), "Malaria medication", "DNI", "Mefloquine is not acceptable for pilot duties during use and for 4 weeks after the last dose. Before return to flying, verify no neurologic or psychiatric symptoms occurred during or after use and contact the AME/FAA as appropriate.", no_fly="4 weeks after the last dose, plus FAA/AME clearance before return to pilot duties."),
    Medication(("clonidine", "catapres", "clorpres", "guanabenz", "guanfacine", "tenex", "methyldopa", "reserpine"), "Centrally acting antihypertensives", "DNI", "AMEs should defer. Consider whether the applicant can be safely transitioned to an FAA-acceptable antihypertensive and evaluate blood-pressure control and side effects."),
    Medication(("pramlintide", "symlin"), "Diabetes medication", "DNI", "AMEs should defer. Use the applicable diabetes protocol; this medication is not included in the acceptable diabetes-medication framework."),
    Medication(("phentermine", "adipex", "fastin", "benzphetamine", "regimex", "diethylpropion", "tenuate", "tempanil", "phendimetrazine", "bontril", "qsymia", "phentermine + topiramate", "bupropion + naltrexone", "contrave", "plenity", "citric acid + cellulose", "lorcaserin", "belviq", "fenfluramine", "pondimin"), "Weight-loss medications", "DNI", "AMEs should defer. Review the underlying obesity/weight-loss indication and applicable weight-loss or diabetes guidance."),
    Medication(("seizure medication",), "Seizure medications", "DNI", "AMEs should defer. This applies even when the medication is being used for a non-seizure indication such as migraine; review the underlying condition and FAA neurologic guidance."),
    Medication(("antipsychotic", "neuroleptic", "mood stabilizer", "stimulant", "adhd medication", "add medication", "tranquilizer"), "Psychiatric/psychotropic medications", "DNI", "AMEs should defer. Identify the exact medication, indication, dose, treatment dates, stability, side effects, and any applicable psychiatric or ADHD protocol."),
    Medication(("antidepressant", "ssri", "snri", "tricyclic antidepressant", "tca", "mao inhibitor", "maoi", "esketamine", "spravato"), "Antidepressants", "DNI / FAA review", "The AME may not issue while an antidepressant protocol is being considered. Conditionally acceptable medications may be considered by FAA Special Issuance only when the applicable criteria are met; unacceptable agents require FAA review.", notes="The exact drug and formulation matter. Use the antidepressant protocol rather than relying on a class label."),
    Medication(("fluvoxamine", "luvox", "paroxetine", "paxil", "levomilnacipran", "fetzima", "bupropion ir", "wellbutrin ir", "vortioxetine", "trintellix"), "Unacceptable antidepressants", "DNI", "AMEs should defer. These are listed as unacceptable antidepressant medications for the FAA antidepressant protocol."),
    Medication(("citalopram", "celexa", "escitalopram", "lexapro", "fluoxetine", "prozac", "sarafem", "sertraline", "zoloft", "desvenlafaxine", "pristiq", "duloxetine", "cymbalta", "venlafaxine", "effexor", "bupropion sr", "bupropion xl", "wellbutrin sr", "wellbutrin xl", "vilazodone", "viibryd"), "Conditionally acceptable antidepressants", "FAA Special Issuance only", "The AME may not issue. FAA case-by-case Special Issuance/Special Consideration may be possible when the applicant has an acceptable diagnosis, has been stable on a single approved medication and dose for at least 3 continuous months, has no disqualifying rule-outs, and completes the required HIMS/psychiatric/neuropsychological process.", no_fly="Do not fly while symptomatic or during medication changes until cleared under the applicable FAA process."),
    Medication(("benzodiazepine", "alprazolam", "xanax", "lorazepam", "ativan", "temazepam", "restoril", "triazolam", "halcion"), "Anti-anxiety/sedative medications", "DNF / routine use: defer", "Do not fly or perform safety-related duties while using. Routine use should be deferred. Review the indication, frequency, impairment, and substance/psychiatric history.", no_fly="At least 5 times the maximum pharmacologic half-life or dosing interval, unless a longer FAA-specific interval applies."),
    Medication(("diphenhydramine", "benadryl", "doxylamine", "unisom", "chlorpheniramine", "coricidin", "chlor-trimeton", "clemastine"), "Sedating antihistamines", "DNF; routine use: defer", "Occasional use may be considered only with required no-fly time and no adverse effects; daily use is not acceptable. Review the underlying allergy or sleep condition.", no_fly="Diphenhydramine/doxylamine: 60 hours. Chlorpheniramine/clemastine: 5 days."),
    Medication(("cetirizine", "zyrtec", "levocetirizine", "xyzal"), "Conditionally acceptable antihistamines", "DNF after dose", "May be used occasionally, generally 1–2 times per week, not daily, if otherwise qualified and without side effects.", no_fly="Cetirizine/levocetirizine: 48 hours after the last dose."),
    Medication(("muscle relaxant", "carisoprodol", "soma", "cyclobenzaprine", "flexeril"), "Muscle relaxants", "DNF; routine use: defer", "Do not fly or perform safety-related duties while using. Review the underlying musculoskeletal condition and medication frequency.", no_fly="At least 5 times the maximum pharmacologic half-life or dosing interval."),
    Medication(("kava", "kava-kava", "kratom", "valerian"), "OTC/dietary supplements", "DNF", "Do not fly or perform safety-related duties while using because of possible sedation, cognitive effects, and uncertain product potency.", no_fly="Use the FAA general no-fly rule: 5 times the maximum half-life or dosing interval, and longer if symptoms persist."),
    Medication(("zolpidem", "ambien", "ambien cr", "edluar", "intermezzo", "eszopiclone", "lunesta", "ramelteon", "rozerem", "zaleplon", "sonata", "zolpimist"), "Sleep aids", "DNF; chronic use: defer", "Occasional or limited use may be allowed for some operational circumstances, but daily/nightly use is not allowed. Evaluate the underlying sleep disorder.", no_fly="Zolpidem IR/CR: 24 hours; Edluar: 36 hours; Intermezzo: 36 hours; Lunesta: 30 hours; Restoril: 72 hours; Rozerem: 24 hours; Sonata: 12 hours; Zolpimist: 48 hours."),
    Medication(("opioid", "morphine", "codeine", "oxycodone", "percocet", "oxycontin", "hydrocodone", "lortab", "vicodin", "tramadol", "ultram"), "Pain medications", "DNF; frequent use: defer", "Do not fly or perform safety-related duties while using. Occasional short-term use may be reviewed after the condition resolves and the medication is discontinued; frequent or recurrent use requires FAA review.", no_fly="At least 5 times the maximum pharmacologic half-life or dosing interval; do not return while impaired or symptomatic."),
    Medication(("prednisone", "prednisolone", "methylprednisolone", "medrol"), "Systemic steroids", "Concern / dose-dependent", "Review the underlying condition, dose, duration, psychiatric effects, glucose effects, infection risk, and treatment changes. Steroid doses over 20 mg prednisone equivalent per day are generally not acceptable for routine issuance and require FAA review under the relevant condition protocol.", no_fly="Do not fly while symptomatic or experiencing significant medication effects; follow the applicable condition-specific guidance."),
    Medication(("isotretinoin", "accutane"), "Acne medication", "Conditional / restriction", "After discontinuation and the required waiting period, the AME may consider issuance only if there are no visual or psychiatric side effects. A night-flying restriction may apply; removal requires the specified eye evaluation and documentation.", no_fly="At least 2 weeks after permanent discontinuation before consideration; verify no visual or psychiatric symptoms."),
    Medication(("meglitinide", "nateglinide", "starlix", "repaglinide", "prandin", "sulfonylurea", "glimepiride", "amaryl", "glipizide", "glucotrol", "glyburide", "diabeta", "tolbutamide", "tolazamide", "gliclazide"), "Diabetes medication", "FAA Special Issuance / protocol", "Diabetes treated with non-insulin hypoglycemic medication requires FAA review for initial certification. Apply the current acceptable-combination and observation-time requirements; evaluate hypoglycemia and end-organ complications."),
    Medication(("metformin", "glucophage", "fortamet", "glutetza", "riomet", "liraglutide", "victoza", "semaglutide", "ozempic", "rybelsus", "wegovy", "tirzepatide", "mounjaro", "zepbound", "dulaglutide", "trulicity", "exenatide", "byetta", "bydureon", "dapagliflozin", "farxiga", "empagliflozin", "jardiance", "canagliflozin", "invokana", "sitagliptin", "januvia", "pioglitazone", "actos"), "Diabetes/weight-loss medications", "FAA Special Issuance or CACI-dependent", "Do not classify from medication name alone. Determine whether the indication is diabetes, prediabetes, or weight loss; confirm the exact regimen, A1C, hypoglycemia history, dose-change observation period, side effects, and whether the applicable CACI or FAA diabetes protocol is met.", notes="Combination medications count by component; the current 2026 diabetes medication chart controls."),
    Medication(("warfarin", "jantoven", "apixaban", "eliquis", "rivaroxaban", "xarelto", "dabigatran", "pradaxa", "edoxaban", "savaysa"), "Anticoagulants", "Concern / FAA review", "The medication may be acceptable when the underlying condition is acceptable and monitoring is stable. Review the indication, bleeding history, thromboembolic history, treatment duration, and the applicable cardiac or thromboembolic protocol.", no_fly="New warfarin: minimum 6 weeks with required INR monitoring. New NOAC/DOAC: minimum 2 weeks, plus any underlying-condition recovery period."),
    Medication(("nitrate", "nitroglycerin", "isosorbide", "ranexa", "ranolazine"), "Cardiac medications", "DNI", "AMEs should defer. Review for angina or coronary heart disease; nitrates and ranolazine are listed as Do Not Issue medications."),
    Medication(("pilocarpine", "vuity", "atropine eye drops"), "Eye medications", "DNI / FAA review", "Pilocarpine and atropine are unacceptable for routine certification because of potential effects on pupil size, night vision, or visual function. Review the underlying eye condition."),
    Medication(("gabapentin", "neurontin", "pregabalin", "lyrica", "topiramate", "topamax", "valproic acid", "depakote", "lacosamide", "vimpat", "lamotrigine", "lamictal"), "Neurologic/migraine medications", "DNI / FAA review", "These medications are generally unacceptable for routine certification in the listed FAA medication guidance. Review the exact indication and the corresponding neurologic or migraine disposition table."),
    Medication(("bupropion + naltrexone", "contrave"), "Weight-loss medication", "DNI", "AMEs should defer; this combination is listed as unacceptable for weight-loss treatment."),
    Medication(("varenicline", "chantix"), "Smoking cessation", "Conditionally acceptable", "May be issued if there is no psychiatric history or concern and the medication is used for smoking cessation. Document the indication and absence of side effects in Item 60.", no_fly="Initial observation: 1 week."),
    Medication(("nicotine gum", "nicotine lozenge", "nicotine patch"), "Smoking cessation", "Acceptable", "Generally acceptable when used for smoking cessation and free of aeromedically significant effects. Document the indication and any side effects."),
    Medication(("tadalafil", "cialis", "sildenafil", "viagra", "vardenafil", "levitra", "staxyn", "avanafil", "stendra"), "Erectile dysfunction/BPH medications", "Conditionally acceptable", "May be acceptable for GU indications when there are no side effects and the underlying condition is not aeromedically significant. Nitrates are not allowed; evaluate hypotension, dizziness, and interactions.", no_fly="Tadalafil PRN: 24 hours; vardenafil: 8 hours; avanafil: 8 hours; sildenafil: 8 hours. Daily tadalafil 2.5/5 mg may be allowed after a 7-day observation if no side effects."),
    Medication(("hydroxychloroquine", "plaquenil", "chloroquine", "aralen"), "Hydroxychloroquine/chloroquine", "Condition-specific", "Provide the required Plaquenil Status Report and eye monitoring. Review visual fields, OCT, macular/retinal findings, color vision concerns, and the underlying rheumatologic condition."),
    Medication(("biologic", "adalimumab", "humira", "certolizumab", "cimzia", "etanercept", "enbrel", "golimumab", "simponi", "infliximab", "remicade", "inflectra", "renflexis", "dupilumab", "dupixent", "omalizumab", "xolair", "rituximab", "rituxan", "abatacept", "orencia", "ustekinumab", "stelara", "guselkumab", "tremfya", "risankizumab", "skyrizi", "vedolizumab", "entyvio"), "Biologics", "Conditionally acceptable / condition-specific", "The underlying condition must be acceptable. A 2-week initial ground trial is generally required; changing biologic/biosimilar may require a 48-hour ground trial. Apply the medication-specific post-dose observation time and the disease-specific CACI/SI criteria.", no_fly="Common post-dose intervals: 4 hours for many agents; 24 hours for infliximab/abatacept; 72 hours for rituximab; 24 hours for omalizumab; 48 hours for natalizumab."),
    Medication(("alcohol", "marijuana", "cannabis", "thc", "cbd", "controlled substance"), "Controlled substances/substances", "DNI / FAA review", "AMEs should defer when use raises substance abuse/dependence or impairment concerns. CBD is not automatically disqualifying, but the underlying indication and potential positive drug test must be reviewed. Marijuana/THC and Schedule I substances are unacceptable for flight duties."),
]


def normalize(text: str) -> str:
    return " ".join(text.lower().replace("/", " ").replace("-", " ").split())


def find_matches(query: str) -> List[Medication]:
    q = normalize(query)
    if not q:
        return []
    matches = []
    for med in MEDICATIONS:
        names = [normalize(n) for n in med.names]
        if any(q == n or q in n or n in q for n in names):
            matches.append(med)
    return matches


def classify_unknown(query: str) -> Medication:
    return Medication((query,), "Not found in this tool's medication index", "UNKNOWN / REVIEW", "This medication was not matched to the indexed FAA AME medication guidance. Do not assume it is acceptable. Identify the exact generic name, formulation, dose, indication, start date, recent changes, and side effects; then consult the current FAA AME Guide, AMCD, or RFS.")

st.title("✈️ FAA AME Medication Flagger")
st.caption(GUIDE_VERSION)
st.warning("Educational decision-support only. This is not a substitute for the current AME Guide, AMCS instructions, an Authorization/AASI letter, or AMCD/RFS guidance. The medication and the underlying condition must both be evaluated.")

with st.sidebar:
    st.header("How to use")
    st.write("Enter one medication per line. Generic names are preferred; brand names and common classes are also recognized.")
    st.write("The index is based primarily on the FAA Guide's Pharmaceuticals and medication-related disposition pages. It is not exhaustive.")
    st.divider()
    show_notes = st.checkbox("Show detailed notes", value=True)
    include_unknown = st.checkbox("Include unmatched medications", value=True)

med_text = st.text_area("Medications", placeholder="Example:\nsertraline\nBenadryl\nmetformin\nwarfarin", height=160)
run = st.button("Flag medications", type="primary", use_container_width=True)

if run or med_text.strip():
    raw = [line.strip() for line in med_text.splitlines() if line.strip()]
    results = []
    for item in raw:
        matches = find_matches(item)
        if matches:
            for match in matches:
                results.append((item, match))
        elif include_unknown:
            results.append((item, classify_unknown(item)))

    counts = {}
    for _, med in results:
        counts[med.status] = counts.get(med.status, 0) + 1

    st.subheader("Summary")
    cols = st.columns(min(max(len(counts), 1), 5))
    for i, (status, count) in enumerate(sorted(counts.items())):
        cols[i % len(cols)].metric(status, count)

    st.subheader("Medication guidance")
    for entered, med in results:
        status = med.status
        if status.startswith("DNI"):
            icon = "🛑"
        elif status.startswith("DNF"):
            icon = "⚠️"
        elif status.startswith("UNKNOWN"):
            icon = "❓"
        elif "FAA" in status or "Concern" in status or "Condition-specific" in status:
            icon = "📄"
        else:
            icon = "✅"

        with st.expander(f"{icon} {entered} — {status}", expanded=True):
            st.markdown(f"**Indexed category:** {med.category}")
            st.markdown(f"**Guidance:** {med.guidance}")
            if med.no_fly:
                st.markdown(f"**No-fly / observation guidance:** {med.no_fly}")
            if show_notes and med.notes:
                st.info(med.notes)
            st.caption("Verify the exact medication, formulation, dose, indication, timing, and current FAA policy before making a certification decision.")

    if not results:
        st.info("Enter at least one medication, one per line.")
else:
    st.info("Enter medications above and select **Flag medications**.")

st.divider()
st.subheader("General FAA medication-screening prompts")
st.markdown("""
- ☐ Confirm the exact generic medication, brand name, formulation, dose, frequency, indication, start date, stop date, and all recent changes.
- ☐ Determine whether the medication is being used for a condition that independently requires FAA review.
- ☐ Ask about sedation, dizziness, visual changes, cognitive effects, mood changes, blood-pressure effects, hypoglycemia, allergic reactions, and other adverse effects.
- ☐ Check whether the medication is new, recently changed, or being used intermittently; apply the applicable ground trial or post-dose no-fly period.
- ☐ Review the current Do Not Issue / Do Not Fly guidance and the relevant disease disposition table, CACI worksheet, AASI, or Authorization letter.
- ☐ Document the medication name, dose, frequency, purpose, side effects, and applicable counseling in Item 60.
- ☐ When guidance is uncertain or the condition/treatment may cause sudden or subtle incapacitation, contact AMCD/RFS or defer.
""")

st.caption("Index scope: selected medication guidance from the 2026 FAA AME Guide, including Pharmaceuticals, Do Not Issue/Do Not Fly, and related disease protocols. Always use the most current official FAA guidance.")
