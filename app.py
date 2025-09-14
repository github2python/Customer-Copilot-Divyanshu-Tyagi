import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ai_classifier import TicketClassifier
from rag_system import RAGSystem
from config import Config
import time

# Page configuration
st.set_page_config(
    page_title="Atlan Customer Support Copilot",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .classification-result {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .rag-response {
        background-color: #f0f9ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #0ea5e9;
    }
    .source-link {
        background-color: #fef3c7;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        border-left: 3px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_systems():
    """Initialize AI systems with caching."""
    classifier = TicketClassifier()
    rag_system = RAGSystem()
    rag_system.populate_knowledge_base()
    return classifier, rag_system

@st.cache_data
def load_sample_tickets():
    """Load sample tickets with caching."""
    try:
        with open('sample_tickets.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Sample tickets file not found. Please ensure sample_tickets.json exists.")
        return []

def display_classification_metrics(classified_tickets):
    """Display classification metrics and charts."""
    if not classified_tickets:
        return
    
    df = pd.DataFrame(classified_tickets)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Tickets", len(df))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        high_priority = len(df[df['priority'] == 'P0 (High)'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("High Priority", high_priority)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        frustrated_count = len(df[df['sentiment'] == 'Frustrated'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Frustrated Users", frustrated_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        unique_topics = len(set([tag for tags in df['topic_tags'] for tag in tags]))
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Topics", unique_topics)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Priority distribution
        priority_counts = df['priority'].value_counts()
        fig_priority = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            title="Priority Distribution",
            color_discrete_map={
                'P0 (High)': '#ef4444',
                'P1 (Medium)': '#f97316',
                'P2 (Low)': '#22c55e'
            }
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        sentiment_counts = df['sentiment'].value_counts()
        fig_sentiment = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            title="Sentiment Distribution",
            color=sentiment_counts.values,
            color_continuous_scale="RdYlBu_r"
        )
        fig_sentiment.update_layout(showlegend=False)
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Topic tags analysis
    all_tags = [tag for tags in df['topic_tags'] for tag in tags]
    tag_counts = pd.Series(all_tags).value_counts()
    
    fig_topics = px.bar(
        x=tag_counts.values,
        y=tag_counts.index,
        orientation='h',
        title="Topic Distribution",
        color=tag_counts.values,
        color_continuous_scale="viridis"
    )
    fig_topics.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_topics, use_container_width=True)

def display_ticket_details(ticket):
    """Display detailed ticket information with complete classification schema."""
    st.markdown('<div class="classification-result">', unsafe_allow_html=True)
    
    # Ticket Header
    st.subheader(f"🎫 {ticket['id']}")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.write(f"**Subject:** {ticket['subject']}")
        st.write(f"**Body:** {ticket['body']}")
    
    with col2:
        st.write("**AI Classification Results:**")
        
        # Topic Tags (as per requirements)
        st.write("**Topic Tags:**")
        if isinstance(ticket['topic_tags'], list):
            for tag in ticket['topic_tags']:
                st.markdown(f"• `{tag}`")
        else:
            st.markdown(f"• `{ticket['topic_tags']}`")
        
        # Sentiment (as per requirements)
        sentiment_emoji = {
            'Frustrated': '😤',
            'Angry': '😠', 
            'Curious': '🤔',
            'Neutral': '😐'
        }
        st.write(f"**Sentiment:** {sentiment_emoji.get(ticket['sentiment'], '😐')} {ticket['sentiment']}")
        
        # Priority (as per requirements)
        priority_color = {
            'P0 (High)': '🔴',
            'P1 (Medium)': '🟡',
            'P2 (Low)': '🟢'
        }
        st.write(f"**Priority:** {priority_color.get(ticket['priority'], '⚪')} {ticket['priority']}")
    
    # AI Reasoning if available
    if 'reasoning' in ticket and ticket['reasoning']:
        st.write(f"**AI Pipeline Reasoning:** {ticket['reasoning']}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

def main():
    # Header
    st.markdown('<h1 class="main-header">🎧 Atlan Customer Support Copilot</h1>', unsafe_allow_html=True)
    
    # Initialize systems
    with st.spinner("Initializing AI systems..."):
        classifier, rag_system = initialize_systems()
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    config = Config()
    
    # API Key status
    st.sidebar.subheader("API Status")
    if config.COHERE_API_KEY:
        st.sidebar.success("✅ Cohere API Key configured")
    else:
        st.sidebar.warning("⚠️ Cohere API Key missing")
    
    if not config.COHERE_API_KEY:
        st.sidebar.error("❌ Cohere API Key missing - using fallback classification")
    
    # Main tabs
    tab1, tab2 = st.tabs(["📊 Bulk Ticket Classification", "🤖 Interactive AI Agent"])
    
    with tab1:
        st.header("Bulk Ticket Classification Dashboard")
        
        # Load and automatically classify tickets on app load
        sample_tickets = load_sample_tickets()
        
        if sample_tickets:
            # Auto-classify tickets on first load
            if 'classified_tickets' not in st.session_state:
                with st.spinner("Ingesting and classifying tickets from sample_tickets file..."):
                    classified_tickets = []
                    for ticket in sample_tickets:
                        classification = classifier.classify_ticket(ticket['subject'], ticket['body'])
                        classified_ticket = {**ticket, **classification}
                        classified_tickets.append(classified_ticket)
                    st.session_state.classified_tickets = classified_tickets
            
            # Manual re-classification options
            with st.expander("🔄 Re-classify Options"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔄 Re-classify with AI", type="primary"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        def update_progress(current, total):
                            progress = current / total
                            progress_bar.progress(progress)
                            status_text.text(f"Classifying ticket {current}/{total}...")
                        
                        with st.spinner("Re-classifying with AI..."):
                            classified_tickets = classifier.classify_bulk_tickets(sample_tickets, update_progress)
                            st.session_state.classified_tickets = classified_tickets
                        
                        progress_bar.empty()
                        status_text.empty()
                
                with col2:
                    if st.button("⚡ Quick Re-classify", type="secondary"):
                        with st.spinner("Quick re-classification..."):
                            classified_tickets = []
                            for ticket in sample_tickets:
                                classification = classifier._fallback_classification(ticket['subject'], ticket['body'])
                                classified_ticket = {**ticket, **classification}
                                classified_tickets.append(classified_ticket)
                            st.session_state.classified_tickets = classified_tickets
            
            # Display results
            if 'classified_tickets' in st.session_state:
                classified_tickets = st.session_state.classified_tickets
                
                st.success(f"✅ Classified {len(classified_tickets)} tickets successfully!")
                
                # Display metrics and charts
                display_classification_metrics(classified_tickets)
                
                # Detailed ticket view
                st.subheader("📋 Detailed Ticket Classifications")
                
                # Filter options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    priority_filter = st.selectbox(
                        "Filter by Priority",
                        ["All"] + config.PRIORITY_LABELS
                    )
                
                with col2:
                    sentiment_filter = st.selectbox(
                        "Filter by Sentiment",
                        ["All"] + config.SENTIMENT_LABELS
                    )
                
                with col3:
                    topic_filter = st.selectbox(
                        "Filter by Topic",
                        ["All"] + config.TOPIC_TAGS
                    )
                
                # Apply filters
                filtered_tickets = classified_tickets.copy()
                
                if priority_filter != "All":
                    filtered_tickets = [t for t in filtered_tickets if t['priority'] == priority_filter]
                
                if sentiment_filter != "All":
                    filtered_tickets = [t for t in filtered_tickets if t['sentiment'] == sentiment_filter]
                
                if topic_filter != "All":
                    filtered_tickets = [t for t in filtered_tickets if topic_filter in t['topic_tags']]
                
                st.write(f"Showing {len(filtered_tickets)} tickets")
                
                # Display filtered tickets
                for ticket in filtered_tickets:
                    display_ticket_details(ticket)
        else:
            st.error("No sample tickets found. Please check the sample_tickets.json file.")
    
    with tab2:
        st.header("Interactive AI Agent")
        st.write("Submit a new customer support query to see AI classification and response.")
        
        # Input form
        with st.form("ticket_form", clear_on_submit=False):
            subject = st.text_input("Ticket Subject", placeholder="Enter the ticket subject...")
            body = st.text_area("Ticket Body", height=150, placeholder="Describe the issue or question...")
            submitted = st.form_submit_button("🚀 Analyze Ticket", type="primary")
        
        if submitted and subject and body:
            # Store the form data to prevent loss after submission
            st.session_state.current_subject = subject
            st.session_state.current_body = body
            # Classification
            with st.spinner("Analyzing ticket..."):
                classification = classifier.classify_ticket(subject, body)
            
            st.subheader("🔍 Internal Analysis (Backend View)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="classification-result">', unsafe_allow_html=True)
                st.write("**Classification Results:**")
                st.write(f"**Topics:** {', '.join(classification['topic_tags'])}")
                st.write(f"**Sentiment:** {classification['sentiment']}")
                st.write(f"**Priority:** {classification['priority']}")
                if 'reasoning' in classification:
                    st.write(f"**Reasoning:** {classification['reasoning']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Determine response type based on exact requirements
                rag_topics = ["How-to", "Product", "Best practices", "API/SDK", "SSO"]
                needs_rag = any(topic in classification['topic_tags'] for topic in rag_topics)
                
                if needs_rag:
                    st.write("**Response Type:** RAG-based answer")
                    st.write("**Knowledge Base:** Atlan Documentation")
                else:
                    st.write("**Response Type:** Classification and routing")
                    st.write("**Action:** Route to appropriate team")
            
            st.subheader("💬 Final Response (Frontend View)")
            
            if needs_rag:
                # Generate RAG response
                with st.spinner("Generating response from knowledge base..."):
                    query = f"{subject} {body}"
                    rag_response = rag_system.generate_rag_response(query)
                
                st.markdown('<div class="rag-response">', unsafe_allow_html=True)
                st.write("**AI Response:**")
                st.write(rag_response['answer'])
                
                if rag_response['sources']:
                    st.write("**Sources (URLs used to create this answer):**")
                    st.info("💡 **Note:** Due to Atlan's documentation structure, nested links may not work directly. Click the root link (https://docs.atlan.com) and navigate to the specific sections mentioned in the response.")
                    for i, source in enumerate(rag_response['sources'], 1):
                        st.markdown(f'<div class="source-link">{i}. 📖 <a href="{source}" target="_blank">{source}</a></div>', unsafe_allow_html=True)
                
                st.write(f"**Confidence:** {rag_response['confidence']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                # Simple routing message
                primary_topic = classification['topic_tags'][0] if classification['topic_tags'] else "General"
                
                st.markdown('<div class="rag-response">', unsafe_allow_html=True)
                st.write("**System Response:**")
                st.write(f"This ticket has been classified as a '{primary_topic}' issue and routed to the appropriate team.")
                st.write("Our specialists will review your request and respond within the standard SLA timeframe.")
                
                if classification['priority'] == 'P0 (High)':
                    st.write("⚡ **High Priority:** This ticket has been escalated for immediate attention.")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit, Cohere, and ChromaDB")

if __name__ == "__main__":
    main()
