import cohere
import google.generativeai as genai
import json
import re
import time
from typing import Dict, List, Optional
from config import Config

class TicketClassifier:
    def __init__(self):
        self.config = Config()
        self.cohere_client = None
        self.last_api_call_time = 0
        self.min_delay_between_calls = 6  # 6 seconds for 10 calls/min limit
   
        
        # Initialize clients based on configuration
        if self.config.USE_COHERE and self.config.COHERE_API_KEY:
            try:
                self.cohere_client = cohere.Client(self.config.COHERE_API_KEY)
            except Exception as e:
                print(f"Failed to initialize Cohere client: {e}")
    
    def _wait_for_rate_limit(self):
        """Ensure we respect the API rate limit (10 calls/min for trial keys)."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call_time
        
        if time_since_last_call < self.min_delay_between_calls:
            wait_time = self.min_delay_between_calls - time_since_last_call
            print(f"Rate limiting: waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
        
        self.last_api_call_time = time.time()
        
       
    
    def _create_classification_prompt(self, subject: str, body: str) -> str:
        """Create a detailed prompt for ticket classification."""
        return f"""
Analyze the following customer support ticket and classify it according to these categories:

**TOPIC TAGS** (select one or more from): {', '.join(self.config.TOPIC_TAGS)}
- How-to: Questions about using features or functionality
- Product: General product questions, feature requests
- Connector: Issues with data source connections (Snowflake, dbt, etc.)
- Lineage: Data lineage tracking, mapping, visualization
- API/SDK: Programming interfaces, automation, integrations
- SSO: Single Sign-On, authentication issues
- Glossary: Business terms, metadata management
- Best practices: Guidance on optimal usage patterns
- Sensitive data: PII, data privacy, security concerns

**SENTIMENT** (select one): {', '.join(self.config.SENTIMENT_LABELS)}
- Frustrated: User is blocked or facing repeated issues
- Curious: User is exploring or learning
- Angry: User is upset about service/product
- Neutral: Matter-of-fact inquiry

**PRIORITY** (select one): {', '.join(self.config.PRIORITY_LABELS)}
- P0 (High): Urgent, business-critical, blocking workflows
- P1 (Medium): Important but not immediately blocking
- P2 (Low): Nice to have, general inquiries

**Ticket:**
Subject: {subject}
Body: {body}

Respond in JSON format:
{{
  "topic_tags": ["tag1", "tag2"],
  "sentiment": "sentiment_label",
  "priority": "priority_label",
  "reasoning": "Brief explanation of your classification"
}}
"""

    def _extract_json_from_response(self, response_text: str) -> Optional[Dict]:
        """Extract JSON from response text, handling various formats."""
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to find JSON within the text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            # Fallback: extract individual fields
            result = {}
            
            # Extract topic tags
            topic_match = re.search(r'"topic_tags":\s*\[(.*?)\]', response_text, re.DOTALL)
            if topic_match:
                tags = re.findall(r'"([^"]*)"', topic_match.group(1))
                result['topic_tags'] = tags
            
            # Extract sentiment
            sentiment_match = re.search(r'"sentiment":\s*"([^"]*)"', response_text)
            if sentiment_match:
                result['sentiment'] = sentiment_match.group(1)
            
            # Extract priority
            priority_match = re.search(r'"priority":\s*"([^"]*)"', response_text)
            if priority_match:
                result['priority'] = priority_match.group(1)
            
            # Extract reasoning
            reasoning_match = re.search(r'"reasoning":\s*"([^"]*)"', response_text)
            if reasoning_match:
                result['reasoning'] = reasoning_match.group(1)
            
            return result if result else None

    def classify_with_cohere(self, subject: str, body: str) -> Optional[Dict]:
        """Classify ticket using Cohere API."""
        if not self.cohere_client:
            return None
        
        try:
            prompt = self._create_classification_prompt(subject, body)
            self._wait_for_rate_limit()  # Respect API rate limit
            response = self.cohere_client.chat(
                model='command-r-plus-08-2024',
                message=prompt,
                max_tokens=500,
                temperature=0.1
            )
            
            return self._extract_json_from_response(response.text)
        except Exception as e:
            print(f"Error with Cohere classification: {e}")
            return None

    

    def classify_ticket(self, subject: str, body: str) -> Dict:
        """Classify a ticket using available AI models."""
        # Try Cohere first if enabled
        if self.config.USE_COHERE and self.cohere_client:
            result = self.classify_with_cohere(subject, body)
            if result:
                return result
        
       
        
        # Fallback classification if both AI models fail
        return self._fallback_classification(subject, body)

    def _fallback_classification(self, subject: str, body: str) -> Dict:
        """Provide fallback classification using keyword matching."""
        text = (subject + " " + body).lower()
        
        # Topic classification based on keywords
        topic_keywords = {
            "Connector": ["snowflake", "connection", "connector", "database", "source", "redshift", "bigquery"],
            "Lineage": ["lineage", "upstream", "downstream", "flow", "dependency", "dag"],
            "API/SDK": ["api", "sdk", "programmatic", "endpoint", "curl", "python", "rest"],
            "SSO": ["sso", "saml", "okta", "authentication", "login", "auth"],
            "Glossary": ["glossary", "term", "business", "metadata", "definition"],
            "How-to": ["how to", "tutorial", "guide", "help", "instructions"],
            "Sensitive data": ["pii", "sensitive", "privacy", "security", "compliance", "audit"],
            "Best practices": ["best practice", "recommendation", "advice", "guidance"]
        }
        
        detected_topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_topics.append(topic)
        
        if not detected_topics:
            detected_topics = ["Product"]
        
        # Sentiment analysis based on keywords
        sentiment = "Neutral"
        if any(word in text for word in ["urgent", "critical", "blocked", "asap", "emergency"]):
            sentiment = "Frustrated"
        elif any(word in text for word in ["angry", "infuriating", "upset", "terrible"]):
            sentiment = "Angry"
        elif any(word in text for word in ["new", "trying", "understand", "learn", "explore"]):
            sentiment = "Curious"
        
        # Priority based on urgency indicators
        priority = "P2 (Low)"
        if any(word in text for word in ["urgent", "critical", "asap", "emergency", "blocked"]):
            priority = "P0 (High)"
        elif any(word in text for word in ["important", "needed", "soon", "deadline"]):
            priority = "P1 (Medium)"
        
        return {
            "topic_tags": detected_topics,
            "sentiment": sentiment,
            "priority": priority,
            "reasoning": "Fallback classification using keyword matching"
        }

    def classify_bulk_tickets(self, tickets: List[Dict], progress_callback=None) -> List[Dict]:
        """Classify multiple tickets in bulk with progress tracking."""
        classified_tickets = []
        total_tickets = len(tickets)
        
        for i, ticket in enumerate(tickets):
            if progress_callback:
                progress_callback(i + 1, total_tickets)
            
            classification = self.classify_ticket(ticket['subject'], ticket['body'])
            classified_ticket = {
                **ticket,
                **classification
            }
            classified_tickets.append(classified_ticket)
        
        return classified_tickets
    
    def classify_batch_with_cohere(self, tickets: List[Dict]) -> List[Dict]:
        """Classify multiple tickets using Cohere in batch mode."""
        if not self.cohere_client:
            return [self._fallback_classification(t['subject'], t['body']) for t in tickets]
        
        try:
            # Create batch prompts
            batch_prompts = []
            for ticket in tickets:
                prompt = self._create_classification_prompt(ticket['subject'], ticket['body'])
                batch_prompts.append(prompt)
            
            # Process in smaller batches to avoid API limits
            batch_size = 5
            all_results = []
            
            for i in range(0, len(batch_prompts), batch_size):
                batch = batch_prompts[i:i + batch_size]
                batch_tickets = tickets[i:i + batch_size]
                
                # Process each prompt in the batch
                batch_results = []
                for j, prompt in enumerate(batch):
                    try:
                        self._wait_for_rate_limit()  # Respect API rate limit
                        response = self.cohere_client.chat(
                            model='command-r-plus-08-2024',
                            message=prompt,
                            max_tokens=300,
                            temperature=0.1
                        )
                        
                        result = self._extract_json_from_response(response.text)
                        if result:
                            batch_results.append(result)
                        else:
                            batch_results.append(self._fallback_classification(
                                batch_tickets[j]['subject'], 
                                batch_tickets[j]['body']
                            ))
                    except Exception as e:
                        print(f"Error classifying ticket {i+j}: {e}")
                        batch_results.append(self._fallback_classification(
                            batch_tickets[j]['subject'], 
                            batch_tickets[j]['body']
                        ))
                
                all_results.extend(batch_results)
            
            return all_results
            
        except Exception as e:
            print(f"Error in batch classification: {e}")
            return [self._fallback_classification(t['subject'], t['body']) for t in tickets]
