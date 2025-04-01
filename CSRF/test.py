import secrets

def generate_csrf_token():
    # 生成一个随机的 CSRF 令牌，通常使用安全的随机数生成器
    csrf_token = secrets.token_hex(16)  # 生成 16 字节的十六进制字符串
    return csrf_token

# 生成 CSRF 令牌
csrf_token = generate_csrf_token()
print("CSRF 令牌:", csrf_token)


# import secrets
#
# def generate_csrf_token():
#     # 生成一个随机的 CSRF 令牌
#     csrf_token = secrets.token_urlsafe(32)  # 生成 32 字节的 URL 安全的随机字符串
#     # 格式化 CSRF 令牌，例如每4个字符加一个横线
#     formatted_token = '-'.join(csrf_token[i:i+4] for i in range(0, len(csrf_token), 4))
#     return formatted_token
#
# # 生成 CSRF 令牌
# csrf_token = generate_csrf_token()
# print("CSRF 令牌:", csrf_token)
