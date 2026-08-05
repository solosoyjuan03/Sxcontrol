import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import { CheckCircle2, XCircle, Sparkles } from 'lucide-react';
import { Exercise, LessonNode, UserProfile } from '../types';
import { MascotByte } from './MascotByte';
import { soundFx } from '../lib/sound';

interface LessonModalProps {
  node: LessonNode;
  profile: UserProfile;
  onFinishLesson: (xpGained: number, nodeCompleted: boolean) => void;
  onClose: () => void;
  onAskAiExplain: (data: { questionTitle: string; questionContent: string; userAnswer: string; correctAnswer: string }) => void;
}

export const LessonModal: React.FC<LessonModalProps> = ({
  node,
  profile,
  onFinishLesson,
  onClose,
  onAskAiExplain
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [selectedBlocks, setSelectedBlocks] = useState<string[]>([]);
  const [availableBlocks, setAvailableBlocks] = useState<string[]>([]);
  const [selectedBugLine, setSelectedBugLine] = useState<number | null>(null);

  const [isAnswered, setIsAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const [xpEarnedTotal, setXpEarnedTotal] = useState(0);

  const exercise: Exercise | undefined = node.exercises[currentIndex];

  // Initialize block options whenever exercise changes
  React.useEffect(() => {
    if (exercise?.type === 'code_blocks' && exercise.codeBlocks) {
      // Shuffle code blocks for challenge
      const shuffled = [...exercise.codeBlocks].sort(() => Math.random() - 0.5);
      setAvailableBlocks(shuffled);
      setSelectedBlocks([]);
    } else {
      setSelectedOption(null);
      setSelectedBugLine(null);
    }
    setIsAnswered(false);
    setIsCorrect(false);
  }, [currentIndex, exercise]);

  if (!exercise && !isFinished) {
    return null;
  }

  // Check user submission
  const handleCheckAnswer = () => {
    if (!exercise || isAnswered) return;

    let userRight = false;
    let userAns = '';
    let correctAns = exercise.correctAnswer || '';

    if (exercise.type === 'multiple_choice' || exercise.type === 'fill_blank') {
      userAns = selectedOption || '';
      userRight = userAns.trim() === correctAns.trim();
    } else if (exercise.type === 'code_blocks') {
      userAns = selectedBlocks.join(' ');
      const targetAns = (exercise.correctOrder || exercise.codeBlocks || []).join(' ');
      userRight = userAns.trim() === targetAns.trim();
      correctAns = targetAns;
    } else if (exercise.type === 'find_bug') {
      userRight = selectedBugLine === exercise.bugLine;
      userAns = `Línea ${selectedBugLine}`;
      correctAns = `Línea ${exercise.bugLine}`;
    }

    setIsAnswered(true);
    setIsCorrect(userRight);

    if (userRight) {
      soundFx.playSuccess();
      setXpEarnedTotal((prev) => prev + 10);
    } else {
      soundFx.playError();
    }
  };

  // Continue to next question or end lesson
  const handleNext = () => {
    if (currentIndex + 1 < node.exercises.length) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      // Finished lesson!
      soundFx.playLevelUp();
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });
      setIsFinished(true);
    }
  };

  // Completion Screen
  if (isFinished) {
    return (
      <div className="fixed inset-0 z-50 bg-white flex flex-col items-center justify-between p-6 max-w-2xl mx-auto w-full animate-in fade-in">
        <div className="w-full text-center space-y-6 my-auto">
          <MascotByte skin={profile.equippedSkin} size="lg" mood="celebrate" speakText="¡Excelente trabajo en código!" />

          <h2 className="text-3xl font-black text-slate-800">¡Lección Completada!</h2>
          <p className="text-sm font-semibold text-slate-500">
            Has dominado el nivel <span className="text-emerald-600 font-bold">{node.title}</span>.
          </p>

          {/* Stats Cards */}
          <div className="flex justify-center max-w-xs mx-auto font-black">
            <div className="bg-amber-50 border-2 border-amber-300 rounded-2xl p-4 text-center w-full">
              <div className="text-xs uppercase text-amber-600">XP Ganados</div>
              <div className="text-3xl text-amber-800">+{xpEarnedTotal + 10} XP</div>
            </div>
          </div>
        </div>

        <button
          onClick={() => {
            onFinishLesson(xpEarnedTotal + 10, true);
            onClose();
          }}
          className="w-full py-4 rounded-2xl font-black text-xl bg-emerald-500 text-white hover:bg-emerald-600 border-b-4 border-emerald-700 active:translate-y-1 active:border-b-0 shadow-xl cursor-pointer"
        >
          CONTINUAR Y GUARDAR
        </button>
      </div>
    );
  }

  const progressPercent = ((currentIndex + 1) / node.exercises.length) * 100;

  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col justify-between max-w-2xl mx-auto w-full h-full">
      {/* Top Bar */}
      <div className="px-4 py-3 flex items-center justify-between border-b-2 border-slate-100 gap-4">
        <button
          onClick={() => {
            soundFx.playClick();
            if (confirm('¿Seguro que quieres salir de la lección? Perderás el progreso de esta sesión.')) {
              onClose();
            }
          }}
          className="text-slate-400 hover:text-slate-700 font-black text-xl px-2 cursor-pointer"
        >
          ✕
        </button>

        {/* Progress Bar */}
        <div className="flex-1 bg-slate-100 h-3.5 rounded-full overflow-hidden border border-slate-200">
          <div
            className="bg-emerald-500 h-full rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Unlimited Practice Badge */}
        <div className="flex items-center gap-1 font-black text-emerald-600 text-xs bg-emerald-50 px-2.5 py-1 rounded-xl border border-emerald-200">
          <span>Práctica Ilimitada ✨</span>
        </div>
      </div>

      {/* Main Exercise Area */}
      <div className="flex-1 overflow-y-auto p-5 space-y-6 flex flex-col justify-center max-w-xl mx-auto w-full">
        {/* Question Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs font-black uppercase text-slate-400 tracking-wider">
            <span>{exercise.type.replace('_', ' ')}</span>
            <span>•</span>
            <span>Pregunta {currentIndex + 1} de {node.exercises.length}</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-800 leading-snug">
            {exercise.question}
          </h2>
        </div>

        {/* Code Snippet Box (If present) */}
        {exercise.codeSnippet && (
          <div className="bg-slate-900 text-slate-100 p-4 rounded-2xl font-mono text-sm border-2 border-slate-800 shadow-inner overflow-x-auto">
            {exercise.type === 'find_bug' ? (
              <div className="space-y-1">
                {exercise.codeSnippet.split('\n').map((line, idx) => {
                  const lineNum = idx + 1;
                  const isSelected = selectedBugLine === lineNum;
                  return (
                    <button
                      key={lineNum}
                      onClick={() => {
                        if (isAnswered) return;
                        soundFx.playClick();
                        setSelectedBugLine(lineNum);
                      }}
                      className={`w-full text-left px-2 py-1 rounded transition-all cursor-pointer flex items-center gap-3 font-mono ${
                        isSelected
                          ? 'bg-rose-500/30 text-rose-300 border border-rose-500/50'
                          : 'hover:bg-slate-800 text-slate-300'
                      }`}
                    >
                      <span className="text-slate-500 text-xs w-4">{lineNum}</span>
                      <span>{line}</span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <pre>{exercise.codeSnippet}</pre>
            )}
          </div>
        )}

        {/* Multiple Choice or Fill Blank Options */}
        {(exercise.type === 'multiple_choice' || exercise.type === 'fill_blank') && exercise.options && (
          <div className="grid grid-cols-1 gap-3">
            {exercise.options.map((opt) => {
              const isSelected = selectedOption === opt;
              return (
                <button
                  key={opt}
                  onClick={() => {
                    if (isAnswered) return;
                    soundFx.playClick();
                    setSelectedOption(opt);
                  }}
                  disabled={isAnswered}
                  className={`p-4 rounded-2xl font-mono text-sm sm:text-base font-bold text-left border-2 border-b-4 transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-sky-50 border-sky-500 border-b-sky-700 text-sky-900'
                      : 'bg-white border-slate-200 border-b-slate-300 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {opt}
                </button>
              );
            })}
          </div>
        )}

        {/* Code Blocks Assembly Type */}
        {exercise.type === 'code_blocks' && (
          <div className="space-y-6">
            {/* Selected Code Line Box */}
            <div className="min-h-[64px] bg-slate-50 border-2 border-dashed border-slate-300 rounded-2xl p-3 flex flex-wrap gap-2 items-center">
              {selectedBlocks.length === 0 && (
                <span className="text-xs text-slate-400 font-bold italic">Toca los bloques abajo para armar la línea de código...</span>
              )}
              {selectedBlocks.map((block, idx) => (
                <button
                  key={`${block}-${idx}`}
                  onClick={() => {
                    if (isAnswered) return;
                    soundFx.playClick();
                    // Remove from selected, return to available
                    setSelectedBlocks((prev) => prev.filter((_, i) => i !== idx));
                    setAvailableBlocks((prev) => [...prev, block]);
                  }}
                  className="px-3 py-2 bg-emerald-500 text-white font-mono font-bold text-sm rounded-xl border-b-2 border-emerald-700 shadow-xs cursor-pointer"
                >
                  {block}
                </button>
              ))}
            </div>

            {/* Available Blocks Palette */}
            <div className="flex flex-wrap gap-2 justify-center">
              {availableBlocks.map((block, idx) => (
                <button
                  key={`${block}-${idx}`}
                  onClick={() => {
                    if (isAnswered) return;
                    soundFx.playClick();
                    // Move from available to selected
                    setAvailableBlocks((prev) => prev.filter((_, i) => i !== idx));
                    setSelectedBlocks((prev) => [...prev, block]);
                  }}
                  className="px-3.5 py-2.5 bg-white border-2 border-b-4 border-slate-200 border-b-slate-300 font-mono font-bold text-sm text-slate-800 rounded-xl hover:bg-slate-100 shadow-xs cursor-pointer"
                >
                  {block}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer Banner State */}
      <div className={`p-5 border-t-2 transition-all ${
        !isAnswered
          ? 'bg-white border-slate-200'
          : isCorrect
          ? 'bg-emerald-100 border-emerald-300 text-emerald-900'
          : 'bg-rose-100 border-rose-300 text-rose-900'
      }`}>
        {!isAnswered ? (
          <button
            onClick={handleCheckAnswer}
            disabled={
              (exercise.type === 'multiple_choice' || exercise.type === 'fill_blank') && !selectedOption ||
              (exercise.type === 'code_blocks' && selectedBlocks.length === 0) ||
              (exercise.type === 'find_bug' && selectedBugLine === null)
            }
            className={`w-full py-4 rounded-2xl font-black text-lg border-b-4 transition-all shadow-lg cursor-pointer ${
              (selectedOption || selectedBlocks.length > 0 || selectedBugLine !== null)
                ? 'bg-emerald-500 text-white border-emerald-700 hover:bg-emerald-600 active:translate-y-1 active:border-b-0'
                : 'bg-slate-200 text-slate-400 border-slate-300 cursor-not-allowed'
            }`}
          >
            COMPROBAR
          </button>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {isCorrect ? (
                  <CheckCircle2 className="w-8 h-8 text-emerald-600 fill-emerald-100" />
                ) : (
                  <XCircle className="w-8 h-8 text-rose-600 fill-rose-100" />
                )}
                <div>
                  <div className="text-lg font-black">{isCorrect ? '¡Excelente!' : 'Solución Incorrecta'}</div>
                  <div className="text-xs font-semibold">
                    {isCorrect
                      ? '+10 XP Ganados'
                      : `Respuesta correcta: ${exercise.correctAnswer || exercise.correctOrder?.join(' ') || ''}`}
                  </div>
                </div>
              </div>

              {/* Ask AI Explanation Button if incorrect */}
              {!isCorrect && (
                <button
                  onClick={() => {
                    soundFx.playClick();
                    onAskAiExplain({
                      questionTitle: exercise.title,
                      questionContent: exercise.question,
                      userAnswer: selectedOption || selectedBlocks.join(' ') || `Línea ${selectedBugLine}`,
                      correctAnswer: exercise.correctAnswer || exercise.correctOrder?.join(' ') || `Línea ${exercise.bugLine}`
                    });
                  }}
                  className="px-3.5 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold text-xs flex items-center gap-1.5 shadow-md transition-all cursor-pointer"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>Explicar con IA</span>
                </button>
              )}
            </div>

            <button
              onClick={handleNext}
              className={`w-full py-4 rounded-2xl font-black text-lg text-white border-b-4 shadow-lg cursor-pointer active:translate-y-1 active:border-b-0 transition-all ${
                isCorrect
                  ? 'bg-emerald-500 border-emerald-700 hover:bg-emerald-600'
                  : 'bg-rose-500 border-rose-700 hover:bg-rose-600'
              }`}
            >
              CONTINUAR
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
