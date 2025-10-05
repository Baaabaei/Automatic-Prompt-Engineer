import streamlit as st 
import time
from datetime import datetime 
from typing import Dict, List, Tuple, Optional 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
import os

from blog_data import blog_posts, privacy_policy, terms_of_service

# Email configuration (add after imports)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change based on your email provider
    'smtp_port': 587,
    'sender_email': 'prompt.engineer.mail@gmail.com',   
    'sender_password': 'prompt engineer_C137',  
    'receiver_email': 'inv.alirezababazadehzarei@gmail.com'
}
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
        # self.rag_system = SimpleRAGSystem()   
    
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
    
    def _init_openai(self):
        """Initialize the Gemini API""" 
        api_key = os.getenv('GEMINI_API_KEY') or st.secrets.get("GEMINI_API_KEY", None)
        
        if not api_key:
            st.warning("⚠️ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
            return None
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')   
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
        # try:
        with open('Desktop/prompt_engineer/assets/styl.css') as f: #==========================> must be changeable
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        # except FileNotFoundError:
        #     st.warning("CSS file not found. Using default styling.")
    
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
            (":material/feedback: Feedback", "feedback"),
            # (":material/security: Privacy Policy", "privacy")  
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
            (":material/web: Blog", "blog"),
            (":material/feedback: Feedback", "feedback")  
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

    def render_footer(self):
        """Render footer with privacy policy link"""
        st.markdown("---")
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0; color: #666;">
            <p>© 2025 Prompt Engineer. All rights reserved.</p>
            <p style="margin-top: 10px;">
                <a href="?page=privacy" style="color: #666; text-decoration: none; margin: 0 15px; cursor: pointer; transition: color 0.3s;" onmouseover="this.style.color='#333'" onmouseout="this.style.color='#666'">Privacy Policy</a> • 
                <a href="?page=terms" style="color: #666; text-decoration: none; margin: 0 15px; cursor: pointer; transition: color 0.3s;" onmouseover="this.style.color='#333'" onmouseout="this.style.color='#666'">Terms of Service</a> • 
                <a href="?page=feedback" style="color: #666; text-decoration: none; margin: 0 15px; cursor: pointer; transition: color 0.3s;" onmouseover="this.style.color='#333'" onmouseout="this.style.color='#666'">Contact</a> • 
                <a href="mailto:inv.alirezababazadehzarei@gmail.com" style="color: #666; text-decoration: none; margin: 0 15px;">Email Us</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
         
    
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

        user_old_prompt = self._render_old_user_prompt()
        
        settings = self._render_more_settings()
        
        if user_old_prompt:
            formatted_old_prompt = goal + "I already have a prompt, please improve it for me, my Current prompt is: \n" + user_old_prompt 
            self._render_prompt_preview_and_actions(formatted_old_prompt, context, settings)
        else:
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
    def _render_old_user_prompt(self) -> str:
        """Ask user for their current prompt to improve"""
        if st.checkbox("Already have a prompt?",help= "if you already have a prompt, you can add it here to improve "):
            return st.text_area(
                "Import your current prompt to improve",
                placeholder="Your current prompt",
                height=100,
                key = "old_user_prompt"
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


            domain = st.selectbox(
                ":material/domain: Domain",
                ["Customer Support", "Healthcare", "Education", 
                 "Legal", "Finance", "Content Creation", "E-commerce", "Travel and Hospitality", "Custom..."],
                key="domain_select"
            )
            if domain == "Custom...":
                domain = st.text_input("Custom persona", placeholder="Act as a...")
            

            output_format = st.selectbox(
                ":material/code: Output Format",
                ["Plain Text", "JSON", "Markdown", "Code Block", "XML", "CSV"],
                key="format_select"
            )

        
        with col_b:
            tone = st.selectbox(
                ":material/mood: Tone",
                ["Professional", "Friendly", "Technical", "Casual", "Formal"],
                key="tone_select"
            )

            LLM = st.selectbox(
                ":material/graph_5: LLM",
                ["Chat_GPT", "Gemini", "Claude", "Deep Seek", "Grok", "Llama"],
                key="model_select"
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
                if st.button(":material/psychology: Generate Prompt with AI", use_container_width=True, type= "primary"):
                    self._generate_prompt_with_ai(goal, context, settings)
            
            # Show generated prompt if it exists
            if 'generated_prompt' in st.session_state and st.session_state.generated_prompt:
                st.markdown("### :material/preview: Generated Prompt")
                st.code(st.session_state.generated_prompt, language="text", height= 500, width="stretch")
                
                with col_save:
                    if st.button(":material/save: Save Generated Prompt", use_container_width=True):
                        self._save_prompt(goal, st.session_state.generated_prompt, settings)
                
                if st.button(":material/manufacturing: Improve prompt?"): #===============================>> COLOR = GREEN / CONTINUE THE LOGIC
                    st.write("please answer these 3 questions")
                      
    def render_terms_of_service(self):
        """Render the terms of service page"""
        st.markdown("""
        <div class="terms-header">
            <h1> Terms of Service</h1>
            <p>Last updated: August 30, 2025</p>
        </div>
        """, unsafe_allow_html=True) 
        st.markdown(terms_of_service)
    def _generate_prompt_with_ai(self, goal: str, context: str, settings: Dict):
        """Use Gemini to generate an optimized prompt based on user inputs"""
        if not self.client:
            st.error("Gemini API not configured. Please add your API key.")
            return
        
        meta_prompt = self._create_meta_prompt(goal, context, settings)
        
        system_instruction = "You are an expert prompt engineer. Your job is to create high-quality, effective prompts based on user requirements. Always return ONLY the final prompt without any explanations or metadata."
        
        full_prompt = f"{system_instruction}\n\n{meta_prompt}"
        
        with st.spinner("🚧 Your prompt is under construction 🚧"):
            try:
                response = self.client.generate_content(full_prompt)
                generated_prompt = response.text.strip()
                st.session_state.generated_prompt = generated_prompt
                st.success("✅ Your optimized prompt has been generated!")
                
            except Exception as e:
                st.error(f"Failed to generate prompt: {e}")
                st.info("💡 Model is unavailable or rate limit exceeded")
    
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
        
    def _send_feedback_email(self, name: str, email: str, feedback_type: str, message: str) -> bool:
        """Send feedback email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = EMAIL_CONFIG['receiver_email']
            msg['Subject'] = f"Prompt Engineer Feedback: {feedback_type}"
            
            body = f"""
            New feedback received from Prompt Engineer App:
            
            Name: {name}
            Email: {email}
            Type: {feedback_type}
            
            Message:
            {message}
            
            Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                server.send_message(msg)
            
            return True
        except Exception as e:
            st.error(f"Failed to send feedback: {str(e)}")
            return False

    def render_feedback(self):
        """Render the feedback page"""
        st.markdown("""
        <div class="feedback-header">
            <h1>📧 Send Feedback</h1>
            <p>We'd love to hear from you! Share your thoughts, report bugs, or suggest features.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("feedback_form"):
                name = st.text_input("Name", placeholder="Your name")
                email = st.text_input("Email", placeholder="your.email@example.com")
                
                feedback_type = st.selectbox(
                    "Feedback Type",
                    ["Bug Report", "Feature Request", "General Feedback", "Question"]
                )
                
                message = st.text_area(
                    "Your Message",
                    placeholder="Tell us what's on your mind...",
                    height=200
                )
                
                submitted = st.form_submit_button("📤 Send Feedback", use_container_width=True)
                
                if submitted:
                    if not name or not email or not message:
                        st.error("Please fill in all required fields")
                    elif '@' not in email:
                        st.error("Please enter a valid email address")
                    else:
                        with st.spinner("Sending feedback..."):
                            if self._send_feedback_email(name, email, feedback_type, message):
                                st.success("✅ Thank you! Your feedback has been sent successfully.")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Failed to send feedback. Please try again later.")
    def render_workspace(self):
        """Render the saved prompts workspace"""
        st.markdown("""
        <div class="workspace-header">
            <h1> My Workspace</h1>
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
            <div class="empty-icon"></div>
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
        return blog_posts
        
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
        
        st.markdown(privacy_policy)

    def _handle_query_params(self):
        """Handle URL query parameters for navigation"""
        query_params = st.query_params
        if 'page' in query_params:  
            page = query_params['page']
            if page in ['home', 'login', 'studio', 'workspace', 'templates', 'blog', 'privacy', 'feedback', 'terms']:
                st.session_state.current_page = page
        
    def run(self):
        """Main application entry point"""
        try:
            self._load_css()
        except:
            pass
        
        self._handle_query_params()
        self.render_sidebar()
        
        # Route to appropriate page
        page_routes = {
            'home': self.render_homepage,
            'login': self.render_login,
            'studio': self.render_prompt_studio,
            'workspace': self.render_workspace,
            'templates': self.render_templates,
            'blog': self.render_blog,           
            'blog_post': self.render_blog_post, 
            'privacy': self.render_privacy_policy,   
            'terms':self.render_terms_of_service,
            'feedback': self.render_feedback
        }
        
        current_page = st.session_state.current_page
        if current_page in page_routes:
            page_routes[current_page]()
            self.render_footer()
        else:
            st.error(f"Unknown page: {current_page}")

def main():
    """Application entry point"""
    app = PromptEngineApp()
    app.run()

if __name__ == "__main__":
    main()
