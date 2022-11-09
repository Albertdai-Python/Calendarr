from tkinter import *


class Calendar(Canvas):

    def load_txt(self):
        with open("data_info.dt", 'r') as f:
            data = [i.split('[-]') for i in f.read().split('\n')]
            dictionary = {}
            for i in data:
                dictionary[i[0]] = [j.split('[@]') for j in i[1].split('[*]')]
            for i in dictionary:
                for j in dictionary[i]:
                    j[1] = j[1].split('~')
                    j[1][0] = j[1][0].split(":")
                    j[1][1] = j[1][1].split(":")
            f.close()
        return dictionary

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.params = {"cal_x": 1000, "cal_y": 800, "border": 20, "year": 2022, "month": 11, "day": 2, "side": 500, "primary_color": '#dee72d', "secondary_color": '#bebdac', "dark": False}
        self.objs = {"obj_list": [], "txt_list": [], "side_txt": [], "side_line": [], "side_block": []}
        self.cal_data = []
        self.master = master
        self.ml = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
        self.place(x=0, y=0)
        self.notes = self.load_txt()

    def set_param(self, **kwargs):
        for i in list(kwargs.keys()):
            self.params[i] = kwargs[i]

    def weekday(self):
        m = self.params["month"]
        y = self.params["year"]
        if m <= 2:
            m += 12
            y -= 1
        return (13 * (m + 1) // 5 + y + y // 4 - y // 100 + y // 400) % 7

    def initiate_calendar(self):
        temp_cal = [0 for _ in range(42)]
        start_day = (self.weekday()-1) % 7
        m = self.params["month"]
        y = self.params["year"]
        if m == 2 and y % 4 == 0:
            self.month_list[1] = 29
        else:
            self.month_list[1] = 28
        for i in range(start_day, self.month_list[m - 1] + start_day):
            temp_cal[i] = i - start_day + 1
        self.cal_data = [temp_cal[i:i + 7] for i in range(0, len(temp_cal), 7)]

    def display_side(self, event):
        if event.x <= self.params["cal_x"] + self.params["border"] and event.y <= self.params["cal_x"] + self.params["border"]:
            item_index = int(self.gettags(self.find_closest(event.x, event.y)[0])[0]) - 1
            self.params["day"] = item_index + 1
        date_string = str(self.params["year"])+'/'+str(self.params["month"])+'/'+str(self.params["day"])
        note_keys = self.notes.keys()
        if date_string not in note_keys:
            info = 'blank'
        else:
            for i in self.objs["side_block"]:
                self.delete(i)
            self.objs["side_block"] = []
            info = self.notes[date_string]
            delta_y = self.params["cal_y"] / 1440
            for i in info:
                name = i[0]
                st_time = int(i[1][0][0]) * 60 + int(i[1][0][1])
                ed_time = int(i[1][1][0]) * 60 + int(i[1][1][1])
                st_time *= delta_y
                ed_time *= delta_y
                self.objs["side_block"].append(self.create_rectangle(self.params["cal_x"]+2*self.params["border"]+17, st_time, self.params["cal_x"]+2*self.params["border"]+self.params["side"], ed_time, width=0, fill=self.params["primary_color"]))
                self.objs["side_block"].append(self.create_text(self.params["cal_x"]+2*self.params["border"]+8.5+self.params["side"]/2, (st_time+ed_time)/2, text=name))

        print(info)

    def draw_cal(self):
        self.master.geometry(f'{self.params["border"]*3+self.params["cal_x"]+self.params["side"]}x{self.params["border"]*2+self.params["cal_y"]}')
        self.config(width=self.params["border"]*3+self.params["cal_x"]+self.params["side"], height=self.params["border"]*2+self.params["cal_y"])
        self.master.title(f'{self.params["year"]}  {self.ml[self.params["month"]-1]}')
        self.initiate_calendar()
        self.objs["obj_list"] = []
        self.objs["txt_list"] = []
        if self.params["dark"]:
            color = 'black'
            color2 = 'white'
        else:
            color = 'white'
            color2 = 'black'
        self.config(bg=color)
        for i in range(6):
            for j in range(7):
                if self.cal_data[i][j] != 0:
                    self.objs["obj_list"].append(
                        self.create_rectangle(self.params["border"] + j * self.params["cal_x"]/7, self.params["border"] + i * self.params["cal_y"]/6, self.params["border"] + (j+1) * self.params["cal_x"]/7, self.params["border"] + (i+1) * self.params["cal_y"]/6, fill=self.params["primary_color"],
                                           activefill=self.params["secondary_color"], width=3, outline=color2, tags=f'{self.cal_data[i][j]}'))
                    self.bind('<Button-1>', self.display_side)
                    self.objs["txt_list"].append(self.create_text(self.params["border"] + (j+0.5) * self.params["cal_x"]/7, (i+0.25) * self.params["cal_y"]/6, text=str(self.cal_data[i][j]), tags=f'{self.cal_data[i][j]}', font='Arial 24'))
                else:
                    self.objs["txt_list"].append(0)
                    self.objs["obj_list"].append(
                        self.create_rectangle(self.params["border"] + j * self.params["cal_x"]/7, self.params["border"] + i * self.params["cal_y"]/6, self.params["border"] + (j+1) * self.params["cal_x"]/7, self.params["border"] + (i+1) * self.params["cal_y"]/6, fill=color, width=3, outline=color2, tags='0'))
        delta_y = self.params["cal_y"] / 24
        for i in range(25):
            self.objs["side_txt"].append(self.create_text(self.params["cal_x"]+2*self.params["border"]+7.5, self.params["border"]+delta_y*i, text=str(i), fill=color2))
            self.objs["side_line"].append(self.create_line(self.params["cal_x"]+2*self.params["border"]+17, self.params["border"]+delta_y*i, self.params["cal_x"]+2*self.params["border"]+self.params["side"], self.params["border"]+delta_y*i, fill=color2, width=2))


w = Tk()
w.geometry('720x620')
c = Calendar(w)
c.draw_cal()
w.mainloop()
