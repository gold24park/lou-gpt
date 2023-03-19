A simple cli demo program based on OpenAI GPT-3.5 Turbo API

![screenshot](./screenshots/screenshot1.png)

## Getting started (Windows)
Download `dist/gpt.exe` file

Open terminal, go to the path you downloaded. 

Run `gpt.exe` with an argument: OpenAI API Key.
```commandline
./gpt.exe <YOUR_OPENAI_API_KEY>
```

## Getting started with Python

#### Setup Environment
Copy & paste your OpenAI API Key on `.env`
```commandline
OPENAI_API_KEY="sk-***************************************"
MAX_TIMEOUT=20
MODEL="gpt-3.5-turbo"
```

#### Install dependencies
```commandline
pip install -r requirements.txt
```

#### Run!
```commandline
python main.py
```


## How to get an OpenAI API KEY
https://platform.openai.com/account/api-keys