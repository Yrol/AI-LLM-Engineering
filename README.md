## AI-LLM-Engineering

An experimental project featuring both backend and frontend functionality to interact with Large Language Models (LLMs). For details, see the [Current capabilities](#current-capabilities) section.

### Current capabilities

- **OpenAI**
    - Web summarizer (supports user and system prompts) - cloud based
    - Generic chat capabilities querying via API calls - cloud based
- **Ollama (TinyLlama)**
    - Generic chat capabilities querying via API calls - local LLM

### Prerequisites
- **Docker** installed on the local system

- **OpenAI** 
    - Top up your OpenAI account with a minimum of $5 from the Billing section. API calls typically cost only a fraction of this amount. 
    - Be sure to generate a secret key from the [OpenAI Developer Settings](https://platform.openai.com/settings/organization/api-keys) page, and add it to the .env file located in the project's backend directory. The key should be named `OPENAI_API_KEY`, unless a different name is specified in the backend source code.

        ![](https://i.imgur.com/HWAqYJG.png)
        ![](https://i.imgur.com/cNePAwQ.png)
        ![](https://i.imgur.com/9fb0lXP.png)


### Tech Stack

- **Backend:** Python (Django)
- **Frontend:** Nuxt (Vue) & Tailwind CSS
- **Containerization:** Docker

### How to Start the Services

To start all the service that includes frontend, backend and LLMs, run:
```
docker-compose down && docker-compose up --build -d
```


> **Note:** The TinyLlama model may take a few minutes to download and build within the Ollama container (`ollama_service`). Monitor the container logs for progress.

![](https://i.imgur.com/6ag7TNi.png)

## Launching the App

Open [http://localhost:3000/](http://localhost:3000/) in your preferred browser.

![](https://i.imgur.com/7keBn0C.png)
![](https://i.imgur.com/ZqDNyLi.png)


### API Endpoints

API endpoints are provided in the `Collections` folder, which can be imported as JSON into Postman or Bruno. For example, you can make a request to: `POST http://localhost:8000/api/ollamachat/`


```
curl --location 'http://localhost:8000/api/ollamachat/'
--header 'Content-Type: application/json'
--data '{
"model": "tinyllama",
"messages": [
{
"role": "user",
"content": "Describe some of the business applications of Generative AI"
}
],
"stream": false
}'
```


### Useful commands

Stop all services and build from scratch
```
docker compose down --rmi all --volumes && docker compose build --no-cache && docker compose up -d
```

