FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

COPY infra/vllm/entrypoint.py .

CMD [ "python", "entrypoint.py" ]