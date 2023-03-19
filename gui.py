from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from get_info import get_data


class set_ui(get_data):

    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.root.geometry("370x400+400+200")
        self.root.title('中国高校排行榜')
        # 设置框架
        self.frame1 = Frame(self.root)
        self.frame1.pack()
        # 设置滚动条
        self.frame2 = Frame(self.root)
        self.frame2.pack()
        self.scroll_text = ScrolledText(self.frame2, font=("宋体", 13))
        self.scroll_text.pack()

    def select_option(self):
        # 设置文本
        label = Label(self.frame1, text="选择需求: ", font=("宋体", 13))
        label.pack(side=LEFT)

        # 设置多选框
        values = ["高校排名", "高校薪资", "选项3"]
        selected_value = StringVar()
        self.combobox = ttk.Combobox(self.frame1, values=values, textvariable=selected_value, state='readonly',
                                     font=("宋体", 13))
        self.combobox.pack(side=RIGHT)

        # 将默认选项设置为第一个
        self.combobox.current(0)
        # 绑定回调函数
        self.combobox.bind("<<ComboboxSelected>>", self.print_selected_value)

    def print_selected_value(self, event):
        # 调用getinfo模块获取数据
        key1_list, key2_list = self.params()
        # flag = input("请输入: ")
        for key1, key2 in zip(key1_list, key2_list):
            sign = self.js_jiami(key2)
            json_data = self.get_info(key1, sign, self.combobox.get())
            # [{"num":1, "name":"清华大学", "score":98}, {...}]
            if self.combobox.get() == "高校排名":
                for data in json_data:
                    self.scroll_text.insert("insert", str(data["num"]))
                    self.scroll_text.insert("insert", str(data["name"]))
                    self.scroll_text.insert("insert", str(data["score"])+'\n')
            if self.combobox.get() == "高校薪资":
                for data in json_data:
                    self.scroll_text.insert("insert", str(data["rank"]))
                    self.scroll_text.insert("insert", str(data["name"]))
                    self.scroll_text.insert("insert", str(data["salary"]) + '\n')


if __name__ == '__main__':
    ui = set_ui()
    ui.select_option()
    ui.root.mainloop()
