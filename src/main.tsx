import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import LevelOne from './LevelOne';
import './styles.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode><LevelOne /></StrictMode>,
);
