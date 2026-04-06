# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
#add a pet and owner, and free time for the User, And busy time for the user. it would have  schedule  feeding requirments, schedule physical actiivty requirements, add grooming , add meds, each of these scheduled tasks will have a priortity assigned to them aswell as a time requirments.
- What classes did you include, and what responsibilities did you assign to each?
 #going to add a simple portal with the name of the owner and the pet name. I want to have a pet class that is the parent class and that other types of pets like dog, cat , fish etc are inherting from it. the attributes of the class duration, Health problems, I guess it would be important to know if its been fed, if it needs to have physical exercise. And maybe requests from the owner on what you want done with the pet. The plan could potentially use a priorty queue to schedule stuff. 

Main Objects:
Owner Object : It needs to have Avaliability period, It needs to have a pet, 
            is 
Pet Object : Type of Pet:(what specices), pet info - health etc
Task Object : What exactly needs to be done, also stores the priorty information, we need time info, and we need prirtoy info from here 
    we need to have time_for compeltion of the task
    
Scheduling Object: this handeling the logic from Task object looks at Owner time for what is possible example if owner has 3 hours and we have two object in task one with pq value of 1 and one with 2, the pq value 1 task if its done in 4 hours and pq value of 2 but done in 2 hours will be completetd first. We not do partial compleititons for now. 




**b. Design changes**

- Did your design change during implementation?
Yes, significant changes were made to improve efficiency and functionality.

- Describe at least one change and why you made it:

**1. Multiple Availability Windows for Owner**
- **Initial:** Owner had a single availability window (start_time, end_time)
- **Changed to:** List of availability windows to support owners with non-continuous free time (e.g., 9am-12pm AND 2pm-6pm)
- **Why:** More realistic scheduling—people have multiple time slots throughout the day, not just one continuous block

**2. Timestamp-based Pet State Tracking**
- **Initial:** Used boolean flags (is_fed: bool, needs_exercise: bool)
- **Changed to:** Timestamp tracking (last_fed_time: Optional[datetime], last_exercise_time: Optional[datetime])
- **Why:** Can track multiple feedings/exercises per day; better for real-world pet care where timing matters; allows calculation of "how long since last feed?"

**3. Unique Task Identifiers**
- **Initial:** Tasks had no unique ID
- **Changed to:** Each Task gets auto-generated UUID (task_id)
- **Why:** Better for tracking, debugging, and preventing duplicate tasks

**4. Cached Scheduling Results**
- **Initial:** `get_scheduled_tasks()` re-sorted the heap every call (O(n log n))
- **Changed to:** Caching scheduled tasks after computation (O(1) retrieval)
- **Why:** Performance improvement—frequent access to scheduled tasks is now instant

**5. Conflict Detection Logic**
- **Initial:** `has_conflicts()` was a stub (TODO)
- **Changed to:** Implemented actual time-slot overlap detection
- **Why:** Can now verify if two tasks are scheduled at overlapping times

**6. Min Heap Stability**
- **Initial:** Heap stored (priority, task) which could cause issues with equal priorities
- **Changed to:** Heap now stores (priority, task_id, task) for stable sorting
- **Why:** Ensures deterministic ordering even when tasks have the same priority

**7. Comprehensive Logging (Production-Ready)**
- **Initial:** No logging system
- **Changed to:** Added `logging` module with DEBUG and INFO level logs throughout the system
- **Why:** Essential for production code—enables debugging, monitoring, and audit trails. Logs key events like:
  - Task scheduling and prioritization
  - Pet feeding/exercise activities
  - Health problem alerts
  - Conflict detection
  - Schedule caching operations

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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
