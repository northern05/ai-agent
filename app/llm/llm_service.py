from fastapi import HTTPException

from app.core.modules_factory import openai_client


def answer_users_msg(msg: str):
    try:
        # Call OpenAI's GPT-4 API
        response = openai_client.chat.completions.with_raw_response.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": msg},
            ],
        )
        # Extract the response from GPT
        reply = response['choices'][0]['message']['content']
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
