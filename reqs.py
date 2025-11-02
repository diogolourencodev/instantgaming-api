from bs4 import BeautifulSoup
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
Este módulo expõe a função instantgaming_search.
"""

def instantgaming_search(
    search_query,
    platform: str | None = None,
    type_value: str | None = None,
    gametype: str | None = None,
    latam_priority: bool = True,
    max_details: int = 6,
    concurrency: int = 6,
):
    """
    Executa busca na Instant Gaming.

    - A busca na Instant Gaming agora usa apenas o parâmetro de pesquisa, sem filtros:
      https://www.instant-gaming.com/pt/pesquisar/?query=QUERY
    - Parâmetros de filtro (platform/type/gametype) estão desativados por enquanto.
    """

    # Normaliza entradas
    q = str(search_query or '').strip()
    platform = (platform or '').strip()
    type_value = (type_value or '').strip()
    gametype = (gametype or '').strip()

    # Montagem da URL apenas com query, sem filtros
    url = f"https://www.instant-gaming.com/pt/pesquisar/?query={q}"

    headers = {
        "Host": "www.instant-gaming.com",
        "Sec-Ch-Ua": '"Chromium";v="141", "Not?A_Brand";v="8"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        # Consultas em inglês
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Priority": "u=0, i",
        "Connection": "keep-alive",
        # Mantém path pt conforme solicitado, mas cabeçalhos em EN
        "Referer": "https://www.instant-gaming.com/en/",
        "X-Forwarded-For": "201.55.32.200",
        "X-Real-IP": "201.55.32.200",
    }

    # Reuse connections for faster subsequent requests
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=concurrency, pool_maxsize=concurrency)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    req = session.get(url, headers=headers, timeout=20)
    req.raise_for_status()

    soup = BeautifulSoup(req.text, "html.parser")
    article_items = soup.find_all("article", class_="item force-badge")

    # Build initial entries from the search page
    entries = []
    for article in article_items:
        title_tag = article.find("span", class_="title")
        link_tag = article.find('a', class_='cover video')
        price_brute = article.find("div", class_="price")
        if not title_tag or not link_tag:
            continue
        title = title_tag.text.strip()
        href = link_tag.get('href')
        full_link = href if (href and href.startswith('http')) else f"https://www.instant-gaming.com{href}"
        price_text = price_brute.text.strip() if price_brute else ''
        entries.append({"title": title, "full_link": full_link, "price_text": price_text})

    # Helper to fetch Latin America variant quickly
    def fetch_latam_variant(link: str):
        try:
            prod_res = session.get(link, headers=headers, timeout=12)
            prod_res.raise_for_status()
            prod_soup = BeautifulSoup(prod_res.text, "html.parser")

            la_option = None
            select = prod_soup.find('select', class_='other-products-choices regions')
            if select:
                for opt in select.find_all('option'):
                    if 'Latin America' in opt.get_text(strip=True):
                        la_option = opt
                        break

            if la_option is None:
                nice = prod_soup.find('div', class_='nice other-products-choices regions')
                if nice:
                    ul = nice.find('ul', class_='list')
                    if ul:
                        for li in ul.find_all('li', class_='option'):
                            if 'Latin America' in li.get_text(strip=True):
                                la_option = li
                                break

            if la_option is not None:
                la_price = (la_option.get('data-product-price') or '').strip()
                la_id = (la_option.get('data-value') or '').strip()
                la_href = (la_option.get('data-href') or '').strip()
                if la_href:
                    return la_price, la_href
                elif la_id:
                    la_link = re.sub(r'(/pt/)(\d+)(-)', lambda m: m.group(1) + la_id + m.group(3), link)
                    return la_price, la_link
        except Exception:
            return None, None
        return None, None

    # Optionally enrich first N entries with LATAM price concurrently
    if latam_priority and entries:
        first_n = entries[:max(0, int(max_details))]
        with ThreadPoolExecutor(max_workers=max(1, int(concurrency))) as executor:
            future_map = {executor.submit(fetch_latam_variant, e["full_link"]): i for i, e in enumerate(first_n)}
            for future in as_completed(future_map):
                idx = future_map[future]
                la_price, la_link = future.result()
                if la_price:
                    entries[idx]["price_text"] = la_price
                if la_link:
                    entries[idx]["full_link"] = la_link

    # Build final result
    result = []
    for e in entries:
        title = e.get("title")
        price = e.get("price_text")
        link = e.get("full_link")
        if title and price:
            result.append({
                "title": title,
                "price": price,
                "link": link,
                "origin": "Instant Gaming"
            })

    return result
"""
Este módulo expõe a função instantgaming_search.
"""
