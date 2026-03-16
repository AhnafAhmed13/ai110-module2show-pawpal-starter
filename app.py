import streamlit as st
from pawpal_store import PawPalStore

if "store" not in st.session_state:
    st.session_state.store = PawPalStore()
if "selected_owner" not in st.session_state:
    st.session_state.selected_owner = None
if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

store: PawPalStore = st.session_state.store

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

# --- Owner selection ---
owner_names = store.get_owner_names()
owner_options = owner_names + ["➕ Add new owner..."]
owner_default_index = (
    owner_names.index(st.session_state.selected_owner)
    if st.session_state.selected_owner in owner_names
    else len(owner_options) - 1
)
selected_owner = st.selectbox("Owner name", owner_options, index=owner_default_index)

if selected_owner == "➕ Add new owner...":
    new_owner_name = st.text_input("Enter new owner name")
    if st.button("Add owner") and new_owner_name.strip():
        error = store.create_owner(new_owner_name.strip())
        if error:
            st.warning(error)
        else:
            st.session_state.selected_owner = new_owner_name.strip()
            st.rerun()
else:
    if st.session_state.selected_owner != selected_owner:
        st.session_state.selected_owner = selected_owner
        st.session_state.selected_pet = None

no_owner = st.session_state.selected_owner is None or selected_owner == "➕ Add new owner..."

# --- Pet selection ---
pet_dicts = store.get_pets(st.session_state.selected_owner) if st.session_state.selected_owner else []
pet_names = [p["name"] for p in pet_dicts]
pet_options = pet_names + ["➕ Add new pet..."]
pet_default_index = (
    pet_names.index(st.session_state.selected_pet)
    if st.session_state.selected_pet in pet_names
    else 0 if pet_names else len(pet_options) - 1
)
selected_pet = st.selectbox("Pet", pet_options, index=pet_default_index, disabled=no_owner)

if selected_pet == "➕ Add new pet...":
    new_pet_name = st.text_input("Enter new pet name", disabled=no_owner)
    species = st.selectbox("Species", ["dog", "cat", "other"], disabled=no_owner)
    if st.button("Add pet", disabled=no_owner) and new_pet_name.strip():
        error = store.add_pet(st.session_state.selected_owner, new_pet_name.strip(), species)
        if error:
            st.warning(error)
        else:
            st.session_state.selected_pet = new_pet_name.strip()
            st.rerun()
else:
    st.session_state.selected_pet = selected_pet
    pet_info = next((p for p in pet_dicts if p["name"] == selected_pet), None)
    if pet_info:
        st.caption(f"Species: {pet_info['species']}")

no_pet = no_owner or selected_pet == "➕ Add new pet..."

# --- Tasks ---
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
    error = store.add_task(
        st.session_state.selected_owner,
        st.session_state.selected_pet,
        task_title, int(duration), priority
    )
    if error:
        st.warning(error)

tasks = store.get_tasks(st.session_state.selected_owner) if st.session_state.selected_owner else []
if tasks:
    st.write("Current tasks:")

    all_pets = ["All"] + sorted({t["pet"] for t in tasks})
    all_priorities = ["All", "high", "medium", "low"]

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        filter_pet = st.selectbox("Filter by pet", all_pets, key="filter_pet")
    with fcol2:
        filter_priority = st.selectbox("Filter by priority", all_priorities, key="filter_priority")
    with fcol3:
        sort_by = st.selectbox("Sort by", ["None", "duration_minutes", "priority"], key="sort_by")

    filtered = [
        t for t in tasks
        if (filter_pet == "All" or t["pet"] == filter_pet)
        and (filter_priority == "All" or t["priority"] == filter_priority)
    ]

    if sort_by == "duration_minutes":
        filtered = sorted(filtered, key=lambda t: t["duration_minutes"])
    elif sort_by == "priority":
        filtered = sorted(filtered, key=lambda t: {"high": 0, "medium": 1, "low": 2}[t["priority"]])

    if filtered:
        st.dataframe(filtered, use_container_width=True, hide_index=True)
    else:
        st.info("No tasks match the current filters.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule ---
st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

available_time = st.slider(
    "Available time (minutes)", min_value=10, max_value=480, value=60, step=10, disabled=no_owner
)

if st.button("Generate schedule", disabled=no_owner):
    store.set_available_time(st.session_state.selected_owner, available_time)
    result = store.generate_schedule(st.session_state.selected_owner)
    if result["scheduled"]:
        st.write("Today's Schedule:")
        st.table(result["scheduled"])
    else:
        st.info("No tasks fit within the available time.")
    if result["excluded"]:
        with st.expander(f"Tasks that didn't fit ({len(result['excluded'])})", expanded=False):
            st.table(result["excluded"])
