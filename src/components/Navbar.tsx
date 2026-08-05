import React, { useState } from 'react';
import { Flame, ChevronDown } from 'lucide-react';
import { Course, UserProfile } from '../types';
import { COURSES } from '../data/coursesData';
import { soundFx } from '../lib/sound';

interface NavbarProps {
  profile: UserProfile;
  currentCourse: Course;
  onSelectCourse: (courseId: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  profile,
  currentCourse,
  onSelectCourse
}) => {
  const [showCourseMenu, setShowCourseMenu] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b-2 border-slate-200 px-4 py-2.5 max-w-5xl mx-auto w-full flex items-center justify-between shadow-xs">
        {/* Course Picker Dropdown */}
        <div className="relative">
          <button
            onClick={() => {
              soundFx.playClick();
              setShowCourseMenu(!showCourseMenu);
            }}
            className="flex items-center gap-2 px-3 py-1.5 rounded-xl border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all cursor-pointer font-bold text-slate-700"
          >
            <span className="text-xl">{currentCourse.icon}</span>
            <span className="hidden sm:inline text-sm font-extrabold">{currentCourse.title}</span>
            <ChevronDown className="w-4 h-4 text-slate-400" />
          </button>

          {showCourseMenu && (
            <div className="absolute top-12 left-0 w-64 bg-white border-2 border-slate-200 rounded-2xl shadow-xl p-2 z-50 animate-in fade-in slide-in-from-top-2">
              <div className="px-3 py-2 text-xs font-black uppercase tracking-wider text-slate-400">
                Curso Activo
              </div>
              <div className="space-y-1">
                {COURSES.map((course) => {
                  const isSelected = course.id === currentCourse.id;
                  return (
                    <button
                      key={course.id}
                      onClick={() => {
                        soundFx.playClick();
                        onSelectCourse(course.id);
                        setShowCourseMenu(false);
                      }}
                      className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl font-bold transition-all text-left ${
                        isSelected
                          ? 'bg-emerald-50 border-2 border-emerald-500 text-emerald-700'
                          : 'hover:bg-slate-100 text-slate-700'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{course.icon}</span>
                        <div>
                          <div className="text-sm font-extrabold">{course.title}</div>
                          <div className="text-xs text-slate-400 font-normal">
                            {course.nodes.length} Nivel(es)
                          </div>
                        </div>
                      </div>
                      {isSelected && <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Gamification Counters */}
        <div className="flex items-center gap-2 sm:gap-4 font-black">
          {/* Streak */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-orange-50 border border-orange-200 text-orange-600">
            <Flame className="w-5 h-5 fill-orange-500 text-orange-500 animate-bounce" />
            <span className="text-sm">{profile.streak} Días</span>
          </div>
        </div>
      </header>
    </>
  );
};
