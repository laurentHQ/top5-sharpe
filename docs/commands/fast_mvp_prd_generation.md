# Fast MVP PRD Generation Command

Transform a simple idea description into a minimal viable Product Requirements Document in 2-4 hours.

## Command Usage

```
/fast-mvp-prd "{SIMPLE_IDEA_DESCRIPTION}"
```

## Purpose

Rapidly transform a simple idea into an MVP-focused PRD that's ready for Task-Master-AI task decomposition. This bypasses extensive market research for quick prototyping and proof-of-concept development.

## Input Format

Replace `{SIMPLE_IDEA_DESCRIPTION}` with your concept:

```
Example: "A web app that helps users track their daily water intake with reminders 
and progress visualization. Users can set daily goals, log water consumption 
throughout the day, and see their hydration patterns over time."
```

## Expected Output

**Primary Deliverable**: `/docs/prd.txt` - Task-Master-AI compatible PRD

**Secondary Artifacts**:
- Core feature list with MVP scope
- Basic user stories and acceptance criteria
- Technical architecture approach
- Success metrics for MVP validation

## Agent Workflow

### Stage 1: Planning & Analysis (30-45 minutes)
**Agent**: tech-lead-orchestrator + Sequential MCP
- Parse and analyze the simple idea description
- Identify core MVP features and essential functionality
- Define basic user personas and primary use cases
- Determine minimal technical architecture approach

### Stage 2: Product Management (60-90 minutes)
**Agent**: product-manager
- Transform idea into product vision and positioning
- Create MVP feature list with must-have vs nice-to-have prioritization
- Write basic user stories for core functionality
- Define success metrics for MVP validation
- Document technical constraints and assumptions

### Stage 3: Research Validation (30 minutes)
**Agent**: general-purpose + WebSearch
- Quick competitive landscape scan (30-minute research limit)
- Identify obvious technical risks and constraints
- Validate feasibility with minimal research
- Find similar open-source projects or examples for reference

### Stage 4: Documentation & Structure (30-45 minutes)
**Agent**: documentation-specialist
- Structure MVP PRD for Task-Master-AI compatibility
- Write concise, actionable specifications
- Create implementation timeline for MVP scope
- Ensure clarity and completeness for task generation

## Quality Gates

### Acceptance Criteria
- [x] MVP PRD generated from simple idea description
- [x] Core features identified with basic user stories and technical approach
- [x] PRD structured for Task-Master-AI parsing and immediate task generation

### Definition of Done
- [x] MVP PRD committed as `/docs/prd.txt` in Task-Master-AI format
- [x] Essential features and constraints documented
- [x] Ready for immediate Task-Master-AI task decomposition

## Performance Targets

- **Total Duration**: 2-4 hours maximum
- **Research Phase**: ≤30 minutes
- **Feature Definition**: ≤90 minutes
- **Documentation**: ≤45 minutes
- **Planning Overhead**: ≤45 minutes

## When to Use Fast MVP Track

✅ **Use Fast MVP when**:
- Simple, well-understood concept
- Rapid prototyping or proof-of-concept needed
- Learning experiment or validation project
- Limited time or resources for extensive research
- Clear problem space with obvious solution approach

❌ **Avoid Fast MVP when**:
- Complex product with multiple stakeholders
- Market validation required before development
- Significant investment or regulatory requirements
- Unclear problem space requiring research
- Enterprise or mission-critical applications

## Integration with Task-Master-AI

The generated PRD is optimized for Task-Master-AI parsing:

```bash
# After PRD generation, use Task-Master-AI to decompose into tasks
taskmaster parse-prd --input docs/prd.txt --output tasks/tasks.json --num-tasks 8-12
```

## MCP Server Requirements

**Required MCP Servers**:
- `Sequential` - Complex analysis and planning
- `WebSearch` - Competitive research and validation
- `Context7` - Technology documentation (optional)

**Tool Requirements**:
- `Read`, `Write` - File operations
- `WebSearch` - Market research
- `TodoWrite` - Progress tracking (optional)

## Command Implementation Example

```yaml
# Task Definition for Kanban Integration
title: "Generate MVP PRD from simple idea description"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "ideation/fast-mvp-prd"
cos: Standard
estimated_duration: "2-4 hours"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - product_manager: {agent: "product-manager", cmd: "MVP PRD from simple idea with core features"}
  - researcher: {agent: "general-purpose", cmd: "quick feasibility and competitive research", tools: "WebSearch"}
  - writer: {agent: "documentation-specialist", cmd: "MVP PRD structure and Task-Master-AI optimization"}
```

## Success Metrics

**Quality Indicators**:
- PRD completeness score: ≥80% for MVP requirements
- Task-Master-AI parsing success: 100%
- Feature clarity rating: ≥4/5 from technical review
- Time to task generation: <30 minutes after PRD completion

**Output Validation**:
- All core user stories have acceptance criteria
- Technical approach is feasible with chosen stack
- Success metrics are measurable and time-bound
- MVP scope is achievable within 2-4 week development cycle

## Next Steps After PRD Generation

1. **Immediate**: Run Task-Master-AI parsing to generate task breakdown
2. **Planning**: Review generated tasks and adjust scope if needed
3. **Development**: Begin implementation using multi-agent workflow
4. **Validation**: Plan MVP testing and feedback collection strategy
5. **Iteration**: Use learnings to expand into comprehensive PRD if needed

---

*This command is designed for rapid iteration and learning. For complex products requiring extensive market validation, use the comprehensive ideation workflow instead.*