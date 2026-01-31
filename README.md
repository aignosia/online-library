# RecoMind

**Website:** [recomind.netlify.app](recomind.netlify.app)

**API SwaggerUI Documentation:** [https://recomind-api.onrender.com/docs](https://recomind-api.onrender.com/docs)

RecoMind is a full-stack online library application created to be simple and to
help the user find books that fit his/her interests.

## Tech Stack

* **Frontend**: React.js & Tailwind CSS.
* **Backend**: FastAPI.
* **Database**: PostgreSQL with pgvector extension.
* **Machine Learning**: A custom recommendation system using content-based
  filtering.

## Data Source

The application uses the Project Gutenberg MarcXML catalog to seed the database.

## Install

### Prerequisites
  
* Python 3.11 (preferred) or above
* Node.js v24.11.0 or above
* PostgreSQL 17 or above
* pgvector 0.7.0 or above

**Note:** If you don't use uv just replace `uv run` by `python` unless specified
otherwise.

### Cloning the repo

```bash
git clone https://github.com/aignosia/online-library.git
```

### Machine Learning

```bash
# Enter the ml directory
cd ml

# Create a virtual environment
# For uv
uv venv
# For other Python installation
python -m venv venv

# Activate the virtual environment
source .venv/bin/activate # for MacOS or Linux
.venv\Scripts\activate # for Windows

# Install the requirements packages
# For uv
uv sync
# For other Python installation
python -m pip install -r requirements.txt

# Convert MarcXML data to a CSV dataset
uv run -m src.data_preprocessing --output /path/to/output/file /path/to/source/file

# Preprocess the dataset for TF-IDF
uv run -m src.tfidf preprocess --output /path/to/output/file /path/to/source/file

# Train the TF-IDF vectorizer and export to a joblib file
uv run -m src.tfidf train --output /path/to/output/file /path/to/source/file

# To test the trained TF-IDF vectorizer
uv run -m src.tfidf test --model /path/to/model/file --data /path/to/data/file book_id
```

### Backend Configuration

```bash
# Enter the back directory
cd back

# Create a virtual environment
# For uv
uv venv
# For other Python installation
python -m venv venv

# Activate virtual environment
source .venv/bin/activate # for MacOS or Linux
.venv\Scripts\activate # for Windows

# Install the requirements packages
# For uv
uv sync
# For other Python installation
python -m pip install -r requirements.txt

# Copy the .env.example file to .env and replace default entries by your
# own configuration
cp .env.example .env

# Run the app
# For uv
uv run fastapi dev 
# For other python installation
fastapi dev app/main.py
```

### Frontend Configuration

```bash
# Enter the front directory
cd front

# Install packages
npm install

# Copy the .env.example file to .env.local and replace default entries by your
# own configuration
cp .env.example .env.local

# Run app
npm run dev
```

### Database Seeding

```bash
# Download Project Gutenberg MarcXML catalog (wget recommended)
wget -P path/to/your/directory https://www.gutenberg.org/cache/epub/feeds/pgmarc.xml

# Enter the back directory
cd back

# To seed the default user
uv run -m scripts.seed user

# To seed the books
uv run -m scripts.seed books --source /path/to/your/marcxml/file 

# To seed book embeddings
uv run -m scripts.seed embeddings
```

## Usage

* Frontend: `http://localhost:5173`
* API documentation:
  * Swagger: `http://localhost:8000/docs`
  * Redoc: `http://localhost:8000/redoc`

## License

This project is licensed under the [MIT License](./LICENSE)
