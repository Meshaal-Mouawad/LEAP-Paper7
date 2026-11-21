from pathlib import Path
import json,csv
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, KeepTogether, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
root=Path(__file__).resolve().parent
report=root/'LEAP_Paper7_Experiment_Redesign_20261119.pdf'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fontb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if Path(font).exists():
 pdfmetrics.registerFont(TTFont('DX',font));pdfmetrics.registerFont(TTFont('DXB',fontb)); face='DX';bold='DXB'
else:
 face='Helvetica';bold='Helvetica-Bold'
styles={
 'title':ParagraphStyle('title',fontName=bold,fontSize=17,leading=22,spaceAfter=11,textColor=colors.HexColor('#182936')),
 'subtitle':ParagraphStyle('subtitle',fontName=bold,fontSize=10.3,leading=15,spaceAfter=8),
 'section':ParagraphStyle('section',fontName=bold,fontSize=11,leading=15,spaceBefore=14,spaceAfter=6,textColor=colors.HexColor('#152A3B')),
 'text':ParagraphStyle('text',fontName=face,fontSize=8.5,leading=13,spaceAfter=7,alignment=TA_LEFT),
 'small':ParagraphStyle('small',fontName=face,fontSize=7.4,leading=10),
 'head':ParagraphStyle('head',fontName=bold,fontSize=7.4,leading=10),
}
def P(x,kind='text'):
 return Paragraph(escape(x).replace('\n','<br/>'),styles[kind])
summary=json.loads((root/'outputs/summary.json').read_text())
rows=list(csv.DictReader((root/'outputs/paired_endpoints.csv').open()))
real=[r for r in rows if r['stratum']=='ARCHIVED_REVISION']
doc=SimpleDocTemplate(str(report),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=17*mm,bottomMargin=16*mm)
flow=[]
flow += [P('LEAP Paper 7 — Redesigned Source-Revision Experiment','title'),P('Executed 19 November 2026  |  Technical evidence study  |  Manuscript unchanged','subtitle')]
flow += [P('Purpose','section'),P('Determine whether a source revision changes the executable KPI behavior, the extracted KPI definition records, or both. The earlier approval-label design is replaced by two directly observable technical outputs.')]
flow += [P('Research questions','section'),P('RQ1: Can executable behavior remain stable while LEAP-derived KPI documentation changes?  RQ2: Can executable behavior change while the selected generated documentation fields remain stable?  RQ3: How do exact-file, code-structure and extracted-detail version signals differ on the same source revisions?')]
flow += [P('Design','section'),P('Nine authenticated before-and-after Git source pairs were replayed using their original SHA-256-verified snapshots. Each pair was analyzed with a fixed offline LEAP extractor and detail engine. Executable structure was compared using Python syntax trees or comment-stripped SQL/ABAP tokens. Python was evaluated in isolated subprocesses using fixed input values; SQL/TSQL was evaluated against deterministic in-memory SQLite fixtures. Two separately labelled controlled changes tested channel independence.')]
flow += [P('Principal results','section')]
summ_table=[['Measure','Observed value'],['Archived revision pairs','9'],['Structure-signature changes','3'],['Extracted-detail changes','6'],['Either measured channel changed','7'],['Comparable execution pairs','7'],['Comparable execution outputs equal','5'],['Execution-preserving pairs with changed details','3'],['Separate controlled tests','2 / 2 PASS']]
tbl=Table([[P(a,'head' if i==0 else 'small'),P(b,'head' if i==0 else 'small')] for i,(a,b) in enumerate(summ_table)],colWidths=[115*mm,59*mm],repeatRows=1)
tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E7EDF2')),('GRID',(0,0),(-1,-1),0.25,colors.HexColor('#BCC8D0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
flow += [tbl,Spacer(1,7)]
flow += [P('Case-level evidence','section')]
source_dict={'P7R01':'ABAP source: documentation inventory changed','P7R02':'Python: formula comment added','P7R03':'SQL: calculation replaced','P7R04':'TSQL: formula wording changed','P7R05':'SQL: KPI description added','P7R06':'SQL: formatting only','P7R07':'TSQL: calculation replaced; missing input bindings','P7R08':'Python: function reformatted','P7R09':'Python: standalone input definitions added'}
header=['Case','Structure','Details','Execution','Observed transition']
mat=[[P(x,'head') for x in header]]
for row in real:
 cid=row['case_id']; status={'EQUAL':'same','DIFFERENT':'changed','NOT_TESTED':'not run','UNRESOLVED_INPUT_BINDINGS':'unbound SQL'}[row['runtime_status']]
 mat.append([P(cid,'small'),P('changed' if row['structure_changed']=='True' else 'same','small'),P('changed' if row['dossier_changed']=='True' else 'same','small'),P(status,'small'),P(source_dict[cid],'small')])
tbl=Table(mat,colWidths=[18*mm,25*mm,25*mm,27*mm,79*mm],repeatRows=1)
tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E7EDF2')),('GRID',(0,0),(-1,-1),0.25,colors.HexColor('#BCC8D0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
flow += [tbl]
flow += [P('Controlled tests','section'),P('A formula-comment multiplier was changed from 24 to 25 while executable code stayed unchanged: the extracted detail changed and execution remained equal. A separate multiplier change in executable code left the formula comment unchanged: execution changed and the selected extracted details remained equal. Both assertions passed.')]
flow += [P('Interpretation for Paper 7','section'),P('Output-specific evidence versions distinguish cases that a file-byte signature would treat identically. Four archived documentation changes are invisible to the executable-structure comparison; one executable-structure change is invisible to the extracted-detail comparison. Two byte-level changes leave both measured channels stable. These outputs provide a source-to-context evidence input for later version-monitor evaluation.')]
flow += [P('Reproduction and preservation','section'),P('All 18 original source files passed manifest-hash checks. The fixed parser, with a naming-only local adjustment, returned identical candidate records to the original parser on all 18 snapshots. A fresh replay of the delivered archive regenerates the same machine-readable outputs. Original source examples are not modified.')]
flow += [P('Scientific decision','section'),P('EXPERIMENT COMPLETE. The new result is a reproducible, output-specific source-revision observation. Paper 7 remains on scientific hold pending the explicit bridge to governance-alert decisions and verification of the contribution against closest published research.')]
flow += [P('Limitations','section'),P('The nine file pairs come from four developer Git transitions and are sample programs. The deterministic fixtures do not establish full program equivalence. One TSQL fragment lacks input bindings in the SQLite fixture, and ABAP execution is unavailable. The documentation comparison covers offline candidate and detail fields, not the complete rendered publication. The test supplies technical change evidence and does not evaluate original business approvals or deployed warning outcomes.')]
def footer(canv,document):
 canv.saveState();canv.setFont(face,7);canv.setFillColor(colors.HexColor('#55636D'))
 canv.drawString(17*mm,10*mm,'LEAP Paper 7  |  dual-endpoint revision experiment')
 canv.drawRightString(A4[0]-17*mm,10*mm,f'{document.page}')
 canv.restoreState()
doc.build(flow,onFirstPage=footer,onLaterPages=footer)
print(report)
