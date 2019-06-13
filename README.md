# leaderboard_api
API for leaderboards.io

## Deploy

### Requirements
- nodejs
- serverless
- AWS CLI

Install serverless

`npm install -g serverless`

Add additional serverless plugins

```sls plugin install -n serverless-wsgi
sls plugin install -n serverless-python-requirements```

Set AWS authentication tokens

```export AWS_ACCESS_KEY_ID=<Access key ID>
export AWS_SECRET_ACCESS_KEY=<Secret access key>```

Deploy to AWS

`sls deploy`
