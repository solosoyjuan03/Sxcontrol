export type ExerciseType =
  | 'multiple_choice'
  | 'fill_blank'
  | 'code_blocks'
  | 'find_bug'
  | 'match_pairs'
  | 'type_code';

export interface Exercise {
  id: string;
  type: ExerciseType;
  title: string;
  question: string;
  codeSnippet?: string;
  options?: string[];
  correctAnswer?: string;
  codeBlocks?: string[];
  correctOrder?: string[];
  bugLine?: number;
  pairs?: { id: string; left: string; right: string }[];
  explanation?: string;
}

export interface LessonNode {
  id: string;
  title: string;
  unit: number;
  unitTitle: string;
  description: string;
  totalLessons: number;
  iconName: string; // Lucide icon name or emoji
  exercises: Exercise[];
}

export interface Course {
  id: string;
  title: string;
  icon: string; // Emoji or identifier
  color: string; // Tailwind color class
  bgColor: string;
  description: string;
  nodes: LessonNode[];
}

export type SkinId = 'default' | 'cyberpunk' | 'wizard' | 'hacker';

export interface UserProfile {
  name: string;
  avatar: string;
  xp: number;
  streak: number;
  currentCourse: string;
  completedNodeIds: string[];
  nodeStars: Record<string, number>; // nodeId -> 1..3
  league: 'Bronce' | 'Plata' | 'Oro' | 'Esmeralda' | 'Diamante';
  equippedSkin: SkinId;
  inventory: SkinId[];
  dailyGoalXp: number;
  todayXp: number;
  lastActiveDate: string;
  totalLessonsCompleted: number;
}

export interface LeagueMember {
  id: string;
  name: string;
  avatar: string;
  xp: number;
  isUser?: boolean;
  rank?: number;
  badge?: string;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  progress: number;
  maxProgress: number;
  unlocked: boolean;
}
