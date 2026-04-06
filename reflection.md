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
- **Changed to:** Implemented actual time-slot overlap detection across all pets using a shared `all_scheduled_tasks` pool
- **Why:** Can now verify if two tasks — even from different pets — are scheduled at overlapping times

**6. Min Heap Stability**
- **Initial:** Heap stored (priority, task) which could cause issues with equal priorities
- **Changed to:** Heap now stores (priority, task_id, task) for stable sorting
- **Why:** Ensures deterministic ordering even when tasks have the same priority

**7. Comprehensive Logging (Production-Ready)**
- **Initial:** No logging system
- **Changed to:** Added `logging` module with DEBUG and INFO level logs throughout the system
- **Why:** Essential for production code—enables debugging, monitoring, and audit trails

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider?

  The scheduler considers three types of constraints:
  1. **Time constraints** — tasks only get placed inside the owner's availability windows, and windows are merged if they overlap so no capacity is wasted
  2. **Priority constraints** — tasks are pulled from a min-heap in priority order (1 = most urgent), so the most important tasks always get the first available slot
  3. **Health and feeding constraints** — if a pet has a health condition relevant to a task type, or hasn't been fed in over 6 hours, the scheduler automatically adjusts that task's priority before building the heap

- How did you decide which constraints mattered most?

  Time comes first because without a valid window nothing can be scheduled at all. Priority comes second because the whole point of the system is urgency-aware ordering. Health and feeding boosts come last — they modify priority values before the heap is built, so they feed into the same priority system rather than being a separate layer.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes:

  The scheduler uses a **greedy bin-packing approach** — it processes tasks strictly in priority order and places each one in the first window with enough room. It does not look ahead to see if a large low-priority task could be swapped with several small high-priority tasks to fill windows more efficiently.

  A second pass does retry skipped tasks in remaining gaps, but it still doesn't reorder tasks globally. True optimal bin-packing is NP-hard, so greedy with a second pass is a deliberate tradeoff: it runs in O(n log n) time and is easy to reason about, at the cost of occasionally leaving capacity unused.

- Why is that tradeoff reasonable for this scenario?

  For a daily pet care app with typically fewer than 10 tasks per pet, the difference between greedy and optimal is negligible in practice. The predictability and speed of greedy scheduling matters more than squeezing out the last few minutes of window capacity.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project?

  AI was used across every phase — but in different roles at each stage. During design, I used it to pressure-test my class structure and identify gaps (like missing conflict detection and skipped task reporting). During implementation, I used it to write and explain specific algorithmic methods like `_resolve_priority_queue` and `_merge_windows`. During testing, I used it to identify edge cases I hadn't thought of (like `sort_by_time` mutating the original list, or recurring tasks inheriting `"complete"` status). During the UI phase, I used it to wire Streamlit components to the scheduler methods I'd already built.

- What kinds of prompts were most helpful?

  The most effective prompts were specific and gave context — for example, referencing `#codebase` or `#file:pawpal_system.py` so the AI could see the actual code rather than guessing. Questions like "what edge cases are missing from these tests?" or "does this conflict detection cover cross-pet scenarios?" gave sharper answers than vague requests like "improve my code."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is:

  When asked about adding a `sort_by_time()` public method to `Scheduler`, the AI suggested it as an optimization. I pushed back — pointing out that `_resolve_priority_queue` already sorts internally, so the new method would be redundant. The AI agreed it wasn't more efficient, but explained its value as a **reusable public API** for callers like `app.py` that need to re-sort after filtering. I kept the method, but only after understanding the real reason — not because the AI said to add it.

- How did you evaluate what the AI suggested?

  I ran the tests after every change. If a suggestion broke an existing test, I investigated why before accepting the fix. I also read the implementation before accepting it — not just the description. When the AI changed `has_conflicts()` to use `all_scheduled_tasks` instead of `cached_scheduled_tasks`, I traced through what that meant for the two existing conflict tests and confirmed they needed updating too.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

  The 53 tests cover seven areas:
  - **Task** — creation, unique IDs, status transitions, scheduled time management
  - **Pet** — feeding/exercise tracking, health problems, requirement assignment
  - **Owner** — availability window management, pet collection
  - **Scheduler** — priority ordering, single and multiple task scheduling
  - **Sort correctness** — chronological ordering, None times at end, non-mutation of original list
  - **Recurrence logic** — daily and weekly due dates, field preservation, new task starts pending, new task has unique ID
  - **schedule_all + filtering** — dict structure, no cross-pet conflicts, filter_by_pet isolation, unknown pet name returns empty, reset clears all state

- Why were these tests important?

  The recurrence and cross-pet conflict tests caught real bugs — the original conflict check only looked at one pet's tasks, and the recurring task needed to be verified it didn't inherit `"complete"` status from its parent. Without tests, both of those issues would have been invisible until a user noticed wrong behavior.

**b. Confidence**

- How confident are you that your scheduler works correctly?

  High confidence for the core path (priority scheduling, conflict detection, filtering, recurrence). Medium confidence for edge cases around the priority boost logic — health keyword matching is based on substring search which could produce false positives with unusual task names.

- What edge cases would you test next?

  - An owner with zero availability minutes (all windows too small for any task)
  - A pet with 10+ tasks and only 30 minutes of total window — verifying the skipped task list is complete and ordered
  - Two tasks with identical priority, type, and duration — verifying UUID tiebreaking in the heap is stable across runs

---

## 5. Reflection

**a. What went well**

The scheduling algorithm came together cleanly once the data model was solid. Having `Task`, `Pet`, and `Owner` as clean dataclasses with no cross-dependencies made it easy to test each one in isolation before writing `Scheduler`. The shared window pool fix (`schedule_all`) was the most satisfying moment — changing from per-pet independent windows to one global pool eliminated the entire class of cross-pet conflicts in a single method.

**b. What you would improve**

The UI currently generates a static schedule on button press but doesn't let you mark tasks complete from the app itself. The recurring task logic exists in the backend — `mark_complete()` returns the next occurrence — but there's no button in Streamlit to trigger it. In a next iteration, I'd add per-task completion buttons in the schedule table so the recurrence feature is actually usable from the UI, not just from `main.py`.

**c. Key takeaway**

The biggest thing I learned is how to use AI as a **separation of concerns tool** — not just as a code generator. Each phase of the project (design, algorithm, testing, UI, documentation) had a different kind of AI interaction. During design it was a critic. During implementation it was a pair programmer. During testing it was an edge case finder. Keeping those roles separate meant I stayed in control of the architecture while letting the AI handle the time-consuming parts that would have slowed me down before.

The key skill isn't prompting — it's knowing when to push back. AI suggestions are fast but not always right for *your* system. The `sort_by_time` example showed that: the AI was technically correct but I had to understand *why* before deciding whether the suggestion fit my design. That judgment — accepting, modifying, or rejecting — is what makes you the lead architect rather than just a reviewer of AI output.

---
