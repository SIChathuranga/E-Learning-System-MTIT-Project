# API Gateway

This workspace copy includes a dependency-free Node.js gateway so the Enrollment Service can be demonstrated immediately.

## Run

```bash
cd api-gateway
node app.js
```

## URLs

- Health: `http://localhost:8080/health`
- Enrollment API: `http://localhost:8080/enrollment-service/enrollments`
- Enrollment Swagger: `http://localhost:8080/enrollment-service/api-docs/`

## Team Contract

If the shared team gateway uses Express and `http-proxy-middleware`, the equivalent route is:

```js
app.use(
  "/enrollment-service",
  createProxyMiddleware({
    target: "http://localhost:5003",
    changeOrigin: true,
    pathRewrite: { "^/enrollment-service": "" },
  }),
);
```
