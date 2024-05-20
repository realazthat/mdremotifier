FROM python:3.12-slim


WORKDIR /mdremotifier

# apt-get -y --no-install-recommends install git=1:2.39.2-1.1 &&
# apt-get -y upgrade &&

COPY . /mdremotifier
RUN apt-get -y update && apt-get -y --no-install-recommends install bash && \
  apt-get -y clean && \
  apt-get -y autoremove && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --no-cache-dir --upgrade pip setuptools wheel && \
  mkdir -p /home/nobody/.local && \
  chown -R nobody:nogroup /mdremotifier /home/nobody/.local && \
  chmod -R a+wrX /mdremotifier


USER nobody
WORKDIR /mdremotifier
ENV PATH=/home/nobody/.local/bin:$PATH
ENV PYTHONPATH=/home/nobody/.local/lib/python3.12/site-packages
RUN pip install --no-cache-dir --prefix=/home/nobody/.local .

# This is where the user will mount their data to.
WORKDIR /data

ENTRYPOINT ["python", "-m", "mdremotifier.cli"]
CMD ["--help"]
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -m mdremotifier.cli --version || exit 1
