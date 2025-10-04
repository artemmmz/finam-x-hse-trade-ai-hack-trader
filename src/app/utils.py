from app.adapters import FinamAPIClient

import re
from rapidfuzz import fuzz

rus_to_eng = {
    'а': 'a','б': 'b','в': 'v','г': 'g','д': 'd','е': 'e','ё': 'yo','ж': 'zh',
    'з': 'z','и': 'i','й': 'y','к': 'k','л': 'l','м': 'm','н': 'n','о': 'o',
    'п': 'p','р': 'r','с': 's','т': 't','у': 'u','ф': 'f','х': 'kh','ц': 'ts',
    'ч': 'ch','ш': 'sh','щ': 'sch','ъ': '','ы': 'y','ь': '','э': 'e','ю': 'yu','я': 'ya'
}


def translit_ru_to_en(text: str) -> str:
    return ''.join(rus_to_eng.get(ch.lower(), ch) for ch in text)


def normalize_company_name(name: str) -> str:
    name = name.lower()
    name = translit_ru_to_en(name)
    name = re.sub(r'\b(ooo|ao|pao|zao|oao|ltd|llc|inc|corp|company)\b', '', name)
    name = re.sub(r'[!@#$%^&*()_+=-]', "", name)
    return name.strip()


def similarity(name: str, assets: list[str]) -> list[float]:
    res = []
    name1 = normalize_company_name(name)
    for asset in assets:
        name2 = normalize_company_name(asset)
        res.append(fuzz.ratio(name1, name2))
    return res


def get_asset_from_text(name: str, finam_client: FinamAPIClient) -> str:
    assets = finam_client.get_assets().get("assets")
    if assets is None:
        return ""
    asset_names = [asset["name"] for asset in assets]
    asset_symbol = [asset["symbol"] for asset in assets]
    asset_similarity = similarity(name, asset_names)

    max_ind = 0
    for ind, sim in enumerate(asset_similarity):
        if sim > asset_similarity[max_ind]:
            max_ind = ind

    symbol = asset_symbol[max_ind]
    return symbol
