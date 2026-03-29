const http = require("http");

const PORT = 8080;
const ROUTES = {
  "/enrollment-service": "http://localhost:5003",
};

function applyCors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
}

function json(res, statusCode, payload) {
  applyCors(res);
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload, null, 2));
}

function findRoute(pathname) {
  return Object.entries(ROUTES).find(
    ([prefix]) => pathname === prefix || pathname.startsWith(`${prefix}/`),
  );
}

async function proxyRequest(req, res, prefix, targetBase) {
  const upstreamPath = req.url.slice(prefix.length) || "/";
  const upstreamUrl = new URL(upstreamPath, targetBase);
  const chunks = [];

  for await (const chunk of req) {
    chunks.push(chunk);
  }

  const body = Buffer.concat(chunks);
  const headers = { ...req.headers };
  delete headers.host;
  delete headers.connection;

  const requestInit = {
    method: req.method,
    headers,
    redirect: "manual",
  };

  if (!["GET", "HEAD"].includes(req.method) && body.length > 0) {
    requestInit.body = body;
  }

  const upstream = await fetch(upstreamUrl, requestInit);
  const buffer = Buffer.from(await upstream.arrayBuffer());
  const responseHeaders = Object.fromEntries(upstream.headers.entries());

  delete responseHeaders["content-encoding"];
  delete responseHeaders["content-length"];
  delete responseHeaders.connection;

  applyCors(res);
  res.writeHead(upstream.status, responseHeaders);
  res.end(buffer);
}

const server = http.createServer(async (req, res) => {
  const requestUrl = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  const { pathname } = requestUrl;

  console.log(`[Gateway] ${req.method} ${pathname}`);

  if (req.method === "OPTIONS") {
    applyCors(res);
    res.writeHead(204);
    res.end();
    return;
  }

  if (pathname === "/health") {
    json(res, 200, {
      status: "OK",
      gateway: "API Gateway",
      timestamp: new Date().toISOString(),
      routes: {
        enrollment: "http://localhost:8080/enrollment-service",
      },
    });
    return;
  }

  const matchedRoute = findRoute(pathname);
  if (!matchedRoute) {
    json(res, 404, { error: "Route not found on API Gateway" });
    return;
  }

  try {
    await proxyRequest(req, res, matchedRoute[0], matchedRoute[1]);
  } catch (error) {
    json(res, 502, {
      error: "Failed to reach upstream service",
      details: error instanceof Error ? error.message : "Unknown gateway error",
    });
  }
});

server.listen(PORT, () => {
  console.log(`API Gateway running on http://localhost:${PORT}`);
  console.log(
    `Enrollment Service route: http://localhost:${PORT}/enrollment-service`,
  );
  console.log(
    `Enrollment Swagger route: http://localhost:${PORT}/enrollment-service/api-docs/`,
  );
});
