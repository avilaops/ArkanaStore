
// Azure Functions v4 (Node 20) - Create Mercado Pago preference
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import * as Sentry from "@sentry/node";
import appInsights from "applicationinsights";

// Init telemetry
if (!appInsights.defaultClient) {
  appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING || "")
    .setAutoCollectRequests(true)
    .setAutoCollectPerformance(true)
    .setAutoCollectExceptions(true)
    .setAutoCollectDependencies(true)
    .setAutoDependencyCorrelation(true)
    .start();
}
const ai = appInsights.defaultClient;

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
  profilesSampleRate: 0.1,
  integrations: [Sentry.extraErrorDataIntegration()],
  beforeSend(event) {
    // Scrub PII
    if (event.request && event.request.headers) {
      delete (event.request.headers as any)["authorization"];
    }
    return event;
  }
});

export async function handler(req: HttpRequest, ctx: InvocationContext): Promise<HttpResponseInit> {
  const body = await req.json();
  const { productId, quantity } = body || {};
  const userAgent = req.headers.get("user-agent") || "unknown";

  // Simple validation
  if (!productId || !quantity) {
    ai.trackEvent({name:"create_preference_validation_error"});
    return { status: 400, jsonBody: { error: "Missing productId or quantity" } };
  }

  // TODO: read product from products.json or DB
  const price = 100.00; // placeholder
  const amount = price * Number(quantity);

  ai.trackEvent({name:"create_preference_requested", properties:{productId, quantity, amount, userAgent}});

  try {
    // TODO: call Mercado Pago preferences API with access token
    const preferenceId = "pref_dummy_" + Date.now();

    ai.trackEvent({name:"create_preference_success", properties:{preferenceId, amount}});
    return { status: 200, jsonBody: { preferenceId } };
  } catch (err: any) {
    ai.trackException({exception: err});
    Sentry.captureException(err);
    return { status: 500, jsonBody: { error: "failed_to_create_preference" } };
  }
}

app.http("create-preference", {
  methods: ["POST"],
  authLevel: "function",
  handler
});
