import{fileURLToPath}from'node:url';import{viteSingleFile}from'vite-plugin-singlefile';
export default{root:fileURLToPath(new URL('.',import.meta.url)),base:'./',plugins:[{
 name:'handoff-only-review',resolveId(id){if(id.startsWith('virtual:'))return '\0'+id;},load(id){if(id.startsWith('\0virtual:'))return 'export default "";';}
},viteSingleFile()],build:{outDir:'../../node_modules/.cache/level1-handoff-review',emptyOutDir:true}};
