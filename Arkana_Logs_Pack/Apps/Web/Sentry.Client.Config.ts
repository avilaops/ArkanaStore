
// sentry.client.config.ts - Next.js client
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.0,
  replaysOnErrorSampleRate: 0.1,
  beforeSend(event) {
    if (event.request) {
      // Purge PII
      if (event.request.headers) {
        delete (event.request.headers as any)['authorization'];
      }
      if (event.request.cookies) {
        event.request.cookies = {};
      }
    }
    return event;
  }
});
