import streamlit as st
import json
import time
from datetime import datetime
import uuid

# Configure the page
st.set_page_config(
    page_title="Prompt Engineer",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('Desktop/prompt_engineer/assets/styl.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    st.warning("CSS file not found. Using default styling.")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'saved_prompts' not in st.session_state:
    st.session_state.saved_prompts = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sample prompt templates
TEMPLATE_LIBRARY = {
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

def render_homepage():
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
    
    st.markdown("---")
    
    # How it works section
    st.markdown("""
    <div class="section-header">
        <h2>How It Works</h2>
        <p>Transform your prompt engineering workflow in three simple steps</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">:material/edit:</div>
            <h3>1. Define Your Goal</h3>
            <p>Start with a simple description of what you want your bot to accomplish</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">:material/tune:</div>
            <h3>2. Refine with Tools</h3>
            <p>Use our visual controls to set persona, format, tone, and task-specific parameters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">:material/rocket_launch:</div>
            <h3>3. Deploy & Test</h3>
            <p>Get your optimized prompt and test it directly in our interface</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features overview
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

def render_login():
    """Simple login/signup page"""
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

def render_prompt_studio():
    """Main prompt engineering interface"""
    st.markdown("""
    <div class="studio-header">
        <h1>:material/construction: Prompt Engineer</h1>
        <p>Build and refine your prompts with precision</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for the interface
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### :material/edit_note: Define Your Goal")
        goal = st.text_area(
            "Describe what you want the AI to do",
            placeholder="e.g., Create a bot that answers questions about our company's API documentation",
            height=100,
            key="goal_input"
        )
        
        st.markdown("### :material/database: Context & Data")
        context = st.text_area(
            "Paste relevant data, documentation, or examples",
            placeholder="Add your documentation, examples, or any context the bot should reference...",
            height=150,
            key="context_input"
        )
        
        st.markdown("### :material/tune: Refinement Controls")
        
        # Persona setting
        col_a, col_b = st.columns(2)
        with col_a:
            persona = st.selectbox(
                ":material/person: Persona",
                ["Helpful assistant", "Senior software engineer", "Customer support agent", "Technical writer", "Data analyst", "Custom..."],
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
        
        # Output format
        output_format = st.selectbox(
            ":material/code: Output Format",
            ["Plain Text", "JSON", "Markdown", "Code Block", "XML", "CSV"],
            key="format_select"
        )
        
        # Task-specific modules
        st.markdown("### :material/extension: Task-Specific Modules")
        
        col_x, col_y = st.columns(2)
        with col_x:
            data_extraction = st.checkbox(":material/data_object: Data Extraction", key="data_extraction")
            if data_extraction:
                extraction_fields = st.text_input("Fields to extract", placeholder="name, email, company, phone")
        
        with col_y:
            classification = st.checkbox(":material/category: Classification", key="classification")
            if classification:
                categories = st.text_input("Categories", placeholder="urgent, normal, low priority")
    
    with col2:
        st.markdown("### :material/preview: Live Preview")
        
        # Generate the prompt based on inputs
        if goal:
            prompt_parts = []
            
            # Add persona
            if persona and persona != "Helpful assistant":
                prompt_parts.append(f"You are {persona.lower()}.")
            
            # Add main instruction
            prompt_parts.append(f"Your task: {goal}")
            
            # Add context if provided
            if context:
                prompt_parts.append(f"\nUse this context:\n{context}")
            
            # Add format instruction
            if output_format != "Plain Text":
                prompt_parts.append(f"\nProvide your response in {output_format} format.")
            
            # Add tone instruction
            if tone != "Professional":
                prompt_parts.append(f"Use a {tone.lower()} tone.")
            
            # Add task-specific instructions
            if data_extraction and 'extraction_fields' in locals():
                prompt_parts.append(f"\nExtract these specific fields: {extraction_fields}")
            
            if classification and 'categories' in locals():
                prompt_parts.append(f"\nClassify into one of these categories: {categories}")
            
            final_prompt = "\n\n".join(prompt_parts)
            
            st.code(final_prompt, language="text")
            
            # Action buttons
            col_save, col_test = st.columns(2)
            
            with col_save:
                if st.button(":material/save: Save Prompt", use_container_width=True):
                    prompt_data = {
                        'id': str(uuid.uuid4()),
                        'name': goal[:50] + "..." if len(goal) > 50 else goal,
                        'prompt': final_prompt,
                        'created': datetime.now().isoformat(),
                        'goal': goal,
                        'persona': persona,
                        'tone': tone,
                        'format': output_format
                    }
                    st.session_state.saved_prompts.append(prompt_data)
                    st.success("Prompt saved!")
            
            with col_test:
                if st.button(":material/play_arrow: Test Prompt", use_container_width=True):
                    with st.spinner("Testing prompt..."):
                        time.sleep(2)  # Simulate API call
                        st.success("Test completed!")
                        st.markdown("**Sample Output:**")
                        if output_format == "JSON":
                            st.json({"status": "success", "message": "This is a sample response"})
                        else:
                            st.write("This is a sample response from your prompt.")

def render_workspace():
    """Saved prompts workspace"""
    st.markdown("""
    <div class="workspace-header">
        <h1>:material/folder_open: My Workspace</h1>
        <p>Manage and organize your saved prompts</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.saved_prompts:
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
    else:
        # Display saved prompts in a grid
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
                                st.code(prompt['prompt'][:200] + "..." if len(prompt['prompt']) > 200 else prompt['prompt'])

def render_templates():
    """Template library"""
    st.markdown("""
    <div class="templates-header">
        <h1>:material/library_books: Template Library</h1>
        <p>Expert-crafted templates to jumpstart your prompt engineering</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display templates in a grid
    templates = list(TEMPLATE_LIBRARY.items())
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
                        # Pre-populate the studio with template data
                        st.session_state.current_page = 'studio'
                        # You would set session state variables here to pre-fill the form
                        st.info(f"Loading {name} template...")
                        st.rerun()

def main():
    """Main application logic"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(""":material/Build: Prompt Engineer """, unsafe_allow_html=True)
        st.logo("Desktop/prompt_engineer/images/logo.png")
        if not st.session_state.logged_in:
            # Public navigation
            if st.button(":material/home: Home", key="nav_home",type="tertiary", use_container_width=False):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.button(":material/login: Sign In", key="nav_login", type="tertiary", use_container_width=False):
                st.session_state.current_page = 'login'
                st.rerun()
            if st.button(":material/web: Blog", key="nav_blog", type="tertiary", use_container_width=False): #Defiiiiiiiiiiiine blog ++++++
                st.session_state.current_page = 'blog'
                st.rerun()
        else:
            # Private navigation
            if st.button(":material/Construction: Prompt Engineer", key="nav_studio",type="tertiary", use_container_width=False):
                st.session_state.current_page = 'studio'
                st.rerun()
            
            if st.button(":material/folder_open: My Workspace", key="nav_workspace",type="tertiary", use_container_width=False):
                st.session_state.current_page = 'workspace'
                st.rerun()
            
            if st.button(":material/library_books: Templates", key="nav_templates", type="tertiary", use_container_width=False):
                st.session_state.current_page = 'templates'
                st.rerun()
            
            st.markdown("---")
            
            if st.button(":material/logout: Sign Out", type="tertiary", key="nav_logout"):
                st.session_state.logged_in = False
                st.session_state.current_page = 'home'
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-footer">
            <small>Built for LLM Engineers<br>by LLM Engineers</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.current_page == 'home':
        render_homepage()
    elif st.session_state.current_page == 'login':
        render_login()
    elif st.session_state.current_page == 'studio':
        render_prompt_studio()
    elif st.session_state.current_page == 'workspace':
        render_workspace()
    elif st.session_state.current_page == 'templates':
        render_templates()

if __name__ == "__main__":
    main()
