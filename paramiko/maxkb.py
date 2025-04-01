# import paramiko
# import time
#
# def get_system_interface(ciscointerface):
#     host = "10.0.31.139"
#     username = "wippe"
#     password = "Esun@1sh"
#
#     # 创建SSH客户端
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     try:
#         ssh_client.connect(hostname=host, username=username, password=password, compress=True, allow_agent=False)
#         cli = ssh_client.invoke_shell(width=999, height=9999)
#         cli.send("\n")
#         time.sleep(1)
#         # 发送命令并获取结果
#         cli.send("terminal length 0\n")
#         time.sleep(1)
#         cli.send("show interfaces " + ciscointerface + "\n")
#         time.sleep(1)
#         result = cli.recv(65535).decode('utf8')
#         print(result)
#
#     except Exception as e:
#         print(f"连接或执行命令时发生错误：{e}")
#
#     finally:
#         # 关闭SSH连接
#         ssh_client.close()
#
# ciscointerface = "e0/0"
# get_system_interface(ciscointerface)
import time

def zzx_py(a):
    b = 2
    c = int(a) + b
    print(c)

a = input()
zzx_py(a)