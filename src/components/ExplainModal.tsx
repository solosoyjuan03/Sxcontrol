import React, { useEffect, useState } from 'react';
import { Sparkles, Lightbulb, Bot, X } from 'lucide-react';
import { MascotByte } from './MascotByte';
import { UserProfile } from '../types';

interface ExplainModalProps {
  data: {
    questionTitle: string;
    questionContent: string;
    userAnswer: string;
    correctAnswer: string;
  };
  profile: UserProfile;
  onClose: () => void;
}

export const ExplainModal: React.FC<ExplainModalProps> = ({ data, profile, onClose }) => {
  const [loading, setLoading] = useState(true);
  const [explanation, setExplanation] = useState<string>('');
  const [tip, setTip] = useState<string>('');

  useEffect(() => {
    let isMounted = true;
    async function fetchAiExplanation() {
      try {
        setLoading(true);
        const res = await fetch('/api/ai/explain', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
        const result = await res.json();
        if (isMounted) {
          setExplanation(result.explanation || 'Respuesta por reglas de sintaxis estándar.');
          setTip(result.tip || 'Revisa la documentación básica.');
        }
      } catch {
        if (isMounted) {
          setExplanation('Byte no pudo conectarse en este momento, pero la respuesta correcta es esa por las reglas de sintaxis.');
          setTip('Comprueba siempre los tipos de datos y operadores.');
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchAiExplanation();
    return () => { isMounted = false; };
  }, [data]);

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 animate-in fade-in">
      <div className="bg-white rounded-3xl p-6 max-w-md w-full border-4 border-purple-200 shadow-2xl relative space-y-4">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 text-slate-500 font-bold hover:bg-slate-200 flex items-center justify-center cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-2 text-xs font-black uppercase text-purple-600 tracking-wider">
          <Sparkles className="w-4 h-4" />
          <span>Explicación del Tutor Byte IA</span>
        </div>

        {/* Mascot */}
        <div className="flex justify-center">
          <MascotByte skin={profile.equippedSkin} size="md" mood={loading ? 'thinking' : 'happy'} />
        </div>

        {loading ? (
          <div className="text-center py-6 space-y-3">
            <div className="inline-block w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm font-bold text-slate-600">Byte está analizando la sintaxis del ejercicio...</p>
          </div>
        ) : (
          <div className="space-y-4 text-slate-800">
            <div className="bg-purple-50 p-4 rounded-2xl border border-purple-200 space-y-2">
              <h4 className="text-sm font-black text-purple-900 flex items-center gap-1.5">
                <Bot className="w-4 h-4 text-purple-600" />
                <span>Explicación:</span>
              </h4>
              <p className="text-sm font-medium leading-relaxed text-slate-700">{explanation}</p>
            </div>

            {tip && (
              <div className="bg-amber-50 p-3.5 rounded-2xl border border-amber-200 flex items-start gap-2.5">
                <Lightbulb className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                <div>
                  <span className="text-xs font-black uppercase text-amber-800">Truco de Byte:</span>
                  <p className="text-xs font-semibold text-amber-900">{tip}</p>
                </div>
              </div>
            )}
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full py-3.5 rounded-2xl font-black bg-purple-600 text-white hover:bg-purple-700 border-b-4 border-purple-800 active:translate-y-1 active:border-b-0 shadow-lg cursor-pointer transition-all"
        >
          ¡ENTENDIDO!
        </button>
      </div>
    </div>
  );
};
