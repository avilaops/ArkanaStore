use yew::prelude::*;

#[function_component(Footer)]
pub fn footer() -> Html {
    html! {
        <footer class="site-footer">
            <div class="container">
                <div class="footer-content">
                    <div class="footer-section">
                        <h3>{"Contato"}</h3>
                        <p>{"WhatsApp: (17) 99665-6163"}</p>
                        <p>{"Email: marceloquintinoalves25@gmail.com"}</p>
                    </div>

                    <div class="footer-section">
                        <h3>{"Redes Sociais"}</h3>
                        <p>{"Instagram: @marcelo_quintino3.0"}</p>
                    </div>

                    <div class="footer-section">
                        <h3>{"Informacoes"}</h3>
                        <p>{"Produtos Maconicos de Qualidade"}</p>
                        <p>{"Envio para todo Brasil"}</p>
                    </div>
                </div>

                <div class="footer-bottom">
                    <p>{"© 2025 Arkana Store - Todos os direitos reservados"}</p>
                    <p>{"Powered by Avila Inc"}</p>
                </div>
            </div>
        </footer>
    }
}
