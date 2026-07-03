# CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

The format is loosely inspired by:
Keep a Changelog
https://keepachangelog.com/

Versioning follows semantic-style iteration for the assignment workflow.


---

# [0.1.0] - 2026-07-03

## Initial MVP Release

Initial implementation of CodeScope AI.

This release introduces a fullstack AI-powered code documentation assistant
capable of repository ingestion, semantic code analysis, vector retrieval,
grounded AI answering, and project documentation generation.


---

# Added


## Core Application Structure

Added modular application architecture:

```text
codescope_ai/
├── app/
│   ├── core/
│   ├── ingestion/
│   ├── rag/
│   ├── documentation/
│   └── ui/
```
