import React, { useState } from 'react';
import { ArrowLeft, Settings, Play, Zap, Clock, Target } from 'lucide-react';
import { TypingSettings } from '../types';

interface TypingInterfaceProps {
  settings: TypingSettings;
  onStartTyping: (text: string) => void;
  onBack: () => void;
  onOpenSettings: () => void;
}

const TypingInterface: React.FC<TypingInterfaceProps> = ({ 
  settings, 
  onStartTyping, 
  onBack, 
  onOpenSettings 
}) => {
  const [text, setText] = useState('');
  const [countdown, setCountdown] = useState(0);

  const handleStartTyping = () => {
    if (!text.trim()) return;
    
    // Start countdown
    setCountdown(4);
    const interval = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          onStartTyping(text);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const estimatedTime = Math.round(text.length * settings.speed);

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
        
        <h2 className="text-2xl font-bold text-white">Typing Interface</h2>
        
        <button
          onClick={onOpenSettings}
          className="button-secondary flex items-center gap-2"
        >
          <Settings className="w-4 h-4" />
          Settings
        </button>
      </div>

      <div className="max-w-4xl mx-auto">
        {/* Stats Bar */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="glass-effect rounded-xl p-4 text-center">
            <Zap className="w-6 h-6 text-primary-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">{settings.speed}s</div>
            <div className="text-white/60 text-sm">Speed/Char</div>
          </div>
          
          <div className="glass-effect rounded-xl p-4 text-center">
            <Target className="w-6 h-6 text-green-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">{settings.errorRate}%</div>
            <div className="text-white/60 text-sm">Error Rate</div>
          </div>
          
          <div className="glass-effect rounded-xl p-4 text-center">
            <Clock className="w-6 h-6 text-blue-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">{estimatedTime}s</div>
            <div className="text-white/60 text-sm">Est. Time</div>
          </div>
          
          <div className="glass-effect rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-white">{text.length}</div>
            <div className="text-white/60 text-sm">Characters</div>
          </div>
        </div>

        {/* Text Input */}
        <div className="glass-effect rounded-2xl p-6 mb-6">
          <label className="block text-white font-semibold mb-3">
            Enter text to type (supports emoji! 🎉):
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type your message here... You can include emojis like 😊 🚀 ✨"
            className="w-full h-40 bg-white/5 border border-white/20 rounded-xl p-4 text-white placeholder-white/40 resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            style={{ fontFamily: 'Consolas, monospace', fontSize: '16px' }}
          />
        </div>

        {/* Action Button */}
        <div className="text-center">
          {countdown > 0 ? (
            <div className="glass-effect rounded-2xl p-8 inline-block">
              <div className="text-6xl font-bold text-primary-400 mb-2">{countdown}</div>
              <div className="text-white/80">Focus your target window...</div>
            </div>
          ) : (
            <button
              onClick={handleStartTyping}
              disabled={!text.trim()}
              className={`button-primary text-xl py-4 px-8 flex items-center gap-3 mx-auto ${
                !text.trim() ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              <Play className="w-6 h-6" />
              Start Typing
            </button>
          )}
        </div>

        {/* Instructions */}
        <div className="mt-8 glass-effect rounded-xl p-6">
          <h3 className="text-white font-semibold mb-3">Instructions:</h3>
          <ol className="space-y-2 text-white/70">
            <li>1. Enter your text in the textarea above</li>
            <li>2. Click "Start Typing" to begin the 4-second countdown</li>
            <li>3. Quickly focus the window where you want the text typed</li>
            <li>4. Watch the bot simulate human-like typing with realistic delays</li>
            <li>5. The floating bot will show progress and animate during typing</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default TypingInterface;