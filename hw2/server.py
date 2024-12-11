import openai
import openai_secrets  # Assuming this module contains your API key

# Correct way to set the OpenAI API key
openai.api_key = openai_secrets.SECRET_KEY

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getHelp')
def getHelp():
    return render_template('getHelp.html')

@app.route('/optimize')
def optimize():
    return render_template('optimize.html')

@app.route('/get_help_with_problem', methods=['POST'])
def get_help_with_problem():
    try:
        global problem_input
        data = request.get_json()
        problem_input = data.get("problem")
        global last_commented_code

        # Construct the GPT prompt
        prompt = (f"Firstly greet the user in a friendly manner and tell them you'll guide them "
                  f"through the problem in the language they are asking for. "
                  f"This is the problem and the language: {problem_input}. "
                  "Then explain this LeetCode problem in a manner that a complete beginner can understand. "
                  "Comment out each line of the code as you go through, highlighting the key concepts."
                  f"Do not reveal the big o.")

        # Send the prompt to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        # Correct way to access the response:
        solution = response.choices[0].message['content'].strip()
        last_commented_code = solution
        return jsonify({"commentedCode": solution})

    except Exception as e:
        print(f"Error occurred: {e}")  # This will print the exact error in the Flask console
        return jsonify({"error": str(e)}), 500
    
@app.route('/optimize_the_current_code', methods=['POST'])
def optimize_the_current_code():
    try:
        global problem_input
        data = request.get_json()
        problem_input = data.get("problem")

        # Construct the GPT prompt
        prompt = (f"Firstly greet the user in a friendly manner and you'll take a look at "
                  f"their current code in the code's language"
                  f"This is the code they have submitted: {problem_input}. "
                  "Then explain this LeetCode problem in a manner that a complete beginner can understand. "
                  "Comment out each line that was optimized and give a reason why. ")

        # Send the prompt to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        # Correct way to access the response:
        solution = response.choices[0].message['content'].strip()
        return jsonify({"commentedCode": solution})

    except Exception as e:
        print(f"Error occurred: {e}")  # This will print the exact error in the Flask console
        return jsonify({"error": str(e)}), 500
    
    

@app.route('/get_big_o', methods=['POST'])
def get_big_o():
    try:
        data = request.get_json()
        theNewProblem = data.get("newProblem")
        theNewestCode = data.get("last_commented_code")

        # Construct a more detailed GPT prompt
        prompt = (
            "Analyze the following code snippet carefully and determine its time complexity. "
            f"The code being analyzed is: {theNewestCode}\n\n"
            f"The user's guess for the time complexity is: {theNewProblem}\n\n"
            "Please follow these steps:\n"
            "1. Say 'Correct if the user's guess is correct' otherwise 'Incorrect if the user in incorrect' \n"
            "2. Provide a detailed explanation of how you arrived at the time complexity\n"
            "3. Explain why the complexity is what it is, highlighting key algorithmic characteristics"
        )

        # Send the prompt to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500  # Increased to allow for more detailed explanation
        )

        # Correct way to access the response:
        solution = response.choices[0].message['content'].strip()
        return jsonify({"commentedCode": solution})

    except Exception as e:
        print(f"Error occurred: {e}")  # This will print the exact error in the Flask console
        return jsonify({"error": str(e)}), 500
    
rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
@app.route('/rate_answer', methods=['POST'])
def rate_answer():
    data = request.get_json()
    rating = data.get('rating')
    if rating and 1 <= rating <= 5:
        rating_counts[rating] += 1  # Update the count for the given rating
        return jsonify({"message": "Rating submitted successfully."}), 200
    else:
        return jsonify({"message": "Invalid rating."}), 400

if __name__ == "__main__":
    app.run(debug=True)
