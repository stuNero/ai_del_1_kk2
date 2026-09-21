# ai_del_1_kk2

## How to run

### IMPORTANT
Before running the app, download the `.csv` data from [kaggle](https://www.kaggle.com/datasets/mobeenfatimah/mental-health-and-burnout-prediction-dataset) and put in `data` folder (create it if it's not present, it should be named 'data'). 
**The app is unusuable without this.**

### Instructions
From the project root, install the dependencies:

```bash
pip install -r requirements.txt
```
#### To run the whole application

```bash
py run.py
```

#### To run specific part of the application

To create the database with the raw dataset:

```bash
cd src/loaders
python load_data.py
```

To clean the dataset and leave only features and target without missing values:

```bash
cd src/loaders
python clean_data.py
```

To evaluate the regression models and save the best to the database:

```bash
cd src/models
python reg_model_eval.py
```

Start the Streamlit app from the `src` directory:

```bash
cd src/app
streamlit run app.py
```
(add `server.headless true` after `run app.py` to avoid the browser opening automatically)

Open the URL shown in the terminal, usually `http://localhost:8501`.
