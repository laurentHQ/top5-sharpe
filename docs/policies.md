# Kanban Board Policies
*Top 5 US Stocks by Sharpe Ratio - Development Workflow*

## Board Overview

Our Kanban board manages the development workflow for the Top 5 US Stocks by Sharpe Ratio application using **strict WIP limits** and **pull policies** to optimize flow and quality.

### Board Columns & WIP Limits

```
Options (Upstream) → Ready/Committed → Design/Decompose [WIP:2] → Build:Generate [WIP:3] → Review [WIP:2] → Test [WIP:2] → Integrate/Release → Done
```

**WIP Limits Enforced**:
- **Design/Decompose**: 2 items maximum
- **Build: Generate**: 3 items maximum  
- **Review**: 2 items maximum
- **Test**: 2 items maximum

**No WIP limits**: Options, Ready/Committed, Integrate/Release, Done

## Pull Policies

### Universal Pull Policy
**"Move right only if WIP < limit and AC clarified"**

All work items must satisfy **both conditions** before advancement:
1. **Capacity Check**: Destination column must have available WIP capacity
2. **Quality Gate**: Acceptance Criteria must be clearly understood and validated

### Column-Specific Progression Criteria

#### Options (Upstream) → Ready/Committed
- **Criteria**: Business value validated, rough scope estimated
- **Responsible**: Product Owner/Business stakeholder sign-off
- **Evidence**: Acceptance criteria written, class of service assigned

#### Ready/Committed → Design/Decompose  
- **Criteria**: WIP < 2, technical approach unclear requiring design
- **Responsible**: Team pulls when capacity available
- **Evidence**: Design questions identified, stakeholder availability confirmed

#### Design/Decompose → Build: Generate
- **Criteria**: WIP < 3, technical design complete and reviewed
- **Responsible**: Implementing agent pulls when ready to start
- **Evidence**: Sequence diagrams complete, interfaces defined, no open design questions

#### Build: Generate → Review
- **Criteria**: WIP < 2, implementation complete per acceptance criteria
- **Responsible**: Developer pushes, reviewer pulls  
- **Evidence**: All acceptance criteria met, basic functionality verified

#### Review → Test
- **Criteria**: WIP < 2, static review passed with no blocking issues
- **Responsible**: Reviewer pushes, tester pulls
- **Evidence**: Code review approved, architecture compliance verified

#### Test → Integrate/Release
- **Criteria**: All tests pass, quality gates satisfied
- **Responsible**: Tester pushes, release manager pulls
- **Evidence**: Test results green, performance budgets met, security cleared

## Classes of Service (Swim Lanes)

Our board uses **4 Classes of Service** with different policies and SLAs:

### 🚨 Expedite (Red Lane)
- **Purpose**: Production incidents, critical security fixes, true system blockers
- **Policy**: Maximum 1 Expedite item in entire system at any time
- **SLA**: Runtime to resolution < 4 hours
- **Team Response**: "Swarm rule" - all available agents pause Standard work until resolved
- **Examples**: 
  - Production hotfix for data corruption
  - Security incident affecting user data
  - Demo-blocking system failure

**Pull Override**: Expedite items bypass WIP limits and move immediately to next available agent

### 📅 Fixed Date (Orange Lane)  
- **Purpose**: Time-sensitive deliverables with external commitments
- **Policy**: Planned work with firm deadlines (demo day, compliance deadlines)
- **SLA**: Must be completed by committed date with no exceptions
- **Team Response**: Protected capacity allocation, risk review required
- **Examples**:
  - Live demo day release
  - Regulatory compliance deadline
  - Conference presentation delivery

**Special Handling**: Risk reviews at 48h, 24h, and 2h before deadline

### 📋 Standard (Blue Lane)
- **Purpose**: Regular feature development and planned improvements  
- **Policy**: Normal flow following standard WIP limits and pull policies
- **SLA**: Best effort based on complexity and dependencies
- **Team Response**: Standard workflow, collaborative execution
- **Examples**:
  - New API endpoints
  - UI component development
  - Performance improvements
  - Bug fixes (non-critical)

**Workflow**: Follows all standard policies and quality gates

### 🔧 Intangible (Green Lane)
- **Purpose**: Technical debt, documentation, process improvements, governance
- **Policy**: Important but flexible timing, can be delayed for higher priority work
- **SLA**: Opportunistic scheduling, target 20% of team capacity
- **Team Response**: Work during low-priority periods or as learning opportunities
- **Examples**:
  - Documentation updates
  - CI/CD improvements  
  - Code refactoring
  - Technical research
  - Process documentation (like this policy!)

**Scheduling**: Fill gaps between Standard work, use for skill development

## WIP Limit Enforcement

### Monitoring & Compliance
- **Visual Indicators**: Column headers display current/max counts (e.g., "Design 1/2")
- **Enforcement**: Team members must verify WIP limits before pulling work
- **Accountability**: Daily standup reviews WIP limit adherence
- **Violations**: Any violation requires immediate team discussion and resolution

### WIP Limit Violation Response
1. **Immediate**: Stop pulling new work into the overflowing column
2. **Team Swarm**: Available team members assist to reduce WIP
3. **Root Cause**: Identify why limit was exceeded (quality issues, scope creep, external dependencies)
4. **Process Improvement**: Adjust policies if needed to prevent recurrence

### Dynamic WIP Adjustment
WIP limits may be temporarily adjusted only by team consensus with:
- **Justification**: Clear business need and time-bounded change
- **Documentation**: Decision rationale recorded in team log
- **Review**: Revert or permanently adjust within 2 sprints

## Blocked Work Escalation

### Escalation Procedures

#### Level 1: Self-Resolution (0-24 hours)
- **Action**: Individual attempts to resolve through research, experimentation, or consultation
- **Documentation**: Log blocker in work item with attempted solutions
- **Timeout**: Escalate after 24 hours if no progress

#### Level 2: Team Support (24-48 hours)  
- **Action**: Raise in daily standup, request team assistance
- **Response**: Team provides pairing, knowledge sharing, or alternative approaches
- **Documentation**: Update work item with team consultation results
- **Timeout**: Escalate after additional 24 hours if blocked

#### Level 3: External Dependencies (48+ hours)
- **Action**: Engage external stakeholders, vendors, or management
- **Response**: Formal dependency tracking, stakeholder communication, alternative planning
- **Documentation**: Escalation log with stakeholder contacts and commitments
- **Management**: May trigger scope reduction or timeline adjustment

### Blocker Categories & Response

**🔴 Critical Blockers** (Production impact, security risk)
- **Response**: Immediate escalation to Level 3, consider Expedite classification
- **Timeline**: Resolution required within 4 hours

**🟡 Standard Blockers** (Feature development impact)  
- **Response**: Follow standard escalation timeline
- **Timeline**: Resolution target within 48 hours

**🟢 Minor Blockers** (Documentation, nice-to-have features)
- **Response**: Work around where possible, batch with similar issues
- **Timeline**: Resolution within 1 week, may be deferred

## Flow Metrics & Measurement

### Primary Flow Metrics

#### Cycle Time
- **Definition**: Time from "Ready/Committed" to "Done" 
- **Target**: Standard work ≤ 2 weeks, Expedite ≤ 4 hours
- **Measurement**: Weekly trend analysis with blockers identified
- **Improvement**: Focus on eliminating delays and reducing batch sizes

#### Throughput  
- **Definition**: Number of work items completed per week
- **Target**: Maintain consistent velocity with quality
- **Measurement**: Weekly completion count by class of service
- **Improvement**: Balance WIP limits and team capacity

#### Work In Progress (WIP)
- **Definition**: Total items actively being worked (Design through Test)
- **Target**: Stay within column limits, minimize total WIP
- **Measurement**: Daily WIP count and limit compliance
- **Improvement**: Optimize WIP limits based on flow patterns

#### Lead Time
- **Definition**: Time from "Options" entry to "Done"
- **Target**: Provide predictable delivery estimates
- **Measurement**: Monthly rolling average by complexity
- **Improvement**: Reduce queue time and eliminate waste

### Quality Metrics

#### Defect Escape Rate
- **Definition**: Issues found after "Test" column completion
- **Target**: < 5% of delivered features require post-release fixes
- **Measurement**: Track issues requiring rollback or hotfixes
- **Improvement**: Strengthen testing practices and review quality

#### Rework Rate
- **Definition**: Items returned from downstream columns
- **Target**: < 10% rework rate between adjacent columns
- **Measurement**: Weekly tracking of backward moves
- **Improvement**: Improve handoff criteria and communication

### Improvement Process

#### Weekly Metrics Review
- **When**: Every Friday during team retrospective
- **Participants**: Full development team
- **Agenda**: Review metrics, identify trends, plan improvements
- **Outcomes**: Action items for process enhancement, policy adjustments

#### Monthly Policy Review
- **When**: Last Friday of each month  
- **Participants**: Team + Product Owner
- **Agenda**: Review policy effectiveness, WIP limit optimization, class of service balance
- **Outcomes**: Policy updates, team agreements, training needs

#### Continuous Improvement Triggers
- **Metric Degradation**: Any metric trending negative for 2 consecutive weeks
- **Policy Violations**: Repeated WIP limit violations or pull policy failures  
- **Team Feedback**: Issues raised in daily standups or retrospectives
- **External Pressure**: Changing business priorities or delivery commitments

## Team Agreements

### Daily Operations
- **Standup Focus**: WIP review, blocker identification, pull opportunities
- **Board Updates**: Real-time movement, status changes within 2 hours
- **Communication**: Slack for quick updates, board comments for context
- **Handoffs**: Clear completion criteria, documented in work item

### Quality Standards  
- **Definition of Done**: Each work item has specific, measurable DoD
- **Acceptance Criteria**: Must be clear before pulling from Ready
- **Testing Requirements**: Automated tests required for all Standard work
- **Review Standards**: Code review mandatory, architecture review for design changes

### Collaboration Protocols
- **Pairing**: Encouraged for complex work, required for knowledge transfer
- **Swarming**: Expedite and blocked items get priority team attention
- **Knowledge Sharing**: Document decisions, share learnings in team channels
- **Skill Development**: Use Intangible work for training and experimentation

---

*This policy document is a living document, updated based on team learning and process improvement. Last updated: [Current Date]*