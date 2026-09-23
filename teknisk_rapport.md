---
created: 2026-09-22 10:28
updated: 2026-09-23 10:50
---
## Bakgrund till arbetet

Först ville vi skapa en klassificerings modell som kunde ta emot bilder av t.ex hundraser eller svampar och prediktera deras ras/art, men läraren förklarade att det var lite överkurs och förmodligen för komplext, så vi valde bort allt som var bild relaterat. 

Men svampar låg kvar som en idé hos oss så ville vi göra nånting svamprelaterade. Det vi hade för idé var att, med hjälp av [SLUs artdatabank](https://www.slu.se/artdatabanken/), kunna prediktera sannolikhet att hitta svampar på en viss tid och plats. Men efter vi utförskade datan och pratade med läraren, insåg vi att det var extremt svårt att komma på en POC i god tid med den kunskapen vi har.

Så nu var vi tvungna att hitta en annan idé, och började vi kolla på Kaggles utbud av dataset och kom på en lista av dataset vi tänkte var intressanta. Där höll vi alla med på att [Mental Health & Burnout Prediction](https://www.kaggle.com/api/v1/datasets/download/mobeenfatimah/mental-health-and-burnout-prediction-dataset) var det mest lockande datasetet för att prediktera utmattnings risk baserat på användarens livsstil.


## Huvudresultat

Datasetet innehöll olika kolumner som kunda funka som target variablen, som *burnout_score*, som är en numerisk skala mellan 0-100 och *burnout_risk*, som är kategoriska värden liksom *low*, *moderate*, *high*.

Vi valde *burnout_score* som våran target för en regressionsmodell eftersom den har modellen var den vi kände oss mer trygga med för att börja med projektet. Men vi sa från början att, om tiden hade tillåtit det, vi skulle implementera en klassificeringsmodell med *burnout_risk* som target istället, och ge användaren både en prediktion om *burnout_score* och *burnout_risk*.

Sen fanns liknande kolumner som *anxiety_score* eller *stress_level* som vi hade också velat änvänd om vi hade haft mer tid att göra så.

## Teknisk Specifikation
### Tech Stack
#### Databas
- `sqlite3`
#### Backend
- `python` : ver. `3.14.4`
#### Frontend
- `Streamlit` + `python`
#### Tester
- `pytest`
- `unittest`

### Standardbibliotek
- `sqlite3`: Används för lagring och överföring av datan: dataset och modeller
- `pathlib`: Används flitigt i repot för [hantering av filvägar](src/config/paths.py)
- `contextlib`: Används mest i kombination med sqlite för att stänga anslutningar till databasen
- `io`: Används för inläsning av bytes från filer såsom modellen i databasen
- `time`: Används för mätning av tid för modellträning
- `typing`: Används för typning av python funktion's parametrar
- `warnings`: Används för borttagningen av ofarliga varningar i konsollen
- `zipfile`: Används för öppnandet av zipfiler, t.ex. dataset fallback metoden
- `re`: Används vid regex matchning i testerna. 
### Externa paket
- `streamlit`: Används som front-end bibliotek för att använda [appen](src/app/app.py). 
- `matplotlib`: Används för visualiseringar av datan
- `seaborn`: Används för visualiseringar av datan
- `pandas`: Används mestadels för utforskning och hantering av datasetet
- `numpy`: Används lite för vissa matematiska metoder och data utforskning i [EDA](notebooks/EDA.ipynb)
- `joblib`: Används för sparning av modell
- `fastapi`: Används för [koppling](src/api/endpoints.py) mellan backend och frontend. Används också för att mocka api och modell i tester.
- `requests`: Används för att göra [api anrop](src/app/app.py#L82) och inläsning av [url](src/loaders/load_data.py)
- `pytest`: Största biblioteket i [unit testerna](tests/unit/test_load_data.py).

*Många av ovanstående bibliotek används också i [testning](tests/unit/test_load_data.py) utav appen*

#### Sci-Kit Learn
##### Modeller
- `sklearn.ensemble`: 
- `sklearn.linear_model`
- `sklearn.tree`
##### Hjälp-paket
- `sklearn.metrics`
- `sklearn.model_selection`
- `sklearn.pipeline`
- `sklearn.preprocessing`
Ovanstående Sci-Kit Learn paket används i hela modell pipelinen: 
[EDA](notebooks/EDA.py) -> [Train -> Val -> Test](src/models/reg_model_eval.py)

## Utvärdering av grupparbetet
> vad har varit bra, vad har ni lärt er, hur har arbetet med Git & GitHub fungerat, något ni hade 
> gjort annorlunda?