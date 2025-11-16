//! # ?? ARKANA STORE - BACKEND API (Rust + Actix-web)
//! 
//! E-commerce de alta performance para produtos maçônicos
//! 
//! ## Features:
//! - REST API completa
//! - Integração com 3 gateways de pagamento
//! - Webhooks seguros e idempotentes
//! - MongoDB para persistência
//! - Tracing e observability
//! 
//! ## Endpoints:
//! - GET  /api/products - Lista produtos
//! - GET  /api/products/:id - Detalhes produto
//! - POST /api/cart/add - Adiciona ao carrinho
//! - POST /api/orders - Criar pedido
//! - POST /webhooks/:gateway - Receber notificações
//! 
//! Data: 16/11/2025
//! Versão: 1.0.0

use actix_web::{web, App, HttpServer, HttpResponse, middleware};
use actix_cors::Cors;
use serde::{Deserialize, Serialize};
use tracing::{info, error};
use std::sync::Arc;
use arkana_shared::*;

mod config;
mod db;
mod handlers;
mod services;
mod webhooks;

use config::AppConfig;

// ===================================================================
// STATE DA APLICAÇÃO
// ===================================================================

pub struct AppState {
    pub config: AppConfig,
    pub db: Arc<db::Database>,
    pub payment_service: Arc<services::PaymentService>,
}

// ===================================================================
// MAIN
// ===================================================================

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Carregar .env
    dotenv::dotenv().ok();

    // Setup logging
    tracing_subscriber::fmt()
        .with_target(false)
        .with_env_filter("arkana_backend=debug,actix_web=info")
        .init();

    // Configurar Sentry
    let _guard = sentry::init((
        std::env::var("SENTRY_DSN").unwrap_or_default(),
        sentry::ClientOptions {
            release: sentry::release_name!(),
            environment: Some(std::env::var("NODE_ENV").unwrap_or_else(|_| "production".into()).into()),
            ..Default::default()
        },
    ));

    info!("?? Iniciando Arkana Store Backend...");

    // Carregar configurações
    let config = AppConfig::from_env().expect("Falha ao carregar configurações");
    
    info!("? Configurações carregadas");
    info!("?? API URL: {}", config.api_base_url);
    info!("?? MongoDB: {}", config.mongo_uri.split('@').last().unwrap_or("***"));

    // Conectar ao MongoDB
    let db = Arc::new(
        db::Database::new(&config.mongo_uri, &config.mongo_db_name)
            .await
            .expect("Falha ao conectar MongoDB")
    );

    info!("? MongoDB conectado");

    // Inicializar serviços
    let payment_service = Arc::new(
        services::PaymentService::new(&config)
    );

    info!("? Payment service inicializado");

    // State compartilhado
    let app_state = web::Data::new(AppState {
        config: config.clone(),
        db,
        payment_service,
    });

    let bind_addr = format!("0.0.0.0:{}", config.port);

    info!("========================================");
    info!("?? ARKANA STORE API RODANDO");
    info!("========================================");
    info!("?? Endereço: http://{}", bind_addr);
    info!("?? Produtos: GET  /api/products");
    info!("?? Carrinho:  POST /api/cart/add");
    info!("?? Pedidos:   POST /api/orders");
    info!("?? Webhooks:  POST /webhooks/:gateway");
    info!("??  Health:   GET  /health");
    info!("========================================");

    // Iniciar servidor
    HttpServer::new(move || {
        let cors = Cors::default()
            .allowed_origin("https://arkanastore.com.br")
            .allowed_origin("http://localhost:8080")
            .allowed_methods(vec!["GET", "POST", "PUT", "DELETE"])
            .allowed_headers(vec![
                actix_web::http::header::AUTHORIZATION,
                actix_web::http::header::CONTENT_TYPE,
            ])
            .max_age(3600);

        App::new()
            .app_data(app_state.clone())
            .wrap(cors)
            .wrap(middleware::Logger::default())
            .wrap(middleware::Compress::default())
            .wrap(sentry_actix::Sentry::new())
            // Health check
            .route("/health", web::get().to(health_check))
            // Products API
            .service(
                web::scope("/api")
                    .service(handlers::products::list_products)
                    .service(handlers::products::get_product)
                    .service(handlers::products::search_products)
                    // Cart
                    .service(handlers::cart::add_to_cart)
                    .service(handlers::cart::get_cart)
                    .service(handlers::cart::update_cart)
                    // Orders
                    .service(handlers::orders::create_order)
                    .service(handlers::orders::get_order)
                    .service(handlers::orders::list_orders)
            )
            // Webhooks
            .service(
                web::scope("/webhooks")
                    .service(webhooks::mercadopago::handle_webhook)
                    .service(webhooks::paypal::handle_webhook)
                    .service(webhooks::stripe::handle_webhook)
            )
    })
    .bind(&bind_addr)?
    .run()
    .await
}

async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "ok",
        "service": "arkana-api",
        "version": env!("CARGO_PKG_VERSION"),
        "timestamp": chrono::Utc::now().to_rfc3339(),
    }))
}
