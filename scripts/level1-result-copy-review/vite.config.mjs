import{fileURLToPath}from'node:url';import{viteSingleFile}from'vite-plugin-singlefile';
export default{root:fileURLToPath(new URL('.',import.meta.url)),base:'./',plugins:[viteSingleFile()],build:{outDir:'../../node_modules/.cache/level1-result-copy-review',emptyOutDir:true}};
