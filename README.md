# Atlan Customer Support Copilot

A comprehensive AI-powered customer support system that automatically classifies tickets and provides intelligent responses using RAG (Retrieval-Augmented Generation) technology with Cohere's AI models.

## 🚀 Features

### Core Functionalities

1. **Bulk Ticket Classification Dashboard**
   - Automatic ingestion and classification of support tickets
   - AI-powered categorization by Topic, Sentiment, and Priority
   - Interactive visualizations and metrics
   - Filtering and search capabilities

2. **Interactive AI Agent**
   - Real-time ticket analysis and classification
   - RAG-based responses using Atlan documentation
   - Persistent form state for better UX
   - Source citation with accessible documentation links

### AI Capabilities

- **Topic Classification**: How-to, Product, Connector, Lineage, API/SDK, SSO, Glossary, Best practices, Sensitive data
- **Sentiment Analysis**: Frustrated, Curious, Angry, Neutral
- **Priority Assessment**: P0 (High), P1 (Medium), P2 (Low)
- **Knowledge Base**: Comprehensive Atlan documentation with accessible references

## 🏗️ Detailed Architecture & Workflow

```
                                CUSTOMER SUPPORT COPILOT ARCHITECTURE
                               ══════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         USER INTERFACE LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐              ┌─────────────────────┐              ┌─────────────────────┐ │
│  │  Bulk Classification │              │  Interactive Agent  │              │   Analytics Panel   │ │
│  │      Dashboard       │              │                     │              │                     │ │
│  │ • Upload Tickets     │              │ • Single Ticket     │              │ • Metrics Display   │ │
│  │ • View Results       │              │ • Real-time Analysis│              │ • Filter Options    │ │
│  │ • Export Data        │              │ • RAG Responses     │              │ • Visualizations    │ │
│  └─────────────────────┘              └─────────────────────┘              └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
           │                                      │                                      │
           ▼                                      ▼                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      APPLICATION LOGIC LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────┐    WORKFLOW    ┌─────────────────────┐    FEEDBACK    ┌─────────────────────┐│
│  │                     │◄──────────────►│                     │◄──────────────►│                     ││
│  │   TICKET CLASSIFIER │                │    ROUTING ENGINE   │                │    RAG SYSTEM       ││
│  │                     │                │                     │                │                     ││
│  │ ┌─────────────────┐ │   CLASSIFICATION│ ┌─────────────────┐ │   RAG REQUEST  │ ┌─────────────────┐ ││
│  │ │ Input Validation│ │                │ │ Topic Analysis  │ │                │ │ Query Processing│ ││
│  │ │ Text Cleaning   │ │                │ │ Priority Route  │ │                │ │ Doc Retrieval   │ ││
│  │ │ Rate Limiting   │ │                │ │ Response Type   │ │                │ │ Answer Generation│ ││
│  │ └─────────────────┘ │                │ └─────────────────┘ │                │ └─────────────────┘ ││
│  └─────────────────────┘                └─────────────────────┘                └─────────────────────┘│
│           │                                      │                                      │           │
│           ▼                                      │                                      ▼           │
│  ┌─────────────────────┐                        │                              ┌─────────────────────┐│
│  │   FALLBACK SYSTEM   │                        │                              │  RESPONSE FORMATTER │ │
│  │                     │                        │                              │                     │ │
│  │ • Keyword Matching  │                        │                              │ • Answer Compilation│ │
│  │ • Rule-based Logic  │                        │                              │ • Source Attribution│ │
│  │ • Default Categories│                        │                              │ • Confidence Scoring│ │
│  └─────────────────────┘                        │                              └─────────────────────┘│
│                                                  │                                                    │
└──────────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      EXTERNAL SERVICES LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────┐    API CALLS    ┌─────────────────────┐                                   │
│  │                     │◄───────────────►│                     │                                   │
│  │    COHERE API       │   (Rate Limited) │   RATE LIMITER      │                                   │
│  │                     │    6 sec delay   │                     │                                   │
│  │ • Chat API          │                 │ • 10 calls/min max  │                                   │
│  │ • command-r-plus    │                 │ • Trial key limits  │                                   │
│  │ • Classification    │                 │ • Queue management  │                                   │
│  │ • Response Gen      │                 │ • Wait notifications │                                   │
│  └─────────────────────┘                 └─────────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        DATA STORAGE LAYER                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────┐                        ┌─────────────────────┐                           │
│  │                     │                        │                     │                           │
│  │     CHROMADB        │◄──────────────────────►│   KNOWLEDGE BASE    │                           │
│  │                     │      EMBEDDINGS        │                     │                           │
│  │ • Vector Storage    │                        │ • Atlan Documentation│                           │
│  │ • Document Chunks   │                        │ • Product Guides     │                           │
│  │ • Similarity Search │                        │ • API References     │                           │
│  │ • Persistent Data   │                        │ • Best Practices     │                           │
│  └─────────────────────┘                        │ • Troubleshooting    │                           │
│                                                 └─────────────────────┘                           │
│                                                                                                     │
│  ┌─────────────────────┐                                                                           │
│  │                     │                                                                           │
│  │  SENTENCE TRANSFORMER│                                                                           │
│  │                     │                                                                           │
│  │ • all-MiniLM-L6-v2  │                                                                           │
│  │ • Local Embeddings  │                                                                           │
│  │ • Fast Processing   │                                                                           │
│  └─────────────────────┘                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                                          DATA FLOW DIAGRAM
                                         ═══════════════════

    User Input ──┐
                 ▼
    ┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
    │   1. VALIDATION     │──────▶│   2. CLASSIFICATION │──────▶│   3. ROUTING        │
    │                     │       │                     │       │                     │
    │ • Input cleaning    │       │ • Cohere API call   │       │ • Topic analysis    │
    │ • Format check      │       │ • Rate limiting     │       │ • Priority check    │
    │ • Error handling    │       │ • Fallback logic    │       │ • Response type     │
    └─────────────────────┘       └─────────────────────┘       └─────────────────────┘
                                           │                              │
                                           │ (if API fails)               │
                                           ▼                              ▼
                                  ┌─────────────────────┐       ┌─────────────────────┐
                                  │  FALLBACK SYSTEM    │       │   RAG PROCESSING    │
                                  │                     │       │                     │
                                  │ • Keyword matching  │       │ • Query embedding   │
                                  │ • Rule-based logic  │       │ • Vector search     │
                                  │ • Default response  │       │ • Doc retrieval     │
                                  └─────────────────────┘       │ • Answer generation │
                                           │                   └─────────────────────┘
                                           │                              │
                                           └──────────────┐               │
                                                         ▼               ▼
                                                ┌─────────────────────┐
                                                │  4. RESPONSE        │
                                                │     FORMATTING      │
                                                │                     │
                                                │ • Answer compilation │
                                                │ • Source attribution│
                                                │ • Confidence scoring │
                                                │ • UI formatting     │
                                                └─────────────────────┘
                                                         │
                                                         ▼
                                                   Final Response
```

## 🏆 Key Improvements

1. **Simplified Architecture**
   - Removed Google Gemini integration for better maintainability
   - Streamlined API key management (Cohere only)
   - Improved error handling and fallback mechanisms

2. **Enhanced User Experience**
   - Persistent form state in Interactive AI Agent
   - Clearer documentation references
   - Improved response formatting

3. **Optimized Performance**
   - Reduced API dependencies
   - Faster response times
   - More reliable fallback classification

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10 (required for compatibility with dependencies)
  - Note: Python 3.10 is specifically required as some dependencies don't have wheel files available for newer Python versions
- Virtual environment (recommended)
- Cohere API key (required for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customer-copilot
   ```

2. **Set up virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   # source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   copy .env.example .env
   
   # Edit .env and add your Cohere API key
   # COHERE_API_KEY=your_api_key_here
   ```

5. **Initialize the knowledge base**
   ```bash
   python -c "from rag_system import RAGSystem; RAGSystem().populate_knowledge_base()"
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```
   
   The application will be available at `http://localhost:8501`

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required for AI features
COHERE_API_KEY=your_cohere_api_key_here

# RAG Configuration (optional)
# CHUNK_SIZE=1000         # Size of text chunks for embedding
# CHUNK_OVERLAP=200       # Overlap between chunks for better context
# MAX_RETRIEVAL_DOCS=5    # Maximum number of documents to retrieve per query
```

## 🎯 Usage

### Bulk Classification Dashboard

1. Navigate to the "Bulk Ticket Classification" tab
2. The system automatically processes and classifies sample tickets on load
3. View metrics, charts, and detailed classifications
4. Use filters to explore tickets by:
   - Priority (P0, P1, P2)
   - Sentiment (Frustrated, Curious, Angry, Neutral)
   - Topic (Connector, Lineage, API/SDK, etc.)

### Interactive AI Agent

1. Go to the "Interactive AI Agent" tab
2. Enter a support ticket subject and description
3. Click "Analyze Ticket" to get:
   - Automatic classification (topic, sentiment, priority)
   - AI-generated response using Atlan documentation
   - Source references for all provided information

### Key Features

- **Persistent Form State**: Your input remains in the form after submission
- **Clear Citations**: All responses include source documentation links
- **Fallback Classification**: Works even without API keys (with reduced functionality)
- **Responsive Design**: Works on both desktop and mobile devices

### Interactive AI Agent

1. Navigate to the "Interactive AI Agent" tab
2. Enter a ticket subject and body
3. View the internal analysis (classification details)
4. See the final response (RAG-based or routing message)

## 🧠 AI Pipeline Design

### Ticket Classification
1. **Input Processing**: Ticket subject and body are cleaned and combined
2. **Feature Extraction**: Text is processed to extract key features
3. **Model Inference**: Cohere API classifies the ticket
4. **Fallback Logic**: If API is unavailable, uses keyword-based classification

### RAG System
1. **Query Processing**: User question is preprocessed and embedded
2. **Vector Search**: Finds most relevant document chunks using ChromaDB
3. **Response Generation**: Cohere generates answer using retrieved context
4. **Source Attribution**: Includes clear references to documentation

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your Cohere API key is set in the `.env` file
   - Verify the key has proper permissions
   - Check your internet connection

2. **Installation Issues**
   - Make sure you're using Python 3.8+
   - Try recreating the virtual environment
   - Check for any error messages during installation

3. **Knowledge Base Problems**
   - Run the knowledge base initialization if documents aren't loading
   - Check disk space if ChromaDB has issues
   - Verify document paths in the code if using custom documents

4. **Documentation Link Limitations**
   - Nested/deep links to specific Atlan documentation sections may not work directly
   - The system provides root URLs (https://docs.atlan.com) for reliability
   - Users need to navigate from the root link to access specific sections
   - Full reference paths are shown in responses for manual navigation

## 📊 Key Design Decisions

### Model Selection
- **Cohere Command-R-Plus**: Provides high-quality reasoning and response generation
- **Fallback Classification**: Ensures 100% uptime even without API access

### Vector Database
- **ChromaDB**: Lightweight, persistent storage for document embeddings
- **Sentence Transformers**: Efficient local embeddings for semantic search
- **Chunking Strategy**: 1000-character chunks with 200-character overlap for context

### UI/UX Improvements
- **Persistent State**: Form inputs are preserved after submission
- **Clear Citations**: Direct links to documentation sources
- **Responsive Design**: Works across desktop and mobile devices
- **Visual Feedback**: Color-coded priorities and sentiment indicators

### Scalability Considerations
- **Efficient Caching**: Streamlit caching for AI systems and data loading
- **Batch Processing**: Handles bulk ticket classification efficiently
- **Modular Architecture**: Clear separation of concerns for maintainability

## 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS for a polished interface
- **AI Models**: Cohere Command-R-Plus for classification and response generation
- **Vector Database**: ChromaDB for document storage and retrieval
- **Embeddings**: Sentence Transformers for efficient semantic search
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express
- **Web Scraping**: BeautifulSoup, Requests

## 📈 Performance Metrics

### System Performance
- **Response Time**: Typically under 3 seconds for classification and response generation
- **Document Retrieval**: Sub-second search across the knowledge base
- **Fallback Classification**: Near-instant keyword-based classification when needed

### Quality Metrics
- **Classification Accuracy**: High accuracy for topic and sentiment classification
- **Response Relevance**: Context-aware answers based on retrieved documentation
- **Source Quality**: Only authoritative Atlan documentation sources used
- **Response Quality**: Human evaluation of generated answers
- **Fallback Coverage**: Seamless fallback to keyword-based classification when needed

## 🚀 Deployment

### 1. Local Development
```bash
# Clone and setup
git clone <repository-url>
cd customer-copilot

# Create virtual environment (Python 3.10 required)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your Cohere API key

# Run application
streamlit run app.py
```

### 2. Streamlit Community Cloud (Recommended)
**Best for:** Quick deployment, free hosting, automatic updates

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub account
   - Select repository
   - Set secrets:
     - `COHERE_API_KEY` = your_api_key

3. **Advantages:**
   - ✅ Free hosting
   - ✅ Automatic SSL/HTTPS
   - ✅ Auto-deploy on git push
   - ✅ Built-in secrets management

### 3. Docker Deployment
**Best for:** Consistent environments, easy scaling

```bash
# Build image
docker build -t customer-copilot .

# Run container
docker run -d \
  --name customer-copilot \
  -p 8501:8501 \
  -e COHERE_API_KEY=your_key \
  -v $(pwd)/chroma_db:/app/chroma_db \
  customer-copilot
```

**Or use Docker Compose:**
```bash
# Set environment variables in .env file
docker-compose up -d
```

### 4. Cloud Platform Deployment

#### AWS Deployment
1. **EC2 Instance:**
   ```bash
   # Launch t3.medium instance (2 vCPU, 4GB RAM)
   # Install Docker
   sudo yum update -y
   sudo yum install -y docker
   sudo service docker start
   
   # Clone and deploy
   git clone <your-repo>
   cd customer-copilot
   docker-compose up -d
   ```

2. **AWS App Runner:**
   - Connect to GitHub repository
   - Set environment variables
   - Auto-scaling capabilities

#### Google Cloud Platform
```bash
# Deploy to Cloud Run
gcloud run deploy customer-copilot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars COHERE_API_KEY=your_key
```

#### Azure Container Instances
```bash
# Create resource group
az group create --name customer-copilot --location eastus

# Deploy container
az container create \
  --resource-group customer-copilot \
  --name customer-copilot-app \
  --image your-registry/customer-copilot \
  --cpu 2 --memory 4 \
  --ports 8501 \
  --environment-variables COHERE_API_KEY=your_key
```

### 5. Production Considerations

#### Performance Optimization
- **Memory:** Minimum 4GB RAM for ChromaDB + embedding models
- **CPU:** 2+ vCPUs for concurrent users
- **Storage:** Persistent volume for ChromaDB data
- **Rate Limiting:** Built-in for trial API keys (10 calls/min)

#### Security
```bash
# Use secrets management
# AWS: AWS Secrets Manager
# GCP: Secret Manager
# Azure: Key Vault
# Docker: Docker Secrets
```

#### Monitoring
```yaml
# docker-compose.yml with monitoring
version: '3.8'
services:
  app:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### Backup Strategy
```bash
# Backup ChromaDB data
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_db/

# Automated backup script
# 0 2 * * * /path/to/backup_script.sh
```

### 6. Domain & SSL Setup

#### Custom Domain
1. **Streamlit Cloud:** Built-in custom domains
2. **Self-hosted:** Use nginx reverse proxy

```nginx
# nginx configuration
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### SSL Certificate
```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 7. Scaling Considerations

#### Load Balancing
```yaml
# docker-compose.yml for multiple instances
version: '3.8'
services:
  app:
    build: .
    deploy:
      replicas: 3
  
  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

#### Database Considerations
- **ChromaDB:** Single instance (not horizontally scalable)
- **Alternative:** Consider Pinecone or Weaviate for production
- **Backup:** Regular ChromaDB data backups essential
## 🔒 Security & Privacy

### Data Protection
- **No Data Storage**: User inputs are processed in memory and not persisted
- **Secure API Calls**: All external API calls use HTTPS
- **Environment Variables**: Sensitive data is stored in `.env` (not version controlled)

### Best Practices
1. Never commit `.env` files to version control
2. Use least-privilege API keys
3. Regularly update dependencies for security patches
4. Monitor API usage for anomalies

## 🛣️ Future Enhancements

### Short Term (Next Release)
- [ ] User authentication and role-based access
- [ ] Support for custom knowledge base documents
- [ ] Enhanced ticket visualization and analytics
- [ ] Multi-language support
- [ ] Export functionality for reports and classifications

### Long Term
- [ ] Integration with ticketing systems (Zendesk, Jira, ServiceNow)
- [ ] Automated knowledge base updates
- [ ] Advanced analytics and reporting dashboard
- [ ] Multi-tenant support
- [ ] Real-time ticket ingestion via webhooks
- [ ] Custom model fine-tuning
- [ ] Automated response suggestions for agents

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m 'Add some feature'`
4. **Push** to the branch: `git push origin feature/your-feature-name`
5. Open a **pull request**

### Development Setup

1. Set up the development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt  # Includes development dependencies
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

3. Format code (before committing):
   ```bash
   black .
   isort .
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Atlan](https://atlan.com/) for the comprehensive documentation
- [Cohere](https://cohere.com/) for their powerful AI models
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [ChromaDB](https://www.trychroma.com/) for vector storage and search
- [Sentence Transformers](https://www.sbert.net/) for efficient text embeddings
- The open source community for the supporting libraries

---

**Built with ❤️ for efficient customer support at scale**
