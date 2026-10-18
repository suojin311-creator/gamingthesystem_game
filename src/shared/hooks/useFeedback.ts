import { useCallback, useEffect, useRef, useState } from 'react';

export type Cue = 'tick' | 'report' | 'evidence' | 'message' | 'paper' | 'chapter';

// One in-memory preference per open game, shared across level mounts.
let pageMuted = false;
// Keep the gesture-unlocked context across chapters. Each unmount still stops
// its voices; retaining a silent context avoids requiring a second audio gesture.
let pageAudio: AudioContext | null = null;
let pageMaster: GainNode | null = null;
const muteSubscribers = new Set<(muted: boolean) => void>();
function setPageMuted(value: boolean) {
  pageMuted = value;
  muteSubscribers.forEach(subscriber => subscriber(value));
}

export function useFeedback() {
  const [muted, setMuted] = useState(pageMuted);
  const [available, setAvailable] = useState(typeof window.AudioContext === 'function');
  const mutedRef = useRef(muted);
  const voices = useRef(new Set<OscillatorNode | AudioBufferSourceNode>());

  const stop = useCallback(() => {
    voices.current.forEach(voice => { try { voice.stop(); } catch { /* Already ended. */ } });
    voices.current.clear();
  }, []);

  const unlock = useCallback(() => {
    if (mutedRef.current || typeof window.AudioContext !== 'function') return;
    try {
      if (!pageAudio || pageAudio.state === 'closed') {
        pageAudio = new AudioContext();
        pageMaster = pageAudio.createGain();
        pageMaster.gain.value = 0.13;
        pageMaster.connect(pageAudio.destination);
      }
      if (pageAudio.state === 'suspended') void pageAudio.resume().catch(() => setAvailable(false));
    } catch { setAvailable(false); }
  }, []);

  const play = useCallback((cue: Cue) => {
    const audio = pageAudio;
    if (mutedRef.current || !audio || audio.state !== 'running' || !pageMaster || document.hidden) return;
    if (cue === 'paper') {
      const noise = audio.createBuffer(1, Math.ceil(audio.sampleRate * .24), audio.sampleRate);
      const samples = noise.getChannelData(0);
      for (let index = 0; index < samples.length; index++) samples[index] = Math.random() * 2 - 1;
      const source = audio.createBufferSource();
      const filter = audio.createBiquadFilter();
      const envelope = audio.createGain();
      source.buffer = noise;
      filter.type = 'bandpass'; filter.frequency.value = 1100; filter.Q.value = .7;
      envelope.gain.setValueAtTime(0, audio.currentTime);
      envelope.gain.linearRampToValueAtTime(.42, audio.currentTime + .035);
      envelope.gain.exponentialRampToValueAtTime(.001, audio.currentTime + .23);
      source.connect(filter); filter.connect(envelope); envelope.connect(pageMaster);
      voices.current.add(source);
      source.onended = () => { voices.current.delete(source); source.disconnect(); filter.disconnect(); envelope.disconnect(); };
      source.start();
      return;
    }
    const notes: Record<Exclude<Cue, 'paper'>, number[]> = {
      tick: [420], report: [523.25, 659.25, 783.99],
      evidence: [360], message: [600], chapter: [196, 174.61],
    };
    notes[cue].forEach((frequency, index) => {
      const oscillator = audio.createOscillator();
      const envelope = audio.createGain();
      const when = audio.currentTime + index * (cue === 'chapter' ? .18 : .115);
      const length = cue === 'chapter' ? .48 : cue === 'tick' ? 0.045 : cue === 'message' ? 0.075 : 0.21;
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(frequency, when);
      envelope.gain.setValueAtTime(0, when);
      envelope.gain.linearRampToValueAtTime(cue === 'chapter' ? .28 : cue === 'tick' ? 0.35 : cue === 'message' ? 0.15 : 0.7, when + (cue === 'chapter' ? .04 : .008));
      envelope.gain.exponentialRampToValueAtTime(0.001, when + length);
      oscillator.connect(envelope);
      envelope.connect(pageMaster!);
      voices.current.add(oscillator);
      oscillator.onended = () => { voices.current.delete(oscillator); oscillator.disconnect(); envelope.disconnect(); };
      oscillator.start(when);
      oscillator.stop(when + length + 0.02);
    });
  }, []);

  useEffect(() => {
    const sync = (value: boolean) => {
      mutedRef.current = value;
      setMuted(value);
      if (value) stop();
    };
    muteSubscribers.add(sync);
    return () => { muteSubscribers.delete(sync); };
  }, [stop]);

  const toggle = useCallback(() => {
    const next = !mutedRef.current;
    mutedRef.current = next;
    setMuted(next);
    setPageMuted(next);
    if (next) stop();
    if (!next) unlock();
  }, [stop, unlock]);

  const reset = useCallback(() => {
    stop();
    mutedRef.current = false;
    setMuted(false);
    setPageMuted(false);
  }, [stop]);

  useEffect(() => {
    const onVisibility = () => { if (document.hidden) stop(); };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      document.removeEventListener('visibilitychange', onVisibility);
      stop();
    };
  }, [stop]);

  return { muted, available, unlock, play, toggle, stop, reset };
}
