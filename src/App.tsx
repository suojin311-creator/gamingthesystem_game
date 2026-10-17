import Gameplay from './Gameplay';
import LevelOne from './levels/level1/LevelOne';
import LevelTwo from './levels/level2/LevelTwo';
import LevelThree from './levels/level3/LevelThree';
import { PREVIEW_PLAYER_NAME } from './shared/utils/playerName';

// All previews use the same level components. Only their entry/continuation differs.
export default function App() {
  if (import.meta.env.MODE === 'level1') {
    return <LevelOne playerName={PREVIEW_PLAYER_NAME} />;
  }
  if (import.meta.env.MODE === 'level2') return <LevelTwo playerName={PREVIEW_PLAYER_NAME} />;
  if (import.meta.env.MODE === 'level3') return <LevelThree playerName={PREVIEW_PLAYER_NAME} />;
  return <Gameplay playerName={PREVIEW_PLAYER_NAME} />;
}
