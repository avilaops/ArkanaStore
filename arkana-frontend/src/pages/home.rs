//! # ??? LANDING PAGE - ARKANA STORE
//! 
//! Página principal da loja de produtos maçônicos
//! 
//! Seções:
//! 1. Hero - "Sua loja de produtos maçônicos"
//! 2. Categorias - Camisetas, Bermudas, Acessórios
//! 3. Produtos em destaque
//! 4. Sobre a maçonaria
//! 5. Depoimentos
//! 6. CTA final

use yew::prelude::*;
use yew_router::prelude::*;
use crate::Route;

#[function_component(Home)]
pub fn home() -> Html {
    html! {
        <div class="home-page">
            // ===================================
            // HERO SECTION
            // ===================================
            <section class="hero">
                <div class="hero-overlay"></div>
                <div class="hero-content">
                    <div class="hero-symbol">
                        {"?"}  // Compasso e Esquadro (Unicode)
                    </div>
                    
                    <h1 class="hero-title">
                        {"??? ARKANA STORE"}
                    </h1>
                    
                    <p class="hero-subtitle">
                        {"Produtos Maçônicos de Qualidade"}
                    </p>
                    
                    <p class="hero-description">
                        {"Camisetas, bermudas e acessórios para irmãos maçons"}
                        <br/>
                        {"Qualidade premium • Envio rápido • Preços justos"}
                    </p>
                    
                    <div class="hero-cta">
                        <Link<Route> to={Route::Products} classes="btn btn-primary btn-lg">
                            {"??? Ver Produtos"}
                        </Link<Route>>
                        
                        <a href="https://wa.me/5517996656163" class="btn btn-secondary btn-lg" target="_blank">
                            {"?? WhatsApp"}
                        </a>
                    </div>
                    
                    <div class="hero-badges">
                        <span class="badge">{"? Frete Grátis acima de R$ 150"}</span>
                        <span class="badge">{"? Parcelamento sem juros"}</span>
                        <span class="badge">{"? Troca facilitada"}</span>
                    </div>
                </div>
            </section>

            // ===================================
            // CATEGORIAS
            // ===================================
            <section class="categories">
                <div class="container">
                    <h2 class="section-title">
                        {"Nossas Categorias"}
                    </h2>
                    
                    <div class="categories-grid">
                        <div class="category-card">
                            <div class="category-icon">{"??"}</div>
                            <h3>{"Camisetas"}</h3>
                            <p>{"Estampas maçônicas exclusivas"}</p>
                            <Link<Route> to={Route::Products} classes="btn btn-outline">
                                {"Ver Camisetas"}
                            </Link<Route>>
                        </div>
                        
                        <div class="category-card">
                            <div class="category-icon">{"??"}</div>
                            <h3>{"Bermudas"}</h3>
                            <p>{"Conforto e estilo casual"}</p>
                            <Link<Route> to={Route::Products} classes="btn btn-outline">
                                {"Ver Bermudas"}
                            </Link<Route>>
                        </div>
                        
                        <div class="category-card">
                            <div class="category-icon">{"??"}</div>
                            <h3>{"Acessórios"}</h3>
                            <p>{"Anéis, pins, pingentes e mais"}</p>
                            <Link<Route> to={Route::Products} classes="btn btn-outline">
                                {"Ver Acessórios"}
                            </Link<Route>>
                        </div>
                        
                        <div class="category-card">
                            <div class="category-icon">{"??"}</div>
                            <h3>{"Bonés"}</h3>
                            <p>{"Proteção com estilo"}</p>
                            <Link<Route> to={Route::Products} classes="btn btn-outline">
                                {"Ver Bonés"}
                            </Link<Route>>
                        </div>
                    </div>
                </div>
            </section>

            // ===================================
            // PRODUTOS EM DESTAQUE
            // ===================================
            <section class="featured-products">
                <div class="container">
                    <h2 class="section-title">
                        {"?? Produtos em Destaque"}
                    </h2>
                    
                    <div class="products-grid">
                        // Produto 1
                        <div class="product-card">
                            <div class="product-image">
                                <img src="/assets/produtos/camiseta-compasso.jpg" alt="Camiseta Compasso e Esquadro" />
                                <span class="product-badge">{"Mais Vendido"}</span>
                            </div>
                            <div class="product-info">
                                <h3>{"Camiseta Compasso e Esquadro"}</h3>
                                <p class="product-description">
                                    {"100% algodão, estampa de alta qualidade"}
                                </p>
                                <div class="product-footer">
                                    <span class="product-price">{"R$ 89,90"}</span>
                                    <button class="btn btn-primary btn-sm">
                                        {"Adicionar"}
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        // Produto 2
                        <div class="product-card">
                            <div class="product-image">
                                <img src="/assets/produtos/bermuda-logos.jpg" alt="Bermuda Logos Maçônicos" />
                                <span class="product-badge new">{"Novo"}</span>
                            </div>
                            <div class="product-info">
                                <h3>{"Bermuda Logos Maçônicos"}</h3>
                                <p class="product-description">
                                    {"Tecido leve, ideal para verão"}
                                </p>
                                <div class="product-footer">
                                    <span class="product-price">{"R$ 79,90"}</span>
                                    <button class="btn btn-primary btn-sm">
                                        {"Adicionar"}
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        // Produto 3
                        <div class="product-card">
                            <div class="product-image">
                                <img src="/assets/produtos/anel-mestre.jpg" alt="Anel Mestre Maçom" />
                                <span class="product-badge premium">{"Premium"}</span>
                            </div>
                            <div class="product-info">
                                <h3>{"Anel Mestre Maçom"}</h3>
                                <p class="product-description">
                                    {"Aço inoxidável, acabamento polido"}
                                </p>
                                <div class="product-footer">
                                    <span class="product-price">{"R$ 149,90"}</span>
                                    <button class="btn btn-primary btn-sm">
                                        {"Adicionar"}
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        // Produto 4
                        <div class="product-card">
                            <div class="product-image">
                                <img src="/assets/produtos/bone-gadu.jpg" alt="Boné G.A.D.U" />
                            </div>
                            <div class="product-info">
                                <h3>{"Boné G.A.D.U"}</h3>
                                <p class="product-description">
                                    {"Bordado em alto relevo"}
                                </p>
                                <div class="product-footer">
                                    <span class="product-price">{"R$ 59,90"}</span>
                                    <button class="btn btn-primary btn-sm">
                                        {"Adicionar"}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section-cta">
                        <Link<Route> to={Route::Products} classes="btn btn-outline btn-lg">
                            {"Ver Todos os Produtos ?"}
                        </Link<Route>>
                    </div>
                </div>
            </section>

            // ===================================
            // SOBRE A MAÇONARIA
            // ===================================
            <section class="about-masonry">
                <div class="container">
                    <div class="about-content">
                        <div class="about-text">
                            <h2>{"Sobre a Maçonaria"}</h2>
                            <p>
                                {"A Maçonaria é uma ordem iniciática que promove valores "}
                                {"universais como fraternidade, liberdade e igualdade."}
                            </p>
                            <p>
                                {"Nossos produtos celebram esses princípios através de "}
                                {"símbolos tradicionais como o Compasso, o Esquadro, "}
                                {"o Olho que Tudo Vê e as Colunas do Templo."}
                            </p>
                            <div class="about-symbols">
                                <span class="symbol" title="Compasso e Esquadro">{"?"}</span>
                                <span class="symbol" title="Olho que Tudo Vê">{"???"}</span>
                                <span class="symbol" title="Colunas">{"???"}</span>
                                <span class="symbol" title="Acácia">{"??"}</span>
                            </div>
                        </div>
                        
                        <div class="about-image">
                            <img src="/assets/simbolos/compasso-esquadro.svg" alt="Compasso e Esquadro" />
                        </div>
                    </div>
                </div>
            </section>

            // ===================================
            // BENEFÍCIOS
            // ===================================
            <section class="benefits">
                <div class="container">
                    <h2 class="section-title">{"Por que comprar na Arkana?"}</h2>
                    
                    <div class="benefits-grid">
                        <div class="benefit-card">
                            <div class="benefit-icon">{"?"}</div>
                            <h3>{"Qualidade Premium"}</h3>
                            <p>{"Materiais selecionados e estampas duráveis"}</p>
                        </div>
                        
                        <div class="benefit-card">
                            <div class="benefit-icon">{"??"}</div>
                            <h3>{"Entrega Rápida"}</h3>
                            <p>{"Enviamos para todo Brasil em até 7 dias"}</p>
                        </div>
                        
                        <div class="benefit-card">
                            <div class="benefit-icon">{"??"}</div>
                            <h3>{"Pagamento Seguro"}</h3>
                            <p>{"Aceitamos PIX, cartão e PayPal"}</p>
                        </div>
                        
                        <div class="benefit-card">
                            <div class="benefit-icon">{"??"}</div>
                            <h3>{"Atendimento Fraterno"}</h3>
                            <p>{"Atendimento personalizado de irmão para irmão"}</p>
                        </div>
                    </div>
                </div>
            </section>

            // ===================================
            // DEPOIMENTOS
            // ===================================
            <section class="testimonials">
                <div class="container">
                    <h2 class="section-title">{"O que dizem nossos irmãos"}</h2>
                    
                    <div class="testimonials-grid">
                        <div class="testimonial-card">
                            <div class="testimonial-stars">{"?????"}</div>
                            <p class="testimonial-text">
                                {"\"Produtos de excelente qualidade! A camiseta ficou "}
                                {"perfeita e a estampa não desbota. Recomendo!\""}
                            </p>
                            <div class="testimonial-author">
                                <strong>{"Ir? João Silva"}</strong>
                                {" - Loja Luz e Verdade"}
                            </div>
                        </div>
                        
                        <div class="testimonial-card">
                            <div class="testimonial-stars">{"?????"}</div>
                            <p class="testimonial-text">
                                {"\"Entrega rápida e produto conforme anunciado. "}
                                {"O anel é lindo e bem acabado.\""}
                            </p>
                            <div class="testimonial-author">
                                <strong>{"Ir? Pedro Santos"}</strong>
                                {" - Loja Harmonia Universal"}
                            </div>
                        </div>
                        
                        <div class="testimonial-card">
                            <div class="testimonial-stars">{"?????"}</div>
                            <p class="testimonial-text">
                                {"\"Atendimento impecável! Marcelo é muito atencioso "}
                                {"e ajudou a escolher o tamanho certo.\""}
                            </p>
                            <div class="testimonial-author">
                                <strong>{"Ir? Carlos Oliveira"}</strong>
                                {" - Loja Estrela do Oriente"}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            // ===================================
            // CTA FINAL
            // ===================================
            <section class="final-cta">
                <div class="container">
                    <h2>{"Pronto para fazer seu pedido?"}</h2>
                    <p>
                        {"Navegue pelo nosso catálogo e encontre produtos que "}
                        {"expressam sua jornada maçônica"}
                    </p>
                    
                    <Link<Route> to={Route::Products} classes="btn btn-primary btn-xl">
                        {"??? Explorar Catálogo Completo"}
                    </Link<Route>>
                    
                    <div class="contact-info">
                        <p>{"Dúvidas? Entre em contato:"}</p>
                        <div class="contact-links">
                            <a href="https://wa.me/5517996656163" target="_blank">
                                {"?? WhatsApp: (17) 99665-6163"}
                            </a>
                            <a href="mailto:marceloquintinoalves25@gmail.com">
                                {"?? Email: marceloquintinoalves25@gmail.com"}
                            </a>
                            <a href="https://instagram.com/marcelo_quintino3.0" target="_blank">
                                {"?? Instagram: @marcelo_quintino3.0"}
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            // ===================================
            // SÍMBOLOS MAÇÔNICOS (Rodapé decorativo)
            // ===================================
            <div class="masonic-symbols-footer">
                <div class="symbols-container">
                    <span class="symbol">{"?"}</span>
                    <span class="symbol">{"???"}</span>
                    <span class="symbol">{"???"}</span>
                    <span class="symbol">{"??"}</span>
                    <span class="symbol">{"?"}</span>
                    <span class="symbol">{"??"}</span>
                    <span class="symbol">{"??"}</span>
                </div>
            </div>
        </div>
    }
}
