from xml.dom import minidom
import os

class StudentModel:
    def __init__(self, xml_path='students.xml'):
        self.xml_path = xml_path
        if not os.path.exists(self.xml_path):
            # create basic file
            with open(self.xml_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="utf-8"?>\\n<students>\\n</students>\\n')
        self.load()

    def load(self):
        self.doc = minidom.parse(self.xml_path)
        self.root = self.doc.documentElement

    def save(self):
        with open(self.xml_path, 'w', encoding='utf-8') as f:
            f.write(self.doc.toprettyxml(indent='  '))

    def _next_id(self):
        students = self.root.getElementsByTagName('student')
        max_id = 0
        for s in students:
            try:
                sid = int(s.getAttribute('id'))
                if sid > max_id:
                    max_id = sid
            except Exception:
                pass
        return str(max_id + 1)

    def get_all_students(self):
        students = []
        for s in self.root.getElementsByTagName('student'):
            sid = s.getAttribute('id')
            name = self._get_text(s, 'name')
            level = self._get_text(s, 'level')
            surahs = []
            surahs_parent = s.getElementsByTagName('surahs')
            if surahs_parent:
                for sur in surahs_parent[0].getElementsByTagName('surah'):
                    surahs.append({
                        'name': sur.getAttribute('name'),
                        'progress': sur.getAttribute('progress')
                    })
            students.append({'id': sid, 'name': name, 'level': level, 'surahs': surahs})
        return students

    def _get_text(self, parent, tagname):
        nodes = parent.getElementsByTagName(tagname)
        if not nodes:
            return ''
        node = nodes[0]
        if node.firstChild:
            return node.firstChild.nodeValue
        return ''

    def add_student(self, name, level):
        sid = self._next_id()
        student = self.doc.createElement('student')
        student.setAttribute('id', sid)

        name_el = self.doc.createElement('name')
        name_el.appendChild(self.doc.createTextNode(name))
        student.appendChild(name_el)

        level_el = self.doc.createElement('level')
        level_el.appendChild(self.doc.createTextNode(str(level)))
        student.appendChild(level_el)

        surahs_el = self.doc.createElement('surahs')
        student.appendChild(surahs_el)

        self.root.appendChild(student)
        self.save()
        self.load()
        return sid

    def delete_student(self, sid):
        for s in list(self.root.getElementsByTagName('student')):
            if s.getAttribute('id') == sid:
                self.root.removeChild(s)
                self.save(); self.load(); return True
        return False

    def find_student_node(self, sid):
        for s in self.root.getElementsByTagName('student'):
            if s.getAttribute('id') == sid:
                return s
        return None

    def add_or_update_surah_progress(self, sid, surah_name, progress):
        s = self.find_student_node(sid)
        if s is None:
            return False
        surahs_parent = s.getElementsByTagName('surahs')
        if not surahs_parent:
            surahs_el = self.doc.createElement('surahs')
            s.appendChild(surahs_el)
        else:
            surahs_el = surahs_parent[0]

        for sur in surahs_el.getElementsByTagName('surah'):
            if sur.getAttribute('name') == surah_name:
                sur.setAttribute('progress', str(progress))
                self.save(); self.load(); return True

        new_sur = self.doc.createElement('surah')
        new_sur.setAttribute('name', surah_name)
        new_sur.setAttribute('progress', str(progress))
        surahs_el.appendChild(new_sur)
        self.save(); self.load(); return True

    def remove_surah(self, sid, surah_name):
        s = self.find_student_node(sid)
        if s is None:
            return False
        surahs_parent = s.getElementsByTagName('surahs')
        if not surahs_parent:
            return False
        surahs_el = surahs_parent[0]
        for sur in list(surahs_el.getElementsByTagName('surah')):
            if sur.getAttribute('name') == surah_name:
                surahs_el.removeChild(sur)
                self.save(); self.load(); return True
        return False

    def get_student(self, sid):
        for st in self.get_all_students():
            if st['id'] == sid:
                return st
        return None
