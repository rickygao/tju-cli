# TJU CLI

A command line tool makes your life better in :school: Tianjin University.

:warning: The codebase is not well organized, but I will do my best effort to mantain it. Any PR is welcome.

## Components

- :badminton: `book` makes [booking places](http://cgzx.tju.edu.cn) automatical;
- :book: `classes` helps retrieve grades from [classes](http://classes.tju.edu.cn).

## Usage

1. :package: Install packages according to `requirements.txt` via `conda` or `pip` and activate the enviroment;

   ```shell
   conda create -n tju-cli -y --file requirements.txt
   conda activate tju-cli
   ```

   or

   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. :pencil: \[Optional\] Modify `config.example.json` and rename it to `config.json` or specify config file by setting environment variable `TJU_CLI_CONFIG_PATH`;
3. :runner: Run scripts `book_cli.py` or `classes_cli.py`;
4. :wave: Have a happy day.
