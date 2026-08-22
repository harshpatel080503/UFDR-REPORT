# AegisTrace
## Agentic RAG Forensic Intelligence Copilot

> **Evidence-grounded digital investigation across large-scale forensic telemetry using hybrid retrieval, cross-encoder reranking, agentic tool orchestration, forensic reasoning, case construction, and automated report generation.**

![UFDR Banner](https://img.shields.io/badge/UFDR-Forensic%20Intelligence-00ff41?style=for-the-badge&logo=security)
![Version](https://img.shields.io/badge/Version-1.0.0--Phase1-blue?style=for-the-badge)

<img width="2816" height="1536" alt="UFDR" src="https://github.com/user-attachments/assets/cd4b071f-d80a-4122-9ec7-11101b6b813f" />

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/AI-Agentic%20RAG-6A5ACD?style=flat-square)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
[![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-FF6F00?style=flat-square)](https://faiss.ai/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Metadata-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Research](https://img.shields.io/badge/Project-Applied%20AI-8A2BE2?style=flat-square)](#research-contributions)

---

## Table of Contents

- [Overview](#overview)
- [Why AegisTrace?](#why-aegistrace)
- [Problem Statement](#problem-statement)
- [What Makes It Agentic RAG?](#what-makes-it-agentic-rag)
- [Core Capabilities](#core-capabilities)
- [System Architecture](#system-architecture)
- [Agentic Investigation Loop](#agentic-investigation-loop)
- [Hybrid Retrieval Architecture](#hybrid-retrieval-architecture)
- [Evidence-to-Reasoning Pipeline](#evidence-to-reasoning-pipeline)
- [Forensic Intelligence Layer](#forensic-intelligence-layer)
- [Case Construction & Investigation Artifacts](#case-construction--investigation-artifacts)
- [Tool Ecosystem](#tool-ecosystem)
- [End-to-End Investigation Trace](#end-to-end-investigation-trace)
- [Dataset](#dataset)
- [Data Representation](#data-representation)
- [Model Training Strategy](#model-training-strategy)
- [Evaluation Methodology](#evaluation-methodology)
- [Quantitative Results](#quantitative-results)
- [Ablation Study](#ablation-study)
- [Failure Analysis](#failure-analysis)
- [Known Limitations](#known-limitations)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Data Preparation & Indexing](#data-preparation--indexing)
- [Running AegisTrace](#running-aegistrace)
- [Example Investigation](#example-investigation)
- [Output Artifacts](#output-artifacts)
- [Research Contributions](#research-contributions)
- [Future Work](#future-work)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

# Overview

**AegisTrace** is an **Agentic RAG Forensic Intelligence Copilot** designed to transform large-scale digital telemetry into investigator-ready evidence and structured forensic intelligence.

Instead of treating forensic investigation as a simple:

```text
Query → Retrieve → LLM → Answer
```

AegisTrace follows a multi-stage investigation workflow:

```text
Investigator Query
        ↓
Query Understanding
        ↓
Agentic Tool Selection
        ↓
Hybrid Evidence Retrieval
        ↓
Candidate Merging
        ↓
Cross-Encoder Reranking
        ↓
Evidence Selection
        ↓
Forensic Reasoning
        ↓
Threat / Risk Assessment
        ↓
Case Construction
        ↓
Timeline + Relationship Graph
        ↓
Investigative Report
        ↓
Interactive Investigation UI
```

The system combines **information retrieval, agentic orchestration, neural reranking, LLM reasoning, structured case construction, and report synthesis** into one forensic investigation workflow.

---

# Why AegisTrace?

Modern enterprise environments generate enormous volumes of digital evidence:

- Web browsing activity
- Email and communication logs
- File access events
- USB/device activity
- Authentication and logon events
- User and organizational metadata

The underlying project dataset contains more than **36M records**, approximately **1,000 synthetic users**, **191 malicious scenarios**, and about **5.9 GB** of raw telemetry across multiple evidence sources.

The challenge is therefore not simply storing logs.

The real challenge is:

> **Finding the right evidence, deciding which forensic tool or reasoning step to use, ranking the strongest evidence, correlating it into an investigation, and producing a grounded report.**

AegisTrace is designed around that workflow.

---

# Problem Statement

Traditional forensic investigation workflows often require analysts to:

1. Search across large volumes of telemetry.
2. Apply user/date/event filters manually.
3. Inspect candidate events.
4. Correlate evidence across different data sources.
5. Determine whether the activity represents a meaningful threat.
6. Build a timeline manually.
7. Construct relationships between entities.
8. Produce an investigation report.

This creates several challenges:

- Information overload
- High analyst effort
- Weak semantic retrieval
- Difficult cross-source correlation
- Inconsistent investigation workflows
- Slow evidence-to-report turnaround
- Limited automation

AegisTrace addresses this by combining:

```text
Retrieval
+
Reranking
+
Agentic Tool Selection
+
Reasoning
+
Case Construction
+
Report Synthesis
```

---

# What Makes It Agentic RAG?

A standard RAG pipeline is typically:

```text
Query
  ↓
Retriever
  ↓
Context
  ↓
LLM
  ↓
Answer
```

AegisTrace extends this into a tool-driven investigation loop.

```text
                         INVESTIGATOR QUERY
                                │
                                ▼
                       QUERY UNDERSTANDING
                                │
                                ▼
                    AGENTIC TOOL / POLICY LAYER
                                │
         ┌──────────────────────┼────────────────────────┐
         │                      │                        │
         ▼                      ▼                        ▼
  SearchEvidence        GetScenarioPolicy       Investigation Action
         │                      │                        │
         └──────────────┬───────┴────────────────────────┘
                        ▼
                 HYBRID RETRIEVAL
                 ├── SQLite metadata
                 └── FAISS semantic search
                        │
                        ▼
                 CANDIDATE MERGE
                        │
                        ▼
               CROSS-ENCODER RERANKER
                        │
                        ▼
                 TOP EVIDENCE SET
                        │
                        ▼
                 FORENSIC REASONING
                        │
           ┌────────────┼─────────────┐
           ▼            ▼             ▼
       Threat Type   Risk Score    Findings
           │            │             │
           └────────────┼─────────────┘
                        ▼
                   CASE BUILDER
                        │
             ┌──────────┴───────────┐
             ▼                      ▼
       Timeline Builder       Graph Builder
             │                      │
             └──────────┬───────────┘
                        ▼
                  REPORT GENERATOR
                        │
                        ▼
                INVESTIGATION UI
```

The system includes a trainable **tool-policy component** whose purpose is to select an appropriate forensic action from query/context.

The documented investigation flow demonstrates evidence search, scenario-policy lookup, forensic reasoning, risk analysis, investigation alerting, and report generation.

---

# Core Capabilities

## 🔎 Hybrid Forensic Retrieval

Combines:

- SQLite metadata filtering
- FAISS semantic search
- user/date constraints
- candidate merging
- deduplication

## 🎯 Cross-Encoder Reranking

Retrieved candidates are rescored using a cross-encoder so that the reasoning stage receives a smaller and more relevant evidence set.

## 🧠 Agentic Tool Selection

A policy model selects the appropriate forensic action/tool based on the investigation context.

## 🕵️ Forensic Reasoning

Retrieved evidence is converted into:

- Threat category
- Risk score
- Findings
- Investigation narrative

## 🧩 Case Construction

Relevant events are grouped into investigation cases and structured findings.

## 🕒 Timeline Reconstruction

Relevant evidence is ordered chronologically to reconstruct the investigation sequence.

## 🕸️ Relationship Graph Construction

Relationships can be represented across:

- Users
- Devices
- Files
- URLs
- Activities
- Events

## 📄 Automated Investigative Reporting

The system generates structured forensic reports containing investigation metadata, findings, analysis, subjects, and graph artifacts.

---

# System Architecture

```text
                    ┌─────────────────────────┐
                    │     Investigator UI     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │ Query Processing │
                       └────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │ Agent / Tool Policy│
                     └──────────┬─────────┘
                                │
              ┌─────────────────┼──────────────────┐
              │                 │                  │
              ▼                 ▼                  ▼
      SearchEvidence     ScenarioPolicy     Action / Alert
              │                 │
              └──────────┬──────┘
                         ▼
                ┌───────────────────┐
                │ Hybrid Retrieval  │
                │                   │
                │ SQLite + FAISS    │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ Candidate Merge   │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ Cross-Encoder     │
                │ Reranking         │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ Evidence Context  │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ Forensic Reasoning│
                └─────────┬─────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
         Threat         Risk         Findings
        Category       Score
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                  ┌──────────────┐
                  │ Case Builder │
                  └──────┬───────┘
                         │
              ┌──────────┴───────────┐
              ▼                      ▼
         Timeline Builder      Graph Builder
              │                      │
              └──────────┬───────────┘
                         ▼
                  ┌──────────────┐
                  │ Report Gen.  │
                  └──────┬───────┘
                         │
                         ▼
                  Investigation UI
```

---

# Agentic Investigation Loop

Example:

```text
Investigator Query:
"Investigate CSC0217 for possible file exfiltration."
```

Workflow:

```text
1. Query Understanding
   - Identify subject
   - Identify threat hypothesis
   - Extract contextual constraints

2. Agent Tool Selection
   - Select SearchEvidence

3. Hybrid Retrieval
   - Metadata filtering
   - Semantic retrieval

4. Evidence Reranking
   - Cross-encoder scoring

5. Scenario Context
   - Retrieve relevant threat-policy context

6. Forensic Reasoning
   - Analyze evidence
   - Estimate risk
   - Classify threat

7. Action Decision
   - Determine whether investigation alert criteria are satisfied

8. Case Construction
   - Subject
   - Timeline
   - Relationships

9. Report Synthesis
   - Findings
   - Risk
   - Evidence
   - Graph
```

---

# Hybrid Retrieval Architecture

## Metadata Retrieval

SQLite provides exact constraints such as:

- User
- Date range
- Metadata fields
- Event identifiers

## Semantic Retrieval

FAISS provides approximate nearest-neighbor semantic retrieval over embedded forensic text.

## Hybrid Retrieval

```text
Exact Metadata Constraints
          +
Semantic Similarity
          ↓
Candidate Evidence
```

## Candidate Reranking

```text
Top Candidates
      ↓
Cross-Encoder
      ↓
Query–Evidence Relevance
      ↓
Top Evidence
```

---

# Evidence-to-Reasoning Pipeline

AegisTrace separates retrieval from reasoning.

```text
Raw Forensic Events
        ↓
Indexed Records
        ↓
Retrieved Candidates
        ↓
Reranked Evidence
        ↓
Evidence Context
        ↓
Forensic Reasoning
        ↓
Threat Assessment
        ↓
Case Findings
        ↓
Report
```

> **The reasoning layer should reason over retrieved forensic evidence rather than rely on unconstrained model knowledge.**

---

# Forensic Intelligence Layer

AegisTrace is not a generic question-answering chatbot.

## Threat Classification

Documented threat categories include:

- `Data Exfiltration`
- `Insider Theft`
- `Sabotage`
- `None`

## Risk Scoring

The reasoning layer produces a **0–10 risk score** as part of the investigation workflow.

## Investigation Alert

The documented example uses:

```text
risk_score >= 7
        ↓
Create Investigation Alert
```

This turns forensic reasoning into an actionable investigation artifact rather than only a generated summary.

---

# Case Construction & Investigation Artifacts

## Investigation Subject

Identifies users/entities involved in a case.

## Timeline

Chronological reconstruction of related activity.

## Relationship Graph

Represents relationships between entities and actions.

## Risk Assessment

Threat category + risk score.

## Investigation Report

Structured Markdown output combining:

- Case information
- Investigation summary
- Relevant subjects
- Evidence context
- Findings
- Analysis
- Timeline
- Graph artifacts

---

# Tool Ecosystem

## `SearchEvidence`

Purpose:

> Retrieve high-signal forensic evidence under semantic and metadata constraints.

Conceptual inputs:

```text
query
user_filter
date_range
```

## `GetScenarioPolicy`

Purpose:

> Retrieve contextual threat/scenario information relevant to the investigation.

Conceptual input:

```text
threat_category
```

## `CreateInvestigationAlert`

Purpose:

> Convert high-confidence forensic reasoning into an actionable investigation alert.

Conceptual inputs:

```text
case_id
risk_score
summary
```

---

# End-to-End Investigation Trace

## Example Query

```text
Investigate suspicious file exfiltration activity for user CSC0217.
```

## AegisTrace Workflow

```text
Query
  ↓
SearchEvidence
  ↓
Relevant evidence retrieved
  ↓
Scenario / policy context
  ↓
Cross-encoder reranking
  ↓
Evidence set
  ↓
Forensic reasoning
  ↓
Risk Score = 8
  ↓
Threat = Data Exfiltration
  ↓
Investigation Alert
  ↓
Timeline
  ↓
Relationship Graph
  ↓
Forensic Report
```

---

# Dataset

AegisTrace is evaluated using the **CERT r4.2 Insider Threat Test Dataset**.

| Property | Value |
|---|---:|
| Raw records | 36M+ |
| Synthetic users | 1,000 |
| Malicious scenarios | 191 |
| Raw data size | ~5.9 GB |
| Time period | 6 months |

### Evidence Sources

| Source | Approx. Volume | Evidence Type |
|---|---:|---|
| `http.jsonl` | ~33M | Web browsing |
| `email.jsonl` | ~2.6M | Communication |
| `file.jsonl` | ~445K | File access |
| `device.jsonl` | ~405K | Device / USB |
| `logon.jsonl` | ~329K | Authentication |
| LDAP + psychometric | ~11K | User / organizational metadata |

---

# Data Representation

Each unified forensic record contains fields such as:

```text
doc_id
timestamp
user
event_type
text
entities
metadata
```

Entities can include:

- Users
- URLs
- Files
- Devices

Metadata can include event-specific details such as:

- Size
- Attachments
- Additional attributes

---

# Model Training Strategy

AegisTrace contains three trainable components.

## 1. Domain-Adapted Retriever

Base:

```text
all-MiniLM-L6-v2
```

Objective:

```text
MultipleNegativesRankingLoss
```

Input:

```text
[query, positive_text]
```

Goal:

> Improve query–evidence semantic alignment for forensic retrieval.

---

## 2. Cross-Encoder Reranker

Base:

```text
ms-marco-MiniLM-L-6-v2
```

Objective:

```text
Binary Cross-Entropy
```

Input:

```text
[query, text, relevance_label]
```

Goal:

> Produce more precise query–evidence relevance scores.

---

## 3. Tool Policy

A classification-oriented policy component selects forensic actions based on query/context.

Example tool classes:

```text
SearchEvidence
ScenarioPolicy
Alert
```

---

# Evaluation Methodology

AegisTrace evaluates both retrieval and reasoning/report-generation behavior.

## Retrieval Metrics

### MRR

Mean Reciprocal Rank — how early the first relevant evidence appears.

### Recall@10

Whether relevant evidence appears among the top 10 results.

### NDCG@10

Rank-weighted relevance quality.

## Reasoning / Generation Metrics

### Threat Accuracy

Correct threat-category classification.

### Risk Score MAE

Mean absolute error of predicted risk score.

### ROUGE

Reference-summary overlap.

### Faithfulness

Evidence-grounding quality.

---

# Quantitative Results

## Retrieval

| Metric | Baseline | Fine-Tuned |
|---|---:|---:|
| **MRR** | 0.4861 | **0.7500** |
| **Recall@10** | 0.9167 | **1.0000** |
| **NDCG@10** | 0.6004 | **0.8194** |

## Reasoning / Generation

| Metric | Baseline | Fine-Tuned |
|---|---:|---:|
| **Threat Accuracy** | 0.38 | 0.31 |
| **Risk Score MAE** | 5.25 | 5.59 |
| **ROUGE-1** | 0.3103 | 0.3202 |
| **ROUGE-2** | 0.0710 | 0.0704 |
| **ROUGE-L** | 0.1905 | 0.1978 |
| **Faithfulness** | 0.8232 | **0.8389** |

---

# Evaluation Interpretation

The evaluation reveals an important system-level insight:

> **Domain-specific retriever fine-tuning substantially improves evidence retrieval, while forensic reasoning/classification remains the major bottleneck.**

Fine-tuning improves:

- MRR
- Recall@10
- NDCG@10
- Faithfulness

while threat classification accuracy and risk-score error do not improve in the same direction.

```text
Better Retrieval
       ≠
Automatically Better Reasoning
```

This makes reasoning quality the next research bottleneck.

---

# Ablation Study

| Configuration | Recall@10 | MRR | NDCG@10 | Faithfulness |
|---|---:|---:|---:|---:|
| **Full fine-tuned system** | **1.000** | **0.750** | **0.819** | **0.839** |
| No fine-tuning | 0.917 | 0.486 | 0.600 | 0.823 |
| No reranker | 0.917 | 0.486 | 0.600 | — |
| FAISS only | ~0.70* | ~0.35* | ~0.50* | — |
| No reasoning engine | — | — | — | 0.00 |

### Key Findings

- Domain-specific retriever fine-tuning improves retrieval quality.
- Cross-encoder reranking improves evidence ordering.
- Metadata filtering improves forensic precision.
- Removing reasoning removes the investigation intelligence layer.

---

# Failure Analysis

## 1. Limited Golden-Query Diversity

The evaluation notes that only a small number of unique users were repeated across the golden set.

**Impact:** retrieval performance can appear optimistic.

**Improvement:** expand the benchmark with more users and diverse forensic query templates.

## 2. No User-Specific Behavioral Baseline

The current system retrieves and correlates observed activity but does not fully model deviations from a user's normal behavior.

**Impact:** limited behavioral anomaly interpretation.

## 3. Batch-Oriented Ingestion

The current pipeline is primarily batch-oriented.

**Impact:** retrospective investigation is stronger than continuous streaming detection.

## 4. Text-Centric Evidence

Current processing is focused on text/log evidence.

**Impact:** native multimodal forensic analysis is not covered.

## 5. Chain-of-Custody Logging

A full signed forensic evidence chain is not implemented.

**Impact:** the system should not be represented as a certified legal-evidence management platform.

## 6. Generator / Risk Reasoning Bottleneck

Retrieval improves strongly, but threat classification and risk estimation remain weaker.

**Implication:** retrieval improvements alone are not enough.

---

# Known Limitations

| Area | Current State | Impact |
|---|---|---|
| Evaluation diversity | Limited golden-query diversity | Generalization uncertainty |
| Behavioral modeling | No user-specific baseline | Limited anomaly interpretation |
| Streaming | Batch-oriented | Not a real-time SOC detector |
| Evidence modalities | Primarily text/log based | No native multimodal analysis |
| Chain of custody | Not fully implemented | Not a production legal-evidence system |
| Generator reasoning | Main bottleneck | Threat/risk quality needs improvement |
| Dataset | Synthetic CERT environment | Real-world generalization requires further validation |

---

# Repository Structure

> Keep this section synchronized with the actual repository file names if the codebase structure changes.

```text
AegisTrace/
│
├── Data Preparation/
│   ├── data_pipeline.py
│   └── enhancing_to_pageindex.py
│
├── Indexing/
│   ├── pipeline.py
│   ├── page indexing
│   ├── embeddings
│   ├── FAISS indexing
│   └── SQLite metadata
│
├── Evaluation/
│   ├── retrieval evaluation
│   ├── generation evaluation
│   └── ablation evaluation
│
├── Reasoning/
│   ├── forensic reasoning
│   ├── threat analysis
│   └── risk assessment
│
├── Reporting/
│   └── report generation
│
├── ufdr-web-app/
│   ├── frontend
│   └── investigation command center
│
├── web_server.py
├── full_pipeline.py
└── README.md
```

---

# Installation

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- Ollama or an Ollama-compatible reasoning endpoint

## 1. Clone the Repository

```bash
git clone https://github.com/harshpatel080503/UFDR-REPORT.git
cd UFDR-REPORT
```

> The GitHub repository may remain named `UFDR-REPORT`; **AegisTrace** is the public project identity used in the README.

## 2. Create Python Environment

### Windows / PowerShell

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Backend Dependencies

```bash
pip install -r Indexing/requirements.txt
pip install -r Evaluation/requirements_eval.txt
pip install fastapi uvicorn python-dotenv requests
```

## 4. Configure Environment Variables

Create `.env` in the project root:

```env
OLLAMA_API_KEY=your_api_key_here
OLLAMA_CLOUD_URL=your_ollama_endpoint_here
```

### Security

Never commit:

```text
.env
API keys
access tokens
private credentials
```

Add `.env` to `.gitignore`.

## 5. Install Frontend Dependencies

```bash
cd ufdr-web-app
npm install
cd ..
```

---

# Data Preparation & Indexing

AegisTrace requires the forensic dataset to be processed and indexed before investigation queries can run.

## Step 1 — Prepare the Dataset

```powershell
python "Data Preparation/data_pipeline.py"
```

## Step 2 — Enhance Records for Indexing

```powershell
python "Data Preparation/enhancing_to_pageindex.py"
```

## Step 3 — Build Search Infrastructure

Run all phases:

```powershell
python Indexing/pipeline.py --phase all
```

Or individually:

```powershell
python Indexing/pipeline.py --phase pageindex
python Indexing/pipeline.py --phase embed
python Indexing/pipeline.py --phase faiss
```

Pipeline:

```text
Metadata / Page Index
        ↓
Embedding Generation
        ↓
FAISS Search Index
```

---

# Running AegisTrace

## 1. Start the Backend

From the project root:

```bash
python web_server.py
```

Backend:

```text
http://localhost:8000
```

## 2. Start the Investigation Command Center

```bash
cd ufdr-web-app
npm run dev
```

Open:

```text
http://localhost:5173
```

## 3. Run a Full Pipeline via CLI

From the project root:

```bash
python full_pipeline.py "Investigate suspicious data exfiltration for user FEB0306"
```

---

# Example Investigation

## Query

```text
Investigate suspicious file exfiltration activity for user CSC0217.
```

## Workflow

```text
Query
  ↓
Tool Selection
  ↓
Evidence Retrieval
  ↓
Cross-Encoder Reranking
  ↓
Forensic Reasoning
  ↓
Risk Assessment
  ↓
Threat Classification
  ↓
Case Construction
  ↓
Timeline + Graph
  ↓
Investigation Report
```

---

# Output Artifacts

AegisTrace can produce:

### Evidence Set

Ranked forensic evidence supporting the investigation.

### Risk Assessment

```text
Threat Category:
Data Exfiltration

Risk Score:
8 / 10
```

### Investigation Alert

Actionable alert when the configured investigation threshold is satisfied.

### Timeline

Chronological reconstruction of relevant activity.

### Relationship Graph

Entity-level investigation topology.

### Investigative Report

Structured Markdown investigation dossier.

---

# Research Contributions

## 1. Hybrid Forensic Retrieval

Combines exact metadata constraints with semantic evidence retrieval.

## 2. Domain-Specific Retriever Fine-Tuning

Adapts embedding retrieval to forensic query/evidence relationships.

## 3. Cross-Encoder Reranking

Adds a contextual second-stage relevance model.

## 4. Agentic Tool Selection

Uses a dedicated policy layer to select investigation operations.

## 5. Evidence-Grounded Reasoning

Reasoning operates over retrieved forensic evidence.

## 6. Automated Case Construction

Transforms evidence into structured investigation artifacts.

## 7. Component-Level Evaluation

Ablation experiments quantify the contribution of major components.

---

# Future Work

The next evolution of AegisTrace focuses on stronger forensic intelligence.

## 🔬 Behavioral Intelligence

Introduce user-specific behavioral baselines and anomaly detection.

```text
Historical User Behavior
        ↓
Normal Behavior Baseline
        ↓
Current Activity
        ↓
Deviation Detection
        ↓
Risk Signal
```

## ⚡ Streaming Investigation

Move from batch-oriented investigation toward incremental evidence ingestion and index updates.

## 🔐 Evidence Provenance & Chain of Custody

Introduce signed audit events across:

```text
Ingestion
   ↓
Retrieval
   ↓
Reranking
   ↓
Reasoning
   ↓
Reporting
```

## 🎥 Multimodal Forensics

Extend the system beyond text/log evidence toward additional forensic modalities.

## 🧠 Better Forensic Reasoning

Improve:

- Threat classification
- Risk calibration
- Evidence-grounded reasoning
- Report quality
- Investigation consistency

---

# Technical Positioning

AegisTrace is:

```text
Not simply:
RAG chatbot

Not simply:
Vector database search

Not simply:
Forensic dashboard

Not simply:
LLM report generator

Instead:

Agentic RAG
+
Hybrid Information Retrieval
+
Neural Reranking
+
Forensic Tool Orchestration
+
Evidence-Grounded Reasoning
+
Case Construction
+
Automated Investigation Reporting
```

---

# Project Maturity

| Layer | Capability |
|---|---|
| Data | Large-scale heterogeneous forensic telemetry |
| Retrieval | Hybrid SQLite + FAISS |
| Ranking | Cross-encoder reranking |
| Agent | Tool-policy layer |
| Reasoning | LLM-based forensic reasoning |
| Case Building | Timeline / subject aggregation |
| Graph | Relationship visualization |
| Reporting | Automated investigation reports |
| Evaluation | Retrieval + generation + ablation |
| UI | Interactive investigation command center |

---

# Key Takeaways

### 01 — Retrieval Quality Matters

Domain-specific retriever fine-tuning substantially improves evidence retrieval.

### 02 — Reranking Matters

Second-stage contextual ranking helps prioritize evidence for reasoning.

### 03 — Agentic Orchestration Matters

Forensic investigation is not a single retrieval operation.

### 04 — Reasoning Is Still the Bottleneck

Improved retrieval does not automatically produce better threat classification or risk estimation.

### 05 — Evidence Grounding Is Critical

Forensic conclusions must remain traceable to the evidence supporting them.

---

# Team

### Infraglyph Unit 01

- **Urvi Kava**
- **Harsh Patel**
- **Prisha Khalasi**
- **Aman Choudhary**

---

# Acknowledgements

This project uses the **CERT Insider Threat Test Dataset (r4.2)** for experimentation and evaluation.

The work focuses on applied research across:

- Information Retrieval
- Agentic RAG
- Forensic Intelligence
- Neural Reranking
- LLM Reasoning
- Evidence-Grounded Generation

---

# Disclaimer

AegisTrace is a research and educational project.

It is **not** a certified digital-forensics platform, legal evidence-management system, or production security operations product.

The evaluation uses a synthetic insider-threat dataset and should not be interpreted as evidence of real-world forensic performance without further validation.

---

# AegisTrace

## Agentic RAG Forensic Intelligence Copilot

> **Retrieve evidence.  
> Rank relevance.  
> Orchestrate investigation.  
> Reason over evidence.  
> Build the case.  
> Generate the report.**
