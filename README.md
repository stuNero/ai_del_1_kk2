# Burnout Predictor

## How to run

### IMPORTANT
If the dataset fails to be fetched from Kaggle's URL, you can download it [yourself](https://www.kaggle.com/datasets/mobeenfatimah/mental-health-and-burnout-prediction-dataset) and put the ZIP file in the project root folder. The program then would fallback to fetch the dataset from there.

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

Start the backend
```bash
py -m uvicorn src.api.endpoints:app --reload
```

Open the URL shown in the terminal, usually `http://localhost:8000`. The endpoints can be tested using Swagger att `http://localhost:8000/docs`


Start the Streamlit app from the `src` directory:

```bash
cd src/app
streamlit run app.py
```
(add `server.headless true` after `run app.py` to avoid the browser opening automatically)

Open the URL shown in the terminal, usually `http://localhost:8501`.


#### To run tests

From the project root:

```bash
pytest -v
```

**IMPORTANT** the database and tables `burnout_data`, `burnout_data_clean` and `models` should be created and populated for the tests to work. It's recommended to run the whole application or at least the steps needed to create the mentioned components.