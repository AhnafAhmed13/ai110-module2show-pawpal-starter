# PawPal+ Project Reflection

## 1. System Design

Core actions:

- Add a pet
- Schedule a walk
- See today's tasks

UML (draft):

- Owner
    - name
    - pets
    - time available
    - add pet ()

- Pet
    - name
    - species
    - tasks
    - add task ()

- Task
    - title
    - duration
    - priority

- Scheduler
    - tasks
    - create schedule ()


**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

> 4 classes: Owner, Pet, Task, Scheduler
> Owner has pets
> Pet has tasks
> Scheduler creates schedule

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

> I replaced the Scheduler class with create schedule function to simplify the design and logic
> However, I reverted back to the the Scheduler class to align it with the project requirements

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

> Dsign, brainstorming, debugging, refactoring

- What kinds of prompts or questions were most helpful?

> When you provide specific context and specify the current and desired behaviors

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

> AI told me to discard the Scheduler class and replace it with a function, I didn't use that suggestion.

- How did you evaluate or verify what the AI suggested?

> Found the exact change AI suggested and reverted it back to the original version.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

> Class methods, UI workflow

- Why were these tests important?

> To verify if the logic was correct

**b. Confidence**

- How confident are you that your scheduler works correctly?

> I'm confident that my version of the scheduler works correctly, because it passed all the tests

- What edge cases would you test next if you had more time?

> Empty and malformed inputs

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

> Multiple user and pet handling

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

> Add date, time, and deadlines to tasks

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

> AI can help you untangle UI and backend and suggest best practices to follow