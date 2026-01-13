# Online Library

This project is an online library with a book recommendation system. It is a
full stack app with React.js and TailwindCSS for the frontend, FastAPI for the
backend, PostgreSQL for the database, and it uses a self-trained ML model for the
recommendation system (the model is not yet ready). The book database used is
the [Project Gutenberg](https://www.gutenberg.org) MarcXML catalog.

## Install

### Prerequisites
  
* Python 3.11 (preferred especially for the ML part) or above
* Node.js v24.11.0
* PostgreSQL

### Cloning the repo

```bash
git clone https://github.com/aignosia/online-library.git
```

### Backend Configuration

* Using uv

  ```bash
  # Enter the back directory
  cd back
  # Create a virtual environment
  uv venv 
  # Although uv use the created virtual environment by default to install package,
  # if you want to activate the virtual environment to make its packages available,
  # use these commands :
  source .venv/bin/activate # for MacOS or Linux
  .venv\Scripts\activate # for Windows
  # Install the requirements packages
  uv pip install -r requirements.txt
  # Copy the .env.example file to .env and replace default entries by your own configuration
  cp .env.example .env
  # run the app
  uv run fastapi dev 
  ```

* Using other Python installation (eg. Pyenv)

  ```bash
  # Create virtual environment
  python -m venv venv
  # Activate virtual environment
  source .venv/bin/activate # for MacOS or Linux
  .venv\Scripts\activate # for Windows
  # Install the requirements packages
  pip install -r requirements.txt
  # Copy the .env.example file to .env and replace default entries by your own configuration
  cp .env.example .env
  # run the app
  fastapi dev
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
  wget -P path/to/you/directory https://www.gutenberg.org/cache/epub/feeds/pgmarc.xml
  # Enter the back directory
  cd back
  # To seed the default user
  uv run -m scripts.seed_db.py --user # if using uv
  python -m scripts.seed_db.py --user # for other python installation
  # To seed the books
  uv run -m scripts.seed_db.py --books --file /path/to/your/file # or
  python -m scripts.seed_db.py --books --file /path/to/your/file
  # To seed both
  uv run -m scripts.seed_db.py --all --file /path/to/your/file # or
  python -m scripts.seed_db.py --all --file /path/to/your/file
  ```

### Machine Learning

* The ML model is not ready yet, but you can open the `eda.py` file in an
  editor that support Jupytext syntax if you are interested in my data
  analysis process. You can also convert it to a Jupyter notebook file using
  Jupytext or another tool if you prefer notebook view.

* But before running it, you need to run the `data_preparation.py` script to
  get the data used in the analysis. To run the `data_preparation.py` script,
  follow these steps:

  ```bash
  # Enter the ml directory
  cd ml
  # Create data directory and copy your MarcXML file inside
  # There is no option to specify custom filename yet
  mkdir data && cp path/to/you/file ./data/pgmarc.xml 
  # Run data conversion pipeline
  python -m src.data_preparation.py
  ```

## Usage

* Frontend: `http://localhost:5173`
* API documentation:
  * Swagger: `http://localhost:8000/docs`
  * Redoc: `http://localhost:8000/redoc`

## License

This project is licensed under the [MIT License](./LICENSE)
