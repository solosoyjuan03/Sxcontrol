import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { createServer as createViteServer } from 'vite';
import { GoogleGenAI, Type } from '@google/genai';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Shared Gemini AI instance initializer
  const getAI = () => {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      return null;
    }
    return new GoogleGenAI({
      apiKey,
      httpOptions: {
        headers: {
          'User-Agent': 'aistudio-build',
        },
      },
    });
  };

  // API Routes
  app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', time: new Date().toISOString() });
  });

  // AI Endpoint 1: Explain answer with Byte mascot persona
  app.post('/api/ai/explain', async (req, res) => {
    try {
      const { questionTitle, questionContent, userAnswer, correctAnswer, language = 'Python' } = req.body;
      const ai = getAI();

      if (!ai) {
        return res.json({
          explanation: `¡Casi! La respuesta correcta es "${correctAnswer}". En ${language || 'código'}, este concepto asegura la sintaxis exacta y el tipo de dato requerido.`,
          tip: "Revisa siempre la diferencia de sintaxis y palabras clave."
        });
      }

      const prompt = `Eres "Pico", un pájaro carpintero naranja y pelirrojo alegre y entusiasmado que enseña programación estilo Duolingo.
El estudiante falló o necesita entender este ejercicio de ${language || 'Python'}.

Pregunta/Consigna: "${questionTitle || ''} - ${questionContent || ''}"
Respuesta del usuario: "${userAnswer}"
Respuesta correcta: "${correctAnswer}"

Instrucciones:
1. Explica de forma súper clara, entusiasta, cercana y en 2-3 frases cortas por qué "${correctAnswer}" es lo correcto.
2. Da un tip rápido o truco nemotécnico.
3. Mantén un tono divertido, motivador y directo en español.

Responde estrictamente en JSON con la estructura:
{
  "explanation": "explicación clara y animada",
  "tip": "un consejo o truco corto"
}`;

      const response = await ai.models.generateContent({
        model: 'gemini-3.6-flash',
        contents: prompt,
        config: {
          responseMimeType: 'application/json',
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              explanation: { type: Type.STRING },
              tip: { type: Type.STRING },
            },
            required: ['explanation', 'tip'],
          },
        },
      });

      const data = JSON.parse(response.text || '{}');
      res.json(data);
    } catch (error) {
      console.error('Error in /api/ai/explain:', error);
      res.status(500).json({
        explanation: 'Byte tuvo un pequeño error en su circuito, pero la respuesta correcta es esa por reglas de sintaxis estándar.',
        tip: 'Practica el ejercicio una vez más.'
      });
    }
  });

  // AI Endpoint 2: Generate dynamic coding lesson on any custom topic
  app.post('/api/ai/generate-lesson', async (req, res) => {
    try {
      const { topic, language = 'Python', level = 'Principiante' } = req.body;
      const ai = getAI();

      if (!ai) {
        return res.status(400).json({
          error: 'Clave GEMINI_API_KEY no configurada. Usa las lecciones predeterminadas.',
        });
      }

      const prompt = `Crea un conjunto de 3 ejercicios interactivos estilo Duolingo para aprender ${language} sobre el tema "${topic}" (Nivel: ${level}).
Genera variedad de tipos de ejercicios entre:
1. 'multiple_choice' (4 opciones)
2. 'fill_blank' (completar código)
3. 'code_blocks' (ordenar piezas de código desordenadas)

Los ejercicios deben estar en español, ser divertidos, progresivos y claros.

Estructura estricta JSON esperada:
{
  "lessonTitle": "Título de la Lección",
  "exercises": [
    {
      "id": "ex1",
      "type": "multiple_choice",
      "question": "Pregunta clara",
      "codeSnippet": "código opcional si aplica",
      "options": ["opcion1", "opcion2", "opcion3", "opcion4"],
      "correctAnswer": "opcion1",
      "explanation": "por qué es correcta"
    },
    {
      "id": "ex2",
      "type": "fill_blank",
      "question": "Completa el código con la palabra faltante",
      "codeSnippet": "function hola() { ___ ('Hola'); }",
      "options": ["console.log", "print", "write", "display"],
      "correctAnswer": "console.log",
      "explanation": "console.log imprime en la consola."
    },
    {
      "id": "ex3",
      "type": "code_blocks",
      "question": "Ordena los bloques para crear la variable",
      "codeBlocks": ["const", "nombre", "=", "'Byte';", "console.log(nombre);"],
      "correctOrder": ["const", "nombre", "=", "'Byte';", "console.log(nombre);"],
      "explanation": "En JS se declara const variable = valor;"
    }
  ]
}`;

      const response = await ai.models.generateContent({
        model: 'gemini-3.6-flash',
        contents: prompt,
        config: {
          responseMimeType: 'application/json',
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              lessonTitle: { type: Type.STRING },
              exercises: {
                type: Type.ARRAY,
                items: {
                  type: Type.OBJECT,
                  properties: {
                    id: { type: Type.STRING },
                    type: { type: Type.STRING },
                    question: { type: Type.STRING },
                    codeSnippet: { type: Type.STRING },
                    options: { type: Type.ARRAY, items: { type: Type.STRING } },
                    codeBlocks: { type: Type.ARRAY, items: { type: Type.STRING } },
                    correctOrder: { type: Type.ARRAY, items: { type: Type.STRING } },
                    correctAnswer: { type: Type.STRING },
                    explanation: { type: Type.STRING },
                  },
                },
              },
            },
            required: ['lessonTitle', 'exercises'],
          },
        },
      });

      const data = JSON.parse(response.text || '{}');
      res.json(data);
    } catch (error) {
      console.error('Error in /api/ai/generate-lesson:', error);
      res.status(500).json({ error: 'No se pudo generar la lección personalizada.' });
    }
  });

  // AI Endpoint 3: Tutor Chat with Byte
  app.post('/api/ai/tutor-chat', async (req, res) => {
    try {
      const { message, history = [] } = req.body;
      const ai = getAI();

      if (!ai) {
        return res.json({
          reply: '¡Hola! Soy Byte 🤖. Parece que la clave API de Gemini aún no está activa en las variables de entorno, ¡pero aquí estoy para acompañarte en tu aprendizaje!',
        });
      }

      const chat = ai.chats.create({
        model: 'gemini-3.6-flash',
        config: {
          systemInstruction: 'Eres Byte 🤖, la mascota y tutor de programación oficial de CodeLingo (estilo Duolingo de programación). Eres entusiasta, breve, usas emojis de código y das explicaciones sencillas en español con pequeños ejemplos visuales de código en Markdown.',
        },
      });

      const result = await chat.sendMessage({ message });
      res.json({ reply: result.text });
    } catch (error) {
      console.error('Error in /api/ai/tutor-chat:', error);
      res.status(500).json({ reply: '¡Ups! Byte tuvo un leve pestañeo. Por favor intenta preguntar de nuevo.' });
    }
  });

  // Vite Integration for dev vs production
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server listening on http://0.0.0.0:${PORT}`);
  });
}

startServer();
