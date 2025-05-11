# 🎓 LearnLytics - Student Grade Prediction System

This project is an end-to-end system that performs **student grade analysis and prediction** using both academic and behavioral data. It includes a complete pipeline for **data preprocessing**, **exploratory analysis**, **model training**, and **serving predictions via a web frontend**.

---

## 📁 Project Structure

```
.
├── backend/              # FAST API based backend and model serving logic
│   └── model/            # Contains the trained model (zip file to be extracted)
├── frontend/             # React-based frontend for user interaction
├── data/                 # Dataset and data creation scripts
└── LearnLytics.ipynb     # Full notebook: EDA, preprocessing, training, evaluation
```

---

## 📊 Features

* Predicts student grades based on multiple factors
* Uses both **academic** and **behavioral** features
* Web-based interface for user input and predictions
* Interactive **frontend** and REST-based **backend**
* Complete EDA and modeling in Jupyter notebook

---

## 🔧 Setup Instructions

### 1. 📦 Backend Setup 

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:

   **On macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **On Windows:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Unzip the model file inside the `model` folder:

   ```bash
   cd model
   unzip student_grade_predictor.zip
   cd ..
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask server:

   ```bash
   python app.py
   ```

   The backend will be running on `http://localhost:8000/`.

6. **Optional (for external access)**: Tunnel the backend using [ngrok](https://ngrok.com/):

   ```bash
   ngrok http 8000
   ```

   Copy the generated ngrok URL for use in the frontend.

---

### 2. 🖥️ Frontend Setup (React App)

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Open the `learnLyticsFrom.jsx` file and **replace the backend URL** with either:

   * The local URL: `http://localhost:8000`
   * Or the ngrok URL (if used)

3. Install dependencies and start the app:

   ```bash
   npm install
   npm start
   ```

   The app will launch in your browser (usually at `http://localhost:3000`).

---

## 📁 Dataset

The dataset used for this project can be found in the `data/` folder. It contains both raw and processed versions. Scripts or notes on how the dataset was created are also included in this directory.

---

## 📓 Jupyter Notebook

All exploratory data analysis, preprocessing steps, model training, and evaluation are documented in `LearnLytics.ipynb`. This notebook serves as a complete report of the machine learning workflow.


---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
