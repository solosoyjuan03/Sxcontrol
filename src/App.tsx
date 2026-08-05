import React, { useState, useEffect } from 'react';
import { Course, LessonNode, UserProfile } from './types';
import { COURSES, INITIAL_PROFILE } from './data/coursesData';
import { Navbar } from './components/Navbar';
import { BottomNav, TabType } from './components/BottomNav';
import { PathView } from './components/PathView';
import { LessonModal } from './components/LessonModal';
import { ExplainModal } from './components/ExplainModal';
import { ProfileView } from './components/ProfileView';

const STORAGE_KEY = 'codelingo_user_profile_v1';

export default function App() {
  // Load profile from localStorage if available
  const [profile, setProfile] = useState<UserProfile>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch {
      // Fallback to initial
    }
    return INITIAL_PROFILE;
  });

  const [activeTab, setActiveTab] = useState<TabType>('path');
  const [activeLessonNode, setActiveLessonNode] = useState<LessonNode | null>(null);

  // AI Explanation Modal state
  const [explainData, setExplainData] = useState<{
    questionTitle: string;
    questionContent: string;
    userAnswer: string;
    correctAnswer: string;
  } | null>(null);

  // Save profile to localStorage on updates
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
    } catch {
      // Storage error fallback
    }
  }, [profile]);

  // Current Course
  const currentCourse = COURSES.find((c) => c.id === profile.currentCourse) || COURSES[0];

  // Course Selector Handler
  const handleSelectCourse = (courseId: string) => {
    setProfile((prev) => ({
      ...prev,
      currentCourse: courseId
    }));
  };

  // Complete a Lesson
  const handleFinishLesson = (xpGained: number, _completedNode: boolean) => {
    if (!activeLessonNode) return;

    const nodeId = activeLessonNode.id;
    setProfile((prev) => {
      const isAlreadyCompleted = prev.completedNodeIds.includes(nodeId);
      const updatedNodeIds = isAlreadyCompleted ? prev.completedNodeIds : [...prev.completedNodeIds, nodeId];
      const updatedStars = { ...prev.nodeStars, [nodeId]: 3 };

      return {
        ...prev,
        xp: prev.xp + xpGained,
        todayXp: prev.todayXp + xpGained,
        completedNodeIds: updatedNodeIds,
        nodeStars: updatedStars,
        totalLessonsCompleted: prev.totalLessonsCompleted + 1
      };
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans antialiased selection:bg-emerald-200">
      {/* Navigation Header */}
      <Navbar
        profile={profile}
        currentCourse={currentCourse}
        onSelectCourse={handleSelectCourse}
      />

      {/* View Router */}
      <main className="max-w-5xl mx-auto min-h-[calc(100vh-120px)]">
        {activeTab === 'path' && (
          <PathView
            course={currentCourse}
            profile={profile}
            onStartLesson={(node) => setActiveLessonNode(node)}
          />
        )}

        {activeTab === 'profile' && <ProfileView profile={profile} />}
      </main>

      {/* Bottom Navigation */}
      <BottomNav activeTab={activeTab} onChangeTab={setActiveTab} />

      {/* Interactive Lesson Modal */}
      {activeLessonNode && (
        <LessonModal
          node={activeLessonNode}
          profile={profile}
          onFinishLesson={handleFinishLesson}
          onClose={() => setActiveLessonNode(null)}
          onAskAiExplain={(data) => setExplainData(data)}
        />
      )}

      {/* AI Explanation Modal */}
      {explainData && (
        <ExplainModal
          data={explainData}
          profile={profile}
          onClose={() => setExplainData(null)}
        />
      )}
    </div>
  );
}
