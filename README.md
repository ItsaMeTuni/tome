# Tome
A notebook and wiki app built for how you think.

Almost all existing apps have a forced taxonomy, placing arbitrary boundaries between
hierarchical levels that inhibit free-form note-taking.

Tome tries to solve this problem with a simple but powerful tree structure and quick
cross-referencing tools to build a full network that mirrors your brain.

For example, many solutions, even those which allow unlimited nesting of pages, create
boundaries between files, disconnecting them from each other. To me, the typical

> Category -> Page -> Heading 1 -> ... -> Heading 6 -> Bullet points -> ...

is just fluff on top of a basic graph of nodes. This structure is flexible enough to
be used for anything!

- To-do lists
- Personal knowledge bases
- Product documentation
- Journals/diaries
- Issue tracking and other project management tools
- Customer relationship management (CRM)
- Note-taking and studying

All of these things can be combined into one app, with the API, ~~rapid node references,
and powerful search~~ to tie nodes together.

## Features
- Flexible hierarchical structure to model how your memory works and work for any
use-case
- ~~Item references for rapid information mapping~~ **coming soon!**
- ~~Many item types to save all sorts of things (images, links, passwords, files...)~~
**coming soon!**
- ~~Multiple workspaces to separate your work, study, and home life~~ **coming soon!**
- Responsive and customisable web interface ~~with keyboard shortcuts~~ **coming soon!**
- ~~Edit history on all items for auditing and revision control~~ **coming soon!**
- ~~Fine-grained permissions for advanced identity and access management~~
**coming soon!**
- ~~Powerful search system~~ **coming soon!**
- Modern security features like multi-factor authentication ~~and end-to-end encryption~~
**coming soon!**
- Advanced REST-ful API for automation
- Easily self-hostable with Docker Compose so your data stay in your control
- ~~Scalable from tiny single-user home installations to massive enterprise deployments~~
**nope**
- ~~Public access so no account is required~~ **coming soon**
- Free and open source (licensed under the [Apache Licence 2.0](./LICENCE.txt))

## Install

You will need Docker and Docker Compose installed on your server.

1. Copy the `docker-compose.yml` file, and customise it to your liking
2. Copy the `example.env` file to `.env`
3. Create a random password to use for the PostgreSQL password and Secret Key.
    - For example: `cat /dev/urandom | tr -dc a-z | head -c 20; echo`
    
    and then replace them in the `.env` file
    
For full `.env` configuration reference, see ~~the docs~~
[`backend/tome/settings`](./backend/tome/settings/)

## FAQ

### Q. Why doesn't it have bold/italic/etc. inline formatting?

A. To me, part of the idea of this app is that you can nest levels of hierarchical
structure for your notes, so if you want to emphasise part of a node you should split
it into some children with links

### Q. Why doesn't it have XYZ feature?

A. This is a passion project developed in my limited free time. Create an issue and
thumbs-up them to tell me what to work on. Or contribute yourself!

## Development
*(see also: [Contributing](#Contributing))*

Tome's backend is written in Python, and the frontend is written in Vue.js. For more
information, see the README files in the frontend and backend directories.

The best way to set up a development environment is with Docker and Docker-Compose. It
might work outside Docker, but I won't recommend or support it.

I work on Linux (Arch), and these instructions are designed to be used on it. macOS
should mostly work; Windows almost certainly won't (use WSL, or install a better OS).

1. Install [Docker](https://docs.docker.com/get-docker/) and
[Docker Compose](https://docs.docker.com/compose/install/) (don't worry, you don't need
to know much unless you're significantly changing the project architecture)
2. Copy `docker-compose.override.example.yml` to `docker-compose.override.yml`
3. Edit `docker-compose.override.yml` to your liking (optional)
4. Copy `example.env` to `.env`
5. Edit `.env`:
    - Generate random passwords for the PostgreSQL password and Secret Key.
        - For example: `cat /dev/urandom | tr -dc a-z | head -c 20; echo`
    - Set the `USERID` to your Unix user ID (use `id`)
6. Run `sudo docker-compose up -d`
7. The frontend is now available at `http://localhost` and the backend at
`http://localhost/api`

Additional instructions to perform common development tasks are provided in the frontend
and backend directories' READMEs.

### Version Bump
List of places where the version needs to be updated:
- [`backend/tome/__init__.py`](./backend/tome/__init__.py)
- [`frontend/package.json`](./frontend/package.json)
