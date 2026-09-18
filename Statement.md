# Project Problem Statement

## The Problem
In college, we have a strict rule that we must maintain at least 75% attendance in every subject. If our attendance goes below 75%, we get debarred and cannot sit for the semester exams. 

The main problem is that our college portal only shows past attendance like "15 out of 20 attended". It does not tell us what will happen next. Students always have two simple questions:
1. "Can I take leave tomorrow for an event or sickness without falling below 75%?"
2. "My attendance is 68%, how many classes do I have to attend continuously to reach 75%?"

Doing this calculation in our head or on paper often leads to mistakes, and many students only find out they are debarred when it is already too late.

---

## What This Project Does
This project is a simple Python program that runs in the terminal to help students plan their attendance easily.

### What it does:
- **Easy Menu:** You just open it and select options (1, 2, 3...) to add subjects or mark attendance.
- **Bunk Calculator:** Tells you the exact number of classes you can miss safely without dropping below 75%.
- **Recovery Helper:** Tells you how many classes you must attend in a row if your percentage is low.
- **Saves Your Data:** Everything is saved in a local SQLite file so your attendance is never lost.
- **Runs Everywhere:** Does not require installing complicated libraries. It runs directly with standard Python.
