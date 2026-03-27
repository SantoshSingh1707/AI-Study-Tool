import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Create mock server
export const server = setupServer(
  // Health check
  rest.get('/health', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        status: 'healthy',
        documents_count: 0,
        available_sources: [],
      })
    );
  }),

  // List documents
  rest.get('/api/documents', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        sources: ['test.pdf', 'sample.docx'],
        total_chunks: 50,
      })
    );
  }),

  // Upload document
  rest.post('/api/upload', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        message: 'Successfully uploaded test.pdf',
        chunks_added: 10,
        pages_processed: 5,
      })
    );
  }),

  // Delete document
  rest.delete('/api/documents/:sourceName', (req, res, ctx) => {
    const { sourceName } = req.params;
    if (sourceName === 'notfound.pdf') {
      return res(ctx.status(404));
    }
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        message: `Deleted ${sourceName}`,
      })
    );
  }),

  // Generate quiz
  rest.post('/api/generate/quiz', (req, res, ctx) => {
    const body = req.body;
    if (body.num_questions > 20) {
      return res(ctx.status(400), ctx.json({ detail: 'Too many questions' }));
    }

    const quizResponse = {
      questions: [
        {
          type: 'MCQ',
          question: 'What is 2 + 2?',
          options: ['3', '4', '5', '6'],
          answer: '4',
          explanation: 'Because 2+2 equals 4',
        },
      ],
      sources: [
        {
          source_file: 'math.pdf',
          similarity_score: 0.85,
          content: 'Math content...',
        },
      ],
    };

    return res(ctx.status(200), ctx.json(quizResponse));
  }),

  // Generate learning content
  rest.post('/api/generate/learning', (req, res, ctx) => {
    const learningResponse = {
      content: '# Summary\n\nThis is a test summary.',
      sources: [],
    };
    return res(ctx.status(200), ctx.json(learningResponse));
  })
);

// Start/stop helpers
export const startMockServer = () => server.listen();
export const stopMockServer = () => server.close();
