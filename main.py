from flask import Flask,request,render_template,jsonify,session
import openai

app=Flask(__name__)
app.secret_key='abc'

openai.api_key='xxxxxxxxxxxxxxxxxxx'

previous_chat_history_size=30

def generate_response_api(input,chat_history=[]):
    chat_history.append({"role":"user","content":input})
    chat_history=chat_history[-previous_chat_history_size:]
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},  # System role (optional)
        {"role": "user", "content": input}  # User's message
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    return response.choices[0].message.content

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/get_response',methods=['POST'])
def get_response():
    user_message=request.form.get('user_message')
    chat_history=session.get('chat_history',[])
    
    bot_response=generate_response_api(user_message,chat_history)
    
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": bot_response})
    
    chat_history = chat_history[-previous_chat_history_size:]
    session['chat_history'] = chat_history
    
    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(debug=True)
    