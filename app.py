import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

if "owner" not in st.session_state:
    st.session_state.owner = None
if "owner_names" not in st.session_state:
    st.session_state.owner_names = []
if "owners" not in st.session_state:
    st.session_state.owners = {}  # name -> Owner object
if "selected_owner_name" not in st.session_state:
    st.session_state.selected_owner_name = None
if "selected_pet_name" not in st.session_state:
    st.session_state.selected_pet_name = None

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

owner_options = st.session_state.owner_names + ["➕ Add new owner..."]
default_index = (
    st.session_state.owner_names.index(st.session_state.selected_owner_name)
    if st.session_state.selected_owner_name in st.session_state.owner_names
    else len(owner_options) - 1
)
selected = st.selectbox("Owner name", owner_options, index=default_index)

if selected == "➕ Add new owner...":
    new_owner_name = st.text_input("Enter new owner name")
    if st.button("Add owner") and new_owner_name.strip():
        name = new_owner_name.strip()
        if name in st.session_state.owner_names:
            st.warning(f"Owner '{name}' already exists. Select them from the dropdown.")
        else:
            new_owner = Owner(name)
            st.session_state.owner_names.append(name)
            st.session_state.owners[name] = new_owner
            st.session_state.owner = new_owner
            st.session_state.selected_owner_name = name
            st.rerun()
    owner_name = new_owner_name.strip() if "new_owner_name" in dir() else ""
else:
    owner_name = selected
    if not st.session_state.owner or st.session_state.owner.name != owner_name:
        st.session_state.owner = st.session_state.owners[owner_name]
        st.session_state.selected_pet_name = None

no_owner = st.session_state.owner is None

current_pets = st.session_state.owner.pets if st.session_state.owner else []
pet_names = [p.name for p in current_pets]
pet_options = pet_names + ["➕ Add new pet..."]
pet_default_index = (
    pet_names.index(st.session_state.selected_pet_name)
    if st.session_state.selected_pet_name in pet_names
    else 0 if pet_names else len(pet_options) - 1
)
selected_pet = st.selectbox("Pet", pet_options, index=pet_default_index, disabled=no_owner)

if selected_pet == "➕ Add new pet...":
    new_pet_name = st.text_input("Enter new pet name", disabled=no_owner)
    species = st.selectbox("Species", ["dog", "cat", "other"], disabled=no_owner)
    if st.button("Add pet", disabled=no_owner) and new_pet_name.strip():
        new_name = new_pet_name.strip()
        if new_name in pet_names:
            st.warning(f"Pet '{new_name}' already exists. Select them from the dropdown.")
        else:
            st.session_state.owner.add_pet(Pet(new_name, species))
            st.session_state.selected_pet_name = new_name
            st.rerun()
    pet_name = new_pet_name.strip() if not no_owner else ""
else:
    pet_name = selected_pet
    st.session_state.selected_pet_name = selected_pet
    existing_pet = next((p for p in current_pets if p.name == selected_pet), None)
    species = existing_pet.species if existing_pet else "dog"
    st.caption(f"Species: {species}")

no_pet = no_owner or selected_pet == "➕ Add new pet..."

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", disabled=no_pet)
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, disabled=no_pet)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, disabled=no_pet)

if st.button("Add task", disabled=no_pet):
    if not st.session_state.owner:
        st.warning("Please select or add an owner first.")
        st.stop()

    pet = next((p for p in st.session_state.owner.pets if p.name == pet_name), None)
    if not pet:
        st.warning("Please select or add a pet first.")
        st.stop()
    pet.add_task(Task(title=task_title, duration=int(duration), priority=priority))

if st.session_state.owner:
    task_table = [
        {"pet": pet.name, "title": t.title, "duration_minutes": t.duration, "priority": t.priority}
        for pet in st.session_state.owner.pets
        for t in pet.tasks
    ]
    if task_table:
        st.write("Current tasks:")
        st.table(task_table)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

available_time = st.slider(
    "Available time (minutes)", min_value=10, max_value=480, value=60, step=10, disabled=no_owner
)

if st.button("Generate schedule", disabled=no_owner):
    if st.session_state.owner:
        st.session_state.owner.available_time = available_time
        schedule = Scheduler(st.session_state.owner).create_schedule()
        if schedule:
            task_table = []
            st.write("Today's Schedule:")
            for t in schedule:
                task_table.append({"title": t.title, "duration_minutes": t.duration, "priority": t.priority})
            st.table(task_table)
        else:
            st.info("No tasks yet. Add one above.")
    else:
        st.info("No tasks yet. Add one above.")
