//! ARKANA STORE - BACKEND API (Rust + Actix-web)
//!
//! E-commerce de alta performance para produtos maconicos

use actix_cors::Cors;
use actix_web::{middleware, web, App, HttpResponse, HttpServer};
use std::sync::Arc;
use tracing::info;

mod config;
mod db;
mod handlers;
mod services;
mod webhooks;

use config::AppConfig;

pub struct AppState {
    pub config: AppConfig,
    pub db: Arc<db::Database>,
    pub payment_service: Arc<services::PaymentService>,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();

    tracing_subscriber::fmt()
        .with_target(false)
        .with_env_filter("arkana_backend=debug,actix_web=info")
        .init();

    let _guard = sentry::init((
        std::env::var("SENTRY_DSN").unwrap_or_default(),
        sentry::ClientOptions {
            release: sentry::release_name!(),
            environment: Some(
                std::env::var("NODE_ENV")
                    .unwrap_or_else(|_| "production".into())
                    .into(),
            ),
            ..Default::default()
        },
    ));

    info!("Iniciando Arkana Store Backend...");

    let config = AppConfig::from_env().expect("Falha ao carregar configuracoes");

    info!("Configuracoes carregadas");
    info!("API URL: {}", config.api_base_url);

    let db = Arc::new(
        db::Database::new(&config.mongo_uri, &config.mongo_db_name)
            .await
            .expect("Falha ao conectar MongoDB"),
    );

    info!("MongoDB conectado");

    let payment_service = Arc::new(services::PaymentService::new(&config));

    info!("Payment service inicializado");

    let app_state = web::Data::new(AppState {
        config: config.clone(),
        db,
        payment_service,
    });

    let bind_addr = format!("0.0.0.0:{}", config.port);

    info!("========================================");
    info!("ARKANA STORE API RODANDO");
    info!("========================================");
    info!("Endereco: http://{}", bind_addr);
    info!("========================================");

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
            .route("/health", web::get().to(health_check))
            .service(
                web::scope("/api")
                    .service(handlers::products::list_products)
                    .service(handlers::products::get_product)
                    .service(handlers::products::search_products)
                    .service(handlers::cart::add_to_cart)
                    .service(handlers::cart::get_cart)
                    .service(handlers::cart::update_cart)
                    .service(handlers::orders::create_order)
                    .service(handlers::orders::get_order)
                    .service(handlers::orders::list_orders),
            )
            .service(
                web::scope("/webhooks")
                    .service(webhooks::mercadopago::handle_webhook)
                    .service(webhooks::paypal::handle_webhook)
                    .service(webhooks::stripe::handle_webhook),
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
