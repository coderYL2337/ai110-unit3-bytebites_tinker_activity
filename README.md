# ByteBites Backend 

## Project Overview
This repository contains the backend logic for ByteBites, a food ordering app. The core models are Customer, Item, Menu, and Order, each implemented as a Python class. Students are expected to understand how to design and connect these classes, manage collections, and implement filtering, sorting, and total calculations. The project emphasizes encapsulation, method design, and the use of Python data structures to model real-world relationships.

## Summary
The core concept students needed to understand is how to translate a real-world system (food ordering) into interconnected Python classes, using methods to expose behaviors and maintain encapsulation. Students are most likely to struggle with designing clean interfaces for filtering and sorting, and with correctly handling edge cases (like empty orders or canceled transactions). AI was helpful for quickly scaffolding class diagrams and method stubs, but sometimes misleading in over-simplifying logic or skipping subtle requirements (such as excluding canceled orders from totals). When guiding a student, I would encourage them to trace the flow of data through each class—asking them to explain how an order is created, updated, and totaled—rather than simply giving the answer. This approach helps them build intuition for object-oriented design and debugging.

## Usage
- All core classes are in `models.py`.
- Run `python3 models.py` for a demo scenario.
- Run `pytest` for full test coverage (see `test_bytebites.py`).

## Files
- `models.py` — main class implementations
- `test_bytebites.py` — pytest suite
- `.gitignore` — standard Python ignores


