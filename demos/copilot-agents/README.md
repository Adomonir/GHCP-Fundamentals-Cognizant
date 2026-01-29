# Copilot Agents Demo

Use the following 3 files to setup your Copilot Agents demo. 
Paste the ISSUE.md file into a new issue in that repository. 

## What this demo shows
- Assign an issue to Copilot to start an agent task
- Monitor progress in AgentHQ
- Re-steer mid-session with a new requirement
- Review the resulting PR like a teammate’s work

## Demo files
- `ISSUE.md` contains the exact issue text to copy/paste into GitHub
- `STEER.md` contains the mid-session requirement change to paste while the agent is working

## Quick demo steps
1. Create a new GitHub Issue by copying the Title and Body from `ISSUE.md`
2. Assign the issue to Copilot to start the agent task
3. Open AgentHQ to monitor progress
4. Paste `STEER.md` into the agent session to re-steer the work
5. Review the PR diff for clarity, completeness, and constraints.
6. Verify the PR edited the README.md file by adding priority levels plus the steered examples. 

---

## Ticket Triage Policy

We triage support tickets using Severity and Priority to ensure consistent handling.

### Severity levels
- **Low**: Minor annoyance with an easy workaround
- **Medium**: Meaningful user impact but workarounds exist
- **High**: Blocks key workflows or causes data loss

### Priority levels
- **P0**: Critical - immediate action required (production down, data loss)
- **P1**: Urgent - resolve within 24 hours (major feature broken, security issue)
- **P2**: Important - resolve within 1 week (moderate impact, plan needed)
- **P3**: Normal - resolve when capacity allows (minor issues, enhancements)

### Severity to Priority mapping
- High Severity → P0 or P1 (depending on scope)
- Medium Severity → P1 or P2 (depending on impact)
- Low Severity → P2 or P3 (depending on demand)

### How to triage in 60 seconds
1. **Read** the ticket description and reproduce steps
2. **Assess** severity based on user impact
3. **Assign** priority based on severity and urgency
4. **Label** the ticket with severity and priority tags
5. **Route** to appropriate team or owner
