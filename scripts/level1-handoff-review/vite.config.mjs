import{fileURLToPath}from'node:url';import{viteSingleFile}from'vite-plugin-singlefile';
export default{root:fileURLToPath(new URL('.',import.meta.url)),base:'./',plugins:[{
 name:'handoff-only-review',enforce:'pre',resolveId(id){if(id.startsWith('virtual:'))return '\0'+id;},load(id){if(id.startsWith('\0virtual:'))return 'export default "";';},
 transform(code,id){if(!id.endsWith('/src/levels/level1/LevelOne.tsx'))return;
 const from='const [guideOpen, setGuideOpen] = useState(showIntro);';
 if(!code.includes(from))throw Error('Review guide delay adapter');
 return code.replace(from,`const [guideOpen, setGuideOpen] = useState(false);
 useEffect(()=>{if(!showIntro)return;const t=setTimeout(()=>{guideWasAutomatic.current=true;setGuideOpen(true);},matchMedia('(prefers-reduced-motion: reduce)').matches?0:1050);return()=>clearTimeout(t);},[showIntro]);`);
 }
},viteSingleFile()],build:{outDir:'../../node_modules/.cache/level1-handoff-review',emptyOutDir:true}};
