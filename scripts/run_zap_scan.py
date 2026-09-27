"""Executa Spider -> aguarda Passive Scan -> gera relatorio HTML via API do ZAP."""

from __future__ import annotations
import sys
from pathlib import Path


import logging
import os
import sys
import time

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

ZAP_BASE_URL = settings.ZAP_API_URL.rstrip("/")
HTTP_TIMEOUT = 30
POLL_INTERVAL_SECONDS = 2
SPIDER_MAX_WAIT_SECONDS = 300
PASSIVE_SCAN_MAX_WAIT_SECONDS = 120
REPORT_PATH = "reports/zap_report.html"

# Opcional: defina ZAP_API_KEY em config.py se a instancia do ZAP exigir
# API key (instalacoes locais exigem por padrao; o comando docker deste
# projeto usa -config api.disablekey=true e nao precisa dela).
_API_KEY = getattr(settings, "ZAP_API_KEY", None)

_session = requests.Session()


def _zap_request(
    format_prefix: str, path: str, params: dict | None = None
) -> requests.Response:
    """Chama a API do ZAP com o prefixo de formato correto.

    Endpoints "other" (conteudo bruto, ex.: htmlreport) exigem o prefixo
    /OTHER/. Chama-los via /JSON/ pode devolver corpo vazio ou incompleto
    dependendo da instalacao/versao do ZAP.
    """
    url = f"{ZAP_BASE_URL}/{format_prefix}/{path}"
    request_params = dict(params or {})
    if _API_KEY:
        request_params["apikey"] = _API_KEY

    response = _session.get(url, params=request_params, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response


def zap_json(path: str, params: dict | None = None) -> dict:
    return _zap_request("JSON", path, params).json()


def zap_other(path: str, params: dict | None = None) -> requests.Response:
    return _zap_request("OTHER", path, params)


def check_zap_connection() -> str:
    data = zap_json("core/view/version/")
    version = data.get("version")
    if not version:
        raise RuntimeError(f"Resposta inesperada da API do ZAP: {data}")
    logger.info("ZAP conectado. Versao: %s", version)
    return version


def start_spider(target_url: str) -> str:
    data = zap_json("spider/action/scan/", {"url": target_url, "recurse": "true"})
    scan_id = data.get("scan")
    if scan_id is None:
        raise RuntimeError(f"Resposta inesperada ao iniciar o Spider: {data}")
    logger.info("Spider iniciado (scanId=%s) contra %s", scan_id, target_url)
    return scan_id


def wait_for_spider(
    scan_id: str, max_wait_seconds: int = SPIDER_MAX_WAIT_SECONDS
) -> None:
    deadline = time.monotonic() + max_wait_seconds
    while True:
        data = zap_json("spider/view/status/", {"scanId": scan_id})
        progress = int(data.get("status", 0))
        logger.info("Progresso do Spider: %d%%", progress)

        if progress >= 100:
            return
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Spider nao terminou em {max_wait_seconds}s (scanId={scan_id})"
            )
        time.sleep(POLL_INTERVAL_SECONDS)


def wait_for_passive_scan(
    max_wait_seconds: int = PASSIVE_SCAN_MAX_WAIT_SECONDS,
) -> None:
    """O Passive Scanner processa a fila de forma assincrona apos o Spider.

    Gerar o relatorio antes dessa fila zerar produz um relatorio incompleto
    (na pratica, as vezes vazio).
    """
    deadline = time.monotonic() + max_wait_seconds
    while True:
        data = zap_json("pscan/view/recordsToScan/")
        pending = int(data.get("recordsToScan", 0))
        logger.info("Registros pendentes no Passive Scanner: %d", pending)

        if pending == 0:
            return
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Passive Scan nao esvaziou a fila em {max_wait_seconds}s"
            )
        time.sleep(POLL_INTERVAL_SECONDS)


def generate_html_report(output_path: str = REPORT_PATH) -> str:
    response = zap_other("core/other/htmlreport/")

    content = response.text
    if not content or "<html" not in content.lower():
        raise RuntimeError(
            "O ZAP retornou um relatorio vazio ou malformado. Verifique "
            "core/view/urls/ e pscan/view/recordsToScan/ antes de gerar o "
            "relatorio novamente."
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as report_file:
        report_file.write(content)

    return os.path.abspath(output_path)


def main() -> int:
    try:
        check_zap_connection()
        scan_id = start_spider(settings.TARGET_API)
        wait_for_spider(scan_id)

        logger.info(
            "Spider finalizado. Aguardando o Passive Scanner esvaziar a fila..."
        )
        wait_for_passive_scan()

        report_path = generate_html_report()
        logger.info("Sucesso! Relatorio gerado em: %s", report_path)
        return 0
    except (requests.RequestException, RuntimeError, TimeoutError) as exc:
        logger.error("Falha na execucao do pipeline ZAP: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
