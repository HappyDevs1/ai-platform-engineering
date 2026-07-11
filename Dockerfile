FROM runpod/base:0.6.2-cuda12.4.1

COPY infra/vllm/entrypoint.py .

CMD [ "python", "entrypoint.py" ]