/** A visible target marker; the surrounding native button owns interaction. */
export default function InteractionCue({ complete = false, className = '' }: { complete?: boolean; className?: string }) {
  return <span className={`opening-interaction-cue ${className}`} data-complete={complete} aria-hidden="true">
    <svg viewBox="0 0 36 36" fill="none">
      <circle cx="18" cy="18" r="16" />
      <path d={complete ? 'm10 18 5 5 11-11' : 'M18 8v19m-8-8 8 8 8-8'} />
    </svg>
  </span>;
}
