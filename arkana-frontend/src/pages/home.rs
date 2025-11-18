use yew::prelude::*;

#[function_component(Home)]
pub fn home() -> Html {
    html! {
        <div class="home-page">
            <section class="hero">
                <div class="hero-logo">
                    <div class="logo-circle">
                        <div class="logo-letter">{"A"}</div>
                        <div class="logo-text">{"ARKANA"}</div>
                    </div>
                </div>

                <h1 class="hero-title">{"COLECAO ESSENCIAL"}</h1>
                <p class="hero-subtitle">{"Pecas atemporais com design minimalista e qualidade excepcional"}</p>

                <div class="hero-cta">
                    <a href="/produtos" class="btn btn-primary btn-lg">{"EXPLORAR COLECAO"}</a>
                    <a href="https://wa.me/5517996656163" class="btn btn-secondary btn-lg">{"FALAR CONOSCO"}</a>
                </div>
            </section>

            <section class="features">
                <div class="feature">
                    <div class="icon">{"✨"}</div>
                    <h3>{"Qualidade Premium"}</h3>
                    <p>{"Produtos com simbolos maconicos autenticos"}</p>
                </div>

                <div class="feature">
                    <div class="icon">{"🚚"}</div>
                    <h3>{"Entrega Rapida"}</h3>
                    <p>{"Enviamos para todo Brasil"}</p>
                </div>

                <div class="feature">
                    <div class="icon">{"💳"}</div>
                    <h3>{"Pagamento Seguro"}</h3>
                    <p>{"Multiplas formas de pagamento"}</p>
                </div>
            </section>

            <section class="categories">
                <h2>{"Categorias"}</h2>
                <div class="category-grid">
                    <div class="category-card">
                        <h3>{"Camisetas"}</h3>
                        <p>{"Modelos exclusivos"}</p>
                    </div>
                    <div class="category-card">
                        <h3>{"Bermudas"}</h3>
                        <p>{"Conforto e estilo"}</p>
                    </div>
                    <div class="category-card">
                        <h3>{"Acessorios"}</h3>
                        <p>{"Aneis e pingentes"}</p>
                    </div>
                    <div class="category-card">
                        <h3>{"Bones"}</h3>
                        <p>{"Protecao com estilo"}</p>
                    </div>
                </div>
            </section>
        </div>
    }
}
