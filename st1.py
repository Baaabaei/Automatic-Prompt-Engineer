import streamlit as st
import json
import time
from datetime import datetime
import uuid
from openai import OpenAI
from typing import Dict, List, Tuple, Optional

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
            'current_page': 'home'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def _load_css(self):
        """Load custom CSS styling"""
        try:
            with open('Desktop/prompt_engineer/assets/styl.css') as f:
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
            (":material/web: Blog", "blog")
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
            (":material/library_books: Templates", "templates")
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
                <h1 class="hero-title">Build Production-Ready Prompts for Your Bots in Minutes</h1>
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
            (":material/edit:", "1. Define Your Goal", "Start with a simple description of what you want your bot to accomplish"),
            (":material/tune:", "2. Refine with Tools", "Use our visual controls to set persona, format, tone, and task-specific parameters"),
            (":material/rocket_launch:", "3. Deploy & Test", "Get your optimized prompt and test it directly in our interface")
        ]
        
        cols = st.columns(3)
        for i, (icon, title, description) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
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
            **:material/settings: Format Control**
            
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
                        st.success("Welcome to Prompt Engineer Studio!")
                        time.sleep(1)
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
            settings = self._render_more_settings()
        
        with col2:
            context = self._render_context_input()
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
        
        with st.expander(":material/settings: More Settings", expanded=False):
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
        """Render prompt preview and action buttons"""
        st.markdown("### :material/preview: Live Preview")
        
        if goal:
            final_prompt = self._generate_prompt(goal, context, settings)
            st.code(final_prompt, language="text")
            
            col_save, col_test = st.columns(2)
            
            with col_save:
                if st.button(":material/save: Save Prompt", use_container_width=True):
                    self._save_prompt(goal, final_prompt, settings)
            
            with col_test:
                if st.button(":material/play_arrow: Test Prompt", use_container_width=True):
                    self._test_prompt(final_prompt, settings['output_format'])
    
    def _generate_prompt(self, goal: str, context: str, settings: Dict) -> str:
        """Generate the final prompt based on inputs"""
        prompt_parts = []
        
        # Add persona
        if settings['persona'] and settings['persona'] != "Helpful assistant":
            prompt_parts.append(f"You are {settings['persona'].lower()}.")
        
        # Add main instruction
        prompt_parts.append(f"Your task: {goal}")
        
        # Add context if provided
        if context:
            prompt_parts.append(f"\nUse this context:\n{context}")
        
        # Add format instruction
        if settings['output_format'] != "Plain Text":
            prompt_parts.append(f"\nProvide your response in {settings['output_format']} format.")
        
        # Add tone instruction
        if settings['tone'] != "Professional":
            prompt_parts.append(f"Use a {settings['tone'].lower()} tone.")
        
        # Add task-specific instructions
        if settings['data_extraction'] and settings['extraction_fields']:
            prompt_parts.append(f"\nExtract these specific fields: {settings['extraction_fields']}")
        
        if settings['classification'] and settings['categories']:
            prompt_parts.append(f"\nClassify into one of these categories: {settings['categories']}")
        
        return "\n\n".join(prompt_parts)
    
    def _save_prompt(self, goal: str, prompt: str, settings: Dict):
        """Save the prompt to session state"""
        prompt_data = {
            'id': str(uuid.uuid4()),
            'name': goal[:50] + "..." if len(goal) > 50 else goal,
            'prompt': prompt,
            'created': datetime.now().isoformat(),
            'goal': goal,
            'persona': settings['persona'],
            'tone': settings['tone'],
            'format': settings['output_format']
        }
        st.session_state.saved_prompts.append(prompt_data)
        st.success("Prompt saved!")
    
    def _test_prompt(self, prompt: str, output_format: str):
        """Test the prompt using Ollama"""
        if not prompt:
            st.warning("Please generate a prompt first.")
            return
        
        with st.spinner("Testing prompt..."):
            try:
                response = self.client.chat.completions.create(
                    model="gemma3:1b",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "Please generate a response based on the prompt."}
                    ]
                )
                st.success("Test completed!")
                st.markdown("**Sample Output:**")
                
                if output_format == "JSON":
                    try:
                        st.json(json.loads(response.choices[0].message.content))
                    except json.JSONDecodeError:
                        st.code(response.choices[0].message.content, language="text")
                else:
                    st.code(response.choices[0].message.content, language="markdown")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    def render_workspace(self):
        """Render the saved prompts workspace"""
        st.markdown("""
        <div class="workspace-header">
            <h1>:material/folder_open: My Workspace</h1>
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
                        
                        if st.button(f":material/play_arrow: Use Template", key=f"template_{i+j}"):
                            st.session_state.current_page = 'studio'
                            st.info(f"Loading {name} template...")
                            st.rerun()
    
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
