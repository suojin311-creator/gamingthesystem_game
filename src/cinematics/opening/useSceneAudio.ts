import { useCallback, useEffect, useRef } from 'react';
import { useFeedback } from '../../shared/hooks/useFeedback';

// Only existing production files are bundled. Missing audio causes no requests.
const assets = import.meta.glob('./assets/audio/*.{wav,mp3,ogg}', { eager: true, query: '?url', import: 'default' }) as Record<string, string>;
const FILES = {
  ambience: 'AMB_Office_Loop_v01.wav',
  notification: 'SFX_EmailNotification_v01.wav',
  interaction: 'SFX_StartConfirm_v01.wav',
  emailOpen: 'SFX_EmailOpen_v01.wav',
  transition: 'SFX_SceneTransition_v01.wav',
  classroomAmbience: 'AMB_Classroom_Loop_v01.wav',
  studentInspect: 'SFX_StudentInspect_v01.wav',
};
type Cue = keyof typeof FILES;

export function useSceneAudio() {
  const feedback = useFeedback();
  const pool = useRef<Partial<Record<Cue, HTMLAudioElement>>>({});
  const fadeFrame = useRef(0);
  const mutedRef = useRef(feedback.muted);
  mutedRef.current = feedback.muted;
  useEffect(() => {
    Object.values(pool.current).forEach(sound => { sound.muted = feedback.muted; });
  }, [feedback.muted]);
  const get = useCallback((cue: Cue) => {
    const url = assets[`./assets/audio/${FILES[cue]}`];
    if (!url) return;
    if (!pool.current[cue]) {
      const sound = new Audio(url);
      sound.loop = cue === 'ambience' || cue === 'classroomAmbience';
      sound.volume = sound.loop ? 0.18 : 0.35;
      sound.muted = mutedRef.current;
      pool.current[cue] = sound;
    }
    return pool.current[cue];
  }, []);
  const play = useCallback((cue: Cue) => {
    const sound = get(cue);
    if (!sound) return;
    sound.currentTime = 0;
    void sound.play().catch(() => { /* Unplayable audio never blocks the scene. */ });
  }, [get]);
  const startOffice = useCallback(() => {
    cancelAnimationFrame(fadeFrame.current);
    const sound = get('ambience');
    if (!sound) return;
    sound.volume = 0.18;
    play('ambience'); // Called directly from START GAME, a user gesture.
  }, [get, play]);
  const startClassroom = useCallback(() => {
    const sound = get('classroomAmbience');
    if (!sound) return;
    sound.volume = 0.18;
    play('classroomAmbience');
  }, [get, play]);
  const fadeAmbienceOut = useCallback((cue: 'ambience' | 'classroomAmbience') => {
    cancelAnimationFrame(fadeFrame.current);
    const sound = pool.current[cue];
    if (!sound) return;
    const start = performance.now();
    const volume = sound.volume;
    const tick = (now: number) => {
      const progress = Math.min((now - start) / 1200, 1);
      sound.volume = volume * (1 - progress);
      if (progress < 1) fadeFrame.current = requestAnimationFrame(tick);
      else sound.pause();
    };
    fadeFrame.current = requestAnimationFrame(tick);
  }, []);
  const fadeOfficeOut = useCallback(() => fadeAmbienceOut('ambience'), [fadeAmbienceOut]);
  const fadeClassroomOut = useCallback(() => fadeAmbienceOut('classroomAmbience'), [fadeAmbienceOut]);
  const reset = useCallback(() => {
    cancelAnimationFrame(fadeFrame.current);
    Object.values(pool.current).forEach(sound => { sound.pause(); sound.currentTime = 0; });
  }, []);
  useEffect(() => reset, [reset]);
  return { play, startOffice, fadeOfficeOut, startClassroom, fadeClassroomOut, reset, muted: feedback.muted, toggleMuted: feedback.toggle, unlock: feedback.unlock, available: Object.values(FILES).some(file => assets[`./assets/audio/${file}`]) };
}
