import streamlit as st
import os
import time
import json
from scripts.pdf_extractor import PDFExtractor
from scripts.claude_api import ClaudeAPI
from scripts.database import CreditDatabase

st.set_page_config(page_title="Credit Extractor", page_icon="🏦", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = CreditDatabase()
if 'extractor' not in st.session_state:
    st.session_state.extractor = PDFExtractor()

with st.sidebar:
    st.title("Credit Extractor")
    page = st.radio("Menu", ["Upload", "Dashboard"])
    st.divider()
    api_key = st.text_input("API Key", type="password")
    if api_key:
        st.success("✅ API key set")
    st.divider()
    stats = st.session_state.db.get_statistics()
    st.metric("Documents", stats['total_documents'])
    st.metric("Total Cost", f"${stats['total_cost']:.2f}")

st.title("🏦 Credit Document Extractor")

if page == "Upload":
    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose file", type=['pdf'])
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")
        
        if st.button("🚀 Extract Terms", type="primary"):
            if not api_key:
                st.error("❌ Enter API key in sidebar")
            else:
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    with st.spinner("Processing..."):
                        start = time.time()
                        
                        # Extract text
                        st.info("📄 Extracting text...")
                        extraction = st.session_state.extractor.extract_all(temp_path)
                        
                        # Analyze with Claude
                        st.info("🤖 Analyzing with Claude...")
                        api = ClaudeAPI(api_key=api_key)
                        terms = api.extract_credit_terms(extraction['text'])
                        
                        # Save to database
                        st.info("💾 Saving to database...")
                        metadata = {
                            'pages_processed': extraction.get('pages_processed', 0),
                            'api_cost': 0.09,
                            'processing_time': time.time() - start
                        }
                        
                        doc_id = st.session_state.db.insert_document(
                            uploaded_file.name, terms, metadata
                        )
                        
                        st.success(f"✅ Extraction Complete!")
                        st.success(f"📄 Doc ID: {doc_id} | ⏱️ {metadata['processing_time']:.1f}s | 💰 ~$0.09")
                        
                        # Display results
                        st.subheader("📋 Extracted Terms")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        # Handle borrower (string or dict)
                        borrower = terms.get('borrower', '')
                        if isinstance(borrower, dict):
                            borrower_name = borrower.get('name', 'N/A')
                        else:
                            borrower_name = borrower or 'N/A'
                        
                        # Handle lender (string, dict, or list)
                        lender = terms.get('lender', '')
                        if isinstance(lender, dict):
                            lender_name = lender.get('name', 'N/A')
                        elif isinstance(lender, list) and len(lender) > 0:
                            first_lender = lender[0]
                            if isinstance(first_lender, dict):
                                lender_name = first_lender.get('name', 'N/A')
                            else:
                                lender_name = str(first_lender)
                        else:
                            lender_name = str(lender) if lender else 'N/A'
                        
                        # Handle loan amount
                        loan = terms.get('loan_details', {})
                        if isinstance(loan, dict):
                            loan_amount = loan.get('total_amount', 'N/A')
                        else:
                            loan_amount = 'N/A'
                        
                        col1.metric("Borrower", borrower_name)
                        col2.metric("Lender", lender_name)
                        col3.metric("Loan Amount", loan_amount)
                        
                        with st.expander("📄 View Full JSON"):
                            st.json(terms)
                        
                        st.download_button(
                            "📥 Download JSON",
                            json.dumps(terms, indent=2),
                            file_name=f"{uploaded_file.name}_extracted.json",
                            mime="application/json"
                        )
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
                
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

elif page == "Dashboard":
    st.header("📊 Dashboard")
    
    stats = st.session_state.db.get_statistics()
    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Documents", stats['total_documents'])
    col2.metric("💰 Total Cost", f"${stats['total_cost']:.2f}")
    col3.metric("⏱️ Avg Time", f"{stats['avg_processing_time']:.1f}s")
    
    st.divider()
    st.subheader("📄 Recent Documents")
    
    docs = st.session_state.db.get_all_documents()
    
    if docs:
        for doc in docs[:10]:
            with st.expander(f"📄 {doc['filename']} - {doc['upload_date'][:10]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Borrower:** {doc['borrower_name'] or 'N/A'}")
                    st.write(f"**Lender:** {doc['lender_name'] or 'N/A'}")
                with col2:
                    st.write(f"**Amount:** {doc['loan_amount'] or 'N/A'}")
                    st.write(f"**Cost:** ${doc['api_cost']:.2f}")
                
                if doc['full_extraction']:
                    with st.expander("View Full JSON"):
                        st.json(json.loads(doc['full_extraction']))
    else:
        st.info("No documents yet. Upload your first document!")

st.caption("Built with Streamlit + Claude AI")
