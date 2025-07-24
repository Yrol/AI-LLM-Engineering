FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl

COPY ollama-init.sh /ollama-init.sh
RUN chmod +x /ollama-init.sh

ENTRYPOINT ["/ollama-init.sh"]
