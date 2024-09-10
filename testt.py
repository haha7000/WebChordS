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

def get_user_input():
    # 사용자로부터 chord 입력받기
    chords = input("Chord를 입력하세요: ")
    
    # 키 변경 수 입력받기
    key_change = int(input("몇 키를 올리거나 낮출지 입력하세요 (+/- 숫자): "))
    
    return chords, key_change

def transform_chords(chords, key_change):
    # 프롬프트 작성: 키에 따른 올바른 표기법(# 또는 b)을 사용하도록 요청
    prompt = (
        f"Transform the following chords by {key_change} semitones: {chords}. Only return the transformed chords."
        "When transposing, use correct notation according to the key. "
        "For example, use 'b' instead of '#' in flat keys like Bb, Eb, Ab, Db, Gb, and F. "
        "Ensure all chords are correctly notated for the resulting key."
    )
    
    response = chat_with_gpt4o_mini(prompt)
    
    # 불필요한 기호 제거 및 정리
    transformed_chords = response.replace("**", "").strip()
    
    return transformed_chords

if __name__ == "__main__":
    chords, key_change = get_user_input()
    transformed_chords = transform_chords(chords, key_change)
    print(transformed_chords)
