import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {viteSingleFile} from 'vite-plugin-singlefile';
import {levelThreeFilmPlugin} from './level3-film.mjs';
const root=fileURLToPath(new URL('../',import.meta.url));
export default{root,base:'./',plugins:[{name:'level3a-review-entry',enforce:'pre',transform(code,id){if(id===resolve(root,'src/main.tsx'))return`import ${JSON.stringify(resolve(root,'scripts/level3-review-entry.jsx'))};`;}},levelThreeFilmPlugin(),viteSingleFile()]};
