from pathlib import Path
import argparse
import json
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth

parser=argparse.ArgumentParser(description='Generate the ORBIT Gantt chart and milestone register.')
parser.add_argument('--output-dir', type=Path, default=Path('output'))
args=parser.parse_args()
OUT=args.output_dir.resolve()
OUT.mkdir(parents=True, exist_ok=True)
W,H=landscape(A4)
INK=HexColor('#18313E');GRAY=HexColor('#56656E');GRID=HexColor('#DCE3E7')
BLUE=HexColor('#0072B2');TEAL=HexColor('#00866A');ORANGE=HexColor('#CC7900');PURPLE=HexColor('#78669D')
styles={k:ParagraphStyle(k,fontName='Helvetica',fontSize=s,leading=l,textColor=INK) for k,s,l in [('body',10,13),('small',9,11.5),('table',10,12.5)]}
def para(c,text,x,y,w,style='body'):
 p=Paragraph(text,styles[style]);pw,ph=p.wrap(w,1000);p.drawOn(c,x,y-ph);return ph

def txt(c,text,x,y,size=10,bold=False,color=INK):
 c.setFillColor(color);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,text)
def date_for(m):
 z=2027*12+7+m-1;y,mo=divmod(z,12);return date(y,mo+1,1)
def fmt(m):return date_for(m).strftime('%m/%y')

milestones=[
('M1',4,'Sampling and assay workflows established','Matched collection, B-lineage enrichment, multiplexed profiling and autologous culture procedures established; initial recovery and assay-control review.'),
('M2',9,'First reconstructed receptors and confirmed binders','Initial matched profiles and receptor libraries assessed; reproducible autologous scFv binders progressed to full-length antibody confirmation.'),
('M3',17,'Discovery analysis completed; validation rules fixed','Ten-patient discovery profiling and screening completed. Receptor-selection quotas, assay thresholds and primary contrasts fixed before validation screening.'),
('M4',22,'Initial antigen identities independently confirmed','Initial antibody targets supported by orthogonal expression and perturbation assays; tumour-state experiments established with Dr Lucy Brooks.'),
('M5',27,'Validation recruitment and paired profiling completed','Twenty additional Oxford patients recruited and matched-compartment profiling completed; reconstruction and autologous screening continue in rolling batches.'),
('M6',32,'Independent receptor-validation pipeline completed','Twenty-patient validation screening completed using the fixed pipeline; patient-level state/compartment comparisons and normal-control reactivity assessed.'),
('M7',35,'Functional screen completed; mechanistic panel selected','Six to eight monoclonals screened for growth, survival and invasion-related effects; three to four selected for detailed studies, with primary readouts and replication requirements defined.'),
('M8',40,'Recognition breadth, cell-state and serum analyses completed','Shared/private and state-associated recognition characterised. Matched sera and available Birmingham/BRAIN MATRIX samples assessed against validated targets.'),
('M9',44,'Detailed mechanistic studies completed','Three to four selected pairs assessed for direct antigen and tumour-cell/immune-effector Fc effects; functional consequences of state-dependent recognition tested.'),
('M10',46,'Independent functional replication completed','Key effects confirmed in independent preparations and, for shared targets, independent target-positive patient models; alternative mechanisms assessed.'),
('M11',48,'Integrated findings and reusable resources delivered','Integrated analysis and manuscripts prepared; consent-compatible methods, code and reagent information released; findings and next steps shared with patients and the Charity.')]

rows=[
('Governance and sample coordination',1,48,GRAY,['M1']),
('Recruitment / banking: discovery',2,12,BLUE,[]),
('Recruitment / banking: validation',2,25,BLUE,[]),
('Discovery single-cell / paired BCR profiling',3,15,BLUE,[]),
('Discovery reconstruction and binding',5,17,BLUE,['M2','M3']),
('Validation single-cell / paired BCR profiling',18,27,BLUE,['M5']),
('Validation reconstruction and binding',22,32,BLUE,['M6']),
('Antigen discovery and confirmation',12,34,TEAL,['M4']),
('Tumour-state and recognition breadth',18,40,TEAL,[]),
('Target-specific serum validation',22,40,TEAL,['M8']),
('Initial functional screen: 6-8 antibodies',20,35,ORANGE,['M7']),
('Detailed mechanisms: 3-4 selected pairs',28,44,ORANGE,['M9']),
('Independent functional replication',35,46,ORANGE,['M10']),
('Integration, manuscripts and resources',34,48,PURPLE,['M11']),
('Patient involvement and communication',1,48,PURPLE,[]),
]
(OUT/'schedule.json').write_text(json.dumps({'start':'2027-08-01','end':'2031-07-31','milestones':[{'id':i,'month':m,'date':fmt(m),'title':t,'deliverable':d} for i,m,t,d in milestones],'workstreams':[{'name':n,'start_month':a,'end_month':b,'milestones':ms} for n,a,b,col,ms in rows]},indent=2))
C=canvas.Canvas(str(OUT/'ORBIT_Gantt_and_Milestones.pdf'),pagesize=(W,H));C.setTitle('ORBIT | Research timeline and milestones');C.setAuthor('Bo Sun')

def header(subtitle,page):
 txt(C,'ORBIT | Research timeline and milestones',32,H-36,19,True)
 txt(C,'Dr Bo Sun  |  Future Leaders Junior Fellowship  |  1 August 2027 - 31 July 2031',32,H-55,10,color=GRAY)
 label='GitHub: Nusob888  |  Source code'
 linkx=W-32-stringWidth(label,'Helvetica',9)
 txt(C,label,linkx,H-55,9,color=BLUE)
 profilewidth=stringWidth('GitHub: Nusob888','Helvetica',9)
 C.linkURL('https://github.com/Nusob888',(linkx,H-57,linkx+profilewidth,H-46),relative=0,thickness=0)
 codex=linkx+stringWidth('GitHub: Nusob888  |  ','Helvetica',9)
 C.linkURL('https://github.com/Nusob888/ORBIT-gantt',(codex,H-57,W-32,H-46),relative=0,thickness=0)
 txt(C,subtitle,32,H-78,11,True)

header('Overlapping workstreams and delivery milestones',1)
x0=290;x1=W-35;gw=x1-x0;mw=gw/48;top=H-136;rh=21;bottom=top-len(rows)*rh
for y in range(4):
 xx=x0+y*12*mw
 C.setFillColor(HexColor('#EAF0F3'));C.rect(xx,top+23,12*mw,22,fill=1,stroke=0)
 txt(C,f'YEAR {y+1} | {2027+y}-{str(2028+y)[2:]}',xx+13,top+30,10,True)
 for q in range(4):
  qx=xx+q*3*mw
  txt(C,f'Q{q+1}',qx+12,top+10,10,color=GRAY)
lookup={i:(m,t,d) for i,m,t,d in milestones}
for j,(name,a,b,col,ids) in enumerate(rows):
 yy=top-j*rh
 if j%2==0:
  C.setFillColor(HexColor('#F5F7F8'));C.rect(32,yy-rh,W-67,rh,fill=1,stroke=0)
 txt(C,name,36,yy-14,10)
 for k in range(49):
  xx=x0+k*mw
  C.setStrokeColor(GRID if k%3==0 else HexColor('#EDF0F2'));C.setLineWidth(.5 if k%3==0 else .25);C.line(xx,yy-rh,xx,yy)
 C.setFillColor(col)
 if j in [0,14]:C.setFillColor(Color(col.red,col.green,col.blue,alpha=.25))
 C.roundRect(x0+(a-1)*mw+1,yy-15,(b-a+1)*mw-2,9,3,fill=1,stroke=0)
 for mid in ids:
  m,_,_=lookup[mid];xx=x0+(m-.5)*mw;cy=yy-10.5
  C.setFillColor(INK);p=C.beginPath();p.moveTo(xx,cy+4);p.lineTo(xx+4,cy);p.lineTo(xx,cy-4);p.lineTo(xx-4,cy);p.close();C.drawPath(p,fill=1,stroke=0)
  labelx=xx+6 if m<45 else xx-stringWidth(mid,'Helvetica-Bold',9)-6
  C.setFillColor(white);C.rect(labelx-1,cy-4,stringWidth(mid,'Helvetica-Bold',9)+2,10,fill=1,stroke=0)
  txt(C,mid,labelx,cy-2.5,9,True)
for k in [0,12,24,36,48]:
 C.setStrokeColor(HexColor('#B4C2CA'));C.setLineWidth(.8);C.line(x0+k*mw,bottom,x0+k*mw,top+45)
yrev=bottom-16;txt(C,'Progress reviews (separate from deliverables)',36,yrev-3,9,color=GRAY)
for m in range(6,49,6):
 xx=x0+(m-.5)*mw;C.setFillColor(GRAY);C.circle(xx,yrev,2.5,fill=1,stroke=0)
ly=bottom-40
for xx,col,label in [(36,BLUE,'Aim 1: origins and binding'),(235,TEAL,'Aim 2: targets and recognition'),(465,ORANGE,'Aim 3: biological function')]:
 C.setFillColor(col);C.roundRect(xx,ly-1,13,7,2,fill=1,stroke=0);txt(C,label,xx+19,ly-1,9)
txt(C,'Q1: Aug-Oct   |   Q2: Nov-Jan   |   Q3: Feb-Apr   |   Q4: May-Jul',36,ly-18,9,color=GRAY)
C.showPage()
header('Milestone register | estimated delivery dates',2)
xx=[32,69,115,365];widths=[37,46,250,W-32-365]
y=H-99
C.setFillColor(INK);C.rect(32,y-22,W-64,22,fill=1,stroke=0)
for x,lab in zip(xx,['ID','MM/YY','Milestone','Deliverable']):txt(C,lab,x+5,y-15,10,True,white)
y-=22
for idx,(mid,m,title,detail) in enumerate(milestones):
 p1=Paragraph(title,styles['table']);_,h1=p1.wrap(widths[2]-12,1000)
 p2=Paragraph(detail,styles['table']);_,h2=p2.wrap(widths[3]-12,1000)
 rr=max(h1,h2)+12
 if idx%2==0:C.setFillColor(HexColor('#F1F5F7'));C.rect(32,y-rr,W-64,rr,fill=1,stroke=0)
 txt(C,mid,xx[0]+5,y-15,10,True);txt(C,fmt(m),xx[1]+5,y-15,10)
 p1.drawOn(C,xx[2]+5,y-6-h1);p2.drawOn(C,xx[3]+5,y-6-h2)
 C.setStrokeColor(GRID);C.setLineWidth(.4);C.line(32,y-rr,W-32,y-rr)
 y-=rr
print('Milestone table bottom',round(y,1))
if y<45:raise ValueError('Milestone table overflows')
C.save()
print(OUT/'ORBIT_Gantt_and_Milestones.pdf')
