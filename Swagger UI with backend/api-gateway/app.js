const http = require("http");

const PORT = 8080;

const SERVICES = {
  "/student-service": {
    name: "Student Service",
    target: "http://localhost:8000",
    docs: "/docs",
    rewrites: [
      ["/openapi.json", "/student-service/openapi.json"],
      ["/docs/oauth2-redirect", "/student-service/docs/oauth2-redirect"],
      ["url: '/student-service/openapi.json'", "url: window.location.origin + '/student-service/openapi.json'"],
      ['url: "/student-service/openapi.json"', 'url: window.location.origin + "/student-service/openapi.json"'],
    ],
  },
  "/course-service": {
    name: "Course Service",
    target: "http://localhost:5002",
    docs: "/api-docs",
  },
  "/enrollment-service": {
    name: "Enrollment Service",
    target: "http://localhost:5003",
    docs: "/api-docs/",
  },
  "/grade-service": {
    name: "Grade Service",
    target: "http://localhost:5004",
    docs: "/apidocs",
    rewrites: [
      ["/flasgger_static", "/grade-service/flasgger_static"],
      ["/apispec.json", "/grade-service/apispec.json"],
      ["/oauth2-redirect.html", "/grade-service/oauth2-redirect.html"],
    ],
  },
};

function applyCors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PUT, PATCH, DELETE, OPTIONS",
  );
}

function sendJson(res, statusCode, payload) {
  applyCors(res);
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload, null, 2));
}

function findService(pathname) {
  return Object.entries(SERVICES).find(
    ([prefix]) => pathname === prefix || pathname.startsWith(`${prefix}/`),
  );
}

function rewriteRedirectLocation(location, prefix, targetBase) {
  if (!location) {
    return location;
  }

  if (location.startsWith("/")) {
    return `${prefix}${location}`;
  }

  if (location.startsWith(targetBase)) {
    const upstreamUrl = new URL(location);
    return `${prefix}${upstreamUrl.pathname}${upstreamUrl.search}`;
  }

  return location;
}

function rewriteHtml(prefix, body) {
  const service = SERVICES[prefix];

  if (!service || !service.rewrites) {
    return body;
  }

  return service.rewrites.reduce(
    (updatedBody, [from, to]) => updatedBody.split(from).join(to),
    body,
  );
}

async function readRequestBody(req) {
  const chunks = [];

  for await (const chunk of req) {
    chunks.push(chunk);
  }

  return Buffer.concat(chunks);
}

async function proxyRequest(req, res, prefix, service) {
  const upstreamPath = req.url.slice(prefix.length) || "/";
  const upstreamUrl = new URL(upstreamPath, service.target);
  const body = await readRequestBody(req);
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
  const responseHeaders = Object.fromEntries(upstream.headers.entries());
  const contentType = responseHeaders["content-type"] || "";

  delete responseHeaders["content-encoding"];
  delete responseHeaders["content-length"];
  delete responseHeaders.connection;

  if (responseHeaders.location) {
    responseHeaders.location = rewriteRedirectLocation(
      responseHeaders.location,
      prefix,
      service.target,
    );
  }

  applyCors(res);

  if (contentType.includes("text/html")) {
    const html = rewriteHtml(prefix, await upstream.text());
    res.writeHead(upstream.status, responseHeaders);
    res.end(html);
    return;
  }

  const buffer = Buffer.from(await upstream.arrayBuffer());
  res.writeHead(upstream.status, responseHeaders);
  res.end(buffer);
}

function gatewayOverview() {
  return Object.entries(SERVICES).reduce((summary, [prefix, service]) => {
    summary[service.name] = {
      gatewayBaseUrl: `http://localhost:${PORT}${prefix}`,
      directServiceUrl: service.target,
      docsViaGateway: `http://localhost:${PORT}${prefix}${service.docs}`,
    };
    return summary;
  }, {});
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

  if (pathname === "/" || pathname === "/health") {
    sendJson(res, 200, {
      status: "OK",
      gateway: "API Gateway",
      port: PORT,
      timestamp: new Date().toISOString(),
      services: gatewayOverview(),
    });
    return;
  }

  const matchedService = findService(pathname);

  if (!matchedService) {
    sendJson(res, 404, {
      error: "Route not found on API Gateway",
      availablePrefixes: Object.keys(SERVICES),
      healthUrl: `http://localhost:${PORT}/health`,
    });
    return;
  }

  try {
    const [prefix, service] = matchedService;
    await proxyRequest(req, res, prefix, service);
  } catch (error) {
    sendJson(res, 502, {
      error: "Failed to reach upstream service",
      details: error instanceof Error ? error.message : "Unknown gateway error",
    });
  }
});

server.listen(PORT, () => {
  console.log(`API Gateway running on http://localhost:${PORT}`);

  for (const [prefix, service] of Object.entries(SERVICES)) {
    console.log(`${service.name}: http://localhost:${PORT}${prefix}`);
    console.log(`${service.name} docs: http://localhost:${PORT}${prefix}${service.docs}`);
  }
});
