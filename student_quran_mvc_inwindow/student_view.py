import tkinter as tk

class StudentView(tk.Tk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.title("Student Qur'an Monitoring - All in one window")
        self.geometry("900x520")

        # Top: form for adding/updating students
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=6)

        tk.Label(top_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(top_frame, width=30)
        self.entry_name.grid(row=0, column=1, padx=4)

        tk.Label(top_frame, text="Level:").grid(row=0, column=2, sticky="w")
        self.entry_level = tk.Entry(top_frame, width=10)
        self.entry_level.grid(row=0, column=3, padx=4)

        tk.Button(top_frame, text="Add Student", command=self.on_add_student).grid(row=0, column=4, padx=6)
        tk.Button(top_frame, text="Update Selected", command=self.on_update_student).grid(row=0, column=5, padx=6)

        # Middle: list of students and details
        mid_frame = tk.Frame(self)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        left = tk.Frame(mid_frame)
        left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left, text="Students").pack(anchor="w")
        self.listbox = tk.Listbox(left, width=36)
        self.listbox.pack(fill=tk.Y, expand=True, padx=4, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        btns_left = tk.Frame(left)
        btns_left.pack(fill=tk.X)
        tk.Button(btns_left, text="Delete Student", command=self.on_delete_student).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(btns_left, text="Refresh", command=self.on_refresh).pack(side=tk.LEFT, padx=4, pady=4)

        right = tk.Frame(mid_frame)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right, text="Details").pack(anchor="w")
        self.detail_text = tk.Text(right, height=18)
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Bottom: surah form
        bottom = tk.Frame(self)
        bottom.pack(fill=tk.X, padx=10, pady=6)

        tk.Label(bottom, text="Surah name:").grid(row=0, column=0, sticky="w")
        self.entry_surah = tk.Entry(bottom, width=30)
        self.entry_surah.grid(row=0, column=1, padx=4)

        tk.Label(bottom, text="Progress %:").grid(row=0, column=2, sticky="w")
        self.entry_progress = tk.Entry(bottom, width=10)
        self.entry_progress.grid(row=0, column=3, padx=4)

        tk.Button(bottom, text="Add/Update Surah for Selected", command=self.on_add_update_surah).grid(row=0, column=4, padx=6)
        tk.Button(bottom, text="Remove Surah from Selected", command=self.on_remove_surah).grid(row=0, column=5, padx=6)

        # Status
        self.status = tk.Label(self, text="", anchor="w")
        self.status.pack(fill=tk.X, padx=10, pady=4)

    # ---- UI callbacks that call controller ----
    def on_add_student(self):
        name = self.entry_name.get().strip()
        level = self.entry_level.get().strip()
        if not name or not level:
            self.set_status("Enter name and level")
            return
        if not level.isdigit():
            self.set_status("Level must be a number")
            return
        if self.controller:
            self.controller.add_student(name, int(level))

    def on_update_student(self):
        sel = self.listbox.curselection()
        if not sel:
            self.set_status("Select a student to update")
            return
        idx = sel[0]
        sid = self.listbox.get(idx).split(" - ")[0]
        name = self.entry_name.get().strip()
        level = self.entry_level.get().strip()
        if not name or not level or not level.isdigit():
            self.set_status("Provide valid name and level")
            return
        if self.controller:
            self.controller.update_student_basic(sid, name, int(level))

    def on_delete_student(self):
        sel = self.listbox.curselection()
        if not sel:
            self.set_status("Select a student to delete")
            return
        idx = sel[0]
        sid = self.listbox.get(idx).split(" - ")[0]
        if self.controller:
            self.controller.delete_student(sid)

    def on_select(self, event):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        sid = self.listbox.get(idx).split(" - ")[0]
        if self.controller:
            self.controller.show_student(sid)

    def on_refresh(self):
        if self.controller:
            self.controller.refresh()

    def on_add_update_surah(self):
        sel = self.listbox.curselection()
        if not sel:
            self.set_status("Select a student first")
            return
        idx = sel[0]
        sid = self.listbox.get(idx).split(" - ")[0]
        surah = self.entry_surah.get().strip()
        progress = self.entry_progress.get().strip()
        if not surah or not progress or not progress.isdigit():
            self.set_status("Provide surah name and numeric progress")
            return
        if self.controller:
            self.controller.add_or_update_surah(sid, surah, int(progress))

    def on_remove_surah(self):
        sel = self.listbox.curselection()
        if not sel:
            self.set_status("Select a student first")
            return
        idx = sel[0]
        sid = self.listbox.get(idx).split(" - ")[0]
        surah = self.entry_surah.get().strip()
        if not surah:
            self.set_status("Enter surah name to remove")
            return
        if self.controller:
            self.controller.remove_surah(sid, surah)

    def set_status(self, text):
        self.status.config(text=text)

    # ---- helpers used by controller to update UI ----
    def populate_students(self, students):
        self.listbox.delete(0, tk.END)
        for s in students:
            display = f"{s['id']} - {s['name']} (Level {s['level']})"
            self.listbox.insert(tk.END, display)

    def show_student_detail(self, student):
        self.detail_text.delete("1.0", tk.END)
        if student is None:
            self.detail_text.insert(tk.END, "No student selected\\n")
            return
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, student['name'])
        self.entry_level.delete(0, tk.END)
        self.entry_level.insert(0, student['level'])

        self.detail_text.insert(tk.END, f"Name: {student['name']}\\n")
        self.detail_text.insert(tk.END, f"Level: {student['level']}\\n")
        self.detail_text.insert(tk.END, "Surahs:\\n")
        if not student['surahs']:
            self.detail_text.insert(tk.END, "  No surahs recorded\\n")
        else:
            for sur in student['surahs']:
                self.detail_text.insert(tk.END, f"  - {sur['name']}: {sur['progress']}%\\n")
