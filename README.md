# ftps3

An AWS Lambda script that syncs an FTP to S3.

To test locally

```bash
pipenv install
SERVER=server USER=user PASSWORD=password BUCKET=bucket pipenv run python ftps3
```
