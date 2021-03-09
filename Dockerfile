# build xxxxx/xxx/task-exporter:0.1.0

FROM python:3.9-slim

WORKDIR /app

# both files are explicitly required!
COPY . /app/

RUN pip install pipenv && \
  apt-get update && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
  pipenv install --deploy --system && \
  apt-get remove -y gcc python3-dev libssl-dev && \
  apt-get autoremove -y && \
  pip uninstall pipenv -y

CMD ["python", "main.py"]