import{fileURLToPath}from'node:url';import{viteSingleFile}from'vite-plugin-singlefile';
export default{root:fileURLToPath(new URL('.',import.meta.url)),base:'./',plugins:[viteSingleFile()],build:{outDir:'../../node_modules/.cache/observation-copy-review',emptyOutDir:true}};
