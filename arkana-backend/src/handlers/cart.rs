use crate::AppState;
use actix_web::{get, post, put, web, HttpResponse};

#[post("/cart/add")]
pub async fn add_to_cart(
    _state: web::Data<AppState>,
    _body: web::Json<serde_json::Value>,
) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "message": "Item added to cart"
    }))
}

#[get("/cart/{session_id}")]
pub async fn get_cart(_state: web::Data<AppState>, _session_id: web::Path<String>) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "data": {
            "items": [],
            "total": 0.0
        }
    }))
}

#[put("/cart/{session_id}")]
pub async fn update_cart(
    _state: web::Data<AppState>,
    _session_id: web::Path<String>,
    _body: web::Json<serde_json::Value>,
) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "message": "Cart updated"
    }))
}
