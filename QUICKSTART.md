# ⚡ Quick Start Guide

Get up and running with the Agentic AI Research Assistant in 5 minutes!

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.9 or higher installed
- ✅ Node.js 18 or higher installed
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Tavily API key ([Get one here](https://tavily.com))

## 🎯 Option 1: Docker (Easiest)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd agentic-ai-research-assistant
```

### Step 2: Set Up Environment

```bash
# Copy example environment file
cp backend/.env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=sk-your-key-here
# TAVILY_API_KEY=tvly-your-key-here
```

### Step 3: Start Everything

```bash
docker-compose up
```

That's it! 🎉

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🛠️ Option 2: Manual Setup

### Step 1: Clone and Navigate

```bash
git clone <your-repo-url>
cd agentic-ai-research-assistant
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start backend
python main.py
```

Backend now running at: http://localhost:8000

### Step 3: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend now running at: http://localhost:3000

### Step 4: Optional - Start Weaviate (New Terminal)

```bash
docker run -d \
  -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e ENABLE_MODULES=text2vec-openai \
  -e OPENAI_APIKEY=your-openai-key \
  semitechnologies/weaviate:latest
```

*Note: The system works without Weaviate, but semantic memory will be disabled.*

## 🎮 Your First Query

1. Open http://localhost:3000 in your browser
2. Type a question like:
   ```
   Explain the latest advancements in AI agent frameworks
   ```
3. Press Enter and watch the magic happen! ✨

You'll see:
- 🧑‍🔬 Researcher gathering sources
- ✍️ Summarizer condensing information
- ✅ Validator checking facts
- 💬 Presenter streaming the answer

## 🔍 Verify Everything Works

### Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "weaviate": "connected",
  "openai": "configured",
  "tavily": "configured"
}
```

### Check Frontend

Open http://localhost:3000 - you should see the chat interface.

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError`
**Solution**: 
```bash
pip install -r requirements.txt
```

**Error**: `OPENAI_API_KEY not found`
**Solution**: Check that `.env` file exists in `backend/` and has your API key

### Frontend won't start

**Error**: `Cannot find module`
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Error**: `Port 3000 already in use`
**Solution**: Kill the process using port 3000 or change port in `vite.config.js`

### Can't connect to backend

**Error**: `Failed to fetch` or `Network Error`
**Solution**: 
1. Verify backend is running on port 8000
2. Check browser console for CORS errors
3. Ensure `VITE_API_URL` is correct (or using default)

### Weaviate connection failed

**Warning in health check**: `weaviate: disconnected`
**Solution**: 
- If using Docker: `docker ps` to check if Weaviate is running
- If not needed: System will work without Weaviate (no semantic memory)
- To start Weaviate: See Step 4 above

## 📚 Next Steps

1. **Read the full README**: See [README.md](README.md)
2. **Explore API docs**: Visit http://localhost:8000/docs
3. **Try example queries**: Use the suggestions in the UI
4. **Customize agents**: Modify files in `backend/agents/`
5. **Deploy to production**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## 💡 Tips

- **Save API costs**: Use specific, focused queries
- **Better results**: Ask clear, well-defined questions
- **Debug issues**: Check browser console and backend logs
- **Monitor usage**: Watch your OpenAI dashboard for token usage

## 🎓 Example Queries to Try

1. "What are the benefits of multi-agent AI systems?"
2. "Compare LangGraph, CrewAI, and AutoGen frameworks"
3. "How does semantic search work in vector databases?"
4. "Explain the latest developments in large language models"

## 🆘 Still Having Issues?

1. Check the logs:
   ```bash
   # Backend logs (in backend terminal)
   # Frontend logs (in frontend terminal)
   ```

2. Verify API keys are valid
3. Check network connectivity
4. Review the [README.md](README.md) for detailed docs
5. Open an issue on GitHub

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Health check returns "healthy"
- [ ] Can submit a query
- [ ] Receives streamed response
- [ ] No errors in console

## 🎉 You're Ready!

You now have a fully functional AI research assistant. Enjoy exploring!

---

**Need help?** Check [README.md](README.md) | **Want to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md)

