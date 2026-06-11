# EAIOS: Enterprise AI Orchestration System

![Status](https://img.shields.io/badge/Status-Production_Ready-blue)
![Architecture](https://img.shields.io/badge/Architecture-Decoupled_Monorepo-black)
![Security](https://img.shields.io/badge/Security-Zero_Trust_JWT-red)

## Executive Summary
EAIOS (Enterprise AI Orchestration System) is a fault-tolerant, Zero-Trust multi-agent operating system. Designed to bypass the fragile nature of standard LLM wrappers, this architecture leverages deterministic state machines to orchestrate complex reasoning tasks asynchronously. 

Built with enterprise scalability in mind, the system completely decouples the cognitive engine from the client interface, ensuring high-throughput, secure, and vendor-agnostic AI deployments.

## Architectural Topology

* **Intelligence Layer (LangGraph & Groq):** Utilizes cyclical state machines to manage agent memory, tool routing, and cognitive loops. Powered by Meta's Llama 3.1 8B on Groq's ultra-low-latency LPU clusters.
* **API Gateway (FastAPI):** A strictly typed, asynchronous Python backend enforcing a Zero-Trust cryptographic perimeter (OAuth2/JWT).
* **Client Interface (Next.js 15):** A server-side rendered (SSR) React frontend utilizing a centralized, intercepted network utility for secure credential transport.
* **State Persistence:** In-memory checkpointer integrated directly into the agent graph to maintain isolated executive thread sessions.

## Security Posture
* **Zero-Trust Execution:** The LangGraph intelligence core is completely isolated. The API gateway physically drops any payload lacking a cryptographically signed JWT before it reaches the reasoning engine.
* **Vendor Abstraction:** Core LLM models are instantiated via LCEL (LangChain Expression Language), allowing instantaneous swapping of third-party vendors (OpenAI, Anthropic, Groq, local Llama) without business logic refactoring.

## Infrastructure Initialization

### 1. Boot the Orchestration Core (Backend)
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## 2. Boot the Executive Dashboard (Frontend)
```bash
cd frontend
npm install
npm run dev

*Architected and maintained by Arpita Jaiswal.*
