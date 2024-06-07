[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask3&demo-title=Flask%203%20%2B%20Vercel&demo-description=Use%20Flask%203%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask3-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)

# Flask + Vercel

we use Flask 3 on Vercel with Serverless Functions

## How it Works

The API have 2 endpoints until now:
1) /report type=POST
2) /iframe type=GET


### Report wait a body to insert on database like this:

{
  "lat": -23.838013,
  "long":  -44.719352
}

Iframe return a iframe html in real time of the map with reports on last 12hrs

### Map
<img src="https://github.com/Victor-Otsuga/cav-91/assets/105857027/94daf6c6-7c54-40ed-a31e-f0a8ecea3515">


### Running Locally

```bash
npm i -g vercel
vercel dev
```

The Flask application is now available at `http://localhost:3000`.

