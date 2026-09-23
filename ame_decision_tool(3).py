import streamlit as st
from datetime import date

st.set_page_config(page_title='FAA AME Offline Decision Tool', page_icon='✈️', layout='wide')

# Offline reference data. Verify this embedded dataset against the current FAA Guide before clinical use.
FAA = {
 'AME Guide':'https://www.faa.gov/ame_guide',
 'Disposition tables':'https://www.faa.gov/ame_guide/dec_cons/disp',
 'CACI worksheets':'https://www.faa.gov/ame_guide/certification_ws',
 'DNI/DNF medications':'https://www.faa.gov/ame_guide/pharm/dni_dnf',
 'Pharmaceutical guidance':'https://www.faa.gov/ame_guide/pharm',
 'Special Issuance/AASI':'https://www.faa.gov/ame_guide/special_iss',
 'Part 67':'https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-67'}

ITEMS = {25:'Head, face, neck, scalp',26:'Nose',27:'Sinuses',28:'Mouth and throat',29:'Ear',30:'Ear drums',31:'Eyes',32:'Ophthalmoscopic',33:'Pupils',34:'Ocular motility',35:'Lungs and chest',36:'Heart',37:'Vascular system',38:'Abdomen and viscera',39:'Anus',40:'Skin',41:'Genitourinary system',42:'Upper and lower extremities',43:'Spine and other musculoskeletal',44:'Identifying body marks, scars, tattoos',45:'Lymphatics',46:'Neurologic',47:'Psychiatric conditions',48:'General systemic',49:'Hearing',50:'Distant vision',51:'Near and intermediate vision',52:'Color vision',53:'Field of vision',54:'Heterophoria',55:'Blood pressure',56:'Pulse',57:'Urinalysis',58:'ECG'}

# FAA DNI/DNF screen list. The app intentionally routes a positive match to no-issue/defer review.
DNI_DNF = ['Amphetamines and amphetamine-like stimulants','Anticonvulsants / antiepileptic drugs','Antipsychotics','Barbiturates','Benzodiazepines','Cannabinoids / medical marijuana','Centrally acting muscle relaxants','Certain sedating antihistamines','Certain sedating antidepressants','Cocaine','Hallucinogens','Hypnotics / sleep aids','Methadone and other opioid-maintenance drugs','Narcotic analgesics / opioids','Phencyclidine (PCP)','Sedating antiemetics','Tranquilizers and other impairing drugs','Any medication causing unacceptable sedation, cognitive impairment, hypotension, or delayed reaction']

CACI = ['Arthritis','Asthma','Bladder Cancer','Breast Cancer','Carotid/Vertebral Artery Stenosis','C-ITP (Chronic Immune Thrombocytopenia)','Chronic Kidney Disease','Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma','Colitis','Colon/Colorectal Cancer','Eosinophilic Esophagitis','Essential Tremor','Glaucoma','Hepatitis C – Chronic','Hypertension','Hypothyroidism','Low Testosterone Hypogonadism','MASH / NASH (Liver)','Migraine and Chronic Headache','Mitral Valve Repair','Polycystic Ovarian Syndrome','Prediabetes','Primary Hemochromatosis','Prostate Cancer','Psoriasis','Renal Cancer','Retained Kidney Stone(s)','Testicular Cancer','Weight Loss Management']

# Embedded decision rules are conservative routing rules, not a replacement for an FAA determination.
ROUTES = {
 'Normal / meets applicable standard':('ISSUE PATHWAY','No abnormality identified in this item. Confirm class-specific standards and complete the rest of the exam.'),
 'Abnormality but clearly insignificant and stable':('ISSUE ONLY IF OTHERWISE QUALIFIED','Document the finding and rationale in the record. Verify no functional effect or disqualifying associated condition.'),
 'Meets a listed CACI pathway':('CACI ISSUE PATHWAY','Complete the selected CACI worksheet in this app; every required criterion must be satisfied and supporting records retained.'),
 'Does not meet CACI criteria':('DEFER','CACI criteria are not met. Defer and submit the required records to FAA.'),
 'Special Issuance / AASI condition':('DEFER / FAA PATHWAY','Do not regular-issue from this screen. Apply the current authorization and required documentation.'),
 'Unexplained, progressive, symptomatic, or functionally significant':('DEFER','Obtain evaluation and records; unresolved aeromedically significant findings require FAA review.'),
 'Unacceptable medication or adverse effect':('DO NOT ISSUE / DEFER','Positive DNI/DNF or impairing medication screen requires medication-specific FAA review and applicant safety counseling.'),
 'Insufficient records or uncertain diagnosis':('HOLD / DEFER','Do not issue until the diagnosis, stability, treatment, and required documentation are established.')}

CACI_Q = {
 'all': [('Diagnosis is established and documented by an appropriate provider?', 'Yes — documentation available'),('Condition is stable, controlled, and without aeromedically significant symptoms?', 'Yes'),('No disqualifying complication, end-organ damage, or functional impairment is present?', 'Yes'),('Treatment is tolerated without impairing side effects?', 'Yes'),('Required time interval, testing, and specialist reports are current?', 'Yes'),('Applicant otherwise meets the applicable medical standards?', 'Yes')],
 'Hypertension':[('Diagnosis and treatment are documented?', 'Yes'),('Blood pressure is controlled on a stable regimen?', 'Yes'),('No significant medication adverse effects or hypotension?', 'Yes'),('No evidence of significant target-organ disease or associated disqualifying condition?', 'Yes'),('Required cardiovascular evaluation/testing is current when indicated?', 'Yes'),('Applicant otherwise meets the applicable standards?', 'Yes')],
 'Asthma':[('Asthma diagnosis, severity, and treatment are documented?', 'Yes'),('Symptoms are stable with no recent exacerbation requiring emergency care or hospitalization?', 'Yes'),('No unacceptable medication effect or uncontrolled bronchospasm?', 'Yes'),('Pulmonary function/other required testing is acceptable when indicated?', 'Yes'),('Applicant otherwise meets the applicable standards?', 'Yes')],
 'Prediabetes':[('Diagnosis and laboratory trend are documented?', 'Yes'),('No hypoglycemia, diabetes complication, or medication impairment?', 'Yes'),('Condition is stable and managed with an acceptable plan?', 'Yes'),('Required laboratory results are current?', 'Yes'),('Applicant otherwise meets the applicable standards?', 'Yes')],
 'Hypothyroidism':[('Diagnosis and treatment are documented?', 'Yes'),('Thyroid replacement is stable and laboratory control is acceptable?', 'Yes'),('No symptoms or adverse effects affecting safe flight?', 'Yes'),('No associated disqualifying disease?', 'Yes'),('Applicant otherwise meets the applicable standards?', 'Yes')],
 'Migraine and Chronic Headache':[('Diagnosis is established and the headache pattern is documented?', 'Yes'),('No loss of consciousness, neurologic deficit, or unexplained episodes?', 'Yes'),('Frequency and severity are stable and compatible with safe duties?', 'Yes'),('Treatment does not impair alertness or cognition?', 'Yes'),('Required evaluation is current?', 'Yes'),('Applicant otherwise meets the applicable standards?', 'Yes')]
}

st.title('FAA AME Offline Decision Tool')
st.warning('This is a decision-support implementation, not an FAA application. The embedded summaries must be checked against the current FAA Guide before certification. When a rule, criterion, medication, or diagnosis is uncertain, defer or obtain FAA guidance.')

with st.sidebar:
 st.header('Exam record')
 applicant = st.text_input('Applicant')
 exam_date = st.date_input('Exam date', date.today())
 cert = st.selectbox('Certificate class', ['First','Second','Third','BasicMed / not an FAA medical certification decision'])
 st.divider(); st.caption('Direct references')
 for n,u in FAA.items(): st.markdown(f'[{n}]({u})')

if 'findings' not in st.session_state: st.session_state.findings=[]
def add(label, route, detail): st.session_state.findings.append({'label':label,'route':route,'detail':detail})

st.header('1. DNI / DNF medication screen')
meds = st.multiselect('Select any prescribed, used, or recently stopped medication class:', DNI_DNF)
med_other = st.text_input('Other medication or substance requiring review (optional)')
if meds or med_other:
 st.error('POSITIVE MEDICATION SCREEN — do not regular-issue solely from this tool.')
 add('Medication review','DO NOT ISSUE / DEFER','Review exact drug, dose, indication, last use, adverse effects, abstinence interval, and FAA medication guidance.')
else: st.success('No listed DNI/DNF medication selected. Continue the full medication and substance history.')

st.header('2. Physical examination and disposition-table routing')
selected_items = st.multiselect('Select every abnormal, reported, or potentially relevant Form 8500-8 item:', [f'Item {n} — {v}' for n,v in ITEMS.items()])
choices = ['Normal / meets applicable standard','Abnormality but clearly insignificant and stable','Meets a listed CACI pathway','Does not meet CACI criteria','Special Issuance / AASI condition','Unexplained, progressive, symptomatic, or functionally significant','Insufficient records or uncertain diagnosis']
for label in selected_items:
 n=int(label.split()[1]); choice=st.radio(label, choices, key=f'item_{n}')
 route,note=ROUTES[choice]
 if choice!='Normal / meets applicable standard': add(label,route,note)

st.header('3. CACI worksheet mode')
caci_selected=st.multiselect('Select applicable CACI condition(s):', CACI)
for condition in caci_selected:
 st.subheader(condition)
 qs=CACI_Q.get(condition,CACI_Q['all']); failed=[]
 for i,(q,yes) in enumerate(qs):
  ans=st.radio(q,['Yes — criterion met','No — criterion not met','Unknown / documentation missing'],key=f'{condition}_{i}')
  if ans!='Yes — criterion met': failed.append(q)
 if failed:
  st.error('CACI NOT SATISFIED — DEFER')
  add(f'CACI: {condition}','DEFER','One or more embedded worksheet criteria are not met or are undocumented.')
 else:
  st.success('Embedded CACI screening criteria satisfied — issue only if otherwise qualified and documentation is retained.')
  add(f'CACI: {condition}','CACI ISSUE PATHWAY','All embedded screening criteria marked met; complete final class-standard review.')

st.header('4. Global safety and completeness checks')
checks=['No unexplained loss of consciousness, seizure, syncope, or neurologic episode','No active suicidal ideation, psychosis, cognitive impairment, or unsafe psychiatric symptom','No current chest pain, decompensation, uncontrolled arrhythmia, or severe exertional limitation','No unsafe medication/substance effect or impairment','All required records, testing, and specialist reports are available','Vision, hearing, examination, vital signs, urinalysis, and ECG requirements are satisfied when applicable','Applicant meets the selected certificate-class standards']
for i,c in enumerate(checks):
 ans=st.radio(c,['Yes','No','Unknown'],key=f'global_{i}',horizontal=True)
 if ans!='Yes': add('Global check','DEFER' if ans=='No' else 'HOLD / DEFER',c+' — '+ans)

st.header('5. Consolidated workflow disposition')
priority={'DO NOT ISSUE / DEFER':4,'DEFER':4,'DEFER / FAA PATHWAY':4,'HOLD / DEFER':3,'CACI ISSUE PATHWAY':2,'ISSUE ONLY IF OTHERWISE QUALIFIED':1}
if not st.session_state.findings:
 st.success('No adverse finding entered. This is not an automatic issue decision; complete the applicable FAA class-standard review.')
else:
 top=max(st.session_state.findings,key=lambda x:priority.get(x['route'],2))
 st.subheader(f"{'🔴' if priority.get(top['route'],2)>=4 else '🟠'} {top['route']}")
 st.write(top['detail'])
 with st.expander('All triggered items'):
  for x in st.session_state.findings: st.markdown(f"- **{x['label']} — {x['route']}**: {x['detail']}")

st.header('6. Documentation')
notes=st.text_area('Block 60 / AME notes draft',height=160,placeholder='Document history, medication review, objective findings, records reviewed, embedded criteria, and final action.')
st.download_button('Download decision summary', '\n'.join([f'Applicant: {applicant}',f'Exam date: {exam_date}',f'Class: {cert}','']+[f"{x['label']} | {x['route']} | {x['detail']}" for x in st.session_state.findings]+['','Notes:',notes]), file_name='ame_decision_summary.txt')
if st.button('Clear all selections'): st.session_state.clear(); st.rerun()

st.caption('Embedded content is a conservative offline workflow layer. FAA disposition tables and CACI worksheets change; maintain version control and validate this dataset against the current FAA publications before use.')
