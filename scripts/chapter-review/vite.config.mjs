import{fileURLToPath}from'node:url';import{viteSingleFile}from'vite-plugin-singlefile';
const here=fileURLToPath(new URL('.',import.meta.url));
// Films are outside this focused chapter/selection review. Never advance into
// them here; full film packaging must use the normal pinned-source builders.
export default{root:here,base:'./',plugins:[{name:'chapter-only-no-movie-payload',resolveId(id){if(id.startsWith('virtual:'))return '\0'+id;},load(id){if(id.startsWith('\0virtual:'))return 'export default "";';}},viteSingleFile()],build:{outDir:'../../node_modules/.cache/chapter-review',emptyOutDir:true}};
