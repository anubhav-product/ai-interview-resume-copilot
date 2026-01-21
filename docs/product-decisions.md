Product Decisions & PM Judgment


1. Problem Framing

Hiring-related AI tools often fall into two extremes:

Manual, time-consuming resume screening with low consistency

Fully automated tools that provide opaque scores or hire/reject recommendations

Both approaches create trust issues for recruiters and frustration for candidates.

Product goal:
Design an AI system that supports human decision-making by providing clear, explainable insights—without automating hiring decisions.

2. Why This Is a Decision-Support Tool (Not Automation)
Decision Made

The product does not recommend hiring or rejection decisions.

Reasoning

Hiring decisions involve context beyond resumes (culture, interviews, references)

Automated decisions increase legal, ethical, and bias risks

Users trust systems more when AI supports—not replaces—their judgment

Tradeoff

Lower automation

Higher trust, adoption, and responsible use

3. Why No Numerical “Fit Score” Is Used
Decision Made

The product avoids numeric fit scores (e.g., 72% match).

Reasoning

Numeric scores imply false precision

Small differences in scores are often meaningless

Users may over-trust numbers without understanding reasoning

Alternative Chosen

A qualitative job-readiness indicator:

Strong

Developing

Early

Each level is accompanied by a short explanation.

4. Explainability as a First-Class Feature
Decision Made

Every identified skill gap includes:

Why the skill matters for the role

How the candidate can improve

Reasoning

Raw gap lists are not actionable

Explainability increases trust and usability

Candidates need guidance, not just diagnosis

Product Impact

Reduces user anxiety

Encourages focused improvement

Improves perceived fairness of AI outputs

5. Suggested Job Roles as Guidance, Not Ranking
Decision Made

The product suggests job roles or career directions, not ranked job matches.

Reasoning

Career paths are exploratory, not deterministic

Ranking roles could mislead users into false certainty

Guidance supports learning and discovery

Guardrails Applied

No “best fit” label

No ranking or ordering by score

Each role includes skills to strengthen

6. Separate Perspectives: Recruiter vs Candidate
Decision Made

The product is designed to serve two user perspectives:

Candidates seeking guidance and improvement

Recruiters seeking structured insights and interview focus areas

Reasoning

Both users interact with the same data differently

Candidates value roadmaps and learning paths

Recruiters value readiness signals and interview guidance

Product Approach

Same AI intelligence, different framing and emphasis.

7. Handling Bias & Sensitive Attributes
Decision Made

The system explicitly ignores:

Age

Gender

Caste

Other sensitive attributes

Reasoning

These attributes are irrelevant to role fit

Including them increases bias risk

Aligns with responsible AI best practices

8. Scope Decisions: What We Chose Not to Build (Yet)
Explicitly Excluded Features

Automated resume ranking across candidates

ATS integrations

Job scraping or auto-apply

Persistent storage of resumes

Reasoning

These add complexity without improving core user value

Increase legal, privacy, and bias concerns

Distract from validating core product value

9. Success Metrics (Qualitative)

Instead of traditional ML accuracy metrics, early success is defined as:

Users reporting clarity on next steps

Recruiters finding interview focus areas useful

Reduced confusion compared to raw resume screening

10. Future Expansion (If Validated)

Potential future directions include:

Skill roadmaps with learning resources

Downloadable career reports

Recruiter dashboards (without ranking)

Resume improvement suggestions

All future features must maintain:

Explainability

Human-in-the-loop control

Avoidance of automated decisions

Summary

This product prioritizes:

Trust over automation

Explainability over scores

Guidance over judgment
