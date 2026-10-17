import Gameplay from './Gameplay';
import LevelOne from './levels/level1/LevelOne';
import { PREVIEW_PLAYER_NAME } from './shared/utils/playerName';

// All previews use the same level components. Only their entry/continuation differs.
const initialLevel = import.meta.env.MODE === 'level2' ? 2 : 1;
export default function App() {
  if (import.meta.env.MODE === 'level1') {
    return <LevelOne playerName={PREVIEW_PLAYER_NAME} />;
  }
  return <Gameplay playerName={PREVIEW_PLAYER_NAME} initialLevel={initialLevel} />;
}
