from plugins import dataManage


class Clock():
    clock_data = dataManage.read_clock()

    def __init__(self):
        pass

    def save(self):
        dataManage.save_clock(self.clock_data)

    def existence(self, group_id, clock_name):
        if not self.clock_data.__contains__(group_id):
            return False
        elif not self.clock_data[group_id].__contains__(clock_name):
            return False
        return True

    def get_clock(self, group_id):
        if not self.clock_data.__contains__(group_id):
            return None
        return self.clock_data[group_id]

    def get_clock_single(self, group_id, clock_name):
        if not self.clock_data.__contains__(group_id):
            return None
        if not self.clock_data[group_id].__contains__(clock_name):
            return None
        return self.clock_data[group_id][clock_name]

    def insert_clock(self, group_id, clock_name):
        if not self.clock_data.__contains__(group_id):
            self.clock_data[group_id] = {}
        elif self.clock_data[group_id].__contains__(clock_name):
            return False
        self.clock_data[group_id][clock_name] = {
            'member': [],
            'remind': {
                'switch': True,
                'hour': 22,
                'minute': 00
            },
            'summary': True
        }
        self.save()
        return True

    def remove_clock(self, group_id, clock_name):
        if not self.clock_data.__contains__(group_id):
            return False
        elif not self.clock_data[group_id].__contains__(clock_name):
            return False
        del self.clock_data[group_id][clock_name]
        if len(self.clock_data[group_id]) == 0:
            del self.clock_data[group_id]
        self.save()
        return True

    def join_clock(self, group_id, qq, clock_name):
        if not self.existence(group_id, clock_name):
            return 1
        del_member = None
        for member in self.clock_data[group_id][clock_name]['member']:
            if member['qq'] == qq:
                del_member = member
                break
        if del_member is None:
            self.clock_data[group_id][clock_name]['member'].append({
                'qq': qq,
                'last': '',
                'continuity': 0
            })
            return 0
        return 2

    def quit_clock(self, group_id, qq, clock_name):
        if not self.existence(group_id, clock_name):
            return 1
        del_member = None
        for member in self.clock_data[group_id][clock_name]['member']:
            if member['qq'] == qq:
                del_member = member
                break
        if del_member is not None:
            self.clock_data[group_id][clock_name]['member'].remove(del_member)
            return 0
        return 2
