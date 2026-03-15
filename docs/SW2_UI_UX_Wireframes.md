# SW2: UI/UX Design and Wireframes - QuizGenerator

**Last Updated**: 2026-03-15  
**Version**: 1.0  
**Status**: Design Phase  
**Author**: AI Assistant

---

## Table of Contents

- [Design Principles](#design-principles)
- [User Flow](#user-flow)
- [Page Layouts & Wireframes](#page-layouts--wireframes)
- [Component Design](#component-design)
- [Color Scheme & Typography](#color-scheme--typography)
- [Responsive Design](#responsive-design)
- [Accessibility Guidelines](#accessibility-guidelines)
- [Interactions & Animations](#interactions--animations)

---

## Design Principles

### 1. Simplicity
- Minimal interface elements
- Clear information hierarchy
- One primary action per page

### 2. Clarity
- Obvious button labels
- Clear error messages
- Explicit status indicators

### 3. Consistency
- Same components look/behave identically
- Consistent spacing and alignment
- Uniform color usage

### 4. Feedback
- Immediate response to user actions
- Clear success/error messages
- Visual confirmation before destructive actions

### 5. Efficiency
- Minimal clicks to reach goal
- Default values pre-filled
- Quick form completion

### 6. Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader friendly

---

## User Flow

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ↓
┌──────────────────────────┐
│  Home Page               │
│  - Welcome message       │
│  - Upload button         │
│  - View past quizzes     │
└────────┬─────────────────┘
         │
         ├─→ [Upload New Quiz]
         │
         ↓
┌──────────────────────────┐
│  Upload Page             │
│  - File input            │
│  - Upload button         │
│  - Validation messages   │
└────────┬─────────────────┘
         │
     [Success]
         │
         ↓
┌──────────────────────────┐
│  Quiz List               │
│  - Recently uploaded     │
│  - Select quiz           │
│  - Start exam button     │
└────────┬─────────────────┘
         │
         ├─→ [Select Quiz & Start Exam]
         │
         ↓
┌──────────────────────────┐
│  Config Page             │
│  - Num questions input   │
│  - Duration input        │
│  - Start button          │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Exam Page               │
│  - Question display      │
│  - Answer options        │
│  - Timer                 │
│  - Navigation buttons    │
└────────┬─────────────────┘
         │
    [All answered OR time expired]
         │
         ↓
┌──────────────────────────┐
│  Results Page            │
│  - Score summary         │
│  - Statistics            │
│  - Take another exam     │
│  - Home button           │
└────────┬─────────────────┘
         │
         ├─→ [Take Another Exam] → Config Page
         └─→ [Home] → Home Page
```

---

## Page Layouts & Wireframes

### Page 1: Home Page (index.html)

**Purpose**: Welcome, navigation hub

**Wireframe**:
```
┌─────────────────────────────────────┐
│ QuizGenerator                       │ (Header)
├─────────────────────────────────────┤
│                                     │
│  Welcome to QuizGenerator           │ (Hero Section)
│  Create and take randomized exams  │
│                                     │
│  [Upload New Quiz]  [View History]  │
│                                     │
├─────────────────────────────────────┤
│                                     │
│ Recent Quizzes:                     │ (Content Section)
│ ─────────────────                   │
│ 1. Sample Math Quiz (50 Q)          │ [Start]
│ 2. Biology 101 (75 Q)               │ [Start]
│ 3. History Quiz (30 Q)              │ [Start]
│                                     │
├─────────────────────────────────────┤
│ © 2026 QuizGenerator                │ (Footer)
└─────────────────────────────────────┘
```

**Components**:
- Header (logo, title)
- Hero section (welcome message, CTAs)
- Recent quizzes list
- Footer (copyright)

**API endpoints used**:
- GET / (render page)
- GET /api/quizzes (fetch recent quizzes)

---

### Page 2: Upload Page (upload.html)

**Purpose**: Upload Excel file with questions

**Wireframe**:
```
┌─────────────────────────────────────┐
│ QuizGenerator > Upload              │ (Breadcrumb)
├─────────────────────────────────────┤
│                                     │
│ Upload Question File                │ (Title)
│                                     │
│ ┌───────────────────────────────┐   │
│ │ Select Excel file:            │   │
│ │ [Choose File]                 │   │ (File Input)
│ │ (.xlsx, .xls, max 10 MB)      │   │
│ └───────────────────────────────┘   │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ File Requirements:            │   │
│ │ • Column: Question            │   │ (Help Text)
│ │ • Columns: Option_A to D      │   │
│ │ • Column: Correct_Answer      │   │
│ │ • Valid values: A/B/C/D       │   │
│ └───────────────────────────────┘   │
│                                     │
│ [Upload]  [Cancel]                  │ (Action Buttons)
│                                     │
│ ┌───────────────────────────────┐   │
│ │ Status message area           │   │ (Status Area)
│ │ (success/error messages)      │   │
│ └───────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Components**:
- Title
- File input (drag-drop)
- Requirements help box
- Action buttons (Upload, Cancel)
- Status/error message area
- Progress indicator (during upload)

**Behavior**:
- File validation on selection
- Progress bar during upload
- Success redirect to quiz list
- Error messages displayed inline

---

### Page 3: Configuration Page (config.html)

**Purpose**: Set exam parameters before starting

**Wireframe**:
```
┌─────────────────────────────────────┐
│ QuizGenerator > Configure Exam       │ (Breadcrumb)
├─────────────────────────────────────┤
│                                     │
│ Configure Your Exam                 │ (Title)
│ Quiz: Sample Math Quiz               │ (Quiz Info)
│ Total Questions: 50                 │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ Number of Questions:          │   │
│ │ [20 ▼]                        │   │ (Dropdown)
│ │ (You have 50 questions)       │   │
│ └───────────────────────────────┘   │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ Exam Duration (minutes):      │   │
│ │ [60]                          │   │ (Number Input)
│ │ (Minimum 1 minute)            │   │
│ └───────────────────────────────┘   │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ Summary:                      │   │ (Summary)
│ │ - 20 random questions         │   │
│ │ - 60 minutes to complete      │   │
│ └───────────────────────────────┘   │
│                                     │
│ [Start Exam]  [Cancel]              │ (Action Buttons)
│                                     │
└─────────────────────────────────────┘
```

**Components**:
- Quiz info display
- Number of questions selector
- Duration input
- Summary box
- Validation messages
- Action buttons

**Validation**:
- num_questions: 1 ≤ num ≤ 50 (example)
- duration: ≥ 1 minute
- Real-time validation feedback

---

### Page 4: Exam Page (exam.html)

**Purpose**: Display exam with questions and timer

**Wireframe**:
```
┌─────────────────────────────────────┐
│ QuizGenerator > Exam                │ (Header)
│ ┌─────────────────────────────────┐ │
│ │ Question 5 of 20   🕐 45:30    │ │ (Progress & Timer)
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│                                     │
│ What is the capital of France?      │ (Question)
│                                     │
│ ☐ London                            │ (Option A)
│ ☐ Berlin                            │ (Option B)
│ ◉ Paris                             │ (Option C - Selected)
│ ☐ Madrid                            │ (Option D)
│                                     │
│ ┌─────────────────────────┬───────┐ │
│ │ [← Previous]            │ [Next →]│ (Navigation)
│ └─────────────────────────┴───────┘ │
│                                     │
│ ⚠ 5 minutes remaining!              │ (Timer Warning)
│                                     │
│ [Submit Exam]                       │ (Submit Button)
│                                     │
└─────────────────────────────────────┘
```

**Components**:
- Progress counter
- Timer display (MM:SS format)
- Question text
- 4 answer options (radio buttons)
- Previous/Next buttons
- Submit button
- Timer warning message (at 5 min)

**Interactions**:
- Click option → select answer
- Click Next → move to next question
- Click Previous → move to previous question
- Timer counts down automatically
- At 0:00 → auto-submit
- At 5:00 → show warning

**Accessibility**:
- Tab through options
- Space/Enter to select
- Screen reader announces timer

---

### Page 5: Results Page (results.html)

**Purpose**: Display exam results and statistics

**Wireframe**:
```
┌─────────────────────────────────────┐
│ QuizGenerator > Results             │ (Header)
├─────────────────────────────────────┤
│                                     │
│ EXAM COMPLETED                      │ (Title)
│                                     │
│ ┌─────────────────────────────────┐ │
│ │  Score: 75.00/100               │ │ (Score Box)
│ │  Status: ✓ PASS                 │ │
│ │  You scored 75% (15 out of 20)  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Statistics:                         │ (Statistics)
│ ─────────────────────────────────   │
│ ✓ Correct:     15 questions         │
│ ✗ Incorrect:   4 questions          │
│ ⊙ Skipped:     1 question           │
│                                     │
│ Time Spent: 35 minutes 20 seconds   │ (Time Info)
│ (Out of 60 minutes allotted)        │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Question Breakdown (Optional):   │ │
│ │ Q1: ✓ Correct                   │ │ (Future Feature)
│ │ Q2: ✗ Incorrect (You: A, Ans: B)│ │
│ │ Q3: ⊙ Skipped                   │ │
│ │ ...                             │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [Take Another Exam]  [Home]         │ (Action Buttons)
│                                     │
└─────────────────────────────────────┘
```

**Components**:
- Title/header
- Score summary box
- Status (PASS/FAIL)
- Statistics section
- Time spent info
- Optional: Question breakdown
- Action buttons

**Styling**:
- Green for PASS status
- Red for FAIL status
- Large, clear score display
- Organized statistics layout

---

## Component Design

### Component 1: Input Fields

**Text Input (Number)**:
```html
<div class="form-group">
  <label for="num_questions">Number of Questions:</label>
  <input type="number" id="num_questions" name="num_questions" 
         min="1" max="50" value="20" required>
  <small class="help-text">You have 50 questions</small>
</div>
```

**Styling**:
- Border: 1px solid #ccc
- Padding: 8px 12px
- Font size: 16px
- Focus: blue border, shadow

### Component 2: Radio Buttons

**Answer Options**:
```html
<div class="options">
  <label class="option-label">
    <input type="radio" name="answer" value="A" required>
    <span class="option-text">Option A text here</span>
  </label>
  <label class="option-label">
    <input type="radio" name="answer" value="B">
    <span class="option-text">Option B text here</span>
  </label>
  <!-- etc -->
</div>
```

**Styling**:
- Large hit targets: 48px minimum
- Hover: light background
- Selected: highlight color
- Focus: outline for keyboard nav

### Component 3: Timer Display

**HTML**:
```html
<div class="timer" id="timer">
  <span class="timer-value">45:30</span>
  <span class="timer-label">Time Remaining</span>
</div>
```

**Styling**:
- Large font (24px+)
- Monospace font for numbers
- Color changes: green → yellow (5 min) → red (< 1 min)
- Updates every second via JavaScript

### Component 4: Button Styles

**Primary Button** (Main action):
```html
<button class="btn btn-primary">Start Exam</button>
```

**Secondary Button** (Alternative action):
```html
<button class="btn btn-secondary">Cancel</button>
```

**Styling**:
- Primary: Blue background, white text
- Secondary: Gray background, dark text
- Hover: Darker shade
- Disabled: Gray, no cursor
- Padding: 12px 24px
- Border radius: 4px

---

## Color Scheme & Typography

### Colors

| Usage | Color | Hex |
|-------|-------|-----|
| Primary | Blue | #007BFF |
| Success | Green | #28A745 |
| Warning | Orange | #FFC107 |
| Danger | Red | #DC3545 |
| Neutral | Gray | #6C757D |
| Background | Light Gray | #F8F9FA |
| Text | Dark Gray | #212529 |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Heading 1 | System Font | 32px | Bold (700) |
| Heading 2 | System Font | 24px | Bold (700) |
| Heading 3 | System Font | 20px | Semi-bold (600) |
| Body Text | System Font | 16px | Regular (400) |
| Timer | Monospace | 28px | Bold (700) |
| Button | System Font | 16px | Semi-bold (600) |
| Label | System Font | 14px | Semi-bold (600) |
| Help Text | System Font | 12px | Regular (400) |

**Font Stack**:
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

---

## Responsive Design

### Breakpoints

| Device | Width | Scaling |
|--------|-------|---------|
| Mobile | < 576px | Single column |
| Tablet | 576px - 992px | 2 columns |
| Desktop | > 992px | Full width |

### Mobile Adjustments
- Buttons: Full width, larger touch targets (48px minimum)
- Input fields: Full width
- Timer: Larger (36px font)
- Question text: Increased line-height
- Options: More padding

### Tablet Adjustments
- 2-column layout for layouts that support it
- Slightly reduced font sizes
- Optimized spacing

### Desktop
- Full-width content area (max-width: 1200px)
- Balanced spacing
- Multi-column layouts where appropriate

---

## Accessibility Guidelines

### WCAG 2.1 Level AA Compliance

**1. Perceivable**
- ✅ Color not only information source (use icons, text)
- ✅ Sufficient color contrast (4.5:1 for text)
- ✅ Text resizable (up to 200%)
- ✅ No auto-playing media

**2. Operable**
- ✅ Keyboard navigation (Tab, Enter, Arrow keys)
- ✅ Focus indicators visible
- ✅ No keyboard traps
- ✅ Minimum 2-second delay for timer

**3. Understandable**
- ✅ Clear, simple language
- ✅ Consistent navigation
- ✅ Help text and labels
- ✅ Error messages clear and specific

**4. Robust**
- ✅ Valid HTML/CSS
- ✅ Semantic HTML elements
- ✅ ARIA labels where needed
- ✅ Works without JavaScript (basic functionality)

### Implementation Details

**Labels**:
```html
<label for="num_questions">Number of Questions:</label>
<input id="num_questions" type="number" ...>
```

**Screen Reader Announcements**:
```html
<div aria-live="polite" aria-atomic="true" id="timer-announcement"></div>
<!-- JS updates this for timer changes -->
```

**Skip Navigation**:
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

**ARIA Roles**:
```html
<div role="status" aria-live="assertive">
  Question 5 of 20
</div>
```

---

## Interactions & Animations

### Interaction 1: Option Selection
**Trigger**: User clicks radio button  
**Effect**:
- Radio becomes selected (filled circle)
- Option background highlights slightly
- Active state persists

### Interaction 2: Timer Countdown
**Trigger**: Page load, updates every second  
**Effect**:
- Smooth number transition
- Color change at 5 minutes (orange warning)
- Color change at < 1 minute (red alert)
- No animation, just updates

### Interaction 3: Button Hover/Click
**Trigger**: Mouse hover, click  
**Effects**:
- Hover: Darker background, slight shadow
- Click: Pressed appearance
- Focus (keyboard): Outline visible

### Interaction 4: File Upload Progress
**Trigger**: File upload starts  
**Effects**:
- Progress bar appears
- Percentage shown
- Disable form during upload
- Show "Uploading..." message

### Interaction 5: Form Validation
**Trigger**: User leaves field or submits  
**Effects**:
- Error message appears below field
- Field border turns red
- Success message (optional) in green
- Prevents form submission if invalid

### Interaction 6: Page Transitions
**Trigger**: Navigation between pages  
**Effects**:
- Fade out current page (200ms)
- Fade in new page (200ms)
- No abrupt jumps

### Animation Preferences
- Respect `prefers-reduced-motion` media query
- Keep animations subtle (200-400ms)
- Use `transform` and `opacity` for performance
- No parallax or complex animations

---

## Error & Success Messages

### Error Message Format
```
⚠ [Icon] Error Title
Description of what went wrong and how to fix it
[Details/Help link]
```

**Examples**:
- "Missing required column: Correct_Answer"
- "File size exceeds 10 MB limit"
- "Invalid correct answer value in row 5"
- "Cannot select 70 questions (only 50 available)"

### Success Message Format
```
✓ [Icon] Success message
[Confirmation details]
```

**Examples**:
- "✓ Quiz uploaded successfully! Total: 50 questions"
- "✓ Exam started. Timer: 60:00"

---

## References

- See `docs/SW1_Requirement_Analysis.md` for UI requirements (FR-1, FR-5, FR-8)
- See `docs/SW2_System_Architecture.md` for component architecture
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
