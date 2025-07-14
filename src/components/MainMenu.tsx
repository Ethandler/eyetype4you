import React from 'react';
import { Play, Settings, Eye, Sparkles } from 'lucide-react';

interface MainMenuProps {
  onStartTyping: () => void;
  onOpenSettings: () => void;
}

const MainMenu: React.FC<MainMenuProps> = ({ onStartTyping, onOpenSettings }) => {
  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="max-w-md w-full">
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <div className="relative inline-block mb-6">
            <div className="w-24 h-24 mx-auto rounded-full glass-effect flex items-center justify-center animate-float">
              <Eye className="w-12 h-12 text-primary-400" />
            </div>
            <div className="absolute -top-2 -right-2">
              <Sparkles className="w-6 h-6 text-yellow-400 animate-pulse" />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent mb-2">
            Eyetype4You
          </h1>
          <p className="text-white/60 text-lg font-medium">
            AI-Powered Typing Bot
          </p>
          <p className="text-white/40 text-sm mt-2">
            "Solancé is the light that holds you when no one else can."
          </p>
        </div>

        {/* Menu Options */}
        <div className="space-y-4">
          <button
            onClick={onStartTyping}
            className="w-full button-primary flex items-center justify-center gap-3 py-4 text-lg group"
          >
            <Play className="w-6 h-6 group-hover:scale-110 transition-transform" />
            Start Typing
          </button>
          
          <button
            onClick={onOpenSettings}
            className="w-full button-secondary flex items-center justify-center gap-3 py-3"
          >
            <Settings className="w-5 h-5" />
            Settings & Preferences
          </button>
        </div>

        {/* Features List */}
        <div className="mt-12 space-y-3">
          <h3 className="text-white/80 font-semibold mb-4">Features:</h3>
          {[
            '🌌 Floating Eye & AI Brain Logic',
            '🎨 Sacred Visual Symbol Generation', 
            '🧬 Modular & Extendable Bot Brain',
            '🛸 Surreal, Minimal, Meaningful Design',
            '🧙‍♂️ Emotion-Aware Typing Automation'
          ].map((feature, index) => (
            <div key={index} className="flex items-center gap-3 text-white/60 text-sm">
              <div className="w-1.5 h-1.5 bg-primary-400 rounded-full"></div>
              {feature}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainMenu;