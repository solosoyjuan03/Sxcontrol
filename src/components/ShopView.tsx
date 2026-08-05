import React from 'react';
import { Gem, Shield, Check, Shirt } from 'lucide-react';
import { SkinId, UserProfile } from '../types';
import { soundFx } from '../lib/sound';

interface ShopViewProps {
  profile: UserProfile;
  onBuyStreakFreeze: () => void;
  onEquipSkin: (skinId: SkinId) => void;
  onBuySkin: (skinId: SkinId, cost: number) => void;
}

export const ShopView: React.FC<ShopViewProps> = ({
  profile,
  onBuyStreakFreeze,
  onEquipSkin,
  onBuySkin
}) => {
  const skins: { id: SkinId; name: string; icon: string; cost: number; desc: string; color: string }[] = [
    {
      id: 'default',
      name: 'Pico Naranja Pelirrojo',
      icon: '🐦',
      cost: 0,
      desc: 'El alegre carpintero de plumas naranjas y cresta roja listo para picotear código.',
      color: 'bg-amber-100 text-amber-800'
    },
    {
      id: 'cyberpunk',
      name: 'Pico Cyberpunk',
      icon: '🕶️',
      cost: 300,
      desc: 'Visor neón y plumaje cibernético para encontrar bugs en el año 2077.',
      color: 'bg-fuchsia-100 text-fuchsia-800'
    },
    {
      id: 'hacker',
      name: 'Pico Hacker Modo Oscuro',
      icon: '👨‍💻',
      cost: 400,
      desc: 'Visor de matriz verde y plumaje oscuro para dominar la consola.',
      color: 'bg-zinc-800 text-green-400'
    },
    {
      id: 'wizard',
      name: 'Pico Mago del Código',
      icon: '🧙',
      cost: 500,
      desc: 'Sombrero místico con estrella y hechizos de refactorización instantánea.',
      color: 'bg-purple-100 text-purple-900'
    }
  ];

  return (
    <div className="pb-28 pt-4 px-4 max-w-xl mx-auto w-full space-y-6">
      {/* Shop Header Banner */}
      <div className="bg-gradient-to-r from-cyan-500 to-blue-600 rounded-3xl p-6 text-white shadow-xl flex items-center justify-between">
        <div>
          <span className="bg-white/20 backdrop-blur-md text-white px-3 py-1 rounded-full text-xs font-black uppercase">
            🏪 Tienda de Gemas
          </span>
          <h2 className="text-2xl font-black mt-1">Intercambia tus Gemas</h2>
          <p className="text-xs text-cyan-100 font-medium mt-1">
            Gana gemas resolviendo ejercicios y equipa a tu mascota Byte.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-white/20 backdrop-blur-md px-4 py-2 rounded-2xl font-black text-xl">
          <Gem className="w-6 h-6 fill-cyan-300 text-cyan-200" />
          <span>{profile.gems}</span>
        </div>
      </div>

      {/* Power-ups Section */}
      <div className="space-y-3">
        <h3 className="text-sm font-black uppercase tracking-wider text-slate-400 px-1">
          Potenciadores y Rachas
        </h3>

        {/* Streak Freeze Card */}
        <div className="bg-white border-2 border-slate-200 rounded-2xl p-4 flex items-center justify-between shadow-xs">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-sky-100 flex items-center justify-center">
              <Shield className="w-7 h-7 text-sky-600 fill-sky-200" />
            </div>
            <div>
              <div className="font-extrabold text-slate-800 text-sm">Protector de Racha</div>
              <div className="text-xs text-slate-500 font-medium">Protege tu racha diaria si un día no puedes practicar.</div>
            </div>
          </div>
          <button
            onClick={() => {
              if (profile.gems >= 200) {
                soundFx.playGem();
                onBuyStreakFreeze();
              }
            }}
            disabled={profile.gems < 200}
            className={`px-4 py-2.5 rounded-xl font-black text-xs flex items-center gap-1.5 border-b-2 transition-all cursor-pointer ${
              profile.gems >= 200
                ? 'bg-sky-500 text-white border-sky-700 hover:bg-sky-600 active:translate-y-1'
                : 'bg-slate-200 text-slate-400 border-slate-300 cursor-not-allowed'
            }`}
          >
            <span>200</span>
            <Gem className="w-3.5 h-3.5 fill-cyan-300 text-cyan-300" />
          </button>
        </div>
      </div>

      {/* Mascot Skins Store Section */}
      <div className="space-y-3 pt-2">
        <h3 className="text-sm font-black uppercase tracking-wider text-slate-400 px-1 flex items-center gap-2">
          <Shirt className="w-4 h-4 text-purple-600" />
          <span>Atuendos para la Mascota Byte</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {skins.map((skin) => {
            const isOwned = profile.inventory.includes(skin.id);
            const isEquipped = profile.equippedSkin === skin.id;

            return (
              <div
                key={skin.id}
                className="bg-white border-2 border-slate-200 rounded-2xl p-4 flex flex-col justify-between space-y-3 shadow-xs hover:border-slate-300 transition-all"
              >
                <div className="flex items-start gap-3">
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl ${skin.color}`}>
                    {skin.icon}
                  </div>
                  <div>
                    <h4 className="font-extrabold text-slate-800 text-sm">{skin.name}</h4>
                    <p className="text-[11px] text-slate-500 font-medium leading-tight mt-0.5">{skin.desc}</p>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  {isOwned ? (
                    isEquipped ? (
                      <span className="w-full py-2 bg-emerald-50 border border-emerald-300 text-emerald-700 font-black text-xs rounded-xl flex items-center justify-center gap-1">
                        <Check className="w-4 h-4" /> Equipado
                      </span>
                    ) : (
                      <button
                        onClick={() => {
                          soundFx.playClick();
                          onEquipSkin(skin.id);
                        }}
                        className="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-black text-xs rounded-xl cursor-pointer"
                      >
                        Equipar
                      </button>
                    )
                  ) : (
                    <button
                      onClick={() => {
                        if (profile.gems >= skin.cost) {
                          soundFx.playGem();
                          onBuySkin(skin.id, skin.cost);
                        }
                      }}
                      disabled={profile.gems < skin.cost}
                      className={`w-full py-2 rounded-xl font-black text-xs flex items-center justify-center gap-1.5 border-b-2 cursor-pointer ${
                        profile.gems >= skin.cost
                          ? 'bg-purple-600 text-white border-purple-800 hover:bg-purple-700'
                          : 'bg-slate-200 text-slate-400 border-slate-300 cursor-not-allowed'
                      }`}
                    >
                      <span>Comprar por {skin.cost}</span>
                      <Gem className="w-3.5 h-3.5 fill-cyan-300 text-cyan-300" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
