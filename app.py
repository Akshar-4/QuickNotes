import streamlit as st
import requests
import json
from datetime import datetime
import io
import random
import PyPDF2

st.set_page_config(
    page_title="Axinity QuickNotes",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)


API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.markdown("""
<style>
    /* Main container styling - COMPACT */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.4;
    }
    
    /* Input Method Buttons - CLEAN AND COMPACT */
    .input-method-buttons {
        display: flex;
        gap: 10px;
        margin-bottom: 1.5rem;
        justify-content: center;
    }
    
    .method-btn {
        padding: 12px 24px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid #667eea;
        background: white;
        color: #667eea;
        font-weight: 600;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
        white-space: nowrap;
    }
    
    .method-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .method-btn.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.2);
    }
    
    /* Text area styling - COMPACT */
    .stTextArea textarea {
        font-size: 14px;
        line-height: 1.5;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px;
        transition: all 0.2s;
        background: #fafafa;
        min-height: 150px;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
        background: white;
    }
    
    /* CLICKABLE Checkbox Card Styling - COMPACT */
    .clickable-card {
        display: flex;
        align-items: center;
        margin: 10px 0;
        padding: 15px;
        background: white;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.2s;
        cursor: pointer !important;
        user-select: none;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
        min-height: 80px;
    }
    
    .clickable-card:hover {
        border-color: #667eea;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    .clickable-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.15);
    }
    
    .card-icon {
        font-size: 1.5rem;
        margin-right: 15px;
        color: #667eea;
        min-width: 35px;
        text-align: center;
    }
    
    .card-content {
        flex: 1;
    }
    
    .card-content h4 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 3px;
    }
    
    .card-content p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
        line-height: 1.3;
    }
    
    .card-checkbox {
        margin-left: 10px;
        min-width: 20px;
        height: 20px;
        border: 2px solid #667eea;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .clickable-card.selected .card-checkbox {
        background: #667eea;
        color: white;
    }
    
    .clickable-card.selected .card-checkbox:after {
        content: "✓";
    }
    
    /* Quiz settings card - COMPACT */
    .settings-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 0.8rem 0;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
    }
    
    .settings-title {
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Button styling - COMPACT */
    .stButton > button {
        font-size: 16px;
        font-weight: 600;
        height: 2.8em;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.2s;
        width: 100%;
        cursor: pointer !important;
        padding: 0.5rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .secondary-btn > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    }
    
    .tertiary-btn > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    }
    
    /* Uploader styling - COMPACT */
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1.2rem;
        border: 2px dashed #667eea;
        text-align: center;
        margin: 0.8rem 0;
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .upload-section:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #eef2ff 0%, #e6e9ff 100%);
    }
    
    /* File info card - COMPACT */
    .file-info {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
    }
    
    .file-icon {
        font-size: 2rem;
    }
    
    .file-details {
        flex: 1;
    }
    
    .file-details h4 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.1rem;
    }
    
    .file-details p {
        margin: 3px 0 0 0;
        color: #666;
        font-size: 0.85rem;
    }
    
    /* Result card styling - COMPACT */
    .result-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 12px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        transition: all 0.2s;
        cursor: default;
    }
    
    .result-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    }
    
    .result-card h3 {
        color: #2c3e50;
        margin-top: 0;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
   
    .quiz-question {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 0.8rem 0;
        transition: all 0.2s;
    }
    
    .quiz-question.correct {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.05);
    }
    
    .quiz-question.incorrect {
        border-color: #ef4444;
        background: rgba(239, 68, 68, 0.05);
    }
    
    .quiz-option {
        display: flex;
        align-items: center;
        padding: 10px 12px;
        margin: 6px 0;
        background: #f8f9fa;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        cursor: pointer;
        transition: all 0.15s;
        font-size: 1rem;
    }
    
    .quiz-option:hover {
        background: #eef2ff;
        border-color: #667eea;
        transform: translateX(3px);
    }
    
    .quiz-option.selected {
        background: #e0e7ff;
        border-color: #667eea;
        font-weight: 600;
    }
    
    .quiz-option.correct-answer {
        background: #d1fae5;
        border-color: #10b981;
        color: #065f46;
    }
    
    .quiz-option.incorrect-answer {
        background: #fee2e2;
        border-color: #ef4444;
        color: #7f1d1d;
    }
    
    .option-letter {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: #667eea;
        color: white;
        border-radius: 50%;
        margin-right: 12px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .score-display {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #667eea;
    }
    
    .score-value {
        font-size: 3rem;
        font-weight: 800;
        color: #667eea;
        margin: 0;
    }
    
    .score-label {
        font-size: 1.2rem;
        color: #666;
        margin: 0.3rem 0 0 0;
        font-weight: 600;
    }
    
 
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 0.8rem 0;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #e7f3ff 0%, #d6e9ff 100%);
        color: #004085;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin: 0.8rem 0;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 0.8rem 0;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
   
    .text-stats {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.8rem 0;
        text-align: center;
    }
    
    .stat-item {
        display: inline-block;
        margin: 0 1rem;
        padding: 0.5rem 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 2px solid #e0e0e0;
        transition: all 0.2s;
    }
    
    .stat-item:hover {
        border-color: #667eea;
        transform: translateY(-1px);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 600;
    }
    

    .feature-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.06);
        text-align: center;
        border-top: 4px solid #667eea;
        transition: all 0.2s;
        cursor: default;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        color: #667eea;
    }
    
    /* Footer - COMPACT */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 2px solid #e0e0e0;
        color: #666;
        font-size: 0.85rem;
    }
    
    /* Compact form elements */
    .stSlider, .stSelectbox, .stMultiSelect {
        margin-bottom: 0.5rem !important;
    }
    
    /* Section headers */
    h2 {
        font-size: 1.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.5rem !important;
    }
    
  
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    

    .stColumn {
        padding: 0 5px !important;
    }
</style>
""", unsafe_allow_html=True)


if 'results' not in st.session_state:
    st.session_state.results = {
        'summary': '',
        'action_items': '',
        'quiz_questions': []
    }
if 'uploaded_text' not in st.session_state:
    st.session_state.uploaded_text = ''
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'text_source' not in st.session_state:
    st.session_state.text_source = 'manual'
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'show_interactive_quiz' not in st.session_state:
    st.session_state.show_interactive_quiz = False
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'paste'
if 'num_questions' not in st.session_state:
    st.session_state.num_questions = 5

if 'summary_selected' not in st.session_state:
    st.session_state.summary_selected = False
if 'action_selected' not in st.session_state:
    st.session_state.action_selected = True  # Default to selected
if 'quiz_selected' not in st.session_state:
    st.session_state.quiz_selected = False


st.markdown("""
<div class="main-header">
    <h1>📝 Axinity QuickNotes</h1>
    <p>Transform text and documents into actionable insights with AI-powered analysis</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class='info-box'>
    <h4 style="margin-top: 0;">🚀 Getting Started</h4>
    <ol style="margin-bottom: 0; padding-left: 1.2rem;">
        <li>Click <strong>Paste Text</strong> or <strong>Upload Document</strong> below</li>
        <li>Enter text or upload a document (.txt or .pdf)</li>
        <li>Click on analysis cards to select options</li>
        <li>Customize quiz settings if quiz is selected</li>
        <li>Click <strong>Start Analysis</strong> and explore results!</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 Choose Input Method")


col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        paste_active = st.session_state.active_tab == 'paste'
        if st.button(
            "📝 **Paste Text**",
            type="primary" if paste_active else "secondary",
            use_container_width=True,
            key="paste_btn"
        ):
            st.session_state.active_tab = 'paste'
            st.rerun()
    
    with btn_col2:
        upload_active = st.session_state.active_tab == 'upload'
        if st.button(
            "📁 **Upload Document**",
            type="primary" if upload_active else "secondary",
            use_container_width=True,
            key="upload_btn"
        ):
            st.session_state.active_tab = 'upload'
            st.rerun()


if st.session_state.active_tab == 'paste':
    text_input = st.text_area(
        "**Enter or paste your text here:**",
        height=180,
        placeholder="""Paste your meeting notes, articles, emails, or any text content here...""",
        help="Enter at least 50 characters for best results",
        key="manual_input"
    )
    
    if text_input.strip():
        st.session_state.text_source = 'manual'
        st.session_state.uploaded_text = text_input
        

        words = len(text_input.split())
        chars = len(text_input)
        
        st.markdown(f"""
        <div class="text-stats">
            <div class="stat-item">
                <div class="stat-value">{words}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{chars}</div>
                <div class="stat-label">Characters</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:  
    st.markdown("""
    <div class="upload-section" onclick="document.getElementById('file-uploader').click()">
        <h4 style="color: #667eea; margin: 0 0 5px 0;">📁 Upload Your Document</h4>
        <p style="font-size: 0.9rem; margin: 2px 0;"><strong>Supported:</strong> .txt files (always works)</p>
        <p style="font-size: 0.85rem; color: #666; margin: 2px 0;">Max file size: 10MB</p>
        <p style="font-size: 0.85rem; color: #667eea; margin-top: 8px; font-weight: 600;">
            Click here or drag & drop
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'pdf'],
        label_visibility="collapsed",
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        
        # Simple extraction function
        def extract_text_from_file(uploaded_file):
            file_type = uploaded_file.name.lower()
            try:
                if file_type.endswith('.txt'):
                    content = uploaded_file.read()
                    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
                    for encoding in encodings:
                        try:
                            text = content.decode(encoding)
                            return text, len(text.split()), len(text.split('\n'))
                        except:
                            continue
                    return content.decode('utf-8', errors='replace'), 0, 0
                elif file_type.endswith('.pdf'):
                    try:
                        import PyPDF2
                        uploaded_file.seek(0)
                        try:
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            text = ""
                            for page in pdf_reader.pages[:10]:  # Limit to 10 pages
                                try:
                                    text += page.extract_text() + "\n\n"
                                except:
                                    try:
                                        text += page.extractText() + "\n\n"
                                    except:
                                        continue
                            return text, len(text.split()), len(pdf_reader.pages)
                        except:
                            return "PDF reading error.", 0, 0
                    except ImportError:
                        return "PyPDF2 not installed.", 0, 0
                else:
                    return "Unsupported file type.", 0, 0
            except:
                return "Error reading file.", 0, 0
        
        # Show file info
        file_size = uploaded_file.size / 1024
        file_size_str = f"{file_size:.1f} KB" if file_size < 1024 else f"{file_size/1024:.1f} MB"
        
        st.markdown(f"""
        <div class="file-info">
            <div class="file-icon">
                📄
            </div>
            <div class="file-details">
                <h4>{uploaded_file.name}</h4>
                <p>Size: {file_size_str} • Type: {uploaded_file.name.split('.')[-1].upper()}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Extract text
        with st.spinner("📖 Reading document..."):
            extracted_text, word_count, item_count = extract_text_from_file(uploaded_file)
            
            if extracted_text.startswith("Error") or "not installed" in extracted_text or "scanned" in extracted_text:
                st.error(extracted_text)
            else:
                st.session_state.uploaded_text = extracted_text
                st.session_state.text_source = 'upload'
                
                st.markdown(f"""
                <div class="text-stats">
                    <div class="stat-item">
                        <div class="stat-value">{word_count}</div>
                        <div class="stat-label">Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{len(extracted_text)}</div>
                        <div class="stat-label">Characters</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"✅ Extracted {word_count} words")

# Beautiful CLICKABLE cards
st.markdown("---")
st.markdown("### 📋 Choose Analysis Options")

# Create columns for clickable cards
col1, col2, col3 = st.columns(3)

# JavaScript to handle card clicks
st.markdown("""
<script>
function toggleCard(cardId) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        key: cardId,
        value: true
    }, '*');
}
</script>
""", unsafe_allow_html=True)

# Summary Card
with col1:
    summary_checkbox = st.checkbox(
        "Enable Summary", 
        value=st.session_state.summary_selected,
        key="summary_card_cb",
        label_visibility="collapsed"
    )
    
    if summary_checkbox != st.session_state.summary_selected:
        st.session_state.summary_selected = summary_checkbox
        st.rerun()
    
    st.markdown(f"""
    <div class="clickable-card {'selected' if st.session_state.summary_selected else ''}" 
         onclick="toggleCard('summary_card_cb')">
        <div class="card-icon">📄</div>
        <div class="card-content">
            <h4>Smart Summary</h4>
            <p>Generate concise summary of key points</p>
        </div>
        <div class="card-checkbox"></div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    action_checkbox = st.checkbox(
        "Enable Action Items", 
        value=st.session_state.action_selected,
        key="action_card_cb",
        label_visibility="collapsed"
    )
    
    if action_checkbox != st.session_state.action_selected:
        st.session_state.action_selected = action_checkbox
        st.rerun()
    
    st.markdown(f"""
    <div class="clickable-card {'selected' if st.session_state.action_selected else ''}" 
         onclick="toggleCard('action_card_cb')">
        <div class="card-icon">✅</div>
        <div class="card-content">
            <h4>Action Items</h4>
            <p>Extract concrete tasks and to-dos</p>
        </div>
        <div class="card-checkbox"></div>
    </div>
    """, unsafe_allow_html=True)

# Interactive Quiz Card
with col3:
    quiz_checkbox = st.checkbox(
        "Enable Quiz", 
        value=st.session_state.quiz_selected,
        key="quiz_card_cb",
        label_visibility="collapsed"
    )
    
    if quiz_checkbox != st.session_state.quiz_selected:
        st.session_state.quiz_selected = quiz_checkbox
        st.rerun()
    
    st.markdown(f"""
    <div class="clickable-card {'selected' if st.session_state.quiz_selected else ''}" 
         onclick="toggleCard('quiz_card_cb')">
        <div class="card-icon">🎯</div>
        <div class="card-content">
            <h4>Interactive Quiz</h4>
            <p>Create and take knowledge test</p>
        </div>
        <div class="card-checkbox"></div>
    </div>
    """, unsafe_allow_html=True)


if st.session_state.quiz_selected:
    st.markdown("---")
    st.markdown("""
    <div class="settings-card">
        <div class="settings-title">
            <span>⚙️</span> Quiz Settings
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Number of questions based on text length
        text_length = len(st.session_state.uploaded_text) if st.session_state.uploaded_text else 0
        word_count = len(st.session_state.uploaded_text.split()) if st.session_state.uploaded_text else 0
        
        # Smart question count calculation
        if word_count < 100:
            default_questions = 3
            max_questions = 5
        elif word_count < 500:
            default_questions = 5
            max_questions = 10
        elif word_count < 2000:
            default_questions = 7
            max_questions = 15
        else:
            default_questions = 10
            max_questions = 20
        
        st.session_state.num_questions = st.slider(
            "**Number of Questions:**",
            min_value=3,
            max_value=min(max_questions, 20),
            value=default_questions,
            help=f"Based on your text ({word_count} words)"
        )
    
    with col2:
        # Question difficulty
        difficulty = st.select_slider(
            "**Difficulty Level:**",
            options=["Easy", "Medium", "Hard"],
            value="Medium",
            help="Adjust question complexity"
        )
        
        # Question types
        question_types = st.multiselect(
            "**Question Types:**",
            options=["Multiple Choice", "True/False", "Short Answer"],
            default=["Multiple Choice"],
            help="Select question formats"
        )

# Action buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 **Start Analysis**", type="primary", use_container_width=True):
        current_text = st.session_state.uploaded_text
        
        if not current_text or len(current_text.strip()) < 10:
            st.markdown("<div class='warning-box'>⚠️ Please enter text or upload a document first</div>", unsafe_allow_html=True)
        elif len(current_text.strip()) < 50:
            st.markdown("<div class='warning-box'>📝 Please provide more text (at least 50 characters)</div>", unsafe_allow_html=True)
        elif not (st.session_state.summary_selected or st.session_state.action_selected or st.session_state.quiz_selected):
            st.markdown("<div class='warning-box'>🔘 Please select at least one analysis option</div>", unsafe_allow_html=True)
        else:
            with st.spinner("🤖 AI is analyzing your content..."):
                # Function to call OpenRouter API
                def call_openrouter_api(prompt):
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                    }
                    
                    data = {
                        "model": "x-ai/grok-4.1-fast:free",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 2000,
                        "temperature": 0.3
                    }
                    
                    try:
                        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
                        if response.status_code == 200:
                            result = response.json()
                            if 'choices' in result and result['choices']:
                                return result['choices'][0]['message']['content']
                        return f"API Error {response.status_code}"
                    except Exception as e:
                        return f"Connection error: {str(e)}"
                
                # Process summary
                if st.session_state.summary_selected:
                    with st.status("📄 Generating summary...", expanded=False) as status:
                        text_to_process = current_text[:5000] if len(current_text) > 5000 else current_text
                        prompt = f"""Create a clear, concise summary of this text/document. Focus on main ideas, key decisions, important information.

Text: {text_to_process}

Provide a well-structured summary with bullet points:"""
                        st.session_state.results['summary'] = call_openrouter_api(prompt)
                        status.update(label="✅ Summary generated", state="complete")
                
                # Process action items
                if st.session_state.action_selected:
                    with st.status("✅ Extracting action items...", expanded=False) as status:
                        text_to_process = current_text[:5000] if len(current_text) > 5000 else current_text
                        prompt = f"""Extract ALL action items, tasks, assignments from this text/document. Format as a numbered list.

Text: {text_to_process}

Action Items (numbered list):"""
                        st.session_state.results['action_items'] = call_openrouter_api(prompt)
                        status.update(label="✅ Action items extracted", state="complete")
                
                # Process quiz
                if st.session_state.quiz_selected:
                    with st.status("🎯 Creating interactive quiz...", expanded=False) as status:
                        text_to_process = current_text[:8000] if len(current_text) > 8000 else current_text
                        num_questions = st.session_state.num_questions
                        
                        prompt = f"""Based on this text, create {num_questions} multiple choice quiz questions. For each question, provide:
1. The question
2. Four answer options (A, B, C, D)
3. The correct answer letter
4. A brief explanation

Format exactly like this:
Q1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [Letter]
Explanation: [Brief explanation]

[Repeat for Q2 through Q{num_questions}]

Text: {text_to_process}"""
                        quiz_result = call_openrouter_api(prompt)
                        
                        # Parse quiz questions
                        questions = []
                        lines = quiz_result.split('\n')
                        current_question = {}
                        
                        for line in lines:
                            line = line.strip()
                            if line.startswith('Q'):
                                if current_question:
                                    questions.append(current_question)
                                current_question = {
                                    'question': line[4:].strip(),
                                    'options': [],
                                    'correct_answer': '',
                                    'explanation': ''
                                }
                            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                                current_question['options'].append(line[3:].strip())
                            elif line.startswith('Correct Answer:'):
                                current_question['correct_answer'] = line[16:].strip()
                            elif line.startswith('Explanation:'):
                                current_question['explanation'] = line[13:].strip()
                        
                        if current_question:
                            questions.append(current_question)
                        
                        # Limit to requested number of questions
                        questions = questions[:num_questions]
                        
                        st.session_state.results['quiz_questions'] = questions
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.show_interactive_quiz = True
                        status.update(label=f"✅ Created {len(questions)} quiz questions", state="complete")
                
                st.markdown("<div class='success-box'>✨ Analysis complete! View results below</div>", unsafe_allow_html=True)

with col2:
    if st.button("💾 **Download Report**", type="secondary", use_container_width=True, key="download_btn"):
        if any(st.session_state.results.values()):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Axinity_QuickNotes_Report_{timestamp}.txt"
            
            content = "=" * 60 + "\n"
            content += "AXINITY QUICKNOTES - AI ANALYSIS REPORT\n"
            content += "=" * 60 + "\n\n"
            content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            if st.session_state.uploaded_file:
                content += f"Source: {st.session_state.uploaded_file.name}\n"
            else:
                content += "Source: Manual Text Input\n"
            
            content += f"Text Length: {len(st.session_state.uploaded_text)} characters\n\n"
            
            if st.session_state.results['summary']:
                content += "-" * 40 + "\n"
                content += "SUMMARY\n"
                content += "-" * 40 + "\n"
                content += st.session_state.results['summary'] + "\n\n"
            
            if st.session_state.results['action_items']:
                content += "-" * 40 + "\n"
                content += "ACTION ITEMS\n"
                content += "-" * 40 + "\n"
                content += st.session_state.results['action_items'] + "\n\n"
            
            if st.session_state.results['quiz_questions']:
                content += "-" * 40 + "\n"
                content += f"QUIZ QUESTIONS ({len(st.session_state.results['quiz_questions'])} questions)\n"
                content += "-" * 40 + "\n"
                for i, q in enumerate(st.session_state.results['quiz_questions'], 1):
                    content += f"Q{i}: {q.get('question', '')}\n"
                    for j, option in enumerate(q.get('options', [])):
                        content += f"  {chr(65+j)}) {option}\n"
                    content += f"Correct Answer: {q.get('correct_answer', '')}\n"
                    if q.get('explanation'):
                        content += f"Explanation: {q.get('explanation', '')}\n"
                    content += "\n"
            
            st.download_button(
                label="⬇️ Download Report",
                data=content,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
                key="download_report"
            )
        else:
            st.warning("No results to download yet. Run an analysis first.")

with col3:
    if st.button("🗑️ **Clear All**", type="secondary", use_container_width=True, key="clear_btn"):
        st.session_state.results = {'summary': '', 'action_items': '', 'quiz_questions': []}
        st.session_state.uploaded_text = ''
        st.session_state.uploaded_file = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.show_interactive_quiz = False
        # Reset analysis options
        st.session_state.summary_selected = False
        st.session_state.action_selected = True
        st.session_state.quiz_selected = False
        st.rerun()

# Display results
if any(st.session_state.results.values()):
    st.markdown("---")
    st.markdown("## 📊 **Analysis Results**")
    
    # Display summary and action items
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.results['summary']:
            st.markdown("""
            <div class="result-card">
                <h3>📄 Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.results['summary'])
    
    with col2:
        if st.session_state.results['action_items']:
            st.markdown("""
            <div class="result-card">
                <h3>✅ Action Items</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.results['action_items'])

# Interactive Quiz Section
if st.session_state.show_interactive_quiz and st.session_state.results['quiz_questions']:
    st.markdown("---")
    st.markdown("## 🎯 **Interactive Quiz**")
    
    questions = st.session_state.results['quiz_questions']
    num_questions = len(questions)
    
    st.markdown(f"### 📝 Quiz: {num_questions} Questions")
    
    if not st.session_state.quiz_submitted:
        # Display quiz questions
        for i, question in enumerate(questions):
            st.markdown(f"#### Question {i+1} of {num_questions}")
            st.markdown(f"**{question.get('question', '')}**")
            
            options = question.get('options', [])
            correct_answer = question.get('correct_answer', '').upper()
            
            # Create a key for this question
            answer_key = f"q{i}"
            
            # Display options as radio buttons
            if len(options) >= 4:
                selected_option = st.radio(
                    "Select your answer:",
                    options=[f"A) {options[0]}",
                            f"B) {options[1]}", 
                            f"C) {options[2]}",
                            f"D) {options[3]}"],
                    key=answer_key,
                    index=None,
                    label_visibility="collapsed"
                )
            else:
                selected_option = st.radio(
                    "Select your answer:",
                    options=[f"{chr(65+j)}) {opt}" for j, opt in enumerate(options)],
                    key=answer_key,
                    index=None,
                    label_visibility="collapsed"
                )
            
            # Store the selected answer
            if selected_option:
                selected_letter = selected_option[0]
                st.session_state.quiz_answers[i] = selected_letter
            
            if i < num_questions - 1:
                st.markdown("---")
        
        # Submit button
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("📤 **Submit Quiz**", type="primary", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.rerun()
        with col2:
            if st.button("🔙 **Back to Analysis**", use_container_width=True):
                st.session_state.show_interactive_quiz = False
                st.rerun()
    
    else:
        # Calculate score
        score = 0
        total = len(questions)
        
        for i, question in enumerate(questions):
            user_answer = st.session_state.quiz_answers.get(i, '').upper()
            correct_answer = question.get('correct_answer', '').upper()
            
            if user_answer == correct_answer:
                score += 1
        
        # Display score
        percentage = (score / total) * 100
        st.markdown(f"""
        <div class="score-display">
            <h1 class="score-value">{score}/{total}</h1>
            <p class="score-label">{percentage:.0f}% Correct</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance comment
        if percentage >= 80:
            st.success("🎉 Excellent! You've mastered the content!")
        elif percentage >= 60:
            st.info("👍 Good job! You understand most of the material.")
        elif percentage >= 40:
            st.warning("📚 Keep learning! Review the material and try again.")
        else:
            st.error("📖 Needs improvement. Study the content and retake the quiz.")
        
        # Display results for each question
        st.markdown("### 📋 Question Review")
        for i, question in enumerate(questions):
            user_answer = st.session_state.quiz_answers.get(i, '').upper()
            correct_answer = question.get('correct_answer', '').upper()
            options = question.get('options', [])
            
            is_correct = user_answer == correct_answer
            
            st.markdown(f"""
            <div class="quiz-question {'correct' if is_correct else 'incorrect'}">
                <h4>Question {i+1}: {question.get('question', '')}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display options with styling
            letters = ['A', 'B', 'C', 'D']
            for j, option in enumerate(options):
                if j >= len(letters):
                    break
                letter = letters[j]
                
                if letter == correct_answer:
                    css_class = "correct-answer"
                elif letter == user_answer and not is_correct:
                    css_class = "incorrect-answer"
                else:
                    css_class = ""
                
                st.markdown(f"""
                <div class="quiz-option {css_class}">
                    <span class="option-letter">{letter}</span>
                    {option}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"**Your answer:** {user_answer if user_answer else 'Not answered'}")
            st.markdown(f"**Correct answer:** {correct_answer}")
            if question.get('explanation'):
                st.markdown(f"**Explanation:** {question.get('explanation')}")
            
            if i < total - 1:
                st.markdown("---")
        
        # Action buttons after quiz
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 **Retake Quiz**", use_container_width=True):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
        with col2:
            if st.button("📊 **New Analysis**", use_container_width=True):
                st.session_state.show_interactive_quiz = False
                st.rerun()
        with col3:
            if st.button("💾 **Save Results**", use_container_width=True):
                quiz_content = f"Quiz Results: {score}/{total} ({percentage:.0f}%)\n\n"
                for i, question in enumerate(questions):
                    quiz_content += f"Q{i+1}: {question.get('question', '')}\n"
                    quiz_content += f"Your Answer: {st.session_state.quiz_answers.get(i, 'Not answered')}\n"
                    quiz_content += f"Correct Answer: {question.get('correct_answer', '')}\n\n"
                
                st.download_button(
                    label="⬇️ Download Results",
                    data=quiz_content,
                    file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# Simple prompt when no text is entered yet
elif not st.session_state.uploaded_text.strip():
    st.info("📝 Please enter text or upload a document to get started!")

# Footer
st.markdown("""
<div class="footer">
    <p>✨ <strong>Axinity QuickNotes</strong> • AI-Powered Document Intelligence</p>
</div>

""", unsafe_allow_html=True)

