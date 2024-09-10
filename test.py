import os
import openai

# 환경 변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt4o_mini(prompt):
    try:
        # API 키가 설정되어 있는지 확인
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 사용 예시
if __name__ == "__main__":
    user_input = "Write your prompt here"
    response = chat_with_gpt4o_mini(user_input)
    print(response)