# 000 Project Ideation & Requirements Tasks

Strategic ideation and requirements analysis tasks that transform initial concepts into comprehensive Product Requirements Documents (PRDs). These tasks provide the critical foundation that enables structured task decomposition and multi-agent development workflows.

## Task Group Priority
**Phase**: Concept Foundation (Pre-Planning)
**Dependencies**: None (starting point for new projects)
**Blocks**: All planning and development work
**Estimated Duration**: 1-2 days (full process) or 2-4 hours (fast MVP)

---

## Fast MVP Track

### Task 0: Fast MVP PRD Generation from Simple Idea

```yaml
title: "Generate MVP PRD from simple idea description"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "ideation/fast-mvp-prd"
description: |
  Rapidly transform a simple idea description into a minimal viable Product Requirements Document.
  This fast track bypasses extensive research for quick prototyping and proof-of-concept development.
acceptance_criteria:
  - "MVP PRD generated from idea placeholder: {SIMPLE_IDEA_DESCRIPTION}"
  - "Core features identified with basic user stories and technical approach"
  - "PRD structured for Task-Master-AI parsing and immediate task generation"
cos: Standard
definition_of_done:
  - "MVP PRD committed as /docs/prd.txt in Task-Master-AI format"
  - "Essential features and constraints documented"
  - "Ready for immediate Task-Master-AI task decomposition"
todo_list:
  planner:
    - "Parse simple idea: {SIMPLE_IDEA_DESCRIPTION}"
    - "Identify core MVP features and essential functionality"
    - "Define basic user personas and primary use cases"
    - "Determine minimal technical architecture approach"
  product_manager:
    - "Transform idea into product vision and positioning"
    - "Create MVP feature list with must-have vs nice-to-have"
    - "Write basic user stories for core functionality"
    - "Define success metrics for MVP validation"
    - "Document technical constraints and assumptions"
  researcher:
    - "Quick competitive landscape scan (30-minute research)"
    - "Identify obvious technical risks and constraints"
    - "Validate feasibility with minimal research"
    - "Find similar open-source projects or examples"
  writer:
    - "Structure MVP PRD for Task-Master-AI compatibility"
    - "Write concise, actionable specifications"
    - "Create implementation timeline for MVP scope"
    - "Ensure clarity and completeness for task generation"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - product_manager: {agent: "product-manager", cmd: "MVP PRD from simple idea with core features"}
  - researcher: {agent: "general-purpose", cmd: "quick feasibility and competitive research", tools: "WebSearch"}
  - writer: {agent: "documentation-specialist", cmd: "MVP PRD structure and Task-Master-AI optimization"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

**Input Format Example:**
```
SIMPLE_IDEA_DESCRIPTION: "A web app that helps users track their daily water intake 
with reminders and progress visualization. Users can set daily goals, log water 
consumption throughout the day, and see their hydration patterns over time."
```

**Fast Track Benefits:**
- **Speed**: 2-4 hours vs 1-2 days for full research
- **MVP Focus**: Essential features only, defer nice-to-have
- **Quick Validation**: Rapid prototype to test core concept
- **Iterative**: Can expand with full research track later

---

## Comprehensive Research Track

---

## Task 1: Idea Validation & Market Research

```yaml
title: "Validate project idea through market research and feasibility analysis"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "ideation/market-validation"
description: |
  Conduct comprehensive market research and technical feasibility analysis to validate the project concept.
  This task ensures the idea addresses real market needs and is technically achievable within project constraints.
acceptance_criteria:
  - "Market research report documenting similar solutions, gaps, and opportunities"
  - "Technical feasibility assessment with risk analysis and mitigation strategies"
  - "Competitive landscape analysis with feature comparison matrix"
cos: Standard
definition_of_done:
  - "Research findings documented in /docs/research/market_analysis.md"
  - "Technical feasibility confirmed with architecture constraints identified"
  - "Stakeholder validation recorded with go/no-go decision"
todo_list:
  planner:
    - "Define research scope and key validation questions"
    - "Identify target market segments and user personas"
    - "Plan competitive analysis methodology and comparison criteria"
    - "Define technical feasibility assessment framework"
  researcher:
    - "Conduct market research using web search and industry sources"
    - "Analyze competitive landscape and feature gaps"
    - "Research technical constraints and implementation challenges"
    - "Gather user feedback and market validation data"
    - "Synthesize findings into actionable insights"
  analyst:
    - "Perform risk assessment and feasibility analysis"
    - "Create competitive feature comparison matrix"
    - "Evaluate technical architecture options and constraints"
    - "Generate recommendations and decision framework"
  reviewer:
    - "Validate research methodology and source credibility"
    - "Review risk assessment completeness and accuracy"
    - "Check feasibility conclusions against technical constraints"
    - "Verify market analysis supports business case"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - researcher: {agent: "general-purpose", cmd: "comprehensive market research with web search validation", tools: "WebSearch, Read, Write"}
  - analyst: {agent: "business-analyst", cmd: "feasibility analysis and competitive assessment"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 2: Requirements Discovery & Stakeholder Analysis

```yaml
title: "Discover functional requirements and analyze stakeholder needs"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "ideation/requirements-discovery"
description: |
  Systematically gather and analyze functional and non-functional requirements from all stakeholders.
  This task creates the requirements foundation that will inform PRD development and technical design.
acceptance_criteria:
  - "Complete stakeholder map with roles, needs, and success criteria"
  - "Functional requirements documented with user stories and acceptance criteria"
  - "Non-functional requirements specified with measurable targets"
cos: Standard
definition_of_done:
  - "Requirements documented in structured format in /docs/requirements/"
  - "Stakeholder needs validated and prioritized"
  - "Requirements traceability matrix created"
todo_list:
  planner:
    - "Design stakeholder analysis framework and interview approach"
    - "Plan requirements gathering methodology and documentation structure"
    - "Define requirement categories and prioritization criteria"
    - "Create validation and traceability framework"
  analyst:
    - "Conduct stakeholder analysis and mapping"
    - "Facilitate requirements gathering sessions"
    - "Document functional requirements as user stories"
    - "Specify non-functional requirements with measurable criteria"
    - "Create requirements prioritization matrix"
    - "Develop requirements traceability documentation"
  researcher:
    - "Research industry standards and best practices"
    - "Validate requirements against market research findings"
    - "Identify regulatory and compliance requirements"
    - "Research technical constraints and platform requirements"
  reviewer:
    - "Review requirements completeness and clarity"
    - "Validate stakeholder needs alignment"
    - "Check requirements feasibility and consistency"
    - "Verify traceability and prioritization logic"
agent_sequence:
  - planner: {tooling: "Sequential MCP + business-analyst"}
  - analyst: {agent: "business-analyst", cmd: "stakeholder analysis and requirements gathering"}
  - researcher: {agent: "general-purpose", cmd: "research industry standards and compliance requirements", tools: "WebSearch, Context7"}
  - reviewer: {agent: "business-analyst", cmd: "requirements validation and gap analysis"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 3: Solution Architecture & Technology Selection

```yaml
title: "Design solution architecture and select technology stack"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "ideation/solution-architecture"
description: |
  Design high-level solution architecture and select appropriate technology stack based on requirements.
  This task establishes the technical foundation and constraints that will guide implementation planning.
acceptance_criteria:
  - "Solution architecture diagram with component interactions and data flow"
  - "Technology stack selection with justification matrix"
  - "Deployment architecture and infrastructure requirements defined"
cos: Standard
definition_of_done:
  - "Architecture diagrams committed to /docs/architecture/"
  - "Technology decisions documented with trade-off analysis"
  - "Infrastructure requirements and constraints specified"
todo_list:
  planner:
    - "Analyze requirements to identify architectural patterns"
    - "Plan technology evaluation criteria and methodology"
    - "Define architecture design principles and constraints"
    - "Plan infrastructure and deployment strategy"
  architect:
    - "Design high-level solution architecture"
    - "Create component interaction and data flow diagrams"
    - "Evaluate technology stack options against requirements"
    - "Design deployment architecture and infrastructure"
    - "Document architectural decisions and trade-offs"
    - "Create technology selection justification matrix"
  researcher:
    - "Research technology options and industry best practices"
    - "Validate architecture patterns against similar projects"
    - "Research performance benchmarks and scalability data"
    - "Investigate security and compliance implications"
  reviewer:
    - "Review architecture alignment with requirements"
    - "Validate technology selection rationale"
    - "Check scalability and performance considerations"
    - "Verify security and compliance coverage"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - architect: {agent: "react-component-architect", cmd: "solution architecture design and technology selection"}
  - researcher: {agent: "general-purpose", cmd: "technology research and validation", tools: "WebSearch, Context7"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 4: PRD Generation & Task Decomposition Preparation

```yaml
title: "Generate comprehensive PRD and prepare for task decomposition"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "ideation/prd-generation"
description: |
  Synthesize all research and analysis into a comprehensive Product Requirements Document.
  This task creates the authoritative specification that will drive Task-Master-AI task decomposition.
acceptance_criteria:
  - "Complete PRD document with all sections: overview, requirements, architecture, success metrics"
  - "PRD structured for optimal Task-Master-AI parsing and task generation"
  - "Success metrics and KPIs defined with measurement strategy"
cos: Standard
definition_of_done:
  - "PRD committed as /docs/prd.txt in Task-Master-AI compatible format"
  - "PRD review completed by all stakeholders"
  - "Task decomposition readiness validated"
todo_list:
  planner:
    - "Design PRD structure optimized for Task-Master-AI parsing"
    - "Plan content synthesis methodology from research artifacts"
    - "Define success metrics and measurement framework"
    - "Plan stakeholder review and approval process"
  product_manager:
    - "Synthesize market research into product positioning"
    - "Transform requirements into product feature specifications"
    - "Create user journey and experience specifications"
    - "Define success metrics and KPIs with measurement plan"
    - "Write comprehensive PRD in Task-Master-AI format"
    - "Include technical architecture and constraints"
  writer:
    - "Structure PRD for clarity and Task-Master-AI compatibility"
    - "Ensure consistent terminology and clear specifications"
    - "Create executive summary and overview sections"
    - "Develop implementation timeline and milestone framework"
  reviewer:
    - "Review PRD completeness against requirements"
    - "Validate technical feasibility and architecture alignment"
    - "Check Task-Master-AI compatibility and parsing readiness"
    - "Verify stakeholder needs coverage and success metrics"
agent_sequence:
  - planner: {tooling: "Sequential MCP + product-manager"}
  - product_manager: {agent: "product-manager", cmd: "comprehensive PRD creation with technical specifications"}
  - writer: {agent: "documentation-specialist", cmd: "PRD structure and clarity optimization"}
  - reviewer: {agent: "business-analyst", cmd: "PRD validation and stakeholder alignment"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: ["Task 1: Market validation", "Task 2: Requirements discovery", "Task 3: Solution architecture"]
```

---

## Task Group Dependencies

**Provides Foundation For:**
- Task-Master-AI PRD parsing and task generation
- Project planning and task decomposition (00_project_planning.md)
- All development task groups (01-06)
- Stakeholder alignment and project governance

**Establishes Framework For:**
- Product vision and market positioning
- Technical architecture and technology decisions
- Success metrics and measurement strategy
- Project scope and timeline planning

**Quality Gates:**
- Market validation confirms project viability
- Requirements coverage validated by all stakeholders
- Technical architecture feasible within constraints
- PRD complete and Task-Master-AI compatible

**Research Integration:**
- Web search for market research and competitive analysis
- Context7 for technology documentation and best practices
- Task-Master-AI for PRD parsing validation
- Sequential MCP for complex analysis and synthesis

**Performance Targets:**
- **Fast MVP Track**: Total completion: <4 hours
- **Comprehensive Track**: 
  - Market research completion: <1 day
  - Requirements gathering: <1 day  
  - Architecture design: <0.5 day
  - PRD generation: <0.5 day
  - Total ideation cycle: <3 days maximum

**Track Selection Guidelines:**
- **Use Fast MVP** when: Simple concept, rapid prototyping, proof-of-concept, learning experiment
- **Use Comprehensive** when: Complex product, market validation needed, significant investment, regulatory requirements