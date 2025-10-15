# Frontend - Agentic AI Research Assistant

Modern React frontend with real-time streaming, built with Vite and TailwindCSS.

## 🚀 Quick Start

### Install Dependencies

```bash
npm install
```

### Configure Environment

Create `.env` file (optional):
```env
VITE_API_URL=http://localhost:8000
```

### Run Development Server

```bash
npm run dev
```

App runs on: `http://localhost:3000`

## 🏗️ Build for Production

```bash
npm run build
```

Output in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 🎨 Features

### Chat Interface
- Clean, modern design
- Real-time message streaming
- Typing indicators
- Agent stage progress

### Message Types
- **User messages**: Blue bubbles on right
- **AI responses**: White bubbles on left with markdown
- **System messages**: Amber bubbles for status updates

### Visual Feedback
- Progress indicators for each agent stage
- Confidence score visualization
- Source count badges
- Error alerts

## 🧩 Component Structure

```
src/
├── components/
│   ├── ChatUI.jsx          # Main chat interface
│   └── MessageBubble.jsx   # Individual messages
├── App.jsx                 # Root component
├── api.js                  # API client
└── index.css               # Global styles
```

### ChatUI Component

Main features:
- Message management
- SSE connection handling
- Input validation
- Example queries

### MessageBubble Component

Renders:
- User/Assistant messages
- Markdown formatting
- Metadata (confidence, sources)
- Timestamps

## 📡 API Integration

### EventSource (SSE)

```javascript
const eventSource = new EventSource(streamUrl);

eventSource.addEventListener('response', (event) => {
  const data = JSON.parse(event.data);
  // Handle streaming chunk
});
```

### HTTP Requests

```javascript
import { createQuery } from './api';

const result = await createQuery("Your question");
```

## 🎨 Styling

### TailwindCSS

Utility-first CSS framework with custom configuration:

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: { ... }
    }
  }
}
```

### Custom Styles

Markdown rendering in `index.css`:
- Headings with proper hierarchy
- Lists with indentation
- Code blocks with syntax highlighting
- Responsive tables

## 🔧 Configuration

### Vite Config

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### Proxy Setup

Development proxy routes `/api/*` to backend, avoiding CORS issues.

## 🐛 Debugging

### Check Backend Connection

1. Open browser console
2. Look for health check errors
3. Verify backend URL in `.env`

### View Network Requests

1. Open DevTools → Network tab
2. Filter for EventSource
3. Check SSE messages

## 📦 Dependencies

Main packages:
- `react` - UI library
- `react-markdown` - Markdown rendering
- `axios` - HTTP client
- `lucide-react` - Icons
- `tailwindcss` - Styling

See `package.json` for full list.

## 🚀 Performance

- Vite for fast HMR
- Code splitting
- Lazy loading
- Optimized builds

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints: sm, md, lg, xl
- Touch-friendly controls
- Adaptive layouts

## 🎯 Best Practices

1. **State Management**: Local state with hooks
2. **Error Handling**: Try-catch with user feedback
3. **Cleanup**: Close EventSource on unmount
4. **Accessibility**: Semantic HTML and ARIA labels

## 📖 Learn More

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [TailwindCSS](https://tailwindcss.com/docs)
- [React Markdown](https://github.com/remarkjs/react-markdown)

