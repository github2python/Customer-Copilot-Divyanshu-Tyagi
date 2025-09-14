import chromadb
from chromadb.config import Settings
import cohere
import json
import time
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Optional
import re
from config import Config

class RAGSystem:
    def __init__(self):
        self.config = Config()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = None
        self.last_api_call_time = 0
        self.min_delay_between_calls = 6  # 6 seconds for 10 calls/min limit
        
        # Initialize AI clients
        self.cohere_client = None
        
        if self.config.USE_COHERE and self.config.COHERE_API_KEY:
            try:
                import cohere
                self.cohere_client = cohere.Client(self.config.COHERE_API_KEY)
            except Exception as e:
                print(f"Failed to initialize Cohere client: {e}")
        
        self._setup_vector_db()
    
    def _wait_for_rate_limit(self):
        """Ensure we respect the API rate limit (10 calls/min for trial keys)."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call_time
        
        if time_since_last_call < self.min_delay_between_calls:
            wait_time = self.min_delay_between_calls - time_since_last_call
            print(f"Rate limiting: waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
        
        self.last_api_call_time = time.time()
    
    def _setup_vector_db(self):
        """Setup ChromaDB collection for storing document embeddings."""
        try:
            self.collection = self.chroma_client.get_collection("atlan_docs")
            print("Existing ChromaDB collection found")
        except Exception as e:
            print(f"No existing collection found, creating new one: {e}")
            try:
                self.collection = self.chroma_client.create_collection(
                    name="atlan_docs",
                    metadata={"description": "Atlan documentation embeddings"}
                )
                print("Created new ChromaDB collection")
                # Initialize the knowledge base after creating collection
                self.populate_knowledge_base()
            except Exception as create_error:
                print(f"Error creating ChromaDB collection: {create_error}")
                raise
    
    def create_knowledge_base(self) -> List[Dict]:
        """Create comprehensive Atlan knowledge base with accessible URLs."""
        return [
            {
                'url': 'https://docs.atlan.com',
                'title': 'Snowflake Connector Setup',
                'content': '''To connect Snowflake to Atlan, you need specific permissions:

Required Permissions:
- USAGE on warehouse, database, and schema
- SELECT on all tables you want to catalog
- SHOW on warehouse and database
- DESCRIBE on tables for schema information

Setup Steps:
1. Create a dedicated service account in Snowflake
2. Grant the required permissions to this account
3. Use the Snowflake connector in Atlan
4. Provide connection details: hostname, warehouse, database, username, password

Common Issues:
- Insufficient permissions cause connection failures
- Network connectivity problems
- Incorrect warehouse or database names
- Service account locked or expired

Reference: Navigate to Atlan Docs > Connectors > Snowflake for detailed setup instructions.''',
                'source': 'docs'
            },
            {
                'url': 'https://docs.atlan.com',
                'title': 'Data Lineage in Atlan',
                'content': '''Atlan automatically captures lineage from various sources:

Supported Connectors for Lineage:
- dbt: Full lineage from models, seeds, and snapshots
- Fivetran: Captures source to destination lineage
- Tableau: Workbook and dashboard lineage
- Airflow: DAG-based lineage tracking
- Snowflake: Query-based lineage (with query history)

Lineage Features:
- Upstream and downstream dependency tracking
- Visual lineage graphs in the UI
- Export lineage as images or PDFs
- Programmatic access via API
- Impact analysis for changes

Troubleshooting:
- Missing lineage often due to insufficient permissions
- Re-run crawlers to refresh lineage data
- Check connector-specific lineage requirements

Reference: Navigate to Atlan Docs > Lineage section for comprehensive lineage documentation.''',
                'source': 'docs'
            },
            {
                'url': 'https://developer.atlan.com',
                'title': 'Atlan REST API',
                'content': '''Atlan provides comprehensive REST APIs for programmatic access:

Authentication:
- API keys for service accounts
- Bearer token authentication
- 90-day key rotation support
- OAuth integration available

Common API Operations:
- GET /api/meta/entity/guid/{guid} - Retrieve asset details
- POST /api/meta/entity/bulk - Create multiple assets
- PUT /api/meta/entity/bulk - Update asset metadata
- GET /api/meta/lineage/{guid} - Get lineage information
- POST /api/meta/search/basic - Search assets

Python SDK:
- Install: pip install pyatlan
- Authentication via API key
- Simplified asset creation and updates
- Built-in retry and error handling

Example Asset Creation:
```python
import pyatlan
client = pyatlan.AtlanClient(api_key="your_key")
asset = client.asset.create_table(
    name="my_table",
    database="my_db",
    schema="my_schema"
)
```

Reference: Visit developer.atlan.com for complete API documentation and SDK guides.''',
                'source': 'developer'
            },
            {
                'url': 'https://docs.atlan.com',
                'title': 'SAML SSO Configuration',
                'content': '''Configure SAML SSO with identity providers:

Supported Identity Providers:
- Okta
- Azure Active Directory
- Auth0
- OneLogin
- Generic SAML 2.0 providers

Configuration Steps:
1. Configure SAML application in your IdP
2. Set up SAML configuration in Atlan
3. Map SAML attributes to Atlan user properties
4. Test with a single user before full rollout

SAML Attribute Mapping:
- Email: Required for user identification
- Groups: For automatic team assignment
- First Name, Last Name: For user profiles
- Department: For organizational structure

Testing SSO:
- Use test mode for specific users
- Verify group assignments work correctly
- Check attribute mapping
- Ensure fallback authentication works

Common Issues:
- Incorrect attribute mapping
- Missing group assertions
- Clock synchronization problems
- Certificate expiration

Reference: Navigate to Atlan Docs > Administration > SSO for detailed SSO setup guides.''',
                'source': 'docs'
            },
            {
                'url': 'https://docs.atlan.com',
                'title': 'Visual Query Builder',
                'content': '''Use Atlan's Visual Query Builder for SQL-free data exploration:

Features:
- Drag-and-drop interface for table selection
- Visual join configuration
- Filter and aggregation options
- Query saving and sharing
- Export results to CSV or Excel

How to Access:
1. Navigate to any table or view asset
2. Click on the "Insights" tab
3. Select "Query Builder"
4. Start building your query visually

Joining Tables:
- Select multiple tables from the catalog
- Define join conditions visually
- Choose join types (inner, left, right, full outer)
- Preview join results before execution

Saving Queries:
- Save queries for future use
- Share queries with team members
- Create query templates
- Schedule query execution (premium feature)

Step-by-step for Business Analysts:
1. Access Visual Query Builder from Insights tab
2. Drag customer, orders, and product tables into workspace
3. Click join icons between tables to define relationships
4. Select join type and matching columns (e.g., customer_id)
5. Choose columns to include in results
6. Apply filters if needed
7. Save query with descriptive name
8. Run query to preview results

Reference: Navigate to Atlan Docs > Insights > Query Builder for complete usage instructions.''',
                'source': 'docs'
            },
            {
                'url': 'https://docs.atlan.com',
                'title': 'Business Glossary Management',
                'content': '''Create and manage business glossaries in Atlan:

Key Features:
- Centralized business term definitions
- Bulk import via CSV or API
- Automatic term linking to assets
- Hierarchical term organization
- Term approval workflows

Setup Steps:
1. Navigate to Governance > Glossary
2. Create new glossary or use existing
3. Add terms with clear definitions
4. Set up approval workflows
5. Link terms to relevant assets

Bulk Import Process:
- Download CSV template from Atlan
- Fill in term names, definitions, and metadata
- Upload CSV file through the interface
- Review and approve imported terms

API Management:
- Use REST API for programmatic glossary management
- Automate term creation and updates
- Integrate with external systems

Best Practices:
- Use consistent naming conventions
- Provide clear, business-friendly definitions
- Establish ownership and stewardship
- Regular review and updates

Reference: Navigate to Atlan Docs > Governance > Glossary for comprehensive glossary management guides.''',
                'source': 'docs'
            },
            {
                'url': 'https://docs.atlan.com',
                'title': 'PII and Sensitive Data Management',
                'content': '''Atlan provides comprehensive PII and sensitive data management:

Automatic Classification:
- Built-in PII classifiers for common data types
- Custom classification rules
- Machine learning-based detection
- Regular expression patterns

Data Protection Features:
- Column-level masking and encryption
- Access controls based on sensitivity
- Audit trails for sensitive data access
- Integration with external DLP tools

Compliance Support:
- GDPR compliance features
- Data retention policies
- Right to be forgotten workflows
- Privacy impact assessments

Setup Process:
1. Enable PII classification in settings
2. Configure classification rules
3. Set up data masking policies
4. Define access controls
5. Monitor and audit access

Integration Options:
- HashiCorp Vault for secrets management
- External DLP solutions
- Identity providers for access control
- SIEM tools for monitoring

Reference: Navigate to Atlan Docs > Security > Data Classification for detailed PII management documentation.''',
                'source': 'docs'
            }
        ]
    
    def populate_knowledge_base(self):
        """Populate the vector database with Atlan documentation."""
        try:
            # Check if collection already has documents
            if self.collection.count() > 0:
                print(f"Knowledge base already populated with {self.collection.count()} documents")
                return
            
            print("Populating knowledge base...")
            
            # Use comprehensive knowledge base
            documents = self.create_knowledge_base()
            
            # Chunk documents
            chunks = []
            for doc in documents:
                doc_chunks = self._chunk_document(doc)
                chunks.extend(doc_chunks)
            
            # Generate embeddings and store
            if chunks:
                texts = [chunk['content'] for chunk in chunks]
                embeddings = self.embedding_model.encode(texts).tolist()
                
                ids = [f"chunk_{i}" for i in range(len(chunks))]
                metadatas = [{
                    'url': chunk['url'],
                    'title': chunk['title'],
                    'source': chunk['source']
                } for chunk in chunks]
                
                self.collection.add(
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                
                print(f"Added {len(chunks)} chunks to knowledge base")
            
        except Exception as e:
            print(f"Error populating knowledge base: {e}")
    
    def _chunk_document(self, doc: Dict) -> List[Dict]:
        """Split document into smaller chunks."""
        content = doc['content']
        chunks = []
        
        # Simple sentence-based chunking
        sentences = re.split(r'[.!?]+', content)
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk + sentence) > self.config.CHUNK_SIZE:
                if current_chunk:
                    chunks.append({
                        'url': doc['url'],
                        'title': doc['title'],
                        'content': current_chunk.strip(),
                        'source': doc['source']
                    })
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add remaining chunk
        if current_chunk:
            chunks.append({
                'url': doc['url'],
                'title': doc['title'],
                'content': current_chunk.strip(),
                'source': doc['source']
            })
        
        return chunks
    
    def retrieve_relevant_docs(self, query: str) -> List[Dict]:
        """Retrieve relevant documents for a query."""
        try:
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=self.config.MAX_RETRIEVAL_DOCS
            )
            
            relevant_docs = []
            for i, doc in enumerate(results['documents'][0]):
                relevant_docs.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else 0
                })
            
            return relevant_docs
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def generate_answer_with_cohere(self, query: str, context_docs: List[Dict]) -> Optional[str]:
        """Generate answer using Cohere API."""
        if not self.cohere_client:
            return None
        
        try:
            context = "\n\n".join([
                f"Source: {doc['metadata']['title']} ({doc['metadata']['url']})\n{doc['content']}"
                for doc in context_docs
            ])
            
            prompt = f"""
Based on the following Atlan documentation, provide a helpful and accurate answer to the user's question.

Context:
{context}

Question: {query}

Instructions:
- Provide a clear, actionable answer based on the documentation
- Include specific steps or examples when relevant
- If the documentation doesn't contain enough information, say so
- Always cite the sources used in your answer

Answer:
"""
            
            self._wait_for_rate_limit()  # Respect API rate limit
            response = self.cohere_client.chat(
                model='command-r-plus-08-2024',
                message=prompt,
                max_tokens=800,
                temperature=0.1
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating answer with Cohere: {e}")
            return None
    
    
    def generate_rag_response(self, query: str, max_docs: int = 5) -> Dict:
        """Generate a complete RAG response with sources."""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(query)
        if not relevant_docs:
            return {
                'answer': "I couldn't find relevant information in the Atlan documentation to answer your question.",
                'sources': [],
                'confidence': 'low'
            }
        
        # Generate answer using Cohere
        answer = None
        
        if self.config.USE_COHERE and self.cohere_client:
            answer = self.generate_answer_with_cohere(query, relevant_docs)
        
        if not answer:
            # Direct response from documentation
            answer = f"Based on the available documentation:\n\n"
            answer += "\n\n".join([doc['content'][:400] for doc in relevant_docs[:2]])
        
        # Extract unique sources
        sources = list(set([doc['metadata']['url'] for doc in relevant_docs]))
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': 'high' if len(relevant_docs) >= 3 else 'medium'
        }
