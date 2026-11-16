# Spring Workers Synchronization Problem

A multiprocessing-based synchronization simulation implemented in Python using Locks and Semaphores.  
This project demonstrates a classic Producer–Consumer style operating system synchronization problem involving picker and loader processes.

---

# Problem Statement

Simulate a fruit tree containing a fixed number of fruits.

Three picker processes run concurrently and pick fruits from the tree. Picked fruits are placed into a crate having 12 slots.

When the crate becomes full:
- Pickers signal the loader process
- Loader transfers the full crate into a truck
- Loader provides a new empty crate
- Pickers resume operation

At the end:
- If a partially filled crate exists, the loader loads it into the truck
- All processes terminate safely

The implementation ensures:
- Mutual exclusion
- Proper synchronization
- No duplicate fruit picking
- Deadlock avoidance

---

# Features

- Multiprocessing-based implementation
- Synchronization using:
  - Locks
  - Semaphores
- Shared memory communication
- Deadlock prevention
- Edge case handling
- Producer–Consumer coordination
- Realistic staggered process execution
- Input validation

---

# Technologies Used

- Python 3.14
- multiprocessing module

---

# Synchronization Mechanisms

| Mechanism | Purpose |
|---|---|
| `tree_lock` | Prevents multiple pickers from accessing tree simultaneously |
| `crate_lock` | Protects crate during insertion/removal |
| `loader_signal` | Signals loader when crate becomes full |
| `picker_wait` | Blocks pickers until loader resets crate |

---

# System Architecture

```text
                +------------------+
                |      TREE        |
                |   Shared Fruits  |
                +------------------+
                          |
         ---------------------------------------
         |                 |                  |
         v                 v                  v
    Picker 1          Picker 2          Picker 3
         \                 |                 /
          \                |                /
           ---------------------------------
                         |
                         v
                 +---------------+
                 |     CRATE     |
                 | 12 Fruit Slots|
                 +---------------+
                         |
                 loader_signal
                         |
                         v
                 +---------------+
                 |    LOADER     |
                 +---------------+
                         |
                         v
                 +---------------+
                 |     TRUCK     |
                 +---------------+
```

---

# How to Run

## Clone Repository

```bash
git clone https://github.com/FatimaaShahid/Spring-Workers-Synchronization-OS-Problem-using-Pthreads-Semaphores-
cd Spring-Workers-Synchronization-OS-Problem-using-Pthreads-Semaphores-
```

---

## Run Program

```bash
python main.py
```

---

# Input

```text
Enter the number of Fruits:
```

---

# Input Validation

The program handles:
- Non-integer input
- Negative input
- Zero fruits edge case

---

# Sample Execution

```text
Enter the number of Fruits: 24

[Picker 1] picked fruit 1
[Picker 2] picked fruit 2
[Picker 3] picked fruit 3

...

[Picker 2] crate FULL -> calling loader

[Loader] Loading FULL crate into truck...

[Loader] New empty crate supplied

========== FINAL TRUCK ==========

Crate 1: [1, 2, 3, ...]
Crate 2: [13, 14, 15, ...]

Total crates loaded: 2
```

---

# Test Cases

## Test Case 1 — Small Input

| Parameter | Value |
|---|---|
| Fruits | 10 |
| Pickers | 3 |
| Crate Size | 12 |

### Expected:
- One partially filled crate

---

## Test Case 2 — Exact Full Crates

| Parameter | Value |
|---|---|
| Fruits | 24 |
| Pickers | 3 |
| Crate Size | 12 |

### Expected:
- Two full crates
- No partial crate

---

## Test Case 3 — Large Input

| Parameter | Value |
|---|---|
| Fruits | 200 |
| Pickers | 3 |
| Crate Size | 12 |

### Expected:
- Multiple crate loads
- Correct synchronization under stress

---

# Key Concepts Demonstrated

- Process Synchronization
- Mutual Exclusion
- Critical Sections
- Semaphores
- Locks
- Shared Memory
- Producer–Consumer Problem
- Deadlock Prevention
- Interprocess Communication (IPC)

---

# Challenges Faced

- Preventing race conditions
- Avoiding deadlocks
- Coordinating multiple pickers
- Handling final partially filled crate
- Synchronizing loader wake-up signals

---

# Future Improvements

- Dynamic picker count
- GUI visualization
- Logging system
- Distributed implementation using sockets
- Performance analytics dashboard

---
Dedication
dedicate this project to our collective hard work, teamwork, and collaboration. Each member contributed their efforts and knowledge to make this project successful.

Group Members:
- Fatima Shahid
- Muhammad Abdullah

---
# Authors

- Asra Siddiqui
- Group CEP Project — Operating Systems

---

# License

This project is developed for academic and educational purposes.
