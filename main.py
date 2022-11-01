from tkinter import *


class Calendar(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.params = {"cal_x": 700, "cal_y": 600, "border": 10, "year": 2022, "month": 11, "day": 2, "side": 300, "primary_color": 'red', "secondary_color": 'purple', "dark": False}
        self.objs = {"obj_list": [], "txt_list": []}
        self.cal_data = []
        self.master = master
        self.ml = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

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
                                           activefill=self.params["secondary_color"], width=3, outline=color2))
                    self.objs["txt_list"].append(self.create_text(self.params["border"] + (j+0.5) * self.params["cal_x"]/7, 2*self.params["border"] + i * self.params["cal_y"]/6, text=str(self.cal_data[i][j])))
                else:
                    self.objs["txt_list"].append(0)
                    self.objs["obj_list"].append(
                        self.create_rectangle(self.params["border"] + j * self.params["cal_x"]/7, self.params["border"] + i * self.params["cal_y"]/6, self.params["border"] + (j+1) * self.params["cal_x"]/7, self.params["border"] + (i+1) * self.params["cal_y"]/6, fill=color, width=3, outline=color2))


w = Tk()
w.geometry('720x620')
c = Calendar(w)
c.draw_cal()
c.pack()
w.mainloop()
