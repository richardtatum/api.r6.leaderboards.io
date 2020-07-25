# api.r6.leaderboards.io
Basic API for r6.leaderboards.io that is used predominantly with the [R6 Discord Bot](https://github.com/richardtatum/r6_discord_bot)

API tokens available on request from our [contact form](https://r6.leaderboards.io/contact). 

## Deploy

### Requirements
- nodejs
- serverless
- AWS CLI

Install serverless

`npm install -g serverless`

Add additional serverless plugins

```bash
sls plugin install -n serverless-wsgi
sls plugin install -n serverless-python-requirements
```

Set AWS authentication tokens

```bash
export AWS_ACCESS_KEY_ID=<Access key ID>
export AWS_SECRET_ACCESS_KEY=<Secret access key>
```

Deploy to AWS

`sls deploy`


## Authors

* **Richard Tatum** - *Python/API Code* - [RichardTatum](https://github.com/richardtatum)
* **Josh Edney** - *Architecture/Serverless integration* - [JoshEdney](https://github.com/joshedney)
