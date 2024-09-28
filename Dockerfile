FROM python:3.9-slim

WORKDIR /chef_app

COPY /chef_app/requirements.txt .
COPY /chef_app .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg
RUN apt-get update
#RUN sed -i 's/deb.debian.org/deb.debian.org/mirror/debian.org/' /etc/apt/sources.list
RUN apt-get update && apt-get upgrade
RUN playwright install --with-deps chromium
RUN apt-get install -y libxcursor1 libgtk-3-0 libgdk-pixbuf2.0-0 libpangocairo-1.0-0 libcairo-gobject2
RUN playwright install --with-deps chromium
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# CMD ["python", "main.py"]
CMD ["gunicorn", "-w", "1", "main:app"]