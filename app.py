import streamlit as st
from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

# ── Owner ──────────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.markdown("**Availability Windows**")
col_a1, col_a2 = st.columns(2)
with col_a1:
    avail_start = st.time_input("Available from", value=time(8, 0))
with col_a2:
    avail_end = st.time_input("Available until", value=time(12, 0))

if st.button("Add availability window"):
    owner.add_availability_window(avail_start, avail_end)

if owner.get_availability_windows():
    for i, (s, e) in enumerate(owner.get_availability_windows()):
        st.text(f"  Window {i+1}: {s.strftime('%I:%M %p')} – {e.strftime('%I:%M %p')}")
else:
    st.info("No availability windows yet. Add one above.")

st.divider()

# ── Pets ───────────────────────────────────────────────────────────────────────
st.subheader("Pets")
col_p1, col_p2 = st.columns(2)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "fish", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, pet_type=species))

if owner.get_pets():
    st.write(f"Your pets: {', '.join(p.name for p in owner.get_pets())}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Tasks ──────────────────────────────────────────────────────────────────────
st.subheader("Tasks")
if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    selected_pet_name = st.selectbox("Add task to pet", pet_names)
    selected_pet = next(p for p in owner.get_pets() if p.name == selected_pet_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.number_input("Priority (1 = urgent)", min_value=1, max_value=10, value=1)
    with col4:
        # frequency powers the recurring task feature in mark_complete()
        frequency = st.selectbox("Repeats", ["none", "daily", "weekly"])

    if st.button("Add task"):
        new_task = Task(
            task_type=task_title,
            priority=int(priority),
            duration=int(duration),
            frequency=None if frequency == "none" else frequency,
        )
        selected_pet.add_requirement(new_task)
        st.success(f"Added '{task_title}' to {selected_pet_name}.")

    for pet in owner.get_pets():
        reqs = pet.get_requirements()
        if reqs:
            st.markdown(f"**{pet.name}'s tasks:**")
            st.table([
                {
                    "Task": t.get_type(),
                    "Duration (min)": t.get_duration(),
                    "Priority": t.get_priority(),
                    "Repeats": t.frequency or "—",
                }
                for t in reqs
            ])
else:
    st.info("Add a pet first, then you can assign tasks to it.")

st.divider()

# ── Generate Schedule ──────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.get_availability_windows():
        st.warning("Add at least one availability window first.")
    elif not owner.get_pets():
        st.warning("Add at least one pet first.")
    else:
        scheduler = Scheduler()
        scheduler.reset()
        scheduler.schedule_all(owner)

        total     = len(scheduler.all_scheduled_tasks)
        skipped   = scheduler.get_skipped_tasks()
        pending   = scheduler.filter_by_status("pending")
        completed = scheduler.filter_by_status("complete")

        # ── Summary metrics ───────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Scheduled",  total)
        m2.metric("Pending",    len(pending))
        m3.metric("Completed",  len(completed))
        m4.metric("Skipped",    len(skipped))

        st.divider()

        # ── Per-pet schedule table (sorted by time) ───────────────────────────
        for pet in owner.get_pets():
            # filter_by_pet() pulls only this pet's tasks from the shared pool
            # sort_by_time() orders them chronologically for display
            pet_tasks = scheduler.sort_by_time(scheduler.filter_by_pet(pet.name))

            st.markdown(f"### {pet.name} ({pet.pet_type})")

            if pet.get_health_problems():
                st.caption(f"Health notes: {', '.join(pet.get_health_problems())}")

            if pet_tasks:
                rows = []
                for task in pet_tasks:
                    t = task.get_scheduled_time()
                    rows.append({
                        "Time":          t.strftime("%I:%M %p") if t else "—",
                        "Task":          task.get_type(),
                        "Duration (min)": task.get_duration(),
                        "Priority":      task.get_priority(),
                        "Repeats":       task.frequency or "—",
                        "Status":        task.get_status(),
                    })
                st.table(rows)
            else:
                st.info(f"No tasks could be scheduled for {pet.name}.")

        st.divider()

        # ── Conflict check ────────────────────────────────────────────────────
        if scheduler.has_conflicts():
            st.error("Scheduling conflicts detected — two or more tasks overlap.")
        else:
            st.success("Schedule generated — no conflicts detected.")

        # ── Skipped tasks warning ─────────────────────────────────────────────
        if skipped:
            st.warning(
                f"{len(skipped)} task(s) could not fit in any availability window."
            )
            with st.expander("See skipped tasks"):
                st.table([
                    {
                        "Pet":           t.pet_name or "—",
                        "Task":          t.get_type(),
                        "Duration (min)": t.get_duration(),
                        "Priority":      t.get_priority(),
                    }
                    for t in skipped
                ])

        # ── Pending / completed breakdown ─────────────────────────────────────
        if pending or completed:
            with st.expander("View by status"):
                if pending:
                    st.markdown("**Pending**")
                    st.table([
                        {
                            "Pet":  t.pet_name or "—",
                            "Task": t.get_type(),
                            "Time": ts.strftime("%I:%M %p") if (ts := t.get_scheduled_time()) else "—",
                        }
                        for t in scheduler.sort_by_time(pending)
                    ])
                if completed:
                    st.markdown("**Completed**")
                    st.table([
                        {
                            "Pet":  t.pet_name or "—",
                            "Task": t.get_type(),
                            "Time": ts.strftime("%I:%M %p") if (ts := t.get_scheduled_time()) else "—",
                        }
                        for t in scheduler.sort_by_time(completed)
                    ])
