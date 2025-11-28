# Smart Task Analyzer  
A mini full-stack application that analyzes tasks and intelligently scores them based on urgency, importance, effort, and dependencies.

This project was built as part of the **Software Development Intern Technical Assessment**.  
It includes a Django REST backend and a pure HTML/CSS/JS frontend.

---

# 🚀 Features
- Add individual tasks through a form
- Paste bulk JSON tasks
- Intelligent scoring algorithm considering:
  - **Urgency** (based on due date)
  - **Importance** (1–10 scale)
  - **Effort** (lower effort = quick wins)
  - **Dependencies** (blocking tasks get higher priority)
- Four sorting strategies:
  - **Smart Balance**
  - **Fastest Wins**
  - **High Impact**
  - **Deadline Driven**
- Clean UI showing:
  - Calculated score
  - Task details
  - Visual priority indicators
- Django REST API for task analysis
- Fully deployable frontend + backend

---

# 🛠️ Technologies Used
### **Backend**
- Python 3
- Django 5
- Django REST Framework
- CORS Headers

### **Frontend**
- HTML
- CSS
- Vanilla JavaScript (Fetch API)
