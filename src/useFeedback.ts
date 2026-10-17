import { useCallback, useEffect, useRef, useState } from 'react';

export type Cue = 'tick' | 'report' | 'evidence' | 'student' | 'message';
const SETTINGS_KEY = 'gaming-the-system:sound:v1';

export function useFeedback() {
  const [muted, setMuted] = useState(() => {
    try { return localStorage.getItem(SETTINGS_KEY) === 'off'; } catch { return false; }
  });
  const [available, setAvailable] = useState(typeof window.AudioContext === 'function');
  const mutedRef = useRef(muted);
  const context = useRef<AudioContext | null>(null);
  const master = useRef<GainNode | null>(null);
  const voices = useRef(new Set<OscillatorNode>());

  const stop = useCallback(() => {
    voices.current.forEach(voice => { try { voice.stop(); } catch { /* Already ended. */ } });
    voices.current.clear();
  }, []);

  const unlock = useCallback(() => {
    if (mutedRef.current || typeof window.AudioContext !== 'function') return;
    try {
      if (!context.current) {
        context.current = new AudioContext();
        master.current = context.current.createGain();
        master.current.gain.value = 0.045;
        master.current.connect(context.current.destination);
      }
      if (context.current.state === 'suspended') void context.current.resume().catch(() => setAvailable(false));
    } catch { setAvailable(false); }
  }, []);

  const play = useCallback((cue: Cue) => {
    const audio = context.current;
    if (mutedRef.current || !audio || audio.state !== 'running' || !master.current || document.hidden) return;
    const notes: Record<Cue, number[]> = {
      tick: [420], report: [523.25, 659.25, 783.99],
      evidence: [360], student: [440, 392], message: [600],
    };
    notes[cue].forEach((frequency, index) => {
      const oscillator = audio.createOscillator();
      const envelope = audio.createGain();
      const when = audio.currentTime + index * 0.115;
      const length = cue === 'tick' ? 0.045 : cue === 'message' ? 0.075 : 0.21;
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(frequency, when);
      envelope.gain.setValueAtTime(0, when);
      envelope.gain.linearRampToValueAtTime(cue === 'tick' ? 0.35 : cue === 'message' ? 0.3 : 0.7, when + 0.008);
      envelope.gain.exponentialRampToValueAtTime(0.001, when + length);
      oscillator.connect(envelope);
      envelope.connect(master.current!);
      voices.current.add(oscillator);
      oscillator.onended = () => { voices.current.delete(oscillator); oscillator.disconnect(); envelope.disconnect(); };
      oscillator.start(when);
      oscillator.stop(when + length + 0.02);
    });
  }, []);

  const toggle = useCallback(() => {
    const next = !mutedRef.current;
    mutedRef.current = next;
    setMuted(next);
    if (next) stop();
    try { localStorage.setItem(SETTINGS_KEY, next ? 'off' : 'on'); } catch { /* Sound still works without storage. */ }
    if (!next) unlock();
  }, [stop, unlock]);

  useEffect(() => {
    const onVisibility = () => { if (document.hidden) stop(); };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      document.removeEventListener('visibilitychange', onVisibility);
      stop();
      const old = context.current;
      context.current = null;
      master.current = null;
      if (old && old.state !== 'closed') void old.close();
    };
  }, [stop]);

  return { muted, available, unlock, play, toggle, stop };
}
