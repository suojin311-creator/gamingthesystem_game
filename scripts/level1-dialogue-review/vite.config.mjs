import{fileURLToPath}from'node:url';import{viteSingleFile}from'vite-plugin-singlefile';
export default{root:fileURLToPath(new URL('.',import.meta.url)),base:'./',plugins:[{
 name:'chapter-metric-copy-review',enforce:'pre',transform(code,id){if(!id.endsWith('/src/shared/components/ChapterTransition.tsx'))return;
 return code.replace('Which sign would tell me the most?','Which metric would tell me the most?');}
},viteSingleFile()],build:{outDir:'../../node_modules/.cache/level1-dialogue-review',emptyOutDir:true}};
