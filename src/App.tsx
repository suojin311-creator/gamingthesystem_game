import Gameplay from './Gameplay';
import { PREVIEW_PLAYER_NAME } from './shared/utils/playerName';

// The dedicated preview starts at Level 2. A fresh full game starts at Level 1.
const initialLevel = import.meta.env.MODE === 'level2' ? 2 : 1;
export default function App() {
  return <Gameplay playerName={PREVIEW_PLAYER_NAME} initialLevel={initialLevel} />;
}
