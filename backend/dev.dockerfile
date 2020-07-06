# this is a dockerfile optimised for development, with development dependencies
#  installed, and the option to run under a specific user id to simplify permissions.
# it is optimised more for build speed

FROM python:3.8

ARG USERID
RUN useradd -mUu "${USERID:-1000}" -s /usr/bin/bash -d /home/user user
USER ${USERID:-1000}

# you probably want to mount /home/user/app as a volume to get live-reloading
WORKDIR /home/user/app/
COPY --chown=user:user . .

RUN pip install --upgrade --user pip setuptools poetry && \
/home/user/.local/bin/poetry install --no-root

# use port > 1024 because we aren't running as root
EXPOSE 8078
ENTRYPOINT ["/home/user/.local/bin/poetry", "run"]
CMD ["uvicorn", "--debug", "--reload", "--port", "8078", "--host", "0.0.0.0", "tome.app:app"]
#CMD bash
