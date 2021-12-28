# ACP2-Twitter-Profile-Scoring

## Development
### Install dependencies
Install Poetry (package manager): https://pypi.org/project/poetry/

Install packages:
```shell
$ poetry install
```

## Deployment
Add your publish SSH key as authorized key to the target host.

Copy .env.dist as .env and fill the values. DEPLOY_SSH_PORT is optional, 22 is used as default.

Run
```
./deploy.sh
```
