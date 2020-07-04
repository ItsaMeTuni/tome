# Tome
A notebook and wiki app built for how you think.

Almost all existing apps have a forced taxonomy, placing arbitrary boundaries between hierarchical levels that inhibit free-form note-taking. Tome tries to solve this problem with a simple but powerful tree structure and quick cross-referencing tools to build a full network that mirrors your brain.

## Features
- ~~Flexible hierarchical structure to model how your memory works~~ **coming soon!**
- ~~Item references for rapid information mapping~~ **coming soon!**
- ~~Many item types to save all sorts of things (images, links, passwords, files...)~~ **coming soon!**
- ~~Multiple workspaces to separate your work, study, and home life~~ **coming soon!**
- Responsive and customisable web interface with keyboard shortcuts
- ~~Edit history on all items for auditing and revision control~~ **coming soon!**
- ~~Fine-grained permissions for advanced identity and access management~~ **coming soon!**
- ~~Modern security features like multi-factor authentication and end-to-end encryption~~ **coming soon!**
- ~~Advanced RESTful API for automation~~ **coming soon!**
- Easily self-hostable with Docker Compose so your data stay in your control
- ~~Scalable from tiny single-user home installations to massive enterprise deployments~~ **nope**
- Free and open source (licensed under the [Apache Licence 2.0](./LICENCE.txt))

## Install
### Using Docker Compose (recommended)
You will need Docker and Docker Compose installed.

1. Copy the `docker-compose.yml` file
2. Copy the `example.env` file and rename it to `.env`
3. Create a random password to use for the PostgreSQL password and Secret Key.
    Here's a simple way to generate these:
    ```bash
    openssl rand -hex 24
    ```
    and then replace them in the `.env` file

### Manually (not recommended)
*TODO*

## Development
Tome's backend is written in Python, and the frontend is written in Vue.js. For more information, see the README files in the frontend and backend directories.
