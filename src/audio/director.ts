import office from './assets/office.ogg?inline';
import metrics from './assets/metrics.ogg?inline';
import reflection from './assets/reflection.ogg?inline';
import lab from './assets/lab.ogg?inline';
import reveal from './assets/reveal.ogg?inline';

export type Scene = 'office' | 'metrics' | 'reflection' | 'lab' | 'reveal' | 'silent';
export type Cue = 'tick' | 'report' | 'evidence' | 'message' | 'paper' | 'chapter' | 'notification' | 'warning' | 'submit' | 'vote' | 'transition';
type Preferences = { muted: boolean; music: number; effects: number };
const urls = { office, metrics, reflection, lab, reveal };
const defaults: Preferences = { muted: false, music: .58, effects: .65 };
const clamp = (n: number) => Math.max(0, Math.min(1, n));
function saved(): Preferences {
  try { const p=JSON.parse(localStorage.getItem('gts-sound')||'{}'); return { muted:p.muted===true,music:Number.isFinite(p.music)?clamp(p.music):defaults.music,effects:Number.isFinite(p.effects)?clamp(p.effects):defaults.effects }; } catch { return defaults; }
}

/** One output owner per document. Films report state; they never create competing music. */
class Director {
  preferences = saved();
  private subscribers = new Set<() => void>();
  private context: AudioContext | null = null;
  private master: GainNode | null = null;
  private musicBus: GainNode | null = null;
  private effectsBus: GainNode | null = null;
  private buffers = new Map<string, Promise<AudioBuffer>>();
  private active: { source: AudioBufferSourceNode; gain: GainNode; start: number; offset: number; scene: Scene } | null = null;
  private voices = new Set<AudioScheduledSourceNode>();
  private scene: Scene = 'silent';
  private intensity = .8;
  private offset = 0;
  private paused = false;
  private hidden = document.hidden;
  private revision = 0;
  private lastCue = new Map<string,number>();
  private revealed = false;
  readonly subscribe = (fn: () => void) => { this.subscribers.add(fn); return () => { this.subscribers.delete(fn); }; };
  readonly snapshot = () => this.preferences;
  get available() { return typeof window.AudioContext === 'function'; }
  get running() { return this.context?.state === 'running'; }
  get state() { return { scene:this.scene, playing:!!this.active && this.running && !this.hidden && !this.paused && !this.preferences.muted, unlocked:!!this.context, voices:this.voices.size, offset:this.offset }; }
  constructor() {
    document.addEventListener('visibilitychange',()=>{this.hidden=document.hidden;this.applyGains();this.sync();if(this.hidden)this.stopEffects();});
  }
  readonly unlock = () => {
    if (!this.available) return;
    if (!this.context) {
      try {
        this.context=new AudioContext();this.master=this.context.createGain();this.master.connect(this.context.destination);
        this.musicBus=this.context.createGain();this.musicBus.connect(this.master);
        this.effectsBus=this.context.createGain();this.effectsBus.connect(this.master);
        this.applyGains();
      } catch { return; }
    }
    const resume=this.context.state==='suspended'?this.context.resume():Promise.resolve();
    void resume.then(()=>this.sync()).catch(()=>{});
  };
  setPreferences(change: Partial<Preferences>) {
    this.preferences={...this.preferences,...change};
    try { localStorage.setItem('gts-sound',JSON.stringify(this.preferences)); } catch { /* Private mode. */ }
    this.applyGains();
    if(this.preferences.muted)this.stopEffects();
    this.sync();this.subscribers.forEach(fn=>fn());
  }
  readonly toggle = () => { this.setPreferences({muted:!this.preferences.muted});if(!this.preferences.muted)this.unlock(); };
  private applyGains() {
    if(!this.context)return;
    const t=this.context.currentTime;
    const set=(node:GainNode|null,value:number,seconds:number)=>{
      if(!node)return;
      node.gain.cancelScheduledValues(t);
      // Zero must remain exact even if Chromium suspended a silent graph's
      // automation processing before the next interaction sound starts.
      if(value===0)node.gain.setValueAtTime(0,t);
      else node.gain.setTargetAtTime(value,t,seconds);
    };
    set(this.master,this.preferences.muted||this.hidden?0:1,.035);
    set(this.musicBus,this.preferences.music*.58,.08);
    set(this.effectsBus,this.preferences.effects*.34,.03);
  }
  setScene(scene: Scene, intensity=.8, paused=false) {
    const changed=this.scene!==scene;
    if(changed){this.stopMusic(.9);this.scene=scene;this.offset=0;if(scene!=='reveal')this.revealed=false;}
    const wasPaused=this.paused;
    this.paused=paused;
    this.intensity=intensity;
    if(changed || wasPaused!==paused)this.sync();
    else if(this.active && this.context)this.active.gain.gain.setTargetAtTime(intensity,this.context.currentTime,.5);
  }
  private stopMusic(fade=.5) {
    const a=this.active,ctx=this.context;
    this.active=null;
    if(!a||!ctx)return;
    this.offset=a.offset+Math.max(0,ctx.currentTime-a.start);
    a.gain.gain.cancelScheduledValues(ctx.currentTime);a.gain.gain.setValueAtTime(a.gain.gain.value,ctx.currentTime);a.gain.gain.linearRampToValueAtTime(0,ctx.currentTime+fade);
    try{a.source.stop(ctx.currentTime+fade+.01);}catch{/* Ended. */}
  }
  private sync() {
    const token=++this.revision,ctx=this.context;
    if(!ctx)return;
    if(this.paused||this.hidden||this.preferences.muted||this.scene==='silent'||ctx.state!=='running') { this.stopMusic(.12);return; }
    if(this.active?.scene===this.scene)return;
    const wanted=this.scene;
    this.stopMusic(.9);
    // New scenes start at the beginning; pause/resume keeps the previous offset.
    const resumeOffset=this.offset;
    if(wanted==='reveal'&&this.revealed&&resumeOffset>=11.9)return;
    let promise=this.buffers.get(wanted);
    if(!promise){promise=fetch(urls[wanted]).then(r=>{if(!r.ok)throw new Error('audio');return r.arrayBuffer();}).then(b=>ctx.decodeAudioData(b));this.buffers.set(wanted,promise);}
    void promise.then(buffer=>{
      if(token!==this.revision||this.hidden||this.paused||this.preferences.muted)return;
      const source=ctx.createBufferSource(),gain=ctx.createGain();source.buffer=buffer;source.loop=wanted!=='reveal';
      source.connect(gain);gain.connect(this.musicBus!);gain.gain.setValueAtTime(0,ctx.currentTime);gain.gain.linearRampToValueAtTime(this.intensity,ctx.currentTime+(wanted==='reveal'?1.4:.9));
      const offset=wanted==='reveal'?Math.min(resumeOffset,buffer.duration-.01):resumeOffset%buffer.duration;
      this.active={source,gain,start:ctx.currentTime,offset,scene:wanted};
      source.onended=()=>{if(this.active?.source===source){this.active=null;this.offset=buffer.duration;if(wanted==='reveal')this.revealed=true;}source.disconnect();gain.disconnect();};
      source.start(0,offset);
    }).catch(()=>{this.buffers.delete(wanted);});
  }
  readonly stopEffects = () => {this.voices.forEach(s=>{try{s.stop();}catch{/* Ended. */}});this.voices.clear();};
  readonly cue = (cue: Cue) => {
    const c=this.context,bus=this.effectsBus;
    if(!c||!bus||c.state!=='running'||this.preferences.muted||this.hidden)return;
    const now=c.currentTime,previous=this.lastCue.get(cue)??-100;
    if(now-previous<(cue==='tick'?.11:.18))return;
    this.lastCue.set(cue,now);
    const voice=(freq:number,when:number,length:number,amp:number,noise=false)=>{
      const env=c.createGain(),filter=c.createBiquadFilter();filter.type='lowpass';filter.frequency.value=noise?1900:2600;
      let s:AudioBufferSourceNode|OscillatorNode;
      if(noise){const b=c.createBuffer(1,Math.ceil(c.sampleRate*length),c.sampleRate),a=b.getChannelData(0);for(let i=0;i<a.length;i++)a[i]=Math.random()*2-1;s=c.createBufferSource();s.buffer=b;}
      else {s=c.createOscillator();s.type='sine';s.frequency.setValueAtTime(freq,when);}
      env.gain.setValueAtTime(0,when);env.gain.linearRampToValueAtTime(amp,when+.008);env.gain.exponentialRampToValueAtTime(.0001,when+length);
      s.connect(filter);filter.connect(env);env.connect(bus);this.voices.add(s);
      s.onended=()=>{this.voices.delete(s);s.disconnect();filter.disconnect();env.disconnect();};s.start(when);s.stop(when+length+.02);
    };
    if(cue==='paper'){voice(0,now,.22,.16,true);return;}
    if(cue==='tick'){voice(540,now,.055,.26);voice(1090,now,.027,.07);voice(0,now,.025,.04,true);return;}
    if(cue==='warning'){voice(174.61,now,.6,.2);voice(220,now+.07,.5,.12);return;}
    if(cue==='message')return; // Authored dialogue stays quiet; no repetitive notification chatter.
    if(cue==='notification'){voice(659.25,now,.45,.2);voice(783.99,now+.12,.5,.17);return;}
    if(cue==='report'||cue==='submit'){voice(392,now,.28,.18);voice(523.25,now+.07,.34,.14);return;}
    if(cue==='chapter'||cue==='transition'){voice(196,now,.7,.15);voice(293.66,now+.12,.65,.08);return;}
    // Both voting choices deliberately share this neutral confirmation.
    voice(cue==='vote'?440:330,now,.16,.16);voice(660,now+.025,.12,.045);
  };
}
export const audioDirector=new Director();
