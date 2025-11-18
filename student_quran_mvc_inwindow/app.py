from student_view import StudentView
from student_controller import StudentController

if __name__ == "__main__":
    view = StudentView(None)
    controller = StudentController(view)
    view.controller = controller
    view.mainloop()
