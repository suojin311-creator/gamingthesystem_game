import { useState, useSyncExternalStore } from 'react';
import { audioDirector } from './director';
import './audio.css';
export default function AudioControls() {
  const [open,setOpen]=useState(false);
  const prefs=useSyncExternalStore(audioDirector.subscribe,audioDirector.snapshot);
  if(!audioDirector.available)return null;
  return <aside className="gts-audio-controls" aria-label="Sound settings">
    <button className="gts-audio-toggle" type="button" aria-expanded={open} aria-controls="gts-audio-settings" onClick={()=>{audioDirector.unlock();setOpen(!open);}}><span aria-hidden="true">{prefs.muted?'♫̸':'♫'}</span><span>Sound</span></button>
    {open&&<div id="gts-audio-settings" className="gts-audio-settings"><button type="button" onClick={audioDirector.toggle}>{prefs.muted?'Turn sound on':'Mute all sound'}</button><label>Music<input aria-label="Music volume" type="range" min="0" max="1" step=".01" value={prefs.music} onChange={e=>audioDirector.setPreferences({music:Number(e.target.value)})}/></label><label>Sound effects<input aria-label="Sound effects volume" type="range" min="0" max="1" step=".01" value={prefs.effects} onChange={e=>audioDirector.setPreferences({effects:Number(e.target.value)})}/></label></div>}
  </aside>;
}
