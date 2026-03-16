from pawpal_system import Task, Pet, Owner, Scheduler

# Create Owner
owner = Owner("Jordan", 60)

# Create Pets
mochi = Pet("Mochi", "dog")
mocha = Pet("Mocha", "cat")

owner.add_pet(mochi)
owner.add_pet(mocha)

# Add Tasks
mochi.add_task(Task("morning walk", "take mochi to walk", 20, 2))
mochi.add_task(Task("morning food", "serve mochi's food", 10, 3))
mocha.add_task(Task("morning play", "play with mocha", 15, 1))
mocha.add_task(Task("vet checkup", "take mocha to the vet", 30, 3))

# Print data
owner.print_pets()
mochi.print_tasks()
mocha.print_tasks()

# Print schedule
schedule = Scheduler(owner).create_schedule()
print("Today's Schedule:")
for t in schedule:
    print('-', t)