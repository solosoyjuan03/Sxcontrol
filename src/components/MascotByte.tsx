import React from 'react';
import { motion } from 'motion/react';
import { SkinId } from '../types';

interface MascotByteProps {
  mood?: 'idle' | 'happy' | 'thinking' | 'sad' | 'celebrate';
  skin?: SkinId;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  speakText?: string;
}

export const MascotByte: React.FC<MascotByteProps> = ({
  mood = 'idle',
  skin = 'default',
  size = 'md',
  className = '',
  speakText
}) => {
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-28 h-28',
    lg: 'w-40 h-40',
    xl: 'w-52 h-52'
  }[size];

  // Theme per skin
  const skinTheme = {
    default: {
      primaryGradStart: '#fb923c', // Vibrant Orange
      primaryGradEnd: '#ea580c',   // Deep Orange
      crestStart: '#ef4444',       // Fiery Red
      crestEnd: '#b91c1c',         // Crimson Red
      bellyColor: '#fef3c7',       // Creamy Warm
      wingColor: '#c2410c',        // Dark Warm Orange
      beakColor: '#f59e0b',        // Amber Gold
      cheekColor: '#f87171'
    },
    cyberpunk: {
      primaryGradStart: '#22d3ee', // Cyan
      primaryGradEnd: '#a855f7',   // Purple
      crestStart: '#f43f5e',       // Neon Magenta
      crestEnd: '#e11d48',
      bellyColor: '#c084fc',
      wingColor: '#6366f1',
      beakColor: '#22c55e',
      cheekColor: '#ec4899'
    },
    hacker: {
      primaryGradStart: '#3f3f46', // Dark Zinc
      primaryGradEnd: '#18181b',
      crestStart: '#22c55e',       // Matrix Green
      crestEnd: '#15803d',
      bellyColor: '#a1a1aa',
      wingColor: '#27272a',
      beakColor: '#4ade80',
      cheekColor: '#22c55e'
    },
    wizard: {
      primaryGradStart: '#818cf8', // Indigo
      primaryGradEnd: '#4f46e5',
      crestStart: '#ef4444',       // Classic Red Crest
      crestEnd: '#991b1b',
      bellyColor: '#e0e7ff',
      wingColor: '#3730a3',
      beakColor: '#fbbf24',        // Gold
      cheekColor: '#f472b6'
    }
  }[skin];

  // Motion animations based on mood
  const floatAnimation = {
    idle: {
      y: [0, -5, 0],
      rotate: [0, 2, -2, 0],
      transition: { duration: 2.5, repeat: Infinity, ease: 'easeInOut' }
    },
    happy: {
      y: [0, -14, 0],
      rotate: [0, -8, 8, 0],
      scale: [1, 1.08, 1],
      transition: { duration: 0.5, repeat: Infinity, ease: 'easeInOut' }
    },
    thinking: {
      rotate: [-5, 8, -5],
      y: [0, -3, 0],
      transition: { duration: 1.8, repeat: Infinity, ease: 'easeInOut' }
    },
    sad: {
      y: [0, 5, 0],
      rotate: [0, -3, 3, 0],
      scale: [1, 0.96, 1],
      transition: { duration: 2.2, repeat: Infinity, ease: 'easeInOut' }
    },
    celebrate: {
      y: [0, -20, 0],
      rotate: [0, 360],
      scale: [1, 1.2, 1],
      transition: { duration: 1.1, repeat: Infinity, ease: 'easeInOut' }
    }
  }[mood];

  return (
    <div className={`relative flex flex-col items-center justify-center ${className}`}>
      {/* Speech Bubble */}
      {speakText && (
        <motion.div
          initial={{ opacity: 0, y: 10, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          className="mb-3 max-w-xs bg-white border-2 border-orange-500 shadow-xl rounded-2xl p-3 text-sm font-black text-slate-800 relative z-20 text-center"
        >
          {speakText}
          <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-white border-r-2 border-b-2 border-orange-500 rotate-45"></div>
        </motion.div>
      )}

      {/* Pico the Woodpecker SVG */}
      <motion.div animate={floatAnimation} className={`${sizeClasses} relative filter drop-shadow-lg`}>
        <svg viewBox="0 0 100 100" className="w-full h-full overflow-visible">
          <defs>
            {/* Body Plumage Gradient */}
            <linearGradient id={`grad-body-${skin}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={skinTheme.primaryGradStart} />
              <stop offset="100%" stopColor={skinTheme.primaryGradEnd} />
            </linearGradient>

            {/* Red Crest Gradient */}
            <linearGradient id={`grad-crest-${skin}`} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor={skinTheme.crestStart} />
              <stop offset="100%" stopColor={skinTheme.crestEnd} />
            </linearGradient>

            {/* Beak Gradient */}
            <linearGradient id={`grad-beak-${skin}`} x1="0%" y1="0%" x2="100%" y2="50%">
              <stop offset="0%" stopColor="#fef08a" />
              <stop offset="100%" stopColor={skinTheme.beakColor} />
            </linearGradient>
          </defs>

          {/* Tail Feathers */}
          <g>
            <path d="M 38 80 L 26 96 L 42 86 Z" fill={skinTheme.wingColor} />
            <path d="M 44 82 L 40 98 L 50 86 Z" fill={skinTheme.crestEnd} />
            <path d="M 50 82 L 56 96 L 56 84 Z" fill={skinTheme.wingColor} />
          </g>

          {/* Red Crest (Copete / Pelirrojo de Carpintero) */}
          <path
            d="M 42 22 C 34 8, 48 2, 54 8 C 60 0, 72 6, 68 18 C 76 12, 80 22, 72 28 C 62 30, 52 28, 42 22 Z"
            fill={`url(#grad-crest-${skin})`}
            stroke="#991b1b"
            strokeWidth="1.2"
          />

          {/* Body Base */}
          <ellipse cx="48" cy="62" rx="22" ry="23" fill={`url(#grad-body-${skin})`} stroke="#7c2d12" strokeWidth="2" />

          {/* Creamy Belly */}
          <ellipse cx="44" cy="65" rx="14" ry="17" fill={skinTheme.bellyColor} />

          {/* Head */}
          <circle cx="50" cy="36" r="21" fill={`url(#grad-body-${skin})`} stroke="#7c2d12" strokeWidth="2" />

          {/* Woodpecker Beak (Largo y afilado) */}
          {mood === 'happy' || mood === 'celebrate' ? (
            <g>
              {/* Upper Beak */}
              <path d="M 64 32 L 95 36 L 64 40 Z" fill={`url(#grad-beak-${skin})`} stroke="#b45309" strokeWidth="1.5" />
              {/* Open Mouth Inside */}
              <path d="M 64 39 L 85 41 L 64 44 Z" fill="#e11d48" />
              {/* Lower Beak */}
              <path d="M 64 42 L 90 46 L 64 46 Z" fill={skinTheme.beakColor} stroke="#b45309" strokeWidth="1" />
            </g>
          ) : (
            <path d="M 64 33 L 95 39 L 64 45 Z" fill={`url(#grad-beak-${skin})`} stroke="#b45309" strokeWidth="1.5" />
          )}

          {/* Cheeks (Rubor rosa) */}
          <ellipse cx="38" cy="42" rx="4" ry="3" fill={skinTheme.cheekColor} opacity="0.6" />

          {/* Eyes according to Mood */}
          {mood === 'happy' || mood === 'celebrate' ? (
            /* Joy Eyes ^ */
            <g>
              <path d="M 38 34 Q 44 26 50 34" fill="none" stroke="#1e293b" strokeWidth="3.5" strokeLinecap="round" />
            </g>
          ) : mood === 'sad' ? (
            /* Sad Eyes T_T */
            <g>
              <circle cx="44" cy="36" r="4" fill="#1e293b" />
              <path d="M 38 28 L 50 31" stroke="#1e293b" strokeWidth="2" strokeLinecap="round" />
              {/* Tear drop */}
              <path d="M 38 42 Q 36 46 38 48 Q 40 46 38 42 Z" fill="#38bdf8" />
            </g>
          ) : mood === 'thinking' ? (
            /* Thinking Eyes Looking up */
            <g>
              <circle cx="44" cy="34" r="5.5" fill="#ffffff" stroke="#1e293b" strokeWidth="1.5" />
              <circle cx="46" cy="31" r="3" fill="#1e293b" />
              <circle cx="47" cy="30" r="1" fill="#ffffff" />
            </g>
          ) : (
            /* Standard Big Cute Bird Eye */
            <g>
              <ellipse cx="45" cy="34" rx="6.5" ry="7.5" fill="#ffffff" stroke="#1e293b" strokeWidth="1.5" />
              <circle cx="46" cy="34" r="4" fill="#0f172a" />
              <circle cx="44" cy="32" r="1.5" fill="#ffffff" />
              <circle cx="48" cy="36" r="0.8" fill="#ffffff" opacity="0.8" />
            </g>
          )}

          {/* Left Wing (Ala plegada o aleteando) */}
          {mood === 'happy' || mood === 'celebrate' ? (
            <motion.path
              animate={{ rotate: [-10, 20, -10] }}
              transition={{ duration: 0.3, repeat: Infinity }}
              d="M 28 52 C 12 50, 10 70, 26 78 C 36 74, 38 60, 28 52 Z"
              fill={skinTheme.wingColor}
              stroke="#7c2d12"
              strokeWidth="1.5"
            />
          ) : (
            <path
              d="M 28 54 C 14 58, 16 78, 30 80 C 40 76, 38 62, 28 54 Z"
              fill={skinTheme.wingColor}
              stroke="#7c2d12"
              strokeWidth="1.5"
            />
          )}

          {/* White Feather Spots on Wing */}
          <circle cx="22" cy="68" r="1.5" fill="#ffffff" opacity="0.9" />
          <circle cx="26" cy="73" r="1.5" fill="#ffffff" opacity="0.9" />

          {/* Feet (Patitas amarillas agarradas) */}
          <path d="M 38 84 L 38 91 M 35 91 L 41 91" stroke="#f59e0b" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M 52 84 L 52 91 M 49 91 L 55 91" stroke="#f59e0b" strokeWidth="2.5" strokeLinecap="round" />

          {/* Skin Accessories */}
          {skin === 'wizard' && (
            /* Wizard Hat on top of Crest */
            <g>
              <path d="M 24 16 L 46 -8 L 62 14 Z" fill="#4c1d95" stroke="#a855f7" strokeWidth="2" />
              <ellipse cx="43" cy="15" rx="20" ry="4" fill="#581c87" stroke="#a855f7" strokeWidth="1.5" />
              <path d="M 46 0 L 48 4 L 52 4 L 49 7 L 50 11 L 46 8 L 42 11 L 43 7 L 40 4 L 44 4 Z" fill="#fbbf24" />
            </g>
          )}

          {skin === 'hacker' && (
            /* Hacker Visor / Matrix Glasses */
            <g>
              <rect x="34" y="28" width="24" height="10" rx="3" fill="#022c22" stroke="#22c55e" strokeWidth="1.5" />
              <line x1="36" y1="33" x2="56" y2="33" stroke="#4ade80" strokeWidth="1" strokeDasharray="2,2" />
            </g>
          )}

          {skin === 'cyberpunk' && (
            /* Cyberpunk Neon Visor */
            <g>
              <polygon points="32,28 58,26 56,38 30,38" fill="#06b6d4" opacity="0.85" stroke="#ec4899" strokeWidth="1.5" />
              <line x1="30" y1="33" x2="58" y2="31" stroke="#ffffff" strokeWidth="1.5" />
            </g>
          )}
        </svg>
      </motion.div>
    </div>
  );
};

