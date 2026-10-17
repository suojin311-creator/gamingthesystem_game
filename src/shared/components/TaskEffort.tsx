import '../styles/task-effort.css';

/** A qualitative task vignette. No invented numerical effort/learning score. */
export default function TaskEffort({ effort }: { effort: 'low' | 'medium' | 'high' }) {
  const low = effort === 'low';
  const high = effort === 'high';
  return <svg className={`task-scene task-scene-${effort}`} viewBox="0 0 160 100" fill="none" aria-hidden="true">
    <ellipse cx="81" cy="90" rx="67" ry="5" fill="#b3a081" opacity=".14" />
    <path d="M12 79H148M23 80V90M139 80V90" stroke="#b59b73" strokeWidth="3" strokeLinecap="round" />
    {high && <g className="task-extra-pages" stroke="#b88b5d" strokeWidth="1.3"><path d="M16 76H48V70H16Z" fill="#e8d7b9" /><path d="M19 70H49V64H19Z" fill="#f6e5c9" /><path d="M22 64H51V58H22Z" fill="#fcf4e3" /></g>}
    <path d="M49 74L60 48H91L81 74H49Z" fill="#fffcf2" stroke="#bca77f" strokeWidth="1.5" />
    <path d="M62 55H81M59 61H75M57 67H68" stroke="#b8b493" strokeWidth="1.7" strokeLinecap="round" />
    {low && <path d="M72 67L75 70L82 62" stroke="#87996a" strokeWidth="2" strokeLinecap="round" />}
    <g className="task-person" transform={low ? 'translate(8 -1) rotate(9 110 65)' : high ? 'rotate(-10 111 66)' : undefined}>
      <path d="M99 51Q109 44 123 51L130 77H96Z" fill={high ? '#b66c50' : low ? '#b9a17b' : '#8c9e77'} />
      <path d="M106 44V51M118 44V51" stroke="#b88e66" strokeWidth="3" />
      <circle cx="112" cy="29" r="15" fill="#ead6b4" stroke="#ac8d65" strokeWidth="1.5" />
      <path d="M97 27Q97 8 113 12Q129 12 127 28L122 21L116 23L111 19L99 29" fill="#6d6450" />
      <path d={low ? 'M103 31H108M116 31H121' : 'M104 31H107M116 31H119'} stroke="#5d5e48" strokeWidth="1.7" strokeLinecap="round" />
      <path d={low ? 'M108 39Q113 42 118 38' : 'M109 39H116'} stroke="#9c704d" strokeWidth="1.4" strokeLinecap="round" />
      {low ? <path d="M101 56L116 66L126 54M125 59L114 71L101 65" stroke="#d1b38a" strokeWidth="6" strokeLinecap="round" /> : <g className="task-writing-hand"><path d="M102 55L94 66L78 67M121 57L125 73H95" stroke="#d1b38a" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" /><path d="M78 64L71 73" stroke="#6b6b52" strokeWidth="2.5" strokeLinecap="round" /></g>}
    </g>
    {high && <g className="task-speed" stroke="#b98860" strokeWidth="2" strokeLinecap="round"><path d="M134 33L144 29M137 42H149M132 22L137 15" /></g>}
    {low && <path d="M134 53Q144 54 142 65" stroke="#b6a488" strokeWidth="1.5" strokeLinecap="round" />}
  </svg>;
}
