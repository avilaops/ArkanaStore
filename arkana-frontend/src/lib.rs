//! # ??? ARKANA STORE - FRONTEND (Yew + WebAssembly)
//!
//! E-commerce SPA de alta performance para produtos ma��nicos
//!
//! ## Features:
//! - Cat�logo de produtos (camisetas, bermudas, acess�rios)
//! - Carrinho de compras reativo
//! - Checkout com m�ltiplos gateways
//! - Landing page otimizada para convers�o
//! - 100% tipado e seguro
//!
//! Build: trunk build --release
//! Serve: trunk serve
//!
//! Data: 16/11/2025
//! Vers�o: 1.0.0

use yew::prelude::*;
use yew_router::prelude::*;

mod pages;
// mod services;

use pages::Home;

// Placeholder components
#[yew::function_component(Products)]
fn products() -> yew::Html {
    yew::html! { <h1>{"🛍️ Produtos - Em breve"}</h1> }
}

#[yew::function_component(Cart)]
fn cart() -> yew::Html {
    yew::html! { <h1>{"🛒 Carrinho - Em breve"}</h1> }
}

#[yew::function_component(Checkout)]
fn checkout() -> yew::Html {
    yew::html! { <h1>{"💳 Checkout - Em breve"}</h1> }
}

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
        Route::NotFound => html! { <h1>{"404 - P�gina n�o encontrada"}</h1> },
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
                <pages::components::Header />

                <main>
                    <Switch<Route> render={switch} />
                </main>

                <pages::components::Footer />
            </div>
        </BrowserRouter>
    }
}

// ===================================================================
// ENTRY POINT
// ===================================================================

fn main() {
    yew::Renderer::<App>::new().render();
}
