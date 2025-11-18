
// sentry.server.config.ts - Next.js server
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
  profilesSampleRate: 0.1,
  beforeSend(event) {
    // Scrub PII and secrets
    if (event.request && event.request.headers) {
      delete (event.request.headers as any)['authorization'];
    }
    return event;
  }
});
