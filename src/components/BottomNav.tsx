import React from 'react';
import { Map, User } from 'lucide-react';
import { soundFx } from '../lib/sound';

export type TabType = 'path' | 'profile';

interface BottomNavProps {
  activeTab: TabType;
  onChangeTab: (tab: TabType) => void;
}

export const BottomNav: React.FC<BottomNavProps> = ({ activeTab, onChangeTab }) => {
  const tabs = [
    { id: 'path' as TabType, label: 'Aprender', icon: Map },
    { id: 'profile' as TabType, label: 'Perfil', icon: User }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white border-t-2 border-slate-200 px-2 py-2 max-w-5xl mx-auto w-full shadow-lg">
      <div className="flex items-center justify-around">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                soundFx.playClick();
                onChangeTab(tab.id);
              }}
              className={`flex flex-col items-center justify-center py-1 px-3 rounded-2xl transition-all cursor-pointer relative ${
                isActive
                  ? 'text-emerald-600 bg-emerald-50 border-2 border-emerald-500 font-black'
                  : 'text-slate-400 hover:text-slate-600 font-bold hover:bg-slate-50'
              }`}
            >
              <Icon className={`w-6 h-6 mb-0.5 ${isActive ? 'stroke-[2.5]' : 'stroke-2'}`} />
              <span className="text-[11px] font-extrabold">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
