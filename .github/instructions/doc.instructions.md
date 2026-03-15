---
description: Create documentation files for the QuizGenerator project
applyTo: 'When creating project documentation, technical specifications, or guides'
---

# Documentation File Creation Rules

## When to Create Documentation Files
- When documenting project features, architecture, or technical specifications
- User asks for creation of guides, tutorials, or process documentation
- Project needs API documentation, deployment guides, or setup instructions
- Creating feature specifications or design documents

## File Naming Convention
- **Format**: `FEATURE_OR_TOPIC_NAME.md` (uppercase letters, underscores for spaces)
- **Examples**: `API_ENDPOINTS.md`, `EXCEL_TEMPLATE_GUIDE.md`, `DEPLOYMENT_SETUP.md`, `DATABASE_SCHEMA.md`
- Keep names concise and descriptive

## Documentation File Structure

### Header & Metadata
```markdown
# Feature/Topic Name

**Last Updated**: YYYY-MM-DD  
**Version**: 1.0  
**Status**: Draft | Final | In Progress  
**Author**: [AI Assistant]

## Overview
Brief description of what this document covers (1-2 sentences).
```

### Table of Contents (Required if 3+ sections)
Automatically generated list of all level-2 headings with anchor links:
```markdown
## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
- [Subsection](#subsection)
```

### Content Guidelines
- **Language**: English (all documentation in English)
- **Format**: Markdown with proper structure
- **Code Examples**: Include when explaining technical features
- **Keep it clear**: Use bullet points, numbered lists, tables when appropriate
- **Best Practices**: Document both "what" and "why"

### Code Blocks
Include language identifier for syntax highlighting:
````markdown
```python
# Python code example
def example_function():
    pass
```

```sql
-- SQL queries
SELECT * FROM table;
```

```bash
# Shell commands
python app.py
```
````

## File Organization

### Directory Structure
All documentation files go into appropriate folders:
```
QuizGenerator/
├── docs/                          # Main documentation folder
│   ├── FEATURES.md               # Feature documentation
│   ├── API.md                    # API endpoints
│   ├── SETUP.md                  # Setup & installation guide
│   ├── DEPLOYMENT.md             # Deployment instructions
│   ├── DATABASE.md               # Database schema (can reference note/)
│   └── ARCHITECTURE.md           # Architecture overview
```

### Documentation vs Notes
- **Documentation** (docs/): Formal, stable, reference material for all developers
- **Notes** (note/): Personal notes, quick findings, implementation details
- **Internal Reference**: Doc can reference content from notes when needed

## Content Standards

### Feature Documentation
- Overview & purpose
- Inputs/outputs (if applicable)
- Usage examples
- Error handling
- Related features/dependencies

### API Documentation
- Endpoint URL and HTTP method
- Request parameters (with types & constraints)
- Response format (success & error cases)
- Example requests/responses
- Authentication/security notes

### Setup/Installation Guide
- Prerequisites & system requirements
- Step-by-step installation
- Configuration details
- Troubleshooting common issues
- Verification steps

### Database Documentation
- Schema overview (tables, relationships)
- Column definitions & constraints
- Indexes
- Example queries
- Optimization notes

## Examples

### Example 1: API Documentation
```markdown
# QuizGenerator API Endpoints

**Last Updated**: 2026-03-03  
**Version**: 1.0  
**Status**: Final

## Overview
Complete API reference for QuizGenerator Flask application endpoints.

## Table of Contents
- [Upload Quiz](#upload-quiz)
- [Get Quiz Config](#get-quiz-config)
- [Submit Quiz](#submit-quiz)

## Upload Quiz

**Endpoint**: `POST /upload`  
**Description**: Upload an Excel file containing quiz questions

### Request
- **Content-Type**: multipart/form-data
- **Parameters**: 
  - `file` (required): Excel file (.xlsx, .xls)

### Response (201 Created)
```json
{
  "quiz_id": "abc-123",
  "total_questions": 100,
  "message": "File uploaded successfully"
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Invalid Excel template: missing column 'question'"
}
```
```

### Example 2: Feature Guide
```markdown
# Quiz Configuration Feature

**Last Updated**: 2026-03-03  
**Version**: 1.0  
**Status**: Final

## Overview
Users can configure number of questions and exam duration before taking a quiz.

## Table of Contents
- [How It Works](#how-it-works)
- [Configuration Parameters](#configuration-parameters)
- [Frontend Implementation](#frontend-implementation)
- [Validation Rules](#validation-rules)

## Configuration Parameters

1. **Number of Questions** (num_questions)
   - Range: 1 to total available questions
   - Type: Integer
   - Default: 20
   - UI: Dropdown select

2. **Exam Duration** (exam_duration)
   - Range: >= 1 minute
   - Type: Integer (minutes)
   - Default: 60
   - UI: Numeric input
```

## Quality Checklist
- [ ] Clear, professional English
- [ ] Proper markdown formatting
- [ ] Table of Contents included (if 3+ sections)
- [ ] Code examples where applicable
- [ ] Links to related documentation
- [ ] Metadata (date, version, status)
- [ ] No outdated information

## File Naming Examples
✅ Good:
- `API_ENDPOINTS.md`
- `EXCEL_TEMPLATE_GUIDE.md`
- `QUIZ_SCORING_LOGIC.md`
- `SETUP_INSTRUCTIONS.md`

❌ Avoid:
- `doc1.md` (too generic)
- `api_endpoints.md` (should be uppercase)
- `setup installation guide.md` (spaces instead of underscores)