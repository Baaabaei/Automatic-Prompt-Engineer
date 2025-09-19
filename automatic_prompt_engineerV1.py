import streamlit as st
import json
import time
from datetime import datetime
import uuid
from openai import OpenAI
from typing import Dict, List, Tuple, Optional
import os

# Configure the page
st.set_page_config(
    page_title="Prompt Engineer",
    page_icon="🛠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PromptEngineApp:
    """Main application class for Prompt Engineer"""
    
    def __init__(self):
        self.template_library = self._init_template_library()
        self.blog_posts = self._init_blog_posts()  # Add this line
        self.client = self._init_openai()
        self._init_session_state()
    
    def _init_template_library(self) -> Dict:
        """Initialize the template library"""
        return {
            "FAQ Bot for Documentation": {
                "description": "Perfect for creating bots that answer questions from your documentation",
                "goal": "Answer user questions based on provided documentation",
                "persona": "Helpful technical support specialist",
                "output_format": "Markdown",
                "tone": "Professional and helpful",
                "context_template": "Use this documentation to answer questions:\n\n{context}\n\nQuestion: {question}"
            },
            "Customer Service Triage Bot": {
                "description": "Routes customer inquiries to the right department",
                "goal": "Classify and route customer inquiries appropriately",
                "persona": "Professional customer service representative",
                "output_format": "JSON",
                "tone": "Friendly and efficient",
                "context_template": "Categories: {categories}\n\nCustomer message: {message}\n\nClassify this inquiry."
            },
            "Code Generation Helper": {
                "description": "Generates code snippets based on requirements",
                "goal": "Generate clean, functional code based on user specifications",
                "persona": "Senior software engineer",
                "output_format": "Code Block",
                "tone": "Technical and precise",
                "context_template": "Requirements: {requirements}\n\nGenerate {language} code that meets these specifications."
            },
            "JSON Data Extractor": {
                "description": "Extracts structured data from unstructured text",
                "goal": "Extract specific data points and format as JSON",
                "persona": "Data processing specialist",
                "output_format": "JSON",
                "tone": "Systematic and accurate",
                "context_template": "Extract the following data from this text: {fields}\n\nText: {input_text}"
            }
        }
    
    def _init_openai(self) -> OpenAI:
        """Initialize the OpenAI client for Ollama"""
        return OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama',
        )
    
    def _init_session_state(self):
        """Initialize session state variables"""
        defaults = {
            'logged_in': False,
            'saved_prompts': [],
            'current_page': 'home',
            'generated_prompt': ''  # Store AI-generated prompts
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def _load_css(self):
        """Load custom CSS styling"""
        try:
            with open('Desktop/prompt_engineer/assets/styl.css') as f: #==========================> must be changeable
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("CSS file not found. Using default styling.")
    
    def render_sidebar(self):
        """Render the sidebar navigation"""
        with st.sidebar:
            st.markdown(""":material/Build: Prompt Engineer """, unsafe_allow_html=True)
            st.logo("https://github.com/Baaabaei/Automatic-Prompt-Engineer/blob/main/logo.png")
            
            if not st.session_state.logged_in:
                self._render_public_nav()
            else:
                self._render_private_nav()
            
            # Footer
            st.markdown("---")
            st.markdown("""
            <div class="sidebar-footer">
                <small>Built for LLM Engineers<br>by LLM Engineers</small>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_public_nav(self):
        """Render navigation for non-logged in users"""
        nav_buttons = [
            (":material/home: Home", "home"),
            (":material/login: Sign In", "login"),
            (":material/web: Blog", "blog"),
            (":material/security: Privacy Policy", "privacy")  
        ]
        
        for label, page in nav_buttons:
            if st.button(label, key=f"nav_{page}", type="tertiary", use_container_width=False):
                st.session_state.current_page = page
                st.rerun()
        
    def _render_private_nav(self):
        """Render navigation for logged in users"""
        nav_buttons = [
            (":material/Construction: Prompt Engineer", "studio"),
            (":material/folder_open: My Workspace", "workspace"),
            (":material/library_books: Templates", "templates"),
            (":material/web: Blog", "blog")  
        ]
        
        for label, page in nav_buttons:
            if st.button(label, key=f"nav_{page}", type="tertiary", use_container_width=False):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        if st.button(":material/logout: Sign Out", type="tertiary", key="nav_logout"):
            st.session_state.logged_in = False
            st.session_state.current_page = 'home'
            st.rerun()
    
    def render_homepage(self):
        """Render the public homepage"""
        st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Make Most Efficient Prompts for Your Bots in Minutes</h1>
                <p class="hero-subtitle">Stop the trial-and-error. Stop getting inconsistent JSON. Transform your prompt engineering workflow with our visual studio.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Building for Free", key="cta_main", use_container_width=True):
                st.session_state.current_page = 'login'
                st.rerun()
        
        self._render_how_it_works()
        self._render_features_overview()
    
    def _render_how_it_works(self):
        """Render the how it works section"""
        st.markdown("---")
        st.markdown("""
        <div class="section-header">
            <h2>How It Works</h2>
            <p>Transform your prompt engineering workflow in three simple steps</p>
        </div>
        """, unsafe_allow_html=True)
        
        steps = [
            ( "1. Define Your Goal", "Start with a simple description of what you want your bot to accomplish"),
            ( "2. Refine with Tools", "Use our visual controls to set persona, format, tone, and task-specific parameters"),
            ( "3. Deploy & Test", "Get your optimized prompt and test it directly in our interface")
        ]
        
        cols = st.columns(3)
        for i, ( title, description) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon"></div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def _render_features_overview(self):
        """Render the features overview section"""
        st.markdown("---")
        st.markdown("""
        <div class="section-header">
            <h2>Built for LLM Engineers & Bot Developers</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **:material/build: Interactive Prompt Builder**
            
            Visual interface with structured inputs, live preview, and instant testing capabilities.
            
            **:material/library_books: Template Library**
            
            Expert-crafted templates for common bot-building tasks and use cases.
            
            **:material/folder: Workspace Organization**
            
            Save, organize, and reuse your prompts with folder management and version control.
            """)
        
        with col2:
            st.markdown("""
            **:material/settings_applications: Format Control**
            
            Ensure consistent JSON, Markdown, or custom format outputs every time.
            
            **:material/psychology: Persona Management**
            
            Fine-tune your bot's personality and expertise level with precision.
            
            **:material/speed: Live Testing**
            
            Test your prompts directly in the platform before deploying to production.
            """)
    
    def render_login(self):
        """Render the login/signup page"""
        st.markdown("""
        <div class="auth-container">
            <h2>Welcome to Prompt Engineer Studio</h2>
            <p>Sign in to access your prompt engineering workspace</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="engineer@company.com")
                password = st.text_input("Password", type="password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    login_btn = st.form_submit_button("Sign In", use_container_width=True)
                with col_b:
                    signup_btn = st.form_submit_button("Sign Up", use_container_width=True)
                
                if login_btn or signup_btn:
                    if email and password:
                        st.session_state.logged_in = True
                        st.session_state.current_page = 'studio'
                        # st.success("Welcome to Prompt Engineer Studio!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Please enter both email and password")
    
    def render_prompt_studio(self):
        """Main prompt engineering interface"""
        st.header(":material/construction: Prompt Engineer", divider=True)
        st.markdown("""
        <div class="studio-header">
            <p>Build and refine your prompts with precision</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the interface
        col1, col2 = st.columns([3, 2])
        
        with col1:
            goal = self._render_goal_input()
        
        with col2:
            context = self._render_context_input()

        settings = self._render_more_settings()

        self._render_prompt_preview_and_actions(goal, context, settings)
        
    def _render_goal_input(self) -> str:
        """Render the goal input section"""
        st.markdown("### :material/edit_note: Define Your Goal")
        return st.text_area(
            "Describe what you want the AI to do",
            placeholder="e.g., Create a bot that answers questions about our company's API documentation",
            height=100,
            key="goal_input"
        )
    
    def _render_more_settings(self) -> Dict:
        """Render the collapsible more settings section"""
        settings = {
            'persona': "Helpful assistant",
            'tone': "Professional",
            'output_format': "Plain Text",
            'data_extraction': False,
            'classification': False,
            'extraction_fields': "",
            'categories': ""
        }
        
        with st.expander(":material/settings_applications: More Settings", expanded=False):
            st.markdown("#### :material/tune: Refinement Controls")
            
            settings.update(self._render_refinement_controls())
            
            st.markdown("---")
            st.markdown("#### :material/extension: Task-Specific Modules")
            
            settings.update(self._render_task_modules())
        
        return settings
    
    def _render_refinement_controls(self) -> Dict:
        """Render refinement controls"""
        col_a, col_b = st.columns(2)
        
        with col_a:
            persona = st.selectbox(
                ":material/person: Persona",
                ["Helpful assistant", "Senior software engineer", "Customer support agent", 
                 "Technical writer", "Data analyst", "Custom..."],
                key="persona_select"
            )
            if persona == "Custom...":
                persona = st.text_input("Custom persona", placeholder="Act as a...")
        
        with col_b:
            tone = st.selectbox(
                ":material/mood: Tone",
                ["Professional", "Friendly", "Technical", "Casual", "Formal"],
                key="tone_select"
            )
        
        output_format = st.selectbox(
            ":material/code: Output Format",
            ["Plain Text", "JSON", "Markdown", "Code Block", "XML", "CSV"],
            key="format_select"
        )
        
        return {
            'persona': persona,
            'tone': tone,
            'output_format': output_format
        }
    
    def _render_task_modules(self) -> Dict:
        """Render task-specific modules"""
        col_x, col_y = st.columns(2)
        
        extraction_fields = ""
        categories = ""
        
        with col_x:
            data_extraction = st.checkbox(":material/data_object: Data Extraction", key="data_extraction")
            if data_extraction:
                extraction_fields = st.text_input("Fields to extract", placeholder="name, email, company, phone")
        
        with col_y:
            classification = st.checkbox(":material/category: Classification", key="classification")
            if classification:
                categories = st.text_input("Categories", placeholder="urgent, normal, low priority")
        
        return {
            'data_extraction': data_extraction,
            'classification': classification,
            'extraction_fields': extraction_fields,
            'categories': categories
        }
    
    def _render_context_input(self) -> str:
        """Render the context input section"""
        st.markdown("### :material/database: Context & Data")
        return st.text_area(
            "Paste relevant data, documentation, or examples",
            placeholder="Add your documentation, examples, or any context the bot should reference...",
            height=100,
            key="context_input"
        )
    
    def _render_prompt_preview_and_actions(self, goal: str, context: str, settings: Dict):
        """Render prompt generation and action buttons"""
        st.markdown("### :material/animated_images: AI Prompt Generation")
        
        if goal:
            col_generate, col_save = st.columns(2)
            
            with col_generate:
                if st.button(":material/psychology: Generate Prompt with AI", use_container_width=True):
                    self._generate_prompt_with_ai(goal, context, settings)
            
            # Show generated prompt if it exists
            if 'generated_prompt' in st.session_state and st.session_state.generated_prompt:
                st.markdown("### :material/preview: Generated Prompt")
                st.code(st.session_state.generated_prompt, language="text")
                
                with col_save:
                    if st.button(":material/save: Save Generated Prompt", use_container_width=True):
                        self._save_prompt(goal, st.session_state.generated_prompt, settings)
                
                if st.button(":material/manufacturing: Improve prompt?"): #===============================>> COLOR = GREEN / CONTINUE THE LOGIC
                    st.write("please answer these 3 questions")
                    
                
    def _generate_prompt_with_ai(self, goal: str, context: str, settings: Dict):
        """Use Ollama to generate an optimized prompt based on user inputs"""
        # Create a meta-prompt to generate the actual prompt
        meta_prompt = self._create_meta_prompt(goal, context, settings)
        
        with st.spinner("🚧 your prompt is under costruction 🚧"):
            try:
                response = self.client.chat.completions.create(
                    model="gemma3:1b",   
                    messages=[
                        {"role": "system", "content": "You are an expert prompt engineer. Your job is to create high-quality, effective prompts based on user requirements. Always return ONLY the final prompt without any explanations or metadata."},
                        {"role": "user", "content": meta_prompt}
                    ],
                    temperature=0.5  # Add some creativity to prompt generation
                )
                
                generated_prompt = response.choices[0].message.content.strip()
                st.session_state.generated_prompt = generated_prompt
                st.success(" your optimized prompt has been generated!")
                
            except Exception as e:
                st.error(f"Failed to generate prompt: {e}")
                st.info("  model is unavailable")
    
    def _create_meta_prompt(self, goal: str, context: str, settings: Dict) -> str:
        """Create a meta-prompt to instruct the AI on how to generate the user's prompt"""
        meta_prompt_parts = []
        
        meta_prompt_parts.append("Create a professional, effective prompt based on these requirements:")
        meta_prompt_parts.append(f"\nGOAL: {goal}")
        
        if context:
            meta_prompt_parts.append(f"\nCONTEXT TO INCLUDE: {context}")
        
        if settings['persona'] != "Helpful assistant":
            meta_prompt_parts.append(f"\nPERSONA: The AI should act as {settings['persona'].lower()}")
        
        if settings['tone'] != "Professional":
            meta_prompt_parts.append(f"\nTONE: Use a {settings['tone'].lower()} tone")
        
        if settings['output_format'] != "Plain Text":
            meta_prompt_parts.append(f"\nOUTPUT FORMAT: Response must be in {settings['output_format']} format")
        
        if settings['data_extraction'] and settings['extraction_fields']:
            meta_prompt_parts.append(f"\nDATA EXTRACTION: Must extract these fields: {settings['extraction_fields']}")
        
        if settings['classification'] and settings['categories']:
            meta_prompt_parts.append(f"\nCLASSIFICATION: Must classify into these categories: {settings['categories']}")
        
        meta_prompt_parts.append("\nCreate a clear, specific, and effective prompt that will reliably achieve the stated goal. Include all necessary instructions and constraints.")
        
        return "\n".join(meta_prompt_parts)
    
    
    def render_workspace(self):
        """Render the saved prompts workspace"""
        st.markdown("""
        <div class="workspace-header">
            <h1>:material/workspaces: My Workspace</h1>
            <p>Manage and organize your saved prompts</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.saved_prompts:
            self._render_empty_workspace()
        else:
            self._render_prompt_grid()
    
    def _render_empty_workspace(self):
        """Render empty workspace state"""
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">:material/folder_off:</div>
            <h3>No prompts saved yet</h3>
            <p>Create your first prompt in the Prompt Studio to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(":material/add: Create First Prompt"):
            st.session_state.current_page = 'studio'
            st.rerun()
    
    def _render_prompt_grid(self):
        """Render grid of saved prompts"""
        for i in range(0, len(st.session_state.saved_prompts), 2):
            col1, col2 = st.columns(2)
            
            for j, col in enumerate([col1, col2]):
                if i + j < len(st.session_state.saved_prompts):
                    prompt = st.session_state.saved_prompts[i + j]
                    
                    with col:
                        with st.container():
                            st.markdown(f"**{prompt['name']}**")
                            st.caption(f"Created: {prompt['created'][:10]} | Format: {prompt['format']}")
                            
                            if st.button(f":material/edit: Edit", key=f"edit_{prompt['id']}"):
                                st.info("Edit functionality would load this prompt in the studio")
                            
                            if st.button(f":material/delete: Delete", key=f"delete_{prompt['id']}"):
                                st.session_state.saved_prompts = [p for p in st.session_state.saved_prompts if p['id'] != prompt['id']]
                                st.rerun()
                            
                            with st.expander("Preview"):
                                preview_text = prompt['prompt'][:200] + "..." if len(prompt['prompt']) > 200 else prompt['prompt']
                                st.code(preview_text)
    
    def render_templates(self):
        """Render the template library"""
        st.markdown("""
        <div class="templates-header">
            <h1>:material/library_books: Template Library</h1>
            <p>Expert-crafted templates to jumpstart your prompt engineering</p>
        </div>
        """, unsafe_allow_html=True)
        
        templates = list(self.template_library.items())
        for i in range(0, len(templates), 2):
            col1, col2 = st.columns(2)
            
            for j, col in enumerate([col1, col2]):
                if i + j < len(templates):
                    name, template = templates[i + j]
                    
                    with col:
                        st.markdown(f"""
                        <div class="template-card">
                            <h3>{name}</h3>
                                <p>{template['description']}</p>
                                <div class="template-tags">
                                    <span class="tag">{template['output_format']}</span>
                                    <span class="tag">{template['tone']}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            #==================watch out the indentation bro
                        if st.button(f":material/play_arrow: Use Template", key=f"template_{i+j}"):
                            st.session_state.current_page = 'studio'
                            st.info(f"Loading {name} template...")
                            st.rerun()
        
        
    def _init_blog_posts(self) -> List[Dict]:
        """Initialize blog posts data"""
        return [
            {
                "id": "prompt-engineering-best-practices",
                "title": "Prompt Engineering Best Practices for Production Systems",
                "author": "Babaei",
                "date": "2025-08-25",
                "category": "Best Practices",
                "excerpt": "Learn the essential techniques for creating robust, reliable prompts that work consistently in production environments.",
                "content": """
    # Prompt Engineering Best Practices for Production Systems

    When building AI-powered applications, the quality of your prompts directly impacts the reliability and effectiveness of your system. Here are the key principles we've learned from deploying hundreds of production prompts.

    ## 1. Be Specific and Clear

    Vague prompts lead to inconsistent outputs. Instead of "analyze this data," specify exactly what type of analysis you want:
    - What metrics should be calculated?
    - What format should the output take?
    - What edge cases should be handled?

    ## 2. Include Examples

    Few-shot learning dramatically improves prompt performance. Always include 2-3 examples of the desired input-output pairs.

    ## 3. Handle Edge Cases

    Production systems encounter unexpected inputs. Your prompts should explicitly handle:
    - Empty or malformed data
    - Ambiguous requests
    - Out-of-scope queries

    ## 4. Test Thoroughly

    Before deploying, test your prompts with:
    - Typical use cases
    - Edge cases
    - Adversarial inputs
    - Different input lengths

    Remember: A well-engineered prompt is the foundation of a reliable AI system.
                """
            },
            {
                "id": "json-output-reliability",
                "title": "Ensuring Reliable JSON Output from Language Models",
                "author": "Babaei",
                "date": "2025-08-20",
                "category": "Technical Guide",
                "excerpt": "Stop dealing with malformed JSON responses. Learn proven techniques to get consistent, parseable JSON every time.",
                "content": """
    # Ensuring Reliable JSON Output from Language Models

    One of the biggest challenges in production LLM systems is getting consistent, well-formed JSON output. Here's how to solve this problem.

    ## The Problem

    Language models sometimes return:
    - Malformed JSON with syntax errors
    - Extra text before or after the JSON
    - Inconsistent field names or structures
    - Missing required fields

    ## Solution 1: Explicit Format Instructions

    Always specify the exact JSON structure you want:

    ```
    Return your response as valid JSON with this exact structure:
    {
    "category": "string",
    "confidence": "number between 0 and 1",
    "explanation": "string"
    }

    Do not include any text before or after the JSON.
    ```

    ## Solution 2: Use Schema Definitions

    Define your expected schema clearly:

    ```
    Required fields:
    - "name" (string): Full name
    - "email" (string): Email address
    - "priority" (string): One of "high", "medium", "low"

    Optional fields:
    - "notes" (string): Additional comments
    ```

    ## Solution 3: Validation Prompts

    Include validation instructions:

    ```
    Before responding, verify that your JSON:
    1. Has valid syntax
    2. Includes all required fields
    3. Uses correct data types
    4. Contains no extra text
    ```

    These techniques have reduced our JSON parsing errors by over 95% in production.
                """
            },
            {
                "id": "chatbot-personality-design",
                "title": "Designing Consistent Chatbot Personalities",
                "author": "Babaei", 
                "date": "2025-08-15",
                "category": "UX Design",
                "excerpt": "Create chatbots with distinctive, consistent personalities that users love to interact with.",
                "content": """
    # Designing Consistent Chatbot Personalities

    Your chatbot's personality is crucial for user engagement and brand consistency. Here's how to design and maintain a compelling bot personality.

    ## Define Core Traits

    Start with 3-5 core personality traits:
    - Professional but approachable
    - Knowledgeable without being condescending  
    - Patient and helpful
    - Slightly humorous when appropriate
    - Proactive in offering assistance

    ## Create a Personality Document

    Document specific behaviors:
    - How does your bot greet users?
    - What tone does it use for different situations?
    - How does it handle errors or confusion?
    - What phrases or expressions are characteristic?

    ## Consistency Techniques

    Use these prompt engineering techniques for consistency:

    ### 1. Role Definition
    ```
    You are Alex, a friendly technical support specialist with 5 years of experience. 
    You're patient, thorough, and enjoy helping people solve complex problems.
    ```

    ### 2. Behavioral Guidelines
    ```
    Communication style:
    - Use casual but professional language
    - Ask clarifying questions when needed
    - Acknowledge user frustration empathetically
    - Celebrate successful solutions
    ```

    ### 3. Response Templates
    Create templates for common scenarios to maintain consistency across interactions.

    ## Testing Personality Consistency

    Regular testing ensures your bot maintains its personality:
    - Test with different user moods (frustrated, excited, confused)
    - Verify responses across various topics
    - Check for personality drift over long conversations

    A well-designed personality makes your chatbot memorable and trustworthy.
                """
            }
        ]

        
    def render_blog(self):
        """Render the blog page"""
        st.markdown("""
        <div class="blog-header">
            <h1>  Prompt Engineering Blog</h1>
            <p>Expert insights, tutorials, and best practices for LLM engineering</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Blog post grid
        for post in self.blog_posts:
            with st.container():
                st.markdown(f"""
                <div class="blog-post-card">
                    <div class="blog-post-meta">
                        <span class="blog-category">{post['category']}</span>
                        <span class="blog-date">{post['date']}</span>
                    </div>
                    <h2>{post['title']}</h2>
                    <p class="blog-author">By {post['author']}</p>
                    <p class="blog-excerpt">{post['excerpt']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button(f"Read More", key=f"read_{post['id']}"):
                        st.session_state.current_blog_post = post['id']
                        st.session_state.current_page = 'blog_post'
                        st.rerun()
                
                st.markdown("---")

    
    def render_blog_post(self):
        """Render individual blog post"""
        if 'current_blog_post' not in st.session_state:
            st.session_state.current_page = 'blog'
            st.rerun()
            return
        
        post_id = st.session_state.current_blog_post
        post = next((p for p in self.blog_posts if p['id'] == post_id), None)
        
        if not post:
            st.error("Blog post not found")
            return
        
        # Back button
        if st.button(":material/arrow_back: Back to Blog"):
            st.session_state.current_page = 'blog'
            st.rerun()
        
        # Post header
        st.markdown(f"""
        <div class="blog-post-header">
            <span class="blog-category">{post['category']}</span>
            <h1>{post['title']}</h1>
            <div class="blog-post-meta">
                <span>By {post['author']}</span> • <span>{post['date']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Post content
        st.markdown(post['content'])

    def render_privacy_policy(self):
        """Render the privacy policy page"""
        st.markdown("""
        <div class="privacy-header">
            <h1> Privacy Policy</h1>
            <p>Last updated: August 30, 2025</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ## Information We Collect
        
        **Account Information**: When you create an account, we collect your email address and any profile information you provide.
        
        **Usage Data**: We collect information about how you use our service, including prompts created, templates used, and feature interactions.
        
        **Technical Data**: We automatically collect IP addresses, browser information, and device identifiers for security and performance purposes.
        
        ## How We Use Your Information
        
        - **Service Provision**: To provide and improve our prompt engineering tools
        - **Account Management**: To manage your account and provide customer support
        - **Analytics**: To understand usage patterns and improve our service
        - **Security**: To protect against fraud and unauthorized access
        
        ## Data Storage and Security
        
        **Local Processing**: Your prompts and data are processed locally when possible. We use industry-standard encryption for data transmission and storage.
        
        **Third-Party Services**: We may use third-party services (like OpenAI/Ollama) for AI processing. These services have their own privacy policies.
        
        **Retention**: We retain your data for as long as your account is active, plus a reasonable period for backup purposes.
        
        ## Your Rights
        
        You have the right to:
        - Access your personal data
        - Correct inaccurate information 
        - Export your prompts and workspace data
        
        ## Cookies and Tracking
        
        We do not use tracking cookies for advertising purposes.
        
        ## Changes to This Policy
        
        We may update this privacy policy from time to time. We will notify users of significant changes via email or in-app notifications.
        
        ## Contact Us
        
        If you have questions about this privacy policy, please contact us at inv.alirezababazadehzarei@gmail.com
        
        
        """)

    
    def run(self):
        """Main application entry point"""
        try:
            self._load_css()
        except:
            pass
            
        self.render_sidebar()
        
        # Route to appropriate page
        page_routes = {
            'home': self.render_homepage,
            'login': self.render_login,
            'studio': self.render_prompt_studio,
            'workspace': self.render_workspace,
            'templates': self.render_templates,
            'blog': self.render_blog,           # Add this line
            'blog_post': self.render_blog_post, # Add this line
            'privacy': self.render_privacy_policy  # Add this line
        }
        
        current_page = st.session_state.current_page
        if current_page in page_routes:
            page_routes[current_page]()
        else:
            st.error(f"Unknown page: {current_page}")

def main():
    """Application entry point"""
    app = PromptEngineApp()
    app.run()

if __name__ == "__main__":
    main()
