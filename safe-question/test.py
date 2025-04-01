import random

# 问题列表
questions = {
    "What color is the sky?": "blue",
    "What is 2 + 2?": "4",
    "What is the capital of France?": "paris"
}

def generate_captcha():
    # 随机选择一个问题
    question, answer = random.choice(list(questions.items()))
    return question, answer

def verify_answer(question, user_answer):
    # 验证用户答案是否正确
    correct_answer = questions.get(question)
    if correct_answer and user_answer.lower() == correct_answer.lower():
        return True
    else:
        return False

def main():
    # 生成验证码
    question, answer = generate_captcha()
    print("Question:", question)

    # 用户输入答案
    user_answer = input("Your answer: ")

    # 验证答案
    if verify_answer(question, user_answer):
        print("Congratulations! Your answer is correct.")
    else:
        print("Sorry, your answer is incorrect.")

if __name__ == "__main__":
    main()
