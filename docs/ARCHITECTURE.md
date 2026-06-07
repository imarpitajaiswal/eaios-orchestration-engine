# Enterprise Agentic AI Operating System (EAIOS)
## High-Level Architecture (HLA) Document

### 1. System Overview
EAIOS is a secure, multi-agent AI orchestration platform designed for enterprise environments. It enables autonomous, specialized AI agents to execute complex business workflows while strictly adhering to compliance, observability, and human-in-the-loop (HITL) governance.

### 2. Core Architecture Tiers
- **Client Tier:** Next.js 15, TypeScript, Tailwind CSS, shadcn/ui.
- **Orchestration & Logic Tier:** Python 3.12, FastAPI, LangGraph, PydanticAI.
- **Data & Memory Tier:** PostgreSQL (Relational/State), Redis (Caching/Broker), Qdrant (Vector/Semantic Memory).
- **Observability & Governance:** LangSmith, OpenTelemetry, native compliance gating.

### 3. Multi-Agent Topology
The system utilizes a hierarchical agentic structure managed via LangGraph:
1.  **Supervisor Agent:** The central routing mechanism. Analyzes user intent, delegates tasks to sub-agents, and synthesizes final output.
2.  **Research Agent:** Integrates with MCP (Model Context Protocol) to query enterprise knowledge bases and external APIs safely.
3.  **Analysis Agent:** Performs quantitative and qualitative reasoning on data retrieved by the Research Agent.
4.  **Execution Agent:** Drafts artifacts, executes code, or triggers external webhooks based on approved parameters.
5.  **Compliance Agent:** An independent, hard-coded guardrail agent that evaluates all outputs against enterprise safety, PII, and security policies before returning data to the Supervisor.

### 4. Data Flow & RAG Integration
- **Ingestion:** Documents are parsed, chunked, embedded via external models, and stored in Qdrant.
- **Retrieval:** The Research Agent queries Qdrant using hybrid search (semantic + keyword).
- **Generation:** Context is injected into the LLM prompt. Output is strictly formatted via PydanticAI to guarantee JSON schema compliance.

### 5. Deployment Infrastructure
Containerized via Docker, initially deployed via Railway, with an established Terraform migration path for AWS (EKS/ECS) integration.