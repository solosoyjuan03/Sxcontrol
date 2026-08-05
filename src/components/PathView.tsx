import React, { useState } from 'react';
import { motion } from 'motion/react';
import { Star, Lock, Crown, Gift, Play, Terminal, Code, GitBranch, Layers, Type, Database, Layout, Box, Component } from 'lucide-react';
import { Course, LessonNode, UserProfile } from '../types';
import { MascotByte } from './MascotByte';
import { soundFx } from '../lib/sound';

interface PathViewProps {
  course: Course;
  profile: UserProfile;
  onStartLesson: (node: LessonNode) => void;
}

export const PathView: React.FC<PathViewProps> = ({
  course,
  profile,
  onStartLesson
}) => {
  const [selectedNode, setSelectedNode] = useState<LessonNode | null>(null);

  // Helper to map icon string to Lucide icon
  const getIcon = (iconName: string) => {
    switch (iconName) {
      case 'Terminal': return Terminal;
      case 'Type': return Type;
      case 'GitBranch': return GitBranch;
      case 'Code': return Code;
      case 'Layers': return Layers;
      case 'Database': return Database;
      case 'Layout': return Layout;
      case 'Box': return Box;
      case 'Component': return Component;
      default: return Code;
    }
  };

  // Group nodes by Unit
  const unitsMap: Record<number, { title: string; nodes: LessonNode[] }> = {};
  course.nodes.forEach((node) => {
    if (!unitsMap[node.unit]) {
      unitsMap[node.unit] = { title: node.unitTitle, nodes: [] };
    }
    unitsMap[node.unit].nodes.push(node);
  });

  return (
    <div className="pb-28 pt-4 px-4 max-w-xl mx-auto w-full">
      {/* Course Header Banner */}
      <div className={`p-5 rounded-3xl bg-gradient-to-r ${course.color} text-white shadow-xl mb-8 relative overflow-hidden flex items-center justify-between`}>
        <div className="relative z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-white/20 backdrop-blur-md rounded-full text-xs font-black uppercase mb-2">
            <span>{course.icon}</span>
            <span>Ruta Oficial de {course.title}</span>
          </div>
          <h2 className="text-2xl font-black">{course.title}</h2>
          <p className="text-xs text-white/90 font-medium max-w-xs mt-1">{course.description}</p>
        </div>
        <MascotByte skin={profile.equippedSkin} size="sm" mood="happy" className="relative z-10" />
      </div>

      {/* Daily Goal Banner */}
      <div className="bg-white border-2 border-slate-200 rounded-2xl p-3.5 mb-6 flex items-center justify-between shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-100 border border-amber-300 flex items-center justify-center font-black text-amber-600 text-lg">
            🎯
          </div>
          <div>
            <div className="text-xs font-black text-slate-400 uppercase tracking-wider">Meta Diaria de XP</div>
            <div className="text-sm font-extrabold text-slate-800">
              {profile.todayXp} / {profile.dailyGoalXp} XP Ganados
            </div>
          </div>
        </div>
        <div className="w-24 bg-slate-100 rounded-full h-3 border border-slate-200 overflow-hidden">
          <div
            className="bg-emerald-500 h-full rounded-full transition-all duration-500"
            style={{ width: `${Math.min(100, (profile.todayXp / profile.dailyGoalXp) * 100)}%` }}
          />
        </div>
      </div>

      {/* Units & Winding Path */}
      {Object.entries(unitsMap).map(([unitNumber, unitData], unitIdx) => (
        <div key={unitNumber} className="mb-12">
          {/* Unit Header */}
          <div className="sticky top-16 z-20 bg-slate-800 text-white p-4 rounded-2xl shadow-md mb-8 border-2 border-slate-700 flex items-center justify-between">
            <div>
              <div className="text-xs font-black uppercase tracking-widest text-emerald-400">
                Unidad {unitNumber}
              </div>
              <h3 className="text-lg font-black">{unitData.title}</h3>
            </div>
            <div className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-3 py-1 rounded-xl text-xs font-extrabold">
              {unitData.nodes.length} Nivel(es)
            </div>
          </div>

          {/* Nodes Zigzag Path */}
          <div className="relative flex flex-col items-center gap-10 my-4">
            {unitData.nodes.map((node, index) => {
              const isCompleted = profile.completedNodeIds.includes(node.id);
              // Active if previous is completed or it's the very first node in course
              const isPrevCompleted = index === 0 ? true : profile.completedNodeIds.includes(unitData.nodes[index - 1]?.id);
              const isActive = !isCompleted && isPrevCompleted;
              const isLocked = !isCompleted && !isActive;

              // Alternating horizontal offset (-36px, 0px, 36px, 0px)
              const offsets = [-36, 0, 36, 0];
              const xOffset = offsets[index % offsets.length];

              const NodeIcon = getIcon(node.iconName);
              const stars = profile.nodeStars[node.id] || (isCompleted ? 3 : 0);

              return (
                <div key={node.id} className="relative flex flex-col items-center">
                  {/* Mascot sitting on active node */}
                  {isActive && (
                    <div className="absolute -top-16 z-30 pointer-events-none animate-bounce">
                      <MascotByte skin={profile.equippedSkin} size="sm" mood="happy" speakText="¡Vamos a programar!" />
                    </div>
                  )}

                  <motion.div
                    style={{ transform: `translateX(${xOffset}px)` }}
                    whileHover={{ scale: 1.08 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <button
                      onClick={() => {
                        soundFx.playClick();
                        if (!isLocked) {
                          setSelectedNode(node);
                        }
                      }}
                      className={`relative w-20 h-20 rounded-full flex items-center justify-center font-black transition-all shadow-xl cursor-pointer ${
                        isCompleted
                          ? 'bg-emerald-500 border-b-8 border-emerald-700 text-white hover:bg-emerald-400'
                          : isActive
                          ? 'bg-amber-400 border-b-8 border-amber-600 text-slate-900 animate-pulse hover:bg-amber-300 ring-4 ring-amber-300/50'
                          : 'bg-slate-200 border-b-8 border-slate-300 text-slate-400 cursor-not-allowed'
                      }`}
                    >
                      {/* Inner Node Icon */}
                      {isLocked ? (
                        <Lock className="w-8 h-8 text-slate-400" />
                      ) : (
                        <NodeIcon className="w-9 h-9 stroke-[2.5]" />
                      )}

                      {/* Crown badge if completed */}
                      {isCompleted && (
                        <span className="absolute -top-2 -right-1 bg-amber-400 text-amber-900 rounded-full p-1 border-2 border-white shadow-xs">
                          <Crown className="w-4 h-4 fill-amber-400" />
                        </span>
                      )}
                    </button>
                  </motion.div>

                  {/* Stars / Label under node */}
                  <div
                    style={{ transform: `translateX(${xOffset}px)` }}
                    className="mt-2 text-center max-w-[130px]"
                  >
                    <div className="text-xs font-black text-slate-700 truncate">{node.title}</div>
                    {!isLocked && (
                      <div className="flex items-center justify-center gap-0.5 mt-0.5">
                        {[1, 2, 3].map((s) => (
                          <Star
                            key={s}
                            className={`w-3.5 h-3.5 ${
                              s <= stars ? 'fill-amber-400 text-amber-400' : 'fill-slate-200 text-slate-300'
                            }`}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}


          </div>
        </div>
      ))}

      {/* Start Lesson Modal Drawer */}
      {selectedNode && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-end sm:items-center justify-center p-4 z-50 animate-in fade-in">
          <div className="bg-white rounded-3xl p-6 max-w-md w-full border-4 border-slate-200 shadow-2xl space-y-4 animate-in slide-in-from-bottom-6">
            <div className="flex items-center justify-between border-b pb-3 border-slate-100">
              <div>
                <span className="text-xs font-black uppercase tracking-wider text-emerald-600">
                  Unidad {selectedNode.unit}
                </span>
                <h3 className="text-2xl font-black text-slate-800">{selectedNode.title}</h3>
              </div>
              <button
                onClick={() => setSelectedNode(null)}
                className="w-9 h-9 rounded-full bg-slate-100 text-slate-500 font-black hover:bg-slate-200 flex items-center justify-center cursor-pointer"
              >
                ✕
              </button>
            </div>

            <p className="text-sm font-medium text-slate-600">{selectedNode.description}</p>

            <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200 flex items-center justify-around font-bold text-xs text-slate-700">
              <div className="flex items-center gap-1.5">
                <span>⚡</span>
                <span>+20 XP Recompensa</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span>📝</span>
                <span>{selectedNode.exercises.length} Ejercicios</span>
              </div>
            </div>

            <button
              onClick={() => {
                soundFx.playClick();
                const nodeToStart = selectedNode;
                setSelectedNode(null);
                onStartLesson(nodeToStart);
              }}
              className="w-full py-4 rounded-2xl font-black text-lg bg-emerald-500 text-white hover:bg-emerald-600 border-b-4 border-emerald-700 active:translate-y-1 active:border-b-0 shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <Play className="w-5 h-5 fill-white" />
              <span>EMPEZAR LECCIÓN</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
