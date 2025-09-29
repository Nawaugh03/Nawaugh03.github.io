from flask import Flask, render_template, request, send_file, session, jsonify
from flask_cors import CORS
from ReaderModel import RRModel
import os, uuid

UPLOAD_FOLDER = "Reciept-Reader/Receipts"
app = Flask(__name__)
CORS(app)
#app.secret_key = "supersecretkey"  # needed for Flask sessions


import uuid

def create_session_folder(base="sessions"):
    if not os.path.exists(base):
        os.makedirs(base)
    session_id = str(uuid.uuid4())
    session_path = os.path.join(base, session_id)
    os.makedirs(session_path)
    return session_id, session_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_session")
def start_session():
    session_id, session_path = create_session_folder()
    session["id"] = session_id
    session["path"] = session_path
    rrmodel.reset_results()  # clear any old results
    return f"Session started: {session_id}"

@app.route("/upload_receipt", methods=["POST"])
def upload_receipt():
    if "receipts" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400
    
    files = request.files.getlist("receipts")  # Get ALL files
    saved_files = []

    file = request.files["receipts"]

    for file in files:
        if file.filename == "":
            continue  # Skip empty files
        reciept_destination = os.path.join(os.getcwd(), UPLOAD_FOLDER)
        filepath = os.path.join(reciept_destination, file.filename)
        file.save(filepath)
        saved_files.append(file.filename)

    #ReceiptDestination = os.path.join(os.getcwd(), UPLOAD_FOLDER)
    #filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    #file.save(filepath)

    # TODO: Run your receipt reader here, then send results
    
    if not saved_files:
        return jsonify({"message": "No valid files uploaded"}), 400

    return jsonify({"message": f"Receipts saved: {', '.join(saved_files)}"})

@app.route("/finish")
def finish():
    if "path" not in session:
        return "No active session.", 400

    # Save results into this session folder
    excel_file = os.path.join(session["path"], "Results.xlsx")
    rrmodel.save_results_excel(excel_file)

    # Send Excel file back to user
    return send_file(excel_file, as_attachment=True)

if __name__ == "__main__":
    rrmodel = RRModel("runs/detect/Fine_tuned_model8/weights/best.pt")
    #if not os.path.exists(UPLOAD_FOLDER):
    #    os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)