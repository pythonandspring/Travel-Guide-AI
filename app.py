from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('gallery.html')  # No need to pass 'places' as we are focusing on the voice search.

@app.route('/search_voice', methods=['POST'])
def search_voice():
    try:
        # Get the speech input from the frontend
        data = request.get_json()
        query = data.get('query', '')  # Get the query sent from the frontend

        # Log the query (For now, just print it in the console)
        print(f"Voice Search Query: {query}")

        return jsonify({
            'status': 'success',
            'query': query  # Return the query back for the frontend to display in the search bar
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while processing your request.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
