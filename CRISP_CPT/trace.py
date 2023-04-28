import helper

class Trace:
    def __init__(self, start_time, end_time, id, parent_id):
        open = False
        if open:
            self.start_time = helper.parse_time(start_time)
            self.end_time = helper.parse_time(end_time)
        else:
            self.start_time = start_time
            self.end_time = end_time
        self.id = id
        self.parent_id = parent_id
        self.parent = None
        self.children = []

    def set_parent(self, par):
        self.parent = par

    def add_child(self, child):
        self.children.append(child)

    def sort_children(self):
        self.children.sort(key=lambda x: x.end_time)

    def print_children(self):
        for u in self.children:
            print(u)

    def __str__(self):  
        return "span_id = " + self.id + " parent_id = " + self.parent_id + " start_time = " + str(self.start_time) + " end_time = "+str(self.end_time)