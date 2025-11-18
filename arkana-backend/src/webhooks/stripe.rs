use actix_web::{post, web, HttpResponse};

#[post("/stripe")]
pub async fn handle_webhook(body: web::Json<serde_json::Value>) -> HttpResponse {
    tracing::info!("Stripe webhook received: {:?}", body);
    HttpResponse::Ok().json(serde_json::json!({"status": "ok"}))
}
