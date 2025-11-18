use yew::prelude::*;

#[function_component(Header)]
pub fn header() -> Html {
    html! {
        <header class="site-header">
            <div class="container">
                <div class="logo">
                    <h1>{"ARKANA"}</h1>
                </div>

                <nav class="main-nav">
                    <a href="/">{"Inicio"}</a>
                    <a href="/produtos">{"Produtos"}</a>
                    <a href="/carrinho">{"Carrinho"}</a>
                </nav>
            </div>
        </header>
    }
}
