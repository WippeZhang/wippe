import tkinter as tk
from tkinter import ttk, simpledialog, scrolledtext
import socket
import threading
import time

class LoginDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="请输入用户名:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1)
        return self.entry

    def apply(self):
        self.result = self.entry.get()

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Room")

        # 获取用户名
        self.username = self.get_username()

        # 创建套接字
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('192.168.199.59', 5555)
        self.client_socket.connect(self.server_address)

        # 发送用户名到服务器
        self.client_socket.send(self.username.encode('utf-8'))

        # 创建聊天记录文本框
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("微软雅黑", 14), height=20, width=55)
        self.chat_history.grid(row=0, column=0, padx=5, pady=5, rowspan=2)

        # 创建用户列表 Label
        self.user_list_label = tk.Label(root, text="聊天室成员", font=("微软雅黑", 12))
        self.user_list_label.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        # 创建用户列表 Listbox
        self.user_list = tk.Listbox(root, font=("微软雅黑", 12), selectbackground="lightgray", height=21, width=20)
        self.user_list.grid(row=1, column=1, padx=5, pady=5, rowspan=1)

        # 创建输入框用于发送消息
        self.message_entry = tk.Entry(root, font=("微软雅黑", 13))
        self.message_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.message_entry.bind("<Return>", self.send_message)

        # 创建发送按钮和快速回复菜单
        style = ttk.Style()
        style.configure("TButton", font=("微软雅黑", 12), padding=5)

        self.send_button = ttk.Menubutton(root, text="发送(S)", style="TButton", direction="below")
        self.send_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.send_button.menu = tk.Menu(self.send_button, tearoff=0)
        self.send_button["menu"] = self.send_button.menu

        self.quick_reply_var = tk.StringVar()
        self.quick_reply_var.set("快速回复")
        self.send_button.menu.add_command(label="中午吃什么？", command=lambda: self.insert_quick_reply("中午吃什么？"))
        self.send_button.menu.add_command(label="¿", command=lambda: self.insert_quick_reply("¿"))

        self.send_button.bind("<Button-1>", lambda event: self.send_message(None))  # 绑定按钮点击事件

        # 创建线程用于接收消息
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        # 创建线程用于更新用户列表
        update_user_list_thread = threading.Thread(target=self.update_user_list)
        update_user_list_thread.start()

    def insert_quick_reply(self, reply_text):
        self.message_entry.insert(tk.END, reply_text)

    def get_username(self):
        dialog = LoginDialog(self.root, "登录")
        return dialog.result

    def send_message(self, event):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
            self.update_chat_history(f"{self.username}: {message}", color="black")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message.startswith("[USERLIST]"):
                    user_list = message.split()[1:]
                    self.update_user_list_widget(user_list)
                else:
                    sender, content = message.split(":", 1)
                    if sender != self.username:
                        self.update_chat_history(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def update_chat_history(self, message, color="black"):
        current_time = time.strftime("%H:%M:%S")
        formatted_message = f"[{current_time}]\n{message}"
        self.chat_history.insert(tk.END, formatted_message + '\n', "tag-right" if message.startswith(f"{self.username}:") else "")
        self.chat_history.tag_config("tag-right", justify='right', foreground=color)
        self.chat_history.yview(tk.END)

    def update_user_list(self):
        while True:
            try:
                user_list_msg = self.client_socket.recv(1024).decode('utf-8')
                if user_list_msg.startswith("[USERLIST]"):
                    user_list = user_list_msg.split()[1:]
                    self.update_user_list_widget(user_list)
            except Exception as e:
                print(f"Error updating user list: {e}")
                break

    def update_user_list_widget(self, user_list):
        # 清空旧的用户列表
        self.user_list.delete(0, tk.END)

        # 添加用户列表
        for username in user_list:
            self.user_list.insert(tk.END, username)




if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClientGUI(root)
    root.mainloop()
