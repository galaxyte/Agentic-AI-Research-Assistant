# 🤝 Contributing to Agentic AI Research Assistant

Thank you for considering contributing to this project! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Project Structure](#project-structure)

## 📜 Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors:

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## 🎯 How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
1. Check the existing issues
2. Verify you're using the latest version
3. Try to reproduce the issue

When filing a bug report, include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python/Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:
- Clear description of the enhancement
- Why it would be useful
- Possible implementation approach
- Examples if applicable

### Code Contributions

Areas where contributions are especially welcome:

**Backend:**
- New agent capabilities
- Additional validation strategies
- Performance optimizations
- Better error handling
- Test coverage

**Frontend:**
- UI/UX improvements
- Accessibility enhancements
- Mobile responsiveness
- New visualization features

**Documentation:**
- Tutorial improvements
- Code examples
- Architecture diagrams
- Deployment guides

## 🛠️ Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- API keys (OpenAI, Tavily)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/your-username/agentic-ai-research-assistant.git
   cd agentic-ai-research-assistant
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Set up frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Development Workflow

1. Make your changes
2. Test thoroughly
3. Commit with clear messages
4. Push to your fork
5. Open a Pull Request

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated (if applicable)

### PR Guidelines

1. **Title**: Clear, descriptive title
   - Good: "Add validation for email addresses in user input"
   - Bad: "Fix bug"

2. **Description**: Include:
   - What changes were made
   - Why they were necessary
   - How to test them
   - Related issues (if any)

3. **Commits**: 
   - Small, focused commits
   - Clear commit messages
   - Follow conventional commits format

4. **Review Process**:
   - Maintainers will review within a few days
   - Address feedback promptly
   - Be open to suggestions

## 💻 Coding Standards

### Python (Backend)

```python
# Use type hints
def process_query(query: str, max_results: int = 5) -> List[Dict]:
    """
    Process a user query.
    
    Args:
        query: The user's search query
        max_results: Maximum number of results to return
        
    Returns:
        List of result dictionaries
    """
    pass

# Follow PEP 8
# Use descriptive variable names
# Add docstrings to functions and classes
# Handle errors appropriately
```

**Style:**
- PEP 8 compliance
- Type hints for function signatures
- Docstrings for all public functions
- Maximum line length: 100 characters

### JavaScript/React (Frontend)

```javascript
// Use functional components
const MessageBubble = ({ message, isLoading = false }) => {
  // Destructure props
  // Use hooks appropriately
  // Add prop types or TypeScript
  
  return (
    <div className="message-bubble">
      {/* JSX */}
    </div>
  );
};

// Export at bottom
export default MessageBubble;
```

**Style:**
- Functional components with hooks
- Descriptive component and variable names
- PropTypes or TypeScript
- TailwindCSS for styling

### Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new validation agent
fix: resolve SSE connection timeout
docs: update deployment guide
style: format code with black
refactor: simplify researcher agent logic
test: add unit tests for summarizer
chore: update dependencies
```

## 📁 Project Structure

```
backend/
├── agents/          # Agent implementations
├── workflows/       # LangGraph workflows
├── utils/           # Utility functions
└── main.py          # FastAPI application

frontend/
├── src/
│   ├── components/  # React components
│   ├── api.js       # API client
│   └── App.jsx      # Root component
└── package.json
```

### Adding a New Agent

1. Create file in `backend/agents/`
2. Implement agent class with `execute()` method
3. Add to workflow in `workflows/research_graph.py`
4. Update documentation

### Adding a New Component

1. Create file in `frontend/src/components/`
2. Implement React component
3. Import in parent component
4. Add styles if needed

## 🧪 Testing Guidelines

### Backend Tests

```python
# test_researcher.py
import pytest
from agents.researcher import researcher_agent

@pytest.mark.asyncio
async def test_researcher_execute():
    state = {"query": "test query"}
    result = await researcher_agent.execute(state)
    assert "research_results" in result
    assert len(result["research_results"]) > 0
```

### Frontend Tests

```javascript
// MessageBubble.test.jsx
import { render, screen } from '@testing-library/react';
import MessageBubble from './MessageBubble';

test('renders user message', () => {
  const message = { role: 'user', content: 'Hello' };
  render(<MessageBubble message={message} />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Questions?

- Open a GitHub Discussion
- Comment on relevant issues
- Tag maintainers in PRs

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🎉**

