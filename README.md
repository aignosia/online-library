# Online Library

This project is an online library with a book recommendation system. It is a
full stack app with React.js and TailwindCSS for the frontend, FastAPI for the
backend, PostgreSQL for the database, and it uses a trained ML model for the
recommendation system (the model is not yet ready). The book database I used is
the [Project Gutenberg](www.gutenberg.org) database using the MarcXML file they
provide on their website but any MarcXML file should work. You can also use
Marc21 file if you modify the file `seed_books.py` a little to support it.

## Install

* Prerequisites :
  * Python 3.11 (preferred especially for the ML part) or above
  * Node.js v24.11.0

* Clone the repo:

```bash
git clone https://github.com/aignosia/online-library.git
```

* For the backend:

  * using uv
  
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
  # run the app
  uv run fastapi dev 
  ```

  * using other Python installation (eg. Pyenv)

  ```bash
  # Create virtual environment
  python -m venv venv
  # Activate virtual environment
  source .venv/bin/activate # for MacOS or Linux
  .venv\Scripts\activate # for Windows
  # Install the requirements packages
  pip install -r requirements.txt
  # run the app
  fastapi dev
  ```

* To seed the database (only MarcXML files are supported unless you modify the code):

```bash
# Enter the back directory
cd back
# To seed the default user
uv run -m scripts.seed_db.py --user # if using uv
python -m scripts.seed_db.py --user # for other python installation
# To seed the books
uv run -m scripts.seed_db.py --books --file "your-file-path"
python -m scripts.seed_db.py --books --file "your-file-path"
# To seed both
uv run -m scripts.seed_db.py --all --file "your-file-path"
python -m scripts.seed_db.py --all --file "your-file-path"
```

* For the frontend:

```bash
# Enter the front directory
cd front
# Install packages
npm install
# Run app
npm run dev
```

* For the ML model:

  * The ML model is not ready yet, but you can open the `eda.py` file in an
    editor that support Jupytext syntax if you are interested in my data
    analysis process. You can also convert it to a Jupyter notebook file using
    Jupytext or another tool if you prefer notebook view.
  
  * But before running it, you need to run the `data_preparation.py` script to
    get the data used in the analysis (Here you should use the Gutenberg MarcXML
    file to get the same results as me). To run the `data_preparation.py` script,
    follow these steps:
  
  ```bash
  # Enter the ml directory
  cd ml
  # Create data directory and copy you MarcXML file inside
  # There is no option to specify custom filename yet
  mkdir data && cp "you-file-path" ./data/pgmarc.xml 
  # Run data conversion pipeline
  python -m src.data_preparation.py
  ```

## Usage

After running the app, open `http://localhost:5173` in your browser to see the frontend.
If you are interested in the API, open `http://localhost:8000/docs` to see the Sagger
documentation or `http://localhost:8000/redoc` to see the Redoc documentation.

## License

This project is licensed under the [MIT License](./LICENSE)
