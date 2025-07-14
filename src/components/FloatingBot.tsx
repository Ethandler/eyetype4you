import React from 'react';
import { Eye, Zap } from 'lucide-react';

interface FloatingBotProps {
  isTyping: boolean;
  progress: number;
  onClick: () => void;
}

const FloatingBot: React.FC<FloatingBotProps> = ({ isTyping, progress, onClick }) => {
  return (
    <div className="fixed top-8 right-8 z-50">
      <div 
        className={`relative cursor-pointer transition-all duration-300 ${
          isTyping ? 'animate-bounce-gentle' : 'animate-float'
        }`}
        onClick={onClick}
      >
        {/* Progress Ring */}
        {isTyping && (
          <div className="absolute inset-0 -m-2">
            <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="4"
                fill="none"
              />
              <circle
                cx="50"
                cy="50"
                r="45"
                stroke="#0099FF"
                strokeWidth="4"
                fill="none"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 45}`}
                strokeDashoffset={`${2 * Math.PI * 45 * (1 - progress / 100)}`}
                className="transition-all duration-300"
              />
            </svg>
          </div>
        )}
        
        {/* Bot Container */}
        <div className={`relative w-20 h-20 rounded-full glass-effect p-4 ${
          isTyping ? 'animate-glow' : 'hover:bg-white/20'
        } transition-all duration-300 group`}>
          
          {/* Eye Icon */}
          <div className="relative w-full h-full flex items-center justify-center">
            <Eye 
              className={`w-8 h-8 text-primary-400 transition-all duration-300 ${
                isTyping ? 'text-primary-300' : 'group-hover:text-primary-300'
              }`} 
            />
            
            {/* Typing indicator */}
            {isTyping && (
              <div className="absolute -bottom-1 -right-1">
                <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />
              </div>
            )}
          </div>
          
          {/* Pulse effect when not typing */}
          {!isTyping && (
            <div className="absolute inset-0 rounded-full bg-primary-500/20 animate-ping"></div>
          )}
        </div>
        
        {/* Status text */}
        <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
          <span className="text-xs text-white/60 font-medium">
            {isTyping ? `${Math.round(progress)}%` : 'Click me!'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default FloatingBot;