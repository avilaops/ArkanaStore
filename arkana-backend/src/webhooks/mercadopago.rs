use actix_web::{web, HttpResponse, post};

#[post("/mercadopago")]
pub async fn handle_webhook(body: web::Json<serde_json::Value>) -> HttpResponse {
    tracing::info!("MercadoPago webhook received: {:?}", body);
    HttpResponse::Ok().json(serde_json::json!({"status": "ok"}))
}
