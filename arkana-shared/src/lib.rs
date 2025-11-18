//! # ARKANA SHARED - Types & Domain Models
//!
//! Tipos compartilhados entre backend (API Rust) e frontend (Yew WASM)
//!
//! ## Modulos:
//! - `product`: Produtos maconicos
//! - `order`: Pedidos e carrinho
//! - `payment`: Integracoes pagamento
//! - `customer`: Dados do cliente

use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};

// ===================================================================
// PRODUTO (Camisetas, Bermudas, Acessorios Maconicos)
// ===================================================================

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Product {
    pub id: Uuid,
    pub sku: String,
    pub name: String,
    pub description: String,
    pub category: ProductCategory,
    pub price: f64,
    pub stock: u32,
    pub images: Vec<String>,
    pub sizes: Option<Vec<String>>, // Para camisetas/bermudas
    pub masonic_symbols: Vec<String>, // Simbolos maconicos no produto
    pub metadata: ProductMetadata,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum ProductCategory {
    Camiseta,        // Camisetas maconicas
    Bermuda,         // Bermudas
    Acessorio,       // Aneis, pingentes, pins
    Bone,            // Bones
    Conjunto,        // Kits
    Outros,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ProductMetadata {
    pub peso_gramas: Option<u32>,
    pub dimensoes_cm: Option<(u32, u32, u32)>, // (L, A, P)
    pub material: Option<String>,
    pub grau_maconico: Option<String>, // Ex: "Aprendiz", "Companheiro", "Mestre"
    pub rito: Option<String>, // Ex: "REAA", "Escoces", "York"
}

// ===================================================================
// CARRINHO E PEDIDO
// ===================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CartItem {
    pub product_id: Uuid,
    pub product_name: String,
    pub quantity: u32,
    pub unit_price: f64,
    pub size: Option<String>, // Tamanho escolhido
    pub subtotal: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Cart {
    pub session_id: Uuid,
    pub items: Vec<CartItem>,
    pub total: f64,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Order {
    pub id: Uuid,
    pub order_number: String, // "ARK-20251116-001"
    pub customer: Customer,
    pub items: Vec<OrderItem>,
    pub subtotal: f64,
    pub shipping: f64,
    pub tax: f64,
    pub total: f64,
    pub status: OrderStatus,
    pub payment: PaymentInfo,
    pub shipping_address: Address,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrderItem {
    pub product_id: Uuid,
    pub sku: String,
    pub name: String,
    pub quantity: u32,
    pub unit_price: f64,
    pub size: Option<String>,
    pub total: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum OrderStatus {
    PendingPayment,     // Aguardando pagamento
    PaymentApproved,    // Pagamento aprovado
    Processing,         // Em separa��o
    Shipped,           // Enviado
    Delivered,         // Entregue
    Cancelled,         // Cancelado
    Refunded,          // Reembolsado
}

// ===================================================================
// PAGAMENTO
// ===================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PaymentInfo {
    pub gateway: PaymentGateway,
    pub payment_id: Option<String>,
    pub status: PaymentStatus,
    pub method: PaymentMethod,
    pub installments: Option<u8>,
    pub paid_at: Option<DateTime<Utc>>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum PaymentGateway {
    MercadoPago,
    PayPal,
    Stripe,
    Pix,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum PaymentStatus {
    Pending,
    Approved,
    Rejected,
    Cancelled,
    Refunded,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum PaymentMethod {
    CreditCard,
    DebitCard,
    Pix,
    PayPal,
    BankSlip, // Boleto
}

// ===================================================================
// CLIENTE
// ===================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Customer {
    pub id: Uuid,
    pub email: String,
    pub name: String,
    pub phone: String,
    pub cpf: Option<String>,
    pub is_mason: bool, // Cliente e macom? (desconto especial)
    pub lodge_name: Option<String>, // Nome da loja maconica
    pub masonic_degree: Option<String>, // Grau maconico
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Address {
    pub street: String,
    pub number: String,
    pub complement: Option<String>,
    pub neighborhood: String,
    pub city: String,
    pub state: String,
    pub zip_code: String,
    pub country: String,
}

// ===================================================================
// WEBHOOK EVENTS
// ===================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebhookEvent {
    pub id: Uuid,
    pub gateway: PaymentGateway,
    pub event_type: String,
    pub event_id: String,
    pub payload: serde_json::Value,
    pub processed: bool,
    pub created_at: DateTime<Utc>,
}

// ===================================================================
// API RESPONSES
// ===================================================================

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<String>,
    pub timestamp: DateTime<Utc>,
}

impl<T> ApiResponse<T> {
    pub fn success(data: T) -> Self {
        Self {
            success: true,
            data: Some(data),
            error: None,
            timestamp: Utc::now(),
        }
    }

    pub fn error(message: impl Into<String>) -> Self {
        Self {
            success: false,
            data: None,
            error: Some(message.into()),
            timestamp: Utc::now(),
        }
    }
}

// ===================================================================
// ERRORS
// ===================================================================

#[derive(Debug, thiserror::Error)]
pub enum ArkanaError {
    #[error("Produto nao encontrado: {0}")]
    ProductNotFound(Uuid),

    #[error("Estoque insuficiente: {0} disponivel, {1} solicitado")]
    InsufficientStock(u32, u32),

    #[error("Pedido nao encontrado: {0}")]
    OrderNotFound(Uuid),

    #[error("Pagamento falhou: {0}")]
    PaymentFailed(String),

    #[error("Erro de validacao: {0}")]
    ValidationError(String),

    #[error("Erro interno: {0}")]
    InternalError(String),
}

pub type ArkanaResult<T> = Result<T, ArkanaError>;
