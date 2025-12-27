import streamlit as st
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Study Partner", layout="centered")

# Custom CSS for Minimal UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .status-pending { color: #ff4b4b; font-weight: bold; }
    .status-completed { color: #28a745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INTERNAL LOGIC (Hidden from User) ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def get_status(task):
    now = datetime.now().time()
    if task['completed']:
        return "Completed"
    if now > task['end_time']:
        return "Pending"
    return "Not Started"

# --- MAIN UI ---
st.title("Study Partner")
st.caption("Focus on your goals. I'll track the rest.")

# 1. Daily Goal Input
with st.expander("+ Add New Task", expanded=True):
    t_name = st.text_input("Task Name", placeholder="e.g. Physics Revision")
    col1, col2 = st.columns(2)
    t_start = col1.time_input("Start Time")
    t_end = col2.time_input("End Time")
    
    if st.button("Add Task"):
        if t_name:
            st.session_state.tasks.append({
                "name": t_name,
                "start_time": t_start,
                "end_time": t_end,
                "completed": False
            })
            st.rerun()

# 2. & 3. Task Tracking & Time-Based Checking
st.markdown("---")
st.subheader("Today's Schedule")

if not st.session_state.tasks:
    st.info("No tasks added yet.")
else:
    for idx, task in enumerate(st.session_state.tasks):
        status = get_status(task)
        col_check, col_text, col_status = st.columns([1, 4, 2])
        
        # Checkbox to mark completed
        is_done = col_check.checkbox("", value=task['completed'], key=f"check_{idx}")
        st.session_state.tasks[idx]['completed'] = is_done
        
        # Task info
        col_text.write(f"**{task['name']}** \n{task['start_time'].strftime('%I:%M %p')} - {task['end_time'].strftime('%I:%M %p')}")
        
        # Status display
        if status == "Pending":
            col_status.markdown(f"<span class='status-pending'>Pending</span>", unsafe_allow_html=True)
        elif status == "Completed":
            col_status.markdown(f"<span class='status-completed'>Done</span>", unsafe_allow_html=True)
        else:
            col_status.text("Waiting...")

# 4. & 5. Night Review (Triggered by a simple button for demo, can be time-locked)
st.markdown("---")
if st.button("Night Review (10 PM)"):
    st.subheader("Daily Review")
    st.write("How much did you complete today?")
    
    done_tasks = [t for t in st.session_state.tasks if t['completed']]
    pending_tasks = [t for t in st.session_state.tasks if get_status(t) == "Pending"]
    total = len(st.session_state.tasks)
    
    if total > 0:
        percent = (len(done_tasks) / total) * 100
        
        st.write(f"• Completed: {len(done_tasks)}")
        st.write(f"• Pending: {len(pending_tasks)}")
        st.write(f"• Completion Rate: **{percent:.0f}%**")
        
        # Simple Feedback
        if percent >= 70:
            st.success("Good job. Goals met.")
        else:
            st.warning("Below target. Aim for more tomorrow.")
    else:
        st.write("No tasks were recorded.")
