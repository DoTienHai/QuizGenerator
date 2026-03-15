# SDLC Phases (Software Development Life Cycle)

**Created**: 2026-03-15  
**Purpose**: Document the major phases of Software Development Life Cycle

---

## Overview

SDLC is a structured process that guides the creation of software from initial concept to deployment and maintenance. QuizGenerator project follows a 6-phase model:

1. **Phase 1: Requirement Analysis** (Planning + Detailed Analysis)
2. **Phase 2: Detail Design** (System Architecture, Database, UI/UX, API, Security, Tech Stack)
3. **Phase 3: Development** (Code Implementation)
4. **Phase 4: Testing** (Quality Assurance)
5. **Phase 5: Deployment** (Release to Production)
6. **Phase 6: Maintenance** (Support & Updates)

---

## Phase 1: Requirement Analysis

**Objective**: Define project scope, requirements, and detailed analysis

**Activities**:
- Identify project goals and business objectives
- Analyze feasibility (technical, financial, operational)
- Define scope and constraints
- Gather detailed functional requirements
- Define use cases and user stories
- Create data models and system specifications
- Analyze business processes
- Identify system constraints and dependencies
- Create requirement analysis document

**Deliverables**:
- Project Charter
- Requirement Analysis Document (RA) - SW1_Requirement_Analysis.md
- Functional Requirements Document
- Use Case Diagrams
- Data Flow Diagrams (DFD)
- Technical Specifications

---

## Phase 2: Detail Design

**Objective**: Create comprehensive system design and specifications

**Activities**:
- System architecture design
- Database schema design
- UI/UX design and wireframes
- API design and contracts
- Security design and threat analysis
- Technology stack selection and justification

**Deliverables**:
- System Architecture Document (SW2_System_Architecture.md)
- Database Design (SW2_Database_Schema.md)
- UI/UX Wireframes (SW2_UI_UX_Wireframes.md)
- API Specification (SW2_API_Design.md)
- Security Design (SW2_Security_Design.md)
- Technology Stack (SW2_Technology_Stack.md)

---

## Phase 3: Development (Implementation)

**Objective**: Write code and build the system

**Activities**:
- Write code following design specifications
- Version control management
- Code reviews and quality checks
- Unit testing
- Integration of components
- Documentation of code

**Deliverables**:
- Source Code
- Code Documentation
- Build/Deployment Scripts
- Version Control History

---

## Phase 4: Testing

**Objective**: Verify system quality and correctness

**Activities**:
- Unit testing (developer testing)
- Integration testing (component interaction)
- System testing (end-to-end)
- User Acceptance Testing (UAT)
- Performance testing
- Security testing
- Bug detection and reporting

**Deliverables**:
- Test Cases and Test Plans
- Test Results Report
- Bug Reports
- UAT Signoff

---

## Phase 5: Deployment

**Objective**: Release system to production environment

**Activities**:
- Environment setup (production)
- Data migration (if applicable)
- System deployment
- User training
- Go-live support
- Rollback plan readiness

**Deliverables**:
- Deployment Plan
- Deployment Checklist
- User Training Materials
- System Documentation
- Go-Live Report

---

## Phase 6: Maintenance & Support

**Objective**: Ensure system stability and handle changes

**Activities**:
- Monitor system performance
- Fix bugs discovered in production
- Provide user support
- Handle change requests
- Performance optimization
- Security patches
- Plan future enhancements

**Deliverables**:
- Maintenance Logs
- Incident Reports
- Patch Release Notes
- Enhancement Requests

---

## Relationship to QuizGenerator Project

**Current Status**: 
- ✅ Phase 1: Requirement Analysis (COMPLETED)
  - Requirement Analysis Document: SW1_Requirement_Analysis.md
  - Single-user model, 8 FRs, MVP scope

- ✅ Phase 2: Detail Design (COMPLETED)
  - System Architecture: SW2_System_Architecture.md
  - Database Schema: SW2_Database_Schema.md
  - UI/UX Wireframes: SW2_UI_UX_Wireframes.md
  - API Design: SW2_API_Design.md
  - Security Design: SW2_Security_Design.md
  - Technology Stack: SW2_Technology_Stack.md

**Upcoming**:
- Phase 3: Development - Implement Flask app with all 8 FRs
- Phase 4: Testing - Unit, integration, system, UAT
- Phase 5: Deployment - Release to user environment
- Phase 6: Maintenance - Support and future enhancements

---

## QuizGenerator Development Model

**Approach**: **Sequential Waterfall** (suitable for well-defined MVP)

**Rationale**:
- ✅ Clear, complete requirements (Phase 1)
- ✅ Comprehensive design (Phase 2)
- ✅ Stable scope (MVP focused, no Phase 2 features)
- ✅ Quality critical (scoring accuracy, data integrity)

**Model Benefits**:
- Each phase has clear deliverables
- Design documented before coding starts
- Reduces rework and scope creep
- Clear communication with users

**Future Enhancement** (Phase 2+ features):
- May shift toward Agile for faster iterations
- Continuous deployment if needed

---

## Key Principles

1. **Requirements First**: Clear requirements prevent costly rework
2. **Design Before Code**: Good design reduces implementation issues
3. **Test Throughout**: Early testing catches bugs cheaply
4. **Documentation**: Clear docs enable maintenance
5. **Quality**: Build quality in, don't test it in
6. **Communication**: Keep stakeholders informed
7. **Flexibility**: Adapt to changing requirements

---

## Metrics & Success Criteria

| Phase | Success Metric |
|-------|---|
| Phase 1 (Requirements) | Clear, measurable requirements defined, all 8 FRs specified |
| Phase 2 (Design) | Complete technical design, 6 design documents approved |
| Phase 3 (Development) | Code follows design 100%, all 8 FRs implemented |
| Phase 4 (Testing) | 100% requirements coverage, zero critical bugs |
| Phase 5 (Deployment) | Smooth launch, user can access and use app |
| Phase 6 (Maintenance) | <1% critical issues, fast bug fixes, user support |

