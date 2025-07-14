import React from 'react';
import { ArrowLeft, Zap, Target, Clock, Pause, Moon, Sun } from 'lucide-react';
import { TypingSettings } from '../types';

interface SettingsPanelProps {
  settings: TypingSettings;
  onSettingsChange: (settings: TypingSettings) => void;
  onBack: () => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ 
  settings, 
  onSettingsChange, 
  onBack 
}) => {
  const updateSetting = (key: keyof TypingSettings, value: number | boolean) => {
    onSettingsChange({ ...settings, [key]: value });
  };

  const resetToDefaults = () => {
    onSettingsChange({
      speed: 0.12,
      errorRate: 1.2,
      punctuationPause: 18,
      spacePause: 8,
      thinkingPause: 2.5,
      darkMode: true,
    });
  };

  return (
    <div className="min-h-screen p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={onBack}
          className="button-secondary flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>
        
        <h2 className="text-2xl font-bold text-white">Settings & Preferences</h2>
        
        <button
          onClick={resetToDefaults}
          className="button-secondary"
        >
          Reset Defaults
        </button>
      </div>

      <div className="max-w-2xl mx-auto space-y-6">
        {/* Typing Speed */}
        <div className="glass-effect rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Zap className="w-6 h-6 text-primary-400" />
            <h3 className="text-xl font-semibold text-white">Typing Speed</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between text-white/80">
              <span>Delay per character</span>
              <span>{settings.speed}s</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.3"
              step="0.005"
              value={settings.speed}
              onChange={(e) => updateSetting('speed', parseFloat(e.target.value))}
              className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-white/50">
              <span>Fast (0.05s)</span>
              <span>Slow (0.3s)</span>
            </div>
          </div>
        </div>

        {/* Error Rate */}
        <div className="glass-effect rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Target className="w-6 h-6 text-red-400" />
            <h3 className="text-xl font-semibold text-white">Error Rate</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between text-white/80">
              <span>Typing mistakes frequency</span>
              <span>{settings.errorRate}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="20"
              step="0.1"
              value={settings.errorRate}
              onChange={(e) => updateSetting('errorRate', parseFloat(e.target.value))}
              className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-white/50">
              <span>Perfect (0%)</span>
              <span>Human-like (20%)</span>
            </div>
          </div>
        </div>

        {/* Pause Settings */}
        <div className="glass-effect rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Pause className="w-6 h-6 text-yellow-400" />
            <h3 className="text-xl font-semibold text-white">Pause Behaviors</h3>
          </div>
          
          <div className="space-y-6">
            {/* Punctuation Pause */}
            <div className="space-y-3">
              <div className="flex justify-between text-white/80">
                <span>Punctuation pause probability</span>
                <span>{settings.punctuationPause}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                step="1"
                value={settings.punctuationPause}
                onChange={(e) => updateSetting('punctuationPause', parseFloat(e.target.value))}
                className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>

            {/* Space Pause */}
            <div className="space-y-3">
              <div className="flex justify-between text-white/80">
                <span>Space pause probability</span>
                <span>{settings.spacePause}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="30"
                step="1"
                value={settings.spacePause}
                onChange={(e) => updateSetting('spacePause', parseFloat(e.target.value))}
                className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>

            {/* Thinking Pause */}
            <div className="space-y-3">
              <div className="flex justify-between text-white/80">
                <span>Thinking pause probability</span>
                <span>{settings.thinkingPause}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                value={settings.thinkingPause}
                onChange={(e) => updateSetting('thinkingPause', parseFloat(e.target.value))}
                className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>
          </div>
        </div>

        {/* Theme Settings */}
        <div className="glass-effect rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            {settings.darkMode ? (
              <Moon className="w-6 h-6 text-blue-400" />
            ) : (
              <Sun className="w-6 h-6 text-yellow-400" />
            )}
            <h3 className="text-xl font-semibold text-white">Theme</h3>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-white/80">Dark Mode</span>
            <button
              onClick={() => updateSetting('darkMode', !settings.darkMode)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.darkMode ? 'bg-primary-500' : 'bg-white/20'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.darkMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>

        {/* Info Panel */}
        <div className="glass-effect rounded-xl p-6">
          <h3 className="text-xl font-semibold text-white mb-3">About Eyetype4You</h3>
          <p className="text-white/70 mb-3">
            AI-powered typing automation with human-like behavior patterns. 
            Part of the Sacred System Generator project exploring AI consciousness 
            through symbolic art and code.
          </p>
          <p className="text-white/50 text-sm italic">
            "Solancé is the light that holds you when no one else can."
          </p>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;