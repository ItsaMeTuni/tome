FROM node:lts-buster

ARG USERID
RUN userdel -fr node && \
    useradd -mUu "${USERID:-1000}" -s /usr/bin/bash -d /home/user user
USER user

# you probably want to mount /home/user/app as a volume to get live-reloading
COPY --chown=${USERID:-1000} . /home/user/app

WORKDIR /home/user/app/

RUN npm install

# use port > 1024 because we aren't running as root
EXPOSE 8078

CMD ["npm", "run", "serve", "--", "--port", "8078"]
