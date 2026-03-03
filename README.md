# 🦾 Architecture for code Automation && better software design

## 📝 Project Description
This repository serves as a comprehensive reference architecture and toolkit for advanced  programming, strictly tailored for automation engineering, robotics, and embedded systems. It moves beyond basic scripting to implement robust, enterprise-grade design patterns. The codebase focuses on hardware-safe state machines, dynamic plugin loading, rigorous memory management, and concurrent data processing to bridge the gap between high-level software and physical hardware control.

## ⚙️ System
The modules in this repository are designed to act as independent but highly cohesive architectural building blocks. 
* **Execution Flow:** Hardware processes are managed via a robust Finite State Machine (`state_machine.py`), ensuring safe transitions and emergency stops.
* **Concurrency:** CPU-bound mathematical calculations (like inverse kinematics) are handled by bypassing the GIL (`multiprocessing.py`), while I/O-bound sensor readings utilize `async.py` and threaded locks.
* **Extensibility:** New sensor drivers or actuators can be dropped into the `dynamic_import/plugins/` folder and are loaded at runtime without modifying the core system.
* **Reliability:** All critical hardware operations are wrapped in advanced context managers and custom decorators to guarantee safe teardown and strict execution timing.

## 🗂️ Code Structure
The repository is modularized by architectural concepts:

```text
python/
├── config/                 # Dynamic configuration managers
│   ├── config_env.py       # Secrets and environment variables (.env)
│   ├── config_json.py      # Standard nested JSON configurations
│   └── config_yaml.py      # Human-readable YAML configs for deployments
├── context/                # Advanced Context Managers (The 'with' statement)
│   ├── class.py            # Class-based robust resource locking
│   └── stack.py            # Dynamic ExitStack for multiple simultaneous devices
├── decorators/             # Metaprogramming for functions
│   ├── atexit.py           # Safe shutdown hooks
│   ├── cache.py            # Memory caching (Memoization) with TTL
│   ├── deprecated.py       # Legacy code warnings
│   ├── get_time.py         # Execution profiling and performance metrics
│   ├── log.py              # Automatic execution auditing
│   └── retry.py            # Fault tolerance with exponential backoff
├── dynamic_import/         # Plugin-based Architecture
│   ├── main.py             # Plugin orchestrator
│   ├── registry.py         # Global driver registry
│   └── plugins/            # Drop-in folder for new hardware modules
├── generators/             # Memory-efficient data pipelines
│   ├── corouties.py        # Push-based data streams (.send)
│   ├── flatten.py          # Yield delegation (yield from)
│   └── lazy.py             # Pull-based lazy evaluation
├── metaclasses/            # Class-level metaprogramming
│   ├── singleton.py        # Hardware port collision prevention (Borg/Singleton)
│   └── validation.py       # Strict interface enforcement at runtime
├── abc.py                  # Abstract Base Classes contracts
├── async.py                # Asynchronous I/O and event loops
├── dataclasses_teste.py    # Immutable payloads and complex states
├── descriptor.py           # Low-level attribute access and validation
├── dunder_methods.py       # Operator overloading and callable instances
├── enum_teste.py           # Bitwise IntFlags and hardware register mapping
├── grafo.py                # Graph theory algorithms (BFS, DFS, Dijkstra)
├── iterators.py            # Custom iteration protocols
├── log.py                  # Centralized Borg-pattern logging system (Rich)
├── multiprocessing.py      # True parallelism with shared C-arrays
├── path.py                 # Path library
└── state_machine.py        # Asynchronous/Synchronous Finite State Machine (FSM)

```



## 📌 Notes

* **Python Version:** Requires Python 3.8+ (Python 3.10+ recommended for advanced Type Hinting capabilities like `Protocol`).
* **Dependencies:** Ensure `pyyaml`, `python-dotenv`, and `rich` are installed via `pip`.
* **Hardware Safety:** When using the `state_machine.py` or `multiprocessing.py` in physical applications, always ensure emergency physical kill-switches are independent of the software layer.


## ⚠️ Common Errors

* **`RecursionError` in Decorators:** Usually caused by forgetting to use `functools.wraps` or calling the wrapper recursively instead of the original function.
* **Deadlocks in Multithreading:** Ensure you are using `threading.RLock()` instead of `Lock()` if a thread needs to acquire the same lock multiple times in a nested method.
* **Corrupt Shared Memory (Multiprocessing):** When using `multiprocessing.Array`, always wrap write operations in a `multiprocessing.Lock()` to avoid race conditions between CPU cores.
* **StopIteration unhandled in Generators:** When manually using `next()` on a custom iterator, ensure you catch the `StopIteration` exception if not using a standard `for` loop.

## 🏷️ Version

* **v1.0.0** - Initial implementation of advanced core concepts and architectural patterns.

## 👥 Team

* **Gabriel Rocha de Souza** - *Automation Engineer & Lead Developer* - Architecture design, implementation, and hardware abstraction logic.


> *"Mastering the machine begins with mastering the logic that binds it."*
