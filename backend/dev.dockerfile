# this is a dockerfile optimised for development, with development dependencies
#  installed, and the option to run under a specific user id to simplify permissions.
# it is optimised more for build speed

FROM python:3.8

ARG USERID
RUN useradd -mUu "${USERID:-0}" -s /usr/bin/bash -d /home/user user || true
USER ${USERID:-0}

# you probably want to mount /home/user/app as a volume to get live-reloading
WORKDIR /home/user/app/
COPY . .

RUN pip install --upgrade --user pip setuptools poetry \
&& poetry install --no-root

# use port > 1024 because we aren't running as root
EXPOSE 8078
ENTRYPOINT poetry run
CMD uvicorn --debug --reload --port 8078 --host 0.0.0.0 tome.app:app
