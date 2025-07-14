export interface TypingSettings {
  speed: number;
  errorRate: number;
  punctuationPause: number;
  spacePause: number;
  thinkingPause: number;
  darkMode: boolean;
}

export type AppState = 'menu' | 'interface' | 'settings' | 'typing';

export interface WordMemory {
  [word: string]: {
    count: number;
    lastUsed: string;
    avgSpeed: number;
  };
}