---
date: 2026-04-03 14:30
summary: Tổng hợp kiến thức CSS - Box Model, Flexbox, Colors, Animation, Display properties và Styling best practices
---

# Kiến Thức CSS - QuizGenerator

## Mục Lục
- [CSS Basics](#css-basics)
- [CSS Selectors](#css-selectors)
- [Box Model](#box-model)
- [Display & Positioning](#display--positioning)
- [Flexbox](#flexbox)
- [Colors & Typography](#colors--typography)
- [Animations](#animations)
- [CSS Best Practices](#css-best-practices)

---

## CSS Basics

### Ý Nghĩa
CSS (Cascading Style Sheets) dùng để styling HTML elements:

```html
<!-- HTML -->
<div style="color: red; font-size: 18px;">Hello</div>
```

### 3 Cách Thêm CSS

#### 1. Inline Styles
```html
<div style="color: red; margin: 10px;">Text</div>
```
**Ưu:** Quick, simple | **Nhược:** Khó bảo trì, không tái sử dụng

#### 2. Internal Stylesheet
```html
<head>
    <style>
        .my-class {
            color: red;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="my-class">Text</div>
</body>
```
**Ưu:** Tài sử dụng | **Nhược:** Chỉ trong 1 file

#### 3. External Stylesheet
```html
<!-- index.html -->
<link rel="stylesheet" href="style.css">
<div class="my-class">Text</div>

<!-- style.css -->
.my-class {
    color: red;
    margin: 10px;
}
```
**Ưu:** Best practice, tái sử dụng nhiều trang | **Nhược:** Add HTTP request

### CSS Syntax
```css
selector {
    property: value;
    property: value;
}
```

**Ví dụ:**
```css
h1 {
    color: #333;           /* Text color */
    font-size: 28px;       /* Font size */
    margin-bottom: 20px;   /* Margin dưới */
}
```

---

## CSS Selectors

### Selector Types

| Selector | Pattern | Ý Nghĩa | Ví Dụ |
|----------|---------|---------|-------|
| **Element** | `p` | Tất cả `<p>` tags | `p { color: red; }` |
| **Class** | `.classname` | Elements có class | `.btn { background: blue; }` |
| **ID** | `#idname` | Element có ID (unique) | `#header { margin: 0; }` |
| **Attribute** | `[attr=value]` | Match attribute | `input[type=file]` |
| **Pseudo-class** | `:hover` | State của element | `a:hover { color: red; }` |
| **Descendant** | `div p` | p bên trong div | `form input` |
| **Child** | `div > p` | p là con trực tiếp | `body > main` |
| **Universal** | `*` | Tất cả elements | `* { margin: 0; }` |

### Specificity (Độ Ưu Tiên)

```css
/* Specificity: 0-0-1 (element selector) */
button { color: blue; }

/* Specificity: 0-1-0 (class selector) - Ưu tiên hơn */
.btn-primary { color: red; }

/* Specificity: 1-0-0 (ID selector) - Ưu tiên nhất */
#submit-btn { color: green; }

/* Specificity: 1-1-1 (ID + class + element) - Ưu tiên cao nhất */
#submit-btn.btn-primary button { color: orange; }

/* !important - Override mọi thứ (tránh dùng) */
button { color: blue !important; }
```

---

## Box Model

### Định Nghĩa
Mỗi HTML element được bọc trong 1 "box" gồm 4 lớp:

```
┌─────────────────────────────────────────┐
│         Margin (khoảng cách ngoài)      │
├─────────────────────────────────────────┤
│      Border (viền / đường viền)         │
├─────────────────────────────────────────┤
│     Padding (khoảng cách trong)         │
├─────────────────────────────────────────┤
│         Content (nội dung)              │
└─────────────────────────────────────────┘
```

### CSS Properties

```css
div {
    /* Content size */
    width: 300px;
    height: 200px;
    
    /* Padding: khoảng cách từ content tới border */
    padding: 20px;                    /* Tất cả 4 sides */
    padding: 10px 20px;               /* top/bottom, left/right */
    padding: 10px 15px 20px 25px;     /* top, right, bottom, left */
    
    /* Border: viền */
    border: 2px solid #333;           /* width style color */
    border-radius: 8px;               /* Góc bo tròn */
    
    /* Margin: khoảng cách từ element tới elements khác */
    margin: 30px;                     /* Tất cả 4 sides */
    margin: auto;                     /* Center ngang (với width cố định) */
    margin: 0 auto;                   /* left/right auto = center */
}
```

### Box Sizing

```css
/* content-box (default) */
div {
    width: 300px;           /* = content width */
    padding: 10px;          /* + padding */
    border: 2px;            /* + border */
    /* Total: 300 + 20 + 4 = 324px */
    box-sizing: content-box;
}

/* border-box (easier) */
div {
    width: 300px;           /* = content + padding + border */
    padding: 10px;          /* Included in 300px */
    border: 2px;            /* Included in 300px */
    /* Total: 300px exactly */
    box-sizing: border-box;
}
```

---

## Display & Positioning

### Display Property

```css
/* display: block (default for div, p, h1) */
div {
    display: block;         /* Take full width, new line */
    width: 50%;             /* Can set width */
    height: 100px;          /* Can set height */
}

/* display: inline (default for span, a, button) */
span {
    display: inline;        /* Only take needed width */
    width: 50%;             /* Width ignored! */
    height: 100px;          /* Height ignored! */
    margin: 10px;           /* Only left/right margin work */
}

/* display: inline-block (best of both) */
button {
    display: inline-block;  /* Inline but can set width/height */
    width: 100px;           /* Works! */
    height: 40px;           /* Works! */
    margin: 10px;           /* All sides work! */
}

/* display: none (hidden, no space) */
.hidden {
    display: none;          /* Disappeared + no space taken */
}

/* display: flex (modern layout) */
div {
    display: flex;          /* See Flexbox section */
}
```

### Visibility vs Display

```css
/* display: none */
.element {
    display: none;          /* ❌ Hidden, NO space taken */
}

/* visibility: hidden */
.element {
    visibility: hidden;     /* ❌ Hidden, BUT space TAKEN */
}

/* opacity */
.element {
    opacity: 0.5;           /* Transparent, space TAKEN */
    opacity: 0;             /* Invisible, space TAKEN */
}
```

### Position

```css
/* position: static (default) */
div {
    position: static;       /* Normal flow */
}

/* position: relative (offset from normal position) */
div {
    position: relative;
    top: 10px;              /* Move down 10px from normal */
    left: 20px;             /* Move right 20px */
}

/* position: absolute (relative to nearest positioned parent) */
div {
    position: absolute;
    top: 50px;              /* 50px from parent's top */
    left: 100px;            /* 100px from parent's left */
}

/* position: fixed (relative to viewport) */
.navbar {
    position: fixed;
    top: 0;                 /* Stick to top */
    left: 0;
    width: 100%;
    z-index: 1000;          /* On top of other elements */
}

/* position: sticky (mix of relative + fixed) */
.header {
    position: sticky;
    top: 0;                 /* Stick to top when scrolled past */
}
```

---

## Flexbox

### Ý Nghĩa
Flexbox (**Flexible Box Layout**) là modern CSS layout dùng để align items dễ dàng:

```html
<div class="container">
    <div class="item">1</div>
    <div class="item">2</div>
    <div class="item">3</div>
</div>
```

### Container Properties

```css
.container {
    display: flex;              /* Enable flexbox */
    
    /* Main axis: ngang (default) */
    flex-direction: row;        /* row | column | row-reverse | column-reverse */
    
    /* Justify content: align on main axis */
    justify-content: center;    /* center | flex-start | flex-end | space-between | space-around */
    
    /* Align items: align on cross axis */
    align-items: center;        /* center | flex-start | flex-end | stretch */
    
    /* Wrap items if overflow */
    flex-wrap: wrap;            /* wrap | nowrap | wrap-reverse */
    
    /* Gap between items */
    gap: 10px;                  /* 10px space between items */
}
```

### Item Properties

```css
.item {
    /* Grow factor (nếu có extra space) */
    flex-grow: 1;               /* Share extra space equally */
    
    /* Shrink factor (nếu không đủ space) */
    flex-shrink: 1;             /* Default: shrink equally */
    
    /* Base size before growing/shrinking */
    flex-basis: auto;           /* auto | 100px | 50% */
    
    /* Shorthand */
    flex: 1;                    /* = grow: 1, shrink: 1, basis: 0 */
}
```

### Common Patterns

```css
/* Center content horizontally & vertically */
.centered {
    display: flex;
    justify-content: center;    /* Center ngang */
    align-items: center;        /* Center dọc */
    height: 200px;              /* Need height for vertical center */
}

/* Horizontal menu */
.navbar {
    display: flex;
    gap: 20px;                  /* Space between items */
    align-items: center;        /* Vertical center */
}

/* Two-column layout */
.container {
    display: flex;
    gap: 20px;
}
.sidebar {
    flex: 0 0 200px;            /* Fixed 200px width */
}
.content {
    flex: 1;                    /* Take remaining space */
}

/* Vertical stack with space between */
.form {
    display: flex;
    flex-direction: column;     /* Stack vertically */
    gap: 15px;                  /* Space between items */
}
```

---

## Colors & Typography

### Colors

```css
/* Named colors */
color: red;
color: blue;
color: transparent;

/* Hex colors */
color: #FF0000;         /* Red */
color: #00FF00;         /* Green */
color: #0000FF;         /* Blue */
color: #333333;         /* Dark gray */

/* RGB colors */
color: rgb(255, 0, 0);  /* Red */
color: rgb(100, 100, 100);  /* Gray */

/* RGBA (with transparency) */
color: rgba(255, 0, 0, 0.5);   /* Red with 50% opacity */

/* HSL colors */
color: hsl(0, 100%, 50%);   /* Red */
color: hsl(120, 100%, 50%);  /* Green */
```

### Typography

```css
h1 {
    /* Font family */
    font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
    
    /* Font size */
    font-size: 28px;
    font-size: 1.75rem;         /* Relative to root */
    
    /* Font weight: bold, normal, 400-900 */
    font-weight: bold;          /* = 700 */
    font-weight: 600;           /* Semi-bold */
    
    /* Font style: italic */
    font-style: italic;
    
    /* Line height: space between lines */
    line-height: 1.5;           /* 1.5x font size */
    line-height: 30px;          /* Fixed 30px */
    
    /* Letter spacing */
    letter-spacing: 2px;        /* Space between characters */
    
    /* Text alignment */
    text-align: center;         /* center | left | right | justify */
    
    /* Text decoration */
    text-decoration: underline; /* none | underline | overline | line-through */
    
    /* Text color */
    color: #333;
}

/* QuizGenerator example */
.timer {
    font-family: 'Arial', monospace;    /* Monospace for timer */
    font-size: 36px;
    font-weight: bold;
    color: #667eea;
    text-align: center;
}
```

### Web Safe Fonts

```css
/* Best practices: list fallbacks */
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
/* Read as: use Segoe UI, if not available use Tahoma, then Geneva, etc. */
```

---

## Animations

### Transitions (Smooth Change)

```css
/* Smooth transition khi property thay đổi */
button {
    background-color: blue;
    transition: background-color 0.3s ease;    /* What, duration, easing */
}

button:hover {
    background-color: red;      /* Animated change from blue → red in 0.3s */
}

/* Multiple properties */
button {
    transition: background-color 0.3s, color 0.2s, transform 0.4s;
}

/* Shorthand: all properties */
button {
    transition: all 0.3s ease;  /* All properties animated */
}
```

### Keyframe Animations

```css
/* Define animation */
@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

/* Apply animation */
.loading {
    animation: spin 1s linear infinite;
    /* animation-name, duration, easing, iteration */
}
```

### Loading Spinner (QuizGenerator)

```css
/* Loading ball quay tròn */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.spinner {
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;          /* Viền xám nhạt */
    border-top: 3px solid #667eea;      /* Viền trên xanh (quay) */
    border-radius: 50%;                 /* Tròn */
    animation: spin 1s linear infinite; /* Quay liên tục */
}
```

### Easing Functions

```css
/* Speed curve */
transition: all 0.3s ease;              /* Starts slow, middle fast, ends slow */
transition: all 0.3s linear;            /* Constant speed */
transition: all 0.3s ease-in;           /* Starts slow, speeds up */
transition: all 0.3s ease-out;          /* Starts fast, slows down */
transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* Custom */
```

---

## CSS Best Practices

### 1. Use Classes Over IDs
```css
/* ❌ Avoid - Too specific, hard to override */
#submit-button {
    background: blue;
}

/* ✅ Use classes */
.btn-primary {
    background: blue;
}
```

### 2. Separate Concerns
```css
/* ❌ Mixed concerns */
.form-container {
    display: flex;           /* Layout */
    background: #f5f5f5;     /* Color */
    padding: 20px;           /* Spacing */
    border: 1px solid #ddd;  /* Border */
}

/* ✅ Separated */
.form-container {
    display: flex;           /* Layout only */
}

.card {
    background: #f5f5f5;     /* Color + border */
    border: 1px solid #ddd;
    padding: 20px;           /* Spacing */
}
```

### 3. Mobile First
```css
/* ❌ Desktop first */
.container {
    width: 1200px;           /* Desktop */
}

@media (max-width: 768px) {
    .container {
        width: 100%;         /* Mobile override */
    }
}

/* ✅ Mobile first */
.container {
    width: 100%;             /* Mobile */
}

@media (min-width: 768px) {
    .container {
        width: 1200px;       /* Desktop */
    }
}
```

### 4. Use CSS Variables
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --spacing-unit: 8px;
    --border-radius: 8px;
}

button {
    background: var(--primary-color);
    padding: calc(var(--spacing-unit) * 2);
    border-radius: var(--border-radius);
}
```

### 5. Naming Convention (BEM)
```css
/* Block Element Modifier */
.btn {
    background: blue;
}

.btn__text {
    color: white;
}

.btn--primary {
    background: blue;
}

.btn--secondary {
    background: gray;
}
```

---

## Tóm Tắt

**CSS trong QuizGenerator:**
- ✅ Box Model: margin, border, padding, content
- ✅ Flexbox để layout: center, space-between, gap
- ✅ Colors: #hex, rgb, rgba
- ✅ Typography: font-family, font-size, line-height
- ✅ Animations: transitions, keyframes, spinning loader
- ✅ Display: block, inline, inline-block, flex, none

**Best Practices:**
1. Use semantic classes (`.btn-primary` not `#btn1`)
2. Flexbox for modern layout (not float)
3. Mobile first approach
4. CSS variables for colors/spacing
5. Separate layout, color, spacing concerns
