import streamlit as st
from pathlib import Path
import warnings
import tempfile
import os
from dotenv import load_dotenv

# Set page config as early as possible for better perceived performance
st.set_page_config(
    page_title="RAG Question Generator",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="expanded"
)

warnings.filterwarnings('ignore')
load_dotenv()

# CSS Overhaul for Premium Feel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@400;600;800&display=swap');

    :root {
        --primary: #8B5CF6;
        --secondary: #10B981;
        --bg-dark: #0F172A;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-main: #F1F5F9;
        --text-muted: #94A3B8;
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, .stHeading {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    /* Glassmorphism Cards */
    .question-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .question-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
    }

    /* Custom Badges */
    .difficulty-badge {
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        display: inline-block;
    }
    .diff-easy { background: rgba(16, 185, 129, 0.2); color: #34D399; }
    .diff-medium { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }
    .diff-hard { background: rgba(239, 68, 68, 0.2); color: #F87171; }

    .score-badge {
        background: rgba(139, 92, 246, 0.2);
        color: #A78BFA;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }

    /* Flashcard Special Styling */
    .flashcard-inner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid var(--primary);
        border-radius: 24px;
        padding: 60px 40px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid var(--glass-border);
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4) !important;
    }

    /* Progress Bar */
    .stProgress > div > div > div {
        background-image: linear-gradient(90deg, var(--primary), #D946EF) !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎓 Ultimate Study Tool")
st.markdown("Your all-in-one AI study platform for mastering documents")

# Load RAG components only once using caching
@st.cache_resource
def validate_generation_inputs(vectorstore, selected_sources, mode="quiz", num_questions=None, question_types=None, topic=None):
    """Validates user inputs before generating content

    Args:
        vectorstore: VectorStore instance
        selected_sources: List of selected source files
        mode: "quiz" or "learning"
        num_questions: Required for quiz mode
        question_types: Required for quiz mode
        topic: Optional topic focus
    """
    errors = []

    # Check available sources
    available_sources = vectorstore.get_available_sources() if vectorstore else []
    if not available_sources:
        errors.append("No documents found in the database. Please upload a document first.")

    # If sources are selected, ensure they exist
    if selected_sources:
        invalid_sources = [s for s in selected_sources if s not in available_sources]
        if invalid_sources:
            errors.append(f"Selected sources not found: {', '.join(invalid_sources)}")

    # Quiz-specific validations
    if mode == "quiz":
        if num_questions is None:
            errors.append("Number of questions is required.")
        elif num_questions < 1 or num_questions > 20:
            errors.append("Number of questions must be between 1 and 20.")

        if not question_types:
            errors.append("Please select at least one question type.")

    # Validate topic length if provided
    if topic and len(topic.strip()) > 200:
        errors.append("Topic focus is too long (max 200 characters).")

    return errors


def load_rag_components(mistral_api_key):
    try:
        # Lazy imports to speed up initial app load
        from src.embedding import EmbeddingManager
        from src.vector_store import VectorStore
        from src.search import RAGRetrieval
        from langchain_mistralai import ChatMistralAI
        
        # Initialize components
        embedding_manager = EmbeddingManager(model_name="multi-qa-MiniLM-L6-cos-v1")
        vectorstore = VectorStore(
            collection_name="pdf_documents",
            persist_directory="data/vector_store"
        )
        vectorstore.initialize_store()
        
        retriever = RAGRetrieval(vectorstore, embedding_manager)
        
        if not mistral_api_key:
            return retriever, None, vectorstore, embedding_manager
            
        llm = ChatMistralAI(
            model="mistral-small-2506", 
            temperature=0.7,
            api_key=mistral_api_key
        )
        
        return retriever, llm, vectorstore, embedding_manager
    except Exception as e:
        st.error(f"Error loading RAG components: {str(e)}")
        return None, None, None, None

# --- Sidebar configuration ---
st.sidebar.title("⚙️ Configuration")

# API Key Retrieval
mistral_key = os.getenv("MISTRAL_API_KEY")

if not mistral_key:
    st.sidebar.error("❌ `MISTRAL_API_KEY` not found in environment.")
    st.sidebar.info("Please set the `MISTRAL_API_KEY` in your `.env` file or environment variables to enable AI study features.")
    st.error("AI features are currently disabled. Please configure the Mistral API key.")

retriever, llm, vectorstore, embedding_manager = load_rag_components(mistral_key)

if retriever is None:
    st.error("Failed to initialize RAG system. Please check your setup.")
    st.stop()

top_k = st.sidebar.slider("Number of source chunks to use", 1, 20, 10)
score_threshold = st.sidebar.slider("Similarity threshold", 0.0, 1.0, 0.20, 0.05)
num_questions = st.sidebar.slider("Number of questions to generate", 1, 15, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Quiz Settings")
question_types = st.sidebar.multiselect(
    "Question Types",
    options=["MCQ", "True/False"],
    default=["MCQ"],
    help="Select the types of questions to include in your quiz"
)

topic_focus = st.sidebar.text_input(
    "Topic Focus (Optional)",
    placeholder="e.g. History of Rome",
    help="Leave empty to generate based on general document content"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Study Modes")
exam_mode = st.sidebar.toggle(
    "Exam Mode",
    value=False,
    help="Timed quiz with no instant feedback. Reveal results only at the end."
)

flashcard_mode = st.sidebar.toggle(
    "Flashcard Mode",
    value=False,
    help="Show one question at a time. Click to reveal answer."
)

if exam_mode:
    exam_duration = st.sidebar.number_input("Duration (minutes)", 1, 60, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Study Performance")
if st.session_state.get("history"):
    import pandas as pd
    hist_df = pd.DataFrame(st.session_state.history)
    hist_df["perf"] = (hist_df["score"] / hist_df["total"]) * 100
    st.sidebar.line_chart(hist_df["perf"])
    st.sidebar.caption("Last 10 quiz scores (%)")
else:
    st.sidebar.info("No quiz history yet. Complete a quiz to see your progress!")
    
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF, TXT, DOCX or PPTX", type=["pdf", "txt", "docx", "pptx"])
if uploaded_file:
    if st.sidebar.button("Process & Add Document", use_container_width=True):
        from src.data_loader import (
            process_single_pdf, process_single_txt, process_single_docx, process_single_pptx, split_document
        )
        with st.sidebar.status("Processing document..."):
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write("Extracting text...")
            if uploaded_file.name.lower().endswith('.pdf'):
                docs = process_single_pdf(temp_path)
            elif uploaded_file.name.lower().endswith('.txt'):
                docs = process_single_txt(temp_path)
            elif uploaded_file.name.lower().endswith('.docx'):
                docs = process_single_docx(temp_path)
            elif uploaded_file.name.lower().endswith('.pptx'):
                docs = process_single_pptx(temp_path)
            else:
                docs = []
            
            if docs:
                st.write("Splitting into chunks...")
                chunks = split_document(docs)
                if chunks:
                    st.write("Generating embeddings...")
                    texts = [c.page_content for c in chunks]
                    embeddings = embedding_manager.generate_embeddings(texts)
                    st.write("Adding to database...")
                    vectorstore.add_documents(chunks, embeddings)
                    st.success(f"Successfully added {uploaded_file.name}!")
                else:
                    st.error("Document processed, but no text chunks found.")
            else:
                st.error("Failed to extract text from document.")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters & Management")
available_sources = vectorstore.get_available_sources()
selected_sources = st.sidebar.multiselect(
    "Filter by Source File",
    options=available_sources,
    default=[],
    help="Select specific documents to generate questions from."
)

if available_sources:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🗑️ Remove Document")
    doc_to_remove = st.sidebar.selectbox("Select document to remove", [""] + available_sources)
    if doc_to_remove and st.sidebar.button("Delete Document", type="primary", use_container_width=True):
        with st.sidebar.status(f"Removing {doc_to_remove}..."):
            success = vectorstore.remove_source(doc_to_remove)
            if success:
                st.success(f"Successfully removed {doc_to_remove}!")
                st.rerun()
            else:
                st.error("Failed to remove the document.")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    RAG Question Generator | Powered by Mistral AI & ChromaDB
</div>
""", unsafe_allow_html=True)


# Navigation
tab_learning, tab_quiz = st.tabs(["📋 Learning Hub", "🎯 Quiz Center"])

with tab_learning:
    st.subheader("📚 Learning & Research")
    st.markdown("Generate summaries and key notes from your documents to build a strong foundation.")
    
    learn_col1, learn_col2 = st.columns([2, 1])
    with learn_col1:
        learn_mode = st.radio("What would you like to generate?", ["Summary", "Key Notes"], horizontal=True)
    with learn_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        learn_btn = st.button("✨ Generate Study Material", type="primary", use_container_width=True)
    
    if learn_btn:
        if llm is None:
            st.error("Please enter a valid Mistral API key in the sidebar configuration to generate study material.")
        else:
            # Validate inputs
            errors = validate_generation_inputs(
                vectorstore=vectorstore,
                selected_sources=selected_sources if selected_sources else [],
                mode="learning",
                topic=topic_focus
            )
            if errors:
                for err in errors:
                    st.error(err)
            else:
                from src.search import generate_learning_content
                with st.spinner(f"Generating {learn_mode}..."):
                    try:
                        content = generate_learning_content(
                            mode=learn_mode,
                            retriever=retriever,
                            llm=llm,
                            top_k=top_k,
                            source_filter=selected_sources if selected_sources else None,
                            topic=topic_focus
                        )
                        st.session_state.learning_content = content
                    except Exception as e:
                        st.error(f"Error generating content: {e}")
                
    if st.session_state.get("learning_content"):
        st.markdown("---")
        st.markdown(f"### 📖 {learn_mode}")
        st.markdown(f"""
        <div class="question-card" style="background: var(--card-bg); line-height: 1.6;">
            {st.session_state.learning_content}
        </div>
        """, unsafe_allow_html=True)
        
        # Download Learning Notes
        st.download_button(
            "📥 Download Study Notes",
            st.session_state.learning_content,
            f"{learn_mode.lower()}_notes.md",
            "text/markdown"
        )

with tab_quiz:
    # --- Main Generator Interface ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        difficulty = st.radio(
            "Select Difficulty Level",
            ["Easy", "Medium", "Hard"],
            key="quiz_diff",
            horizontal=True,
            help="Easy: Recall based, Medium: Understanding/Application, Hard: Analysis/Synthesis"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🚀 Generate New Quiz", type="primary", key="quiz_gen_btn", use_container_width=True)
    
    # Initialize Session State
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_sources" not in st.session_state:
        st.session_state.quiz_sources = []
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "history" not in st.session_state:
        st.session_state.history = []
    if "learning_content" not in st.session_state:
        st.session_state.learning_content = None
    
    if generate_btn:
        if llm is None:
            st.error("Please enter a valid Mistral API key in the sidebar configuration to generate a quiz.")
        else:
            # Validate inputs
            errors = validate_generation_inputs(
                vectorstore=vectorstore,
                selected_sources=selected_sources if selected_sources else [],
                mode="quiz",
                num_questions=num_questions,
                question_types=question_types,
                topic=topic_focus
            )
            if errors:
                for err in errors:
                    st.error(err)
            else:
                from src.search import generate_questions
                with st.spinner("Analyzing documents and crafting MCQs..."):
                    try:
                        results = generate_questions(
                            difficulty=difficulty,
                            retriever=retriever,
                            llm=llm,
                            num_questions=num_questions,
                            top_k=top_k,
                            min_score=score_threshold,
                            source_filter=selected_sources if selected_sources else None,
                            topic=topic_focus,
                            question_types=question_types if question_types else ["MCQ"]
                        )
                        st.session_state.quiz_data = results["questions"]
                        st.session_state.quiz_sources = results["sources"]
                        st.session_state.user_answers = {}
                        st.session_state.quiz_submitted = False
                        import time
                        st.session_state.start_time = time.time()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating quiz: {e}")
                    st.error(f"Error generating quiz: {str(e)}")
    
    # Display Quiz
    if st.session_state.quiz_data:
        st.markdown("---")
        colp, colt = st.columns([3, 1])
        with colp:
            st.markdown("### 📝 Interactive Quiz")
        
        # Progress Bar
        answered_count = len([v for v in st.session_state.user_answers.values() if v is not None])
        total_questions = len(st.session_state.quiz_data)
        progress = answered_count / total_questions
        st.progress(progress, text=f"Progress: {answered_count}/{total_questions} answered")
    
        if exam_mode and not st.session_state.quiz_submitted:
            import time
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, (exam_duration * 60) - elapsed)
            mins, secs = divmod(int(remaining), 60)
            with colt:
                st.metric("⏳ Time Remaining", f"{mins:02d}:{secs:02d}")
            
            if remaining <= 0:
                st.warning("⏰ Time is up! Submitting your quiz automatically...")
                st.session_state.quiz_submitted = True
                st.rerun()
    
        if st.session_state.quiz_submitted:
            # Calculate Score
            score = 0
            for i, q in enumerate(st.session_state.quiz_data):
                if st.session_state.user_answers.get(f"q_{i}") == q["answer"]:
                    score += 1
            
            # Display Result Card
            if score == total_questions:
                st.balloons()
                st.success(f"### 🎉 PERFECT SCORE! {score} / {total_questions}")
            elif score >= total_questions * 0.7:
                st.success(f"### 👏 Great Job! Your Score: {score} / {total_questions}")
            else:
                st.warning(f"### Keep Practicing! Your Score: {score} / {total_questions}")
            
            # CSV Export
            import pandas as pd
            quiz_df = pd.DataFrame(st.session_state.quiz_data)
            csv = quiz_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Quiz as CSV",
                csv,
                "quiz.csv",
                "text/csv",
                key='download-quiz-csv'
            )
            
            # Add to history
            import time
            st.session_state.history.append({
                "timestamp": time.time(),
                "score": score,
                "total": total_questions,
                "difficulty": difficulty
            })
            
            st.markdown("<br>", unsafe_allow_html=True)
    
        # Question Display
        if flashcard_mode and not st.session_state.quiz_submitted:
            if "card_idx" not in st.session_state:
                st.session_state.card_idx = 0
                
            idx = st.session_state.card_idx
            q = st.session_state.quiz_data[idx]
            
            with st.container():
                st.markdown(f"### 🗂️ Flashcard {idx+1} / {total_questions}")
                st.markdown(f"<div class='flashcard-inner'>{q['question']}</div>", unsafe_allow_html=True)
                
                show_ans = st.button("👁️ Reveal Answer", use_container_width=True)
                if show_ans:
                    st.success(f"**Answer:** {q['answer']}")
                    st.info(f"**Explanation:** {q['explanation']}")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("⬅️ Previous", disabled=idx==0, use_container_width=True):
                        st.session_state.card_idx -= 1
                        st.rerun()
                with c3:
                    if st.button("Next ➡️", disabled=idx==total_questions-1, use_container_width=True):
                        st.session_state.card_idx += 1
                        st.rerun()
                        
            st.info("💡 Switch to 'List View' (Disable Flashcard Mode) to submit and see your final score!")
        else:
            # Determine badge class based on difficulty
            badge_class = "diff-easy" if difficulty == "Easy" else "diff-medium" if difficulty == "Medium" else "diff-hard"
    
            # Question Display
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"""
                <div class="question-card">
                    <div class="difficulty-badge {badge_class}">QUESTION {i+1}</div>
                    <div style="font-size: 20px; font-weight: 700; margin-bottom: 15px; color: var(--text-main); font-family: 'Outfit';">
                        {q["question"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Options below the card for interactivity
                with st.container():
                    
                    # Options
                    answer_key = f"q_{i}"
                    if st.session_state.quiz_submitted:
                        # Disabled radio buttons after submission
                        correct_answer = q["answer"]
                        user_selected = st.session_state.user_answers.get(answer_key)
                        
                        # Show correct/incorrect icons
                        for opt in q["options"]:
                            if opt == correct_answer:
                                st.markdown(f"✅ **{opt}** (Correct Answer)")
                            elif opt == user_selected:
                                st.markdown(f"❌ ~~{opt}~~ (Your choice)")
                            else:
                                st.markdown(f"▫️ {opt}")
                        
                        with st.expander("💡 View Explanation"):
                            st.info(q["explanation"])
                            
                            # Ask a Follow-up
                            st.markdown("---")
                            st.caption("🤖 Need more help? Ask a follow-up about this topic:")
                            follow_up = st.text_input("Follow-up question", key=f"fup_{i}", label_visibility="collapsed")
                            if follow_up:
                                with st.spinner("AI is thinking..."):
                                    # Simple RAG call for explanation
                                    fup_prompt = f"""The user has a question about a quiz item.
                                    Context: {q.get('explanation')}
                                    Question: {follow_up}
                                    Helpful Answer:"""
                                    fup_resp = llm.invoke([fup_prompt])
                                    st.write(fup_resp.content)
                    else:
                        # Interactive Radio
                        st.session_state.user_answers[answer_key] = st.radio(
                            f"Select your answer for Q{i+1}:",
                            q["options"],
                            key=f"radio_{i}",
                            index=None,
                            label_visibility="collapsed"
                        )
                    st.markdown("---")
    
        # Action Buttons
        if not st.session_state.quiz_submitted:
            if st.button("🏁 Submit Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.rerun()
        else:
            if st.button("🔄 Take Another Quiz", use_container_width=True):
                st.session_state.quiz_data = None
                st.session_state.quiz_submitted = False
                st.rerun()
    
        # Sources
        if st.session_state.quiz_sources:
            with st.expander("📚 View Study Sources"):
                for source in st.session_state.quiz_sources:
                    score = source.get('similarity_score', 0)
                    badge_class = "score-high" if score >= 0.7 else "score-medium" if score >= 0.5 else "score-low"
                    st.markdown(
                        f"**{source.get('source_file')}** (Page {source.get('page')}) <span class='score-badge {badge_class}'>{score:.1%}</span>", 
                        unsafe_allow_html=True
                    )
                    st.caption(source.get('content', ''))
    
    else:
        if not available_sources:
            st.info("👈 Start by uploading a document in the sidebar.")
        else:
            st.info("Click 'Generate New Quiz' to start.")
