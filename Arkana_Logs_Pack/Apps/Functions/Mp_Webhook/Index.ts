
// Azure Functions v4 (Node 20) - Mercado Pago Webhook
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import * as crypto from "crypto";
import * as Sentry from "@sentry/node";
import appInsights from "applicationinsights";

if (!appInsights.defaultClient) {
  appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING || "")
    .setAutoCollectRequests(true)
    .setAutoCollectExceptions(true)
    .setAutoCollectDependencies(true)
    .start();
}
const ai = appInsights.defaultClient;

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
  profilesSampleRate: 0.1
});

const IDEMP_SECRET = process.env.IDEMP_SECRET || "changeme";

function idemKey(id: string) {
  return crypto.createHmac("sha256", IDEMP_SECRET).update(id).digest("hex");
}

// naive in-memory cache for demo; replace with durable storage in prod
const seen = new Set<string>();

export async function handler(req: HttpRequest, ctx: InvocationContext): Promise<HttpResponseInit> {
  const payload = await req.json().catch(() => ({}));
  const eventId = payload?.id || payload?.data?.id || String(Date.now());
  const key = idemKey(eventId);

  ai.trackEvent({ name: "mp_webhook_received", properties: { eventId, topic: payload?.type || payload?.type_id || "unknown" } });

  if (seen.has(key)) {
    ai.trackEvent({ name: "mp_webhook_duplicate", properties: { eventId } });
    return { status: 200, body: "duplicate" };
  }
  seen.add(key);

  try {
    const status = payload?.data?.status || "unknown";

    if (status === "approved") {
      ai.trackEvent({ name: "purchase_approved", properties: { eventId } });
      // TODO: persist order, send confirmation email
    } else if (status === "rejected" || status === "cancelled") {
      ai.trackEvent({ name: "payment_failed", properties: { eventId, status } });
    } else {
      ai.trackEvent({ name: "payment_pending", properties: { eventId, status } });
    }

    return { status: 200, body: "ok" };
  } catch (err: any) {
    ai.trackException({ exception: err });
    Sentry.captureException(err);
    return { status: 500, body: "error" };
  }
}

app.http("mp-webhook", {
  methods: ["POST"],
  authLevel: "function",
  handler
});
