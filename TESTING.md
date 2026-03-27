# 🧪 Testing Guide

Comprehensive testing setup for both backend (Python) and frontend (TypeScript).

---

## 📊 Test Coverage

| Layer | Technology | Coverage |
|-------|------------|----------|
| Backend | pytest + pytest-asyncio | Target: 80%+ |
| Frontend | Vitest + Testing Library | Target: 70%+ |
| Integration | MSW (Mock Service Worker) | API contract tests |

---

## 🐍 Backend Testing (Python)

### Quick Start

```bash
cd backend

# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_vector_store.py -v

# Run with markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Watch mode (requires pytest-watch)
ptw tests/
```

### Test Structure

```
backend/tests/
├── conftest.py           # Fixtures & test configuration
├── test_api.py           # API endpoint tests
├── test_vector_store.py  # VectorStore unit tests
├── test_embedding.py     # EmbeddingManager tests
├── test_data_loader.py   # Document loader tests
├── test_search.py        # RAG retrieval & generation tests
├── test_config.py        # Configuration tests
└── test_validation.py    # Pydantic validation tests
```

### Fixtures Available

- `settings` - Test-specific Settings object
- `temp_dir` - Temporary directory (auto-cleanup)
- `sample_document` - Mock Document instance
- `sample_documents` - List of 3 mock Documents
- `sample_embeddings` - Random numpy array (3×384)
- `mock_vector_store` - Mocked ChromaDB collection
- `mock_embedding_manager` - Mocked SentenceTransformer
- `mock_llm` - Mocked ChatMistralAI
- `client` - FastAPI TestClient

### Writing Tests

```python
import pytest
from unittest.mock import MagicMock, patch
from src.vector_store import VectorStore

def test_add_documents(mock_vector_store, sample_documents, sample_embeddings):
    """Test adding documents to vector store"""
    vs = VectorStore()
    vs.collection = mock_vector_store

    vs.add_documents(sample_documents, sample_embeddings)

    mock_vector_store.add.assert_called_once()
```

---

## ⚛️ Frontend Testing (TypeScript)

### Quick Start

```bash
cd frontend

# Install dependencies (includes test deps)
npm install

# Run tests once
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test -- --watch

# Run with UI
npm run test:ui

# Run specific test
npx vitest run src/test/components/Button.test.tsx
```

### Test Structure

```
frontend/src/test/
├── setup.ts                 # Global test setup (mocks, DOM config)
├── mockApi.ts               # MSW mock server for API
├── components/
│   ├── Button.test.tsx
│   ├── Card.test.tsx
│   ├── Badge.test.tsx
│   ├── Progress.test.tsx
│   └── Switch.test.tsx
├── store/
│   └── useAppStore.test.ts
└── utils/
    └── helpers.test.ts
```

### Mocking API Calls

We use **MSW (Mock Service Worker)** to mock HTTP requests:

```typescript
import { server } from '@/test/mockApi';
import { rest } from 'msw';

// Add new mocks
server.use(
  rest.post('/api/generate/quiz', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ questions: [...], sources: [...] })
    );
  })
);
```

### Writing Component Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Testing Store

```typescript
import { useAppStore } from '@/store/useAppStore';
import { beforeEach } from 'vitest';

beforeEach(() => {
  // Reset store state
  useAppStore.setState(useAppStore.getInitialState());
});

it('sets available sources', () => {
  const { setAvailableSources } = useAppStore.getState();
  setAvailableSources(['doc1.pdf']);

  expect(useAppStore.getState().availableSources).toContain('doc1.pdf');
});
```

---

## 🎯 Running All Tests

```bash
# Backend tests
cd backend
make test

# Frontend tests
cd frontend
make test

# All tests (frontend + backend)
make test-all
```

---

## 📈 Coverage Reports

### Backend

```bash
cd backend
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

View report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Frontend

```bash
cd frontend
npm run test:coverage
```

Coverage report generated in `frontend/coverage/` directory.

---

## 🏗️ Test Best Practices

1. **Mock External Services**
   - Always mock LLM calls (Mistral AI)
   - Mock database operations (ChromaDB)
   - Mock file system operations
   - Use fixtures for reusable test data

2. **Test Isolation**
   - Each test should be independent
   - Use `beforeEach` to reset state
   - Clean up temporary files/directories
   - Don't rely on test execution order

3. **Arrange-Act-Assert**
   ```python
   def test_something():
       # Arrange: setup test data
       data = create_test_data()

       # Act: execute function
       result = function_under_test(data)

       # Assert: verify results
       assert result == expected
   ```

4. **Descriptive Test Names**
   - `test_<function>_with_valid_input_returns_expected`
   - `test_<function>_raises_error_on_invalid_input`

5. **Use Factories**
   - Create factory functions for test data
   - Reuse common patterns
   ```python
   def make_document(content: str, source: str = "test.pdf"):
       return Document(page_content=content, metadata={"source_file": source})
   ```

6. **Test Error Cases**
   - Invalid inputs
   - Missing dependencies
   - Edge cases (empty lists, null values)
   - Exception handling

---

## 🔍 Common Patterns

### Mocking LLM Responses

```python
with patch('src.search.ChatMistralAI') as mock_llm:
    mock_instance = MagicMock()
    mock_instance.invoke.return_value.content = '{"questions": [...]}'
    mock_llm.return_value = mock_instance
    # ... run test
```

### Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("difficulty,expected", [
    ("Easy", "low"),
    ("Medium", "medium"),
    ("Hard", "high"),
])
def test_difficulty_levels(difficulty, expected):
    result = get_difficulty_level(difficulty)
    assert result == expected
```

---

## 🐛 Troubleshooting

### Tests fail with "ModuleNotFoundError"

```bash
# Backend: Add parent to path is handled in conftest.py
cd backend && python -m pytest tests/

# Frontend: Ensure vite.config.ts alias is correct
npm test
```

### MSW not intercepting requests

```typescript
// Ensure test setup includes msw.start()
import { server } from '@/test/mockApi';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Coverage not generating

```bash
# Backend: Ensure pytest-cov installed
pip install pytest-cov

# Frontend: Check vitest.config.ts coverage settings
npm run test:coverage
```

---

## 📋 CI/CD Integration

### GitHub Actions Example

```yaml
name: Backend Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## ✅ Pre-commit Hooks (Recommended)

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11
  - repo: local
    hooks:
      - id: pytest
        name: Run tests
        entry: bash -c "cd backend && pytest tests/"
        language: system
        pass_filenames: false
```

---

**Happy Testing!** 🎉
