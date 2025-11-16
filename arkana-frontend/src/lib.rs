//! # ??? ARKANA STORE - FRONTEND (Yew + WebAssembly)
//! 
//! E-commerce SPA de alta performance para produtos maçônicos
//! 
//! ## Features:
//! - Catálogo de produtos (camisetas, bermudas, acessórios)
//! - Carrinho de compras reativo
//! - Checkout com múltiplos gateways
//! - Landing page otimizada para conversão
//! - 100% tipado e seguro
//! 
//! Build: trunk build --release
//! Serve: trunk serve
//! 
//! Data: 16/11/2025
//! Versão: 1.0.0

use yew::prelude::*;
use yew_router::prelude::*;
use gloo_net::http::Request;
use arkana_shared::*;

mod components;
mod pages;
mod services;

use pages::{Home, Products, Cart, Checkout};

// ===================================================================
// ROTAS
// ===================================================================

#[derive(Clone, Routable, PartialEq)]
enum Route {
    #[at("/")]
    Home,
    #[at("/produtos")]
    Products,
    #[at("/carrinho")]
    Cart,
    #[at("/checkout")]
    Checkout,
    #[not_found]
    #[at("/404")]
    NotFound,
}

fn switch(routes: Route) -> Html {
    match routes {
        Route::Home => html! { <Home /> },
        Route::Products => html! { <Products /> },
        Route::Cart => html! { <Cart /> },
        Route::Checkout => html! { <Checkout /> },
        Route::NotFound => html! { <h1>{"404 - Página não encontrada"}</h1> },
    }
}

// ===================================================================
// APP PRINCIPAL
// ===================================================================

#[function_component(App)]
fn app() -> Html {
    html! {
        <BrowserRouter>
            <div class="app">
                <components::Header />
                
                <main>
                    <Switch<Route> render={switch} />
                </main>
                
                <components::Footer />
            </div>
        </BrowserRouter>
    }
}

// ===================================================================
// ENTRY POINT
// ===================================================================

fn main() {
    wasm_logger::init(wasm_logger::Config::default());
    
    tracing::info!("?? Arkana Store WASM iniciando...");
    
    yew::Renderer::<App>::new().render();
}
