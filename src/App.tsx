import React, { useState, useEffect } from 'react';
import FloatingBot from './components/FloatingBot';
import MainMenu from './components/MainMenu';
import TypingInterface from './components/TypingInterface';
import SettingsPanel from './components/SettingsPanel';
import { TypingSettings, AppState } from './types';

const defaultSettings: TypingSettings = {
  speed: 0.12,
  errorRate: 1.2,
  punctuationPause: 18,
  spacePause: 8,
  thinkingPause: 2.5,
  darkMode: true,
};

function App() {
  const [appState, setAppState] = useState<AppState>('menu');
  const [settings, setSettings] = useState<TypingSettings>(defaultSettings);
  const [isTyping, setIsTyping] = useState(false);
  const [typingProgress, setTypingProgress] = useState(0);

  // Load settings from localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('eyetype4you-settings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);

  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem('eyetype4you-settings', JSON.stringify(settings));
  }, [settings]);

  const handleStartTyping = (text: string) => {
    setIsTyping(true);
    setAppState('typing');
    
    // Simulate typing progress
    const duration = text.length * settings.speed * 1000;
    const interval = duration / 100;
    let progress = 0;
    
    const progressInterval = setInterval(() => {
      progress += 1;
      setTypingProgress(progress);
      
      if (progress >= 100) {
        clearInterval(progressInterval);
        setTimeout(() => {
          setIsTyping(false);
          setTypingProgress(0);
          setAppState('menu');
        }, 1000);
      }
    }, interval);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-primary-900/20 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Floating Bot - Always visible */}
      <FloatingBot 
        isTyping={isTyping} 
        progress={typingProgress}
        onClick={() => setAppState(appState === 'menu' ? 'interface' : 'menu')}
      />

      {/* Main Content */}
      <div className="relative z-10">
        {appState === 'menu' && (
          <MainMenu 
            onStartTyping={() => setAppState('interface')}
            onOpenSettings={() => setAppState('settings')}
          />
        )}
        
        {appState === 'interface' && (
          <TypingInterface 
            settings={settings}
            onStartTyping={handleStartTyping}
            onBack={() => setAppState('menu')}
            onOpenSettings={() => setAppState('settings')}
          />
        )}
        
        {appState === 'settings' && (
          <SettingsPanel 
            settings={settings}
            onSettingsChange={setSettings}
            onBack={() => setAppState('menu')}
          />
        )}
      </div>
    </div>
  );
}

export default App;