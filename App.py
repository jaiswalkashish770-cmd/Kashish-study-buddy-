import streamlit as st
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Study Partner",
    layout="centered"
)

# =========================
# PINK THEME CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #ffe6f0;
}

h1, h2, h3 {
    color: #d63384;
    text-align: center;
}

button {
    background-color: #ff69b4 !important;
    color: white !important;
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    background-color: #fff0f5;
    border-radius: 12px;
    padding: 10px;
}

.completed {
    background-color: #d4edda;
    padding: 8px;
    border-radius: 8px;
}

.pending {
    background-color: #fff3cd;
    padding: 8px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# =========================
# TITLE
# =========================
st.title("Study Partner 💗")
st.write("Focus on your goals. I'll track the rest.")

# =========================
# ADD TASK
# =========================
with st.expander("➕ Add New Task"):
    task_name = st.text_input("Task Name", placeholder="e.g. Physics Revision")
    start_time = st.time_input("Start Time", value=datetime.strptime("04:30", "%H:%M").time())
    end_time = st.time_input("End Time", value=datetime.strptime("05:30", "%H:%M").time())

    if st.button("Add Task"):
        if task_name.strip() == "":
            st.warning("Task name empty hai")
        else:
            st.session_state.tasks.append({
                "name": task_name,
                "start": start_time,
                "end": end_time,
                "status": "not started"
            })
            st.success("Task added 💖")

# =========================
# TODAY SCHEDULE
# =========================
st.subheader("Today's Schedule")

if not st.session_state.tasks:
    st.info("No tasks added yet.")
else:
    now = datetime.now().time()

    for i, task in enumerate(st.session_state.tasks):
        if task["status"] != "completed" and now > task["end"]:
            task["status"] = "pending"

        col1, col2 = st.columns([3, 1])

        with col1:
            if task["status"] == "completed":
                st.markdown(f"<div class='completed'>✅ {task['name']}</div>", unsafe_allow_html=True)
            elif task["status"] == "pending":
                st.markdown(f"<div class='pending'>⚠️ {task['name']}</div>", unsafe_allow_html=True)
            else:
                st.write(f"🕒 {task['name']}")

        with col2:
            if st.button("Done", key=i):
                st.session_state.tasks[i]["status"] = "completed"

# =========================
# NIGHT REVIEW
# =========================
st.divider()
st.subheader("🌙 Night Review (10 PM)")

if st.button("Night Review"):
    done_tasks = [t for t in st.session_state.tasks if t["status"] == "completed"]
    pending_tasks = [t for t in st.session_state.tasks if t["status"] == "pending"]
    total = len(st.session_state.tasks)

    if total > 0:
        percent = (len(done_tasks) / total) * 100

        st.write(f"✅ Completed: {len(done_tasks)}")
        st.write(f"⚠️ Pending: {len(pending_tasks)}")
        st.write(f"📊 Completion Rate: **{percent:.0f}%**")

        if percent >= 70:
            st.success("Good job Kashish 💖 Goals met!")
        else:
            st.warning("Below target. Kal aur achha karna 🌸")
    else:
        st.write("No tasks were recorded today.")
