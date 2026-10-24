import React from 'react';import{createRoot}from'react-dom/client';
import ObservationContent from '../../src/shared/components/ObservationContent';
import{THREE_OUTCOMES,SIX_EVIDENCE,FINAL_EVIDENCE}from'../../src/levels/level2/data';
import type{MetricId}from'../../src/shared/data/metrics';
import '../../src/shared/styles/base.css';import '../../src/levels/level2/styles.css';
const all:MetricId[]=['prep','part','focus','discuss','reflect','peer'];
const cases:{label:string,evidence:string,ids:MetricId[]}[]=[
 {label:'3 metrics · Visible',evidence:THREE_OUTCOMES.visible.evidence,ids:['prep','part','focus']},
 {label:'3 metrics · Quality',evidence:THREE_OUTCOMES.quality.evidence,ids:['discuss','reflect','peer']},
 {label:'3 metrics · Mixed',evidence:THREE_OUTCOMES.mixed.evidence,ids:['prep','reflect','peer']},
 {label:'6 metrics',evidence:SIX_EVIDENCE,ids:all},{label:'100 metrics',evidence:FINAL_EVIDENCE,ids:all}];
createRoot(document.getElementById('root')!).render(<div className="game-page level-two" style={{margin:'24px auto',padding:0,width:'calc(100% - 64px)',maxWidth:1160,background:'transparent',boxShadow:'none',border:0}}>{cases.map((c,i)=><section key={c.label} data-case={i} style={{marginBottom:24}}><h2 style={{font:'600 13px Arial,sans-serif',color:'#77796b',margin:'0 0 9px'}}>{c.label}</h2><div className="l2-results"><article className="l2-observation classroom-observation"><ObservationContent evidence={c.evidence} metricIds={c.ids}/></article></div></section>)}</div>);
