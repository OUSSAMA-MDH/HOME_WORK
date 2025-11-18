# Student Qur'an Monitoring (MVC - All in one window)

This project implements a simple Qur'an memorization tracking desktop app using the MVC pattern.
All interactions (add/update/delete students and surah progress) happen in a single window — no input popups are required.

## Files

- `app.py` - entry point
- `student_model.py` - XML DOM model
- `student_view.py` - Tkinter single-window UI
- `student_controller.py` - controller to connect model and view
- `students.xml` - sample data

## Run

```bash
python app.py
```

Requirements: Python 3.8+ (Tkinter is included in standard Python installs)

