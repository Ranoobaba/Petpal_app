import streamlit as st
from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State: Owner persists (and pets + their tasks live inside it) ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

# --- Owner Info ---
st.subheader("Owner")
new_name = st.text_input("Owner name", value=owner.name)
owner.name = new_name

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
        st.text(f"  Window {i+1}: {s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}")
else:
    st.info("No availability windows yet. Add one above.")

st.divider()

# --- Add a Pet ---
st.subheader("Pets")
col_p1, col_p2 = st.columns(2)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "fish", "other"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, pet_type=species)
    owner.add_pet(new_pet)

if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    st.write(f"Your pets: {', '.join(pet_names)}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add Tasks to a Pet ---
st.subheader("Tasks")
if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    selected_pet_name = st.selectbox("Add task to pet", pet_names)
    selected_pet = next(p for p in owner.get_pets() if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.number_input("Priority (1 = most urgent)", min_value=1, max_value=10, value=1)

    if st.button("Add task"):
        new_task = Task(task_type=task_title, priority=priority, duration=int(duration))
        selected_pet.add_requirement(new_task)

    # Show tasks for each pet
    for pet in owner.get_pets():
        reqs = pet.get_requirements()
        if reqs:
            st.markdown(f"**{pet.name}'s tasks:**")
            task_data = [
                {"Task": t.get_type(), "Duration (min)": t.get_duration(), "Priority": t.get_priority()}
                for t in reqs
            ]
            st.table(task_data)
else:
    st.info("Add a pet first, then you can assign tasks to it.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.get_availability_windows():
        st.warning("Add at least one availability window first.")
    elif not owner.get_pets():
        st.warning("Add at least one pet first.")
    else:
        scheduler = Scheduler()
        scheduler.reset()
        schedule_map = scheduler.schedule_all(owner)

        for pet in owner.get_pets():
            st.markdown(f"### {pet.name} ({pet.pet_type})")
            if pet.get_health_problems():
                st.caption(f"Health notes: {', '.join(pet.get_health_problems())}")
            scheduled = schedule_map.get(pet.name, [])
            if scheduled:
                rows = []
                for task in scheduled:
                    t = task.get_scheduled_time()
                    time_str = t.strftime("%I:%M %p") if t else "N/A"
                    rows.append({
                        "Time": time_str,
                        "Task": task.get_type(),
                        "Duration (min)": task.get_duration(),
                        "Priority": task.get_priority(),
                    })
                st.table(rows)
            else:
                st.info(f"No tasks fit within availability for {pet.name}.")

        skipped = scheduler.get_skipped_tasks()
        if skipped:
            st.warning(
                f"Could not schedule: {', '.join(t.get_type() for t in skipped)}"
            )

        if scheduler.has_conflicts():
            st.error("Scheduling conflicts detected across pets.")
        else:
            st.success("Schedule generated — no conflicts.")
