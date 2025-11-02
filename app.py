from flask import Flask, render_template, request, redirect, url_for
import urllib
from reqs import instantgaming_search

app = Flask(__name__)


def get_strings(lang: str):
    if lang == 'en':
        return {
            'subtitle': 'Find the best game prices across stores',
            'obs': 'Note: If the game does not appear, it may be out of stock or there was an issue during the search.',
            'input_placeholder': 'Type the game name...',
            'search_button': '🔍 Search',
            'loading_text': 'Searching for the best prices...',
            'no_results_title': 'No games found for',
            'no_results_tip': 'Try different terms or check the spelling.',
            'error_unexpected': 'An unexpected error occurred. Please try again.',
            'eneba_manual_title': '🔍 Manual Search on Eneba',
            'eneba_manual_cta': 'Click to search manually',
            'eneba_manual_warn': 'We could not automatically retrieve Eneba data. Click here to perform a manual search on the official site.',
            'eneba_manual_badge': '⚠️ Manual Search',
            'lang_pt': 'PT-BR',
            'lang_en': 'EN',
            'credits_by': 'Built by'
        }
    return {
        'subtitle': 'Encontre os melhores preços de jogos em todas as lojas',
        'obs': 'OBS: Se o jogo não aparecer, é porque ele não está em estoque no momento ou houve um problema na pesquisa.',
        'input_placeholder': 'Digite o nome do jogo...',
        'search_button': '🔍 Buscar',
        'loading_text': 'Procurando os melhores preços...',
        'no_results_title': 'Nenhum jogo encontrado para',
        'no_results_tip': 'Tente usar termos diferentes ou verificar a ortografia.',
        'error_unexpected': 'Ocorreu um erro inesperado. Tente novamente.',
        'eneba_manual_title': '🔍 Pesquisa Manual na Eneba',
        'eneba_manual_cta': 'Clique para pesquisar manualmente',
        'eneba_manual_warn': 'Não foi possível obter os dados da Eneba automaticamente. Clique aqui para fazer uma pesquisa manual no site oficial.',
        'eneba_manual_badge': '⚠️ Pesquisa Manual',
        'lang_pt': 'PT-BR',
        'lang_en': 'EN',
        'credits_by': 'Feito por'
    }


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route('/')
def index():
    # Renderiza a documentação bilíngue incorporada em templates/index.html
    return render_template("index.html", title="Instant Gaming API")

@app.route('/search')
def search_game():
    lang = request.args.get('lang', 'pt')
    t = get_strings(lang)
    return render_template("search.html", title="Instant Gaming API", lang=lang, t=t)

@app.route('/api/search')
def search_game_api():
    query = request.args.get('query')
    if not query:
        return {"error": "Missing 'query' parameter"}, 400
    game_f = urllib.parse.quote(query)
    # Performance controls (optional)
    latam_priority_raw = request.args.get('latam_priority', '1')
    latam_priority = latam_priority_raw.lower() not in ('0', 'false', 'no')
    max_details = request.args.get('max_details')
    concurrency = request.args.get('concurrency')
    try:
        max_details = int(max_details) if max_details is not None else 6
    except ValueError:
        max_details = 6
    try:
        concurrency = int(concurrency) if concurrency is not None else 6
    except ValueError:
        concurrency = 6

    result = instantgaming_search(
        game_f,
        platform=None,
        type_value=None,
        gametype=None,
        latam_priority=latam_priority,
        max_details=max_details,
        concurrency=concurrency,
    )
    return result

@app.route('/api/search/<game>')
def search_game_api_legacy(game):
    # Compat: redireciona para nova rota com querystring
    return redirect(url_for('search_game_api', query=game))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
