import {fileURLToPath} from 'node:url';
import {viteSingleFile} from 'vite-plugin-singlefile';
export default {root:fileURLToPath(new URL('.',import.meta.url)),base:'./',plugins:[{
 name:'assessment-review-only',enforce:'pre',transform(code,id){
  if(!id.endsWith('/src/levels/level1/LevelOne.tsx'))return;
  return code.replace('function ResultChart(', 'export function ResultChart(')
   .replace('<span className="eyebrow">{metric.shortName}</span>', '<span aria-hidden="true" />')
   .replace('{assessmentReport && <p className="assessment-report-label">Percentage of students meeting the criteria</p>}', '');
 }
},viteSingleFile()],build:{outDir:'../../node_modules/.cache/level1-assessment-review',emptyOutDir:true}};
