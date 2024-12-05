from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, template_folder="src")
if __name__ == "__main__":
    app.run(debug=True, port=5001)
# Route to render the main page
@app.route("/")
def index():
    return render_template("index.html")

# API to get all images and their usernames (file names without extension)
@app.route("/api/images")
def get_images():
    skins_folder = os.path.join(app.static_folder, "skins")
    try:
        # Get all image file names from the skins folder
        images = [
            {
                "image_path": f"skins/{file}",
                "username": os.path.splitext(file)[0]  # Get the file name without the extension
            }
            for file in os.listdir(skins_folder)
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        return jsonify(images)
    except FileNotFoundError as e:
        print(f"Error: {e}")  # Debugging line
        return jsonify({"error": "Skins folder not found"}), 500

if __name__ == "__main__":
    app.run(debug=True)
