import streamlit as st
import os
from utils import get_available_datasets

st.set_page_config(
    page_title="Cinema English Hub",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UI Header ---
st.title("🎬 Cinema English: The Visual Memory Hub")
st.markdown("### *\"Where words become scenes.\"*")

st.divider()

# --- System Status ---
datasets = get_available_datasets()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Library Status", "Online 🟢")
with col2:
    st.metric("Available Scripts", f"{len(datasets)} Sets")
with col3:
    st.metric("AI Engine", "Active ⚡")

st.info("👈 Please select **'01 Cinema Card'** from the sidebar to start training.")

# --- Quick Preview ---
if datasets:
    st.subheader("📂 Loaded Data:")
    for d in datasets:
        st.text(f"📄 {d}")
else:
    st.error("No data found! Please run 'visual_converter.py' first.")