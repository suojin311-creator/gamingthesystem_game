import base from '../ending-animation/preview.config.mjs';
import {fileURLToPath} from 'node:url';
const entry=fileURLToPath(new URL('./preview-entry.jsx',import.meta.url));
const original=base.plugins[0];
export default {...base,plugins:[{...original,name:'independent-ending-copy-review',transform(code,id){
 if(id===base.root+'/src/main.tsx')return 'import '+JSON.stringify(entry)+';';
 return original.transform(code,id);
}},...base.plugins.slice(1)]};
