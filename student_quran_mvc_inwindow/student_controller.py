from student_model import StudentModel

class StudentController:
    def __init__(self, view):
        self.view = view
        self.model = StudentModel()
        self.refresh()

    def refresh(self):
        students = self.model.get_all_students()
        self.view.populate_students(students)
        self.view.show_student_detail(None)
        self.view.set_status("Refreshed")

    def add_student(self, name, level):
        sid = self.model.add_student(name, level)
        self.refresh()

        students = self.model.get_all_students()
        for i, s in enumerate(students):
            if s['id'] == sid:
                self.view.listbox.selection_clear(0, 'end')
                self.view.listbox.selection_set(i)
                self.view.listbox.activate(i)
                self.show_student(sid)
                break

    def delete_student(self, sid):
        ok = self.model.delete_student(sid)
        if ok:
            self.refresh()
            self.view.set_status("Student deleted")
        else:
            self.view.set_status("Delete failed")

    def show_student(self, sid):
        student = self.model.get_student(sid)
        self.view.show_student_detail(student)
        self.view.set_status(f"Showing student {sid}")

    def update_student_basic(self, sid, name, level):
        node = self.model.find_student_node(sid)
        if node is None:
            self.view.set_status("Student not found")
            return

        name_nodes = node.getElementsByTagName('name')
        if name_nodes and name_nodes[0].firstChild:
            name_nodes[0].firstChild.nodeValue = name
        else:
            n = self.model.doc.createElement('name')
            n.appendChild(self.model.doc.createTextNode(name))
            node.appendChild(n)

        level_nodes = node.getElementsByTagName('level')
        if level_nodes and level_nodes[0].firstChild:
            level_nodes[0].firstChild.nodeValue = str(level)
        else:
            l = self.model.doc.createElement('level')
            l.appendChild(self.model.doc.createTextNode(str(level)))
            node.appendChild(l)

        self.model.save()
        self.model.load()
        self.refresh()
        self.view.set_status("Student updated")

    def add_or_update_surah(self, sid, surah, progress):
        ok = self.model.add_or_update_surah_progress(sid, surah, progress)
        if ok:
            self.show_student(sid)
            self.view.set_status("Surah updated")
        else:
            self.view.set_status("Failed to update surah")

    def remove_surah(self, sid, surah):
        ok = self.model.remove_surah(sid, surah)
        if ok:
            self.show_student(sid)
            self.view.set_status("Surah removed")
        else:
            self.view.set_status("Remove failed")
