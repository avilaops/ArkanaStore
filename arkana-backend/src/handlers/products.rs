use crate::AppState;
use actix_web::{get, web, HttpResponse};

#[get("/products")]
pub async fn list_products(_state: web::Data<AppState>) -> HttpResponse {
    let products: Vec<serde_json::Value> = vec![];
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "data": products,
        "total": 0
    }))
}

#[get("/products/{id}")]
pub async fn get_product(_state: web::Data<AppState>, _id: web::Path<String>) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": false,
        "error": "Not implemented"
    }))
}

#[get("/products/search")]
pub async fn search_products(_state: web::Data<AppState>) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "data": [],
        "total": 0
    }))
}
