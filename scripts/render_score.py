"""Render this project's original, deterministic chamber score. No sampled music."""
from pathlib import Path
import subprocess, tempfile, json
import numpy as np
from scipy.io.wavfile import write
OUT=Path(__file__).resolve().parents[1]/'src/audio/assets'
SR=32000
rng=np.random.default_rng(311)
def note(m):return 440*2**((m-69)/12)
def render(name,kind):
 seconds=64 if kind!='reveal' else 12
 audio=np.zeros((SR*seconds,2),dtype=np.float64)
 def add(m,start,duration,amp=.1,pan=0,voice='felt'):
  n=int(SR*duration);t=np.arange(n)/SR;f=note(m)
  if voice=='felt':
   wave=sum((.62**(h-1))*np.sin(2*np.pi*f*(h+.0006*h*h)*t)*np.exp(-t*(.65+h*.32)) for h in range(1,7))
   env=(1-np.exp(-t*95))*np.minimum(1,(duration-t)/.3)
  else:
   wave=sum(np.sin(2*np.pi*f*h*t+np.sin(t*.7)*.003*h)/h**2 for h in range(1,5))
   env=np.sin(np.pi*np.clip(t/duration,0,1))**1.5
  wave*=env*amp
  signal=np.stack([wave*np.sqrt((1-pan)/2),wave*np.sqrt((1+pan)/2)],axis=1)
  # Small, damped room reflections; no long or harsh tail.
  for delay,gain in [(0,1),(.079,.12),(.137,.09),(.223,.07),(.361,.04)]:
   i=int((start+delay)*SR);end=min(len(audio),i+n)
   if i<len(audio):audio[i:end]+=signal[:end-i]*gain
 chords=[[50,57,60,64],[46,53,57,60],[48,55,58,62],[45,52,57,60]]
 if kind=='reveal':
  for i,m in enumerate([38,50,57,60,64,69]):add(m,.3+i*.12,10.5-i*.12,.045 if i<2 else .03,(i-2.5)*.13,'bow')
  for i,m in enumerate([69,72,76]):add(m,2+i*.7,7,.08,(i-1)*.3)
 else:
  for bar in range(8):
   chord=chords[bar%4];base=bar*8
   for i,m in enumerate(chord):add(m,base,7.6,.018 if kind=='metrics' else .024,(i-1.5)*.3,'bow')
   motif=[chord[2]+12,chord[3]+12,chord[1]+12,chord[2]+12]
   times=[.6,2.6,4.6,6.6] if kind=='metrics' else [.8,3.5,6.1]
   if kind=='reflection':times=[1.2,5.2]
   for i,x in enumerate(times):add(motif[i],base+x,3.8,.105 if kind=='metrics' else .12,(i%3-1)*.35)
   if kind=='metrics':
    for x in [1.6,3.6,5.6,7.6]:add(chord[1]+12,base+x,.5,.028, .25)
   if kind=='lab' and bar%2==0:add(chord[3]+24,base+5.5,2.3,.035,.5)
 # Low-level air gives the score a room rather than absolute digital silence.
 noise=rng.normal(0,.00012,audio.shape);audio+=noise
 if kind=='reveal':audio*=np.minimum(1,np.arange(len(audio))/(SR*.5))[:,None]*np.minimum(1,(len(audio)-np.arange(len(audio)))/(SR*2.5))[:,None]
 else:
  # Fold the final reverb into the start, then match boundary DC for a quiet loop.
  audio[:int(.5*SR)]*=np.linspace(0,1,int(.5*SR))[:,None]
  audio[-int(.5*SR):]*=np.linspace(1,0,int(.5*SR))[:,None]
 peak=np.max(np.abs(audio));audio*=min(1,.68/max(peak,1e-6))
 with tempfile.TemporaryDirectory() as tmp:
  wav=Path(tmp)/'score.wav';write(wav,SR,(audio*32767).astype(np.int16))
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libvorbis','-q:a','4',str(OUT/f'{name}.ogg')],check=True)
 print(name,round(peak,3),(OUT/f'{name}.ogg').stat().st_size)
for name,kind in [('office','office'),('metrics','metrics'),('reflection','reflection'),('lab','lab'),('reveal','reveal')]:render(name,kind)
(OUT/'SCORE.json').write_text(json.dumps({'author':'Gaming the System original procedural score','generator':'scripts/render_score.py','sampleRate':SR,'tracks':{'office':64,'metrics':64,'reflection':64,'lab':64,'reveal':12},'externalSamples':False},indent=2)+'\n')
