use crate::AppState;
use actix_web::{get, post, web, HttpResponse};

#[post("/orders")]
pub async fn create_order(
    _state: web::Data<AppState>,
    _body: web::Json<serde_json::Value>,
) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "data": {
            "order_id": "ARK-20251118-001",
            "status": "pending_payment"
        }
    }))
}

#[get("/orders/{order_id}")]
pub async fn get_order(_state: web::Data<AppState>, _order_id: web::Path<String>) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": false,
        "error": "Order not found"
    }))
}

#[get("/orders")]
pub async fn list_orders(_state: web::Data<AppState>) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "data": [],
        "total": 0
    }))
}
