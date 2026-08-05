import React from 'react';
import { Trophy, Flame, ChevronUp, Shield } from 'lucide-react';
import { LeagueMember, UserProfile } from '../types';

interface LeaderboardViewProps {
  profile: UserProfile;
  members: LeagueMember[];
}

export const LeaderboardView: React.FC<LeaderboardViewProps> = ({ profile, members }) => {
  // Update member XP for user
  const updatedMembers = members.map((m) =>
    m.isUser ? { ...m, xp: profile.xp, name: `${profile.name} (Tú)` } : m
  ).sort((a, b) => b.xp - a.xp).map((m, idx) => ({ ...m, rank: idx + 1 }));

  return (
    <div className="pb-28 pt-4 px-4 max-w-xl mx-auto w-full space-y-6">
      {/* League Header Card */}
      <div className="bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 rounded-3xl p-6 text-slate-900 shadow-xl relative overflow-hidden text-center space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-white/30 backdrop-blur-md rounded-full text-xs font-black uppercase">
          <Trophy className="w-4 h-4 fill-amber-900 text-amber-900" />
          <span>Liga de Código • {profile.league}</span>
        </div>
        <h2 className="text-3xl font-black">Tabla de Clasificación</h2>
        <p className="text-xs font-bold text-amber-950 max-w-xs mx-auto">
          Los 3 primeros avanzan a la siguiente liga al finalizar la semana. ¡Gana XP completando lecciones!
        </p>
      </div>

      {/* Promotion Zone Info Banner */}
      <div className="bg-emerald-50 border-2 border-emerald-300 rounded-2xl p-3 flex items-center justify-between text-xs font-bold text-emerald-800">
        <div className="flex items-center gap-2">
          <ChevronUp className="w-5 h-5 text-emerald-600 stroke-[3]" />
          <span>Zona de Ascenso (Puestos 1 - 3)</span>
        </div>
        <span className="bg-emerald-200 text-emerald-900 px-2.5 py-0.5 rounded-full font-black">
          Quedan 3 días
        </span>
      </div>

      {/* Leaderboard Members List */}
      <div className="bg-white border-2 border-slate-200 rounded-3xl overflow-hidden shadow-xs divide-y-2 divide-slate-100">
        {updatedMembers.map((member) => {
          const isTop3 = member.rank! <= 3;
          return (
            <div
              key={member.id}
              className={`p-4 flex items-center justify-between transition-all ${
                member.isUser
                  ? 'bg-emerald-50 border-l-4 border-l-emerald-500 font-extrabold'
                  : 'hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center gap-4">
                {/* Rank Badge */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-black text-sm ${
                  member.rank === 1 ? 'bg-amber-400 text-slate-900 shadow-xs' :
                  member.rank === 2 ? 'bg-slate-300 text-slate-800' :
                  member.rank === 3 ? 'bg-amber-700 text-white' :
                  'text-slate-400 font-extrabold'
                }`}>
                  {member.rank === 1 ? '🥇' : member.rank === 2 ? '🥈' : member.rank === 3 ? '🥉' : member.rank}
                </div>

                {/* Avatar & Name */}
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{member.avatar}</span>
                  <div>
                    <div className="text-sm font-black text-slate-800 flex items-center gap-1.5">
                      <span>{member.name}</span>
                      {member.badge && <span>{member.badge}</span>}
                    </div>
                    {isTop3 && (
                      <span className="text-[10px] font-black uppercase text-emerald-600">Ascendiendo 🚀</span>
                    )}
                  </div>
                </div>
              </div>

              {/* XP */}
              <div className="flex items-center gap-1 font-black text-slate-700">
                <Flame className="w-4 h-4 fill-orange-500 text-orange-500" />
                <span>{member.xp} XP</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
