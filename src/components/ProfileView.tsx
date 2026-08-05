import React from 'react';
import { Award, CheckCircle2 } from 'lucide-react';
import { Achievement, UserProfile } from '../types';
import { MascotByte } from './MascotByte';

interface ProfileViewProps {
  profile: UserProfile;
}

export const ProfileView: React.FC<ProfileViewProps> = ({ profile }) => {
  const achievements: Achievement[] = [
    {
      id: 'a1',
      title: 'Primeros Pasos',
      description: 'Completa tu primera lección de código.',
      icon: '⚡',
      progress: Math.min(1, profile.totalLessonsCompleted),
      maxProgress: 1,
      unlocked: profile.totalLessonsCompleted >= 1
    },
    {
      id: 'a2',
      title: 'Espíritu Imparable',
      description: 'Mantén una racha de al menos 3 días.',
      icon: '🔥',
      progress: Math.min(3, profile.streak),
      maxProgress: 3,
      unlocked: profile.streak >= 3
    },
    {
      id: 'a3',
      title: 'Estudiante Dedicado',
      description: 'Acumula más de 150 XP de práctica.',
      icon: '⭐',
      progress: Math.min(150, profile.xp),
      maxProgress: 150,
      unlocked: profile.xp >= 150
    },
    {
      id: 'a4',
      title: 'Programador Imparable',
      description: 'Completa al menos 3 lecciones de código.',
      icon: '🏆',
      progress: Math.min(3, profile.totalLessonsCompleted),
      maxProgress: 3,
      unlocked: profile.totalLessonsCompleted >= 3
    }
  ];

  return (
    <div className="pb-28 pt-4 px-4 max-w-xl mx-auto w-full space-y-6">
      {/* Profile Header Card */}
      <div className="bg-white border-2 border-slate-200 rounded-3xl p-6 shadow-xs flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 rounded-2xl bg-emerald-100 border-2 border-emerald-300 flex items-center justify-center text-4xl shadow-xs">
            {profile.avatar}
          </div>
          <div>
            <span className="text-xs font-black uppercase text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
              Desarrollo de Software
            </span>
            <h2 className="text-xl font-black text-slate-800 mt-1">{profile.name}</h2>
            <p className="text-xs font-semibold text-slate-400">Estudiante Técnico</p>
          </div>
        </div>
        <MascotByte skin={profile.equippedSkin} size="sm" mood="happy" />
      </div>

      {/* Main Stats Grid */}
      <div className="grid grid-cols-3 gap-3 font-black">
        <div className="bg-orange-50 border-2 border-orange-200 rounded-2xl p-4 flex flex-col items-center text-center">
          <div className="w-10 h-10 rounded-xl bg-orange-200 flex items-center justify-center text-orange-700 text-xl mb-1">
            🔥
          </div>
          <div className="text-lg text-orange-900">{profile.streak} Días</div>
          <div className="text-[10px] uppercase text-orange-600 font-bold">Racha Actual</div>
        </div>

        <div className="bg-amber-50 border-2 border-amber-200 rounded-2xl p-4 flex flex-col items-center text-center">
          <div className="w-10 h-10 rounded-xl bg-amber-200 flex items-center justify-center text-amber-700 text-xl mb-1">
            ⚡
          </div>
          <div className="text-lg text-amber-900">{profile.xp} XP</div>
          <div className="text-[10px] uppercase text-amber-600 font-bold">Experiencia</div>
        </div>

        <div className="bg-purple-50 border-2 border-purple-200 rounded-2xl p-4 flex flex-col items-center text-center">
          <div className="w-10 h-10 rounded-xl bg-purple-200 flex items-center justify-center text-purple-700 text-xl mb-1">
            🎯
          </div>
          <div className="text-lg text-purple-900">{profile.totalLessonsCompleted}</div>
          <div className="text-[10px] uppercase text-purple-600 font-bold">Lecciones</div>
        </div>
      </div>

      {/* Achievements Section */}
      <div className="space-y-3">
        <h3 className="text-sm font-black uppercase tracking-wider text-slate-400 px-1 flex items-center gap-2">
          <Award className="w-4 h-4 text-emerald-600" />
          <span>Logros e Insignias</span>
        </h3>

        <div className="space-y-3">
          {achievements.map((ach) => (
            <div
              key={ach.id}
              className={`bg-white border-2 rounded-2xl p-4 flex items-center justify-between shadow-xs transition-all ${
                ach.unlocked ? 'border-emerald-300 bg-emerald-50/40' : 'border-slate-200 opacity-80'
              }`}
            >
              <div className="flex items-center gap-3.5">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl ${
                  ach.unlocked ? 'bg-amber-100 border-2 border-amber-300' : 'bg-slate-100'
                }`}>
                  {ach.icon}
                </div>
                <div>
                  <div className="font-extrabold text-slate-800 text-sm flex items-center gap-1.5">
                    <span>{ach.title}</span>
                    {ach.unlocked && <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
                  </div>
                  <div className="text-xs text-slate-500 font-medium">{ach.description}</div>
                </div>
              </div>

              {ach.unlocked && (
                <div className="text-right">
                  <span className="text-xs font-black text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                    Completado
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
