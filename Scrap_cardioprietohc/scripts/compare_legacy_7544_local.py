#!/usr/bin/env python3
"""
Comparación básica entre legacy (HC 7544) y local:
- Extrae campos de "Datos Personales" desde el PDF legacy.
- Extrae labels + names del formulario de edición local (pacientes/<id>/editar/).
- Genera reporte JSON y MD con diferencias.
"""
import argparse
import json
import re
import subprocess
import unicodedata
from pathlib import Path

import httpx
from bs4 import BeautifulSoup


def _norm(text: str) -> str:
    text = text or ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text).strip()
    return text


def _norm_date_ddmmyyyy(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    # yyyy-mm-dd -> dd/mm/yyyy
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", value)
    if m:
        y, mo, d = m.groups()
        return f"{d}/{mo}/{y}"
    # dd/mm/yyyy -> dd/mm/yyyy
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", value)
    if m:
        d, mo, y = m.groups()
        return f"{d}/{mo}/{y}"
    return value


def _norm_sexo_fm(value: str) -> str:
    v = (value or "").strip().lower()
    if v in ("f", "femenino", "mujer"):
        return "F"
    if v in ("m", "masculino", "h", "hombre"):
        return "M"
    return (value or "").strip()


def _extract_legacy_personal_fields(pdf_path: Path):
    pdf_text = subprocess.check_output(["pdftotext", str(pdf_path), "-"]).decode(
        "utf-8", errors="ignore"
    )
    lines = [l.strip() for l in pdf_text.splitlines()]
    # Recorta sección "1. Datos Personales" hasta "2. Diagnósticos"
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith("1. Datos Personales"):
            start = i + 1
        if line.startswith("2. Diagnósticos"):
            end = i
            break
    if start is None:
        start = 0
    if end is None:
        end = len(lines)
    section = [l for l in lines[start:end] if ":" in l]
    fields = []
    for line in section:
        label, value = line.split(":", 1)
        label = label.strip()
        value = value.strip()
        if label:
            fields.append({"label": label, "value": value})
    return fields


def _extract_local_form_fields(url: str):
    html = httpx.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # labels (incluye radios/checkboxes no asociados)
    labels = [l.get_text(strip=True) for l in soup.find_all("label")]
    labels = [l for l in labels if l]

    id_to_label = {}
    for lab in soup.find_all("label"):
        if lab.get("for"):
            id_to_label[lab["for"]] = lab.get_text(strip=True)

    fields = []
    values = {}
    for el in soup.find_all(["input", "select", "textarea"]):
        name = el.get("name")
        if not name or name == "csrfmiddlewaretoken":
            continue
        el_id = el.get("id", "")
        label = id_to_label.get(el_id, "")
        el_type = el.get("type", "")
        fields.append(
            {
                "name": name,
                "label": label,
                "type": el.name,
                "input_type": el_type,
            }
        )

        # valor actual
        val = None
        if el.name == "select":
            sel = el.find("option", selected=True)
            if sel is not None:
                val = sel.get_text(strip=True) or sel.get("value", "")
        elif el.name == "textarea":
            val = el.get_text(strip=True)
        else:
            if el_type in ("radio", "checkbox"):
                if el.has_attr("checked"):
                    val = el.get("value", "")
            else:
                val = el.get("value", "")

        if val is not None:
            if name in values:
                if isinstance(values[name], list):
                    values[name].append(val)
                else:
                    values[name] = [values[name], val]
            else:
                values[name] = val

    return labels, fields, values


def main():
    ap = argparse.ArgumentParser(description="Comparar legacy 7544 vs local")
    ap.add_argument(
        "--legacy-pdf",
        default="scrap_legacy/crawl_7544/downloads/Historia_Clinica.pdf",
    )
    ap.add_argument("--local-edit-url", default="http://127.0.0.1:8090/pacientes/11570/editar/")
    ap.add_argument(
        "--out-dir", default="Scrap_cardioprietohc/data/reports"
    )
    args = ap.parse_args()

    legacy_pdf = Path(args.legacy_pdf)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    legacy_fields = _extract_legacy_personal_fields(legacy_pdf)
    local_labels, local_fields, local_values = _extract_local_form_fields(args.local_edit_url)

    legacy_labels_norm = {_norm(f["label"]) for f in legacy_fields}
    local_labels_norm = {_norm(l) for l in local_labels}

    missing_in_local = sorted(
        l for l in legacy_labels_norm if l and l not in local_labels_norm
    )
    extra_in_local = sorted(
        l for l in local_labels_norm if l and l not in legacy_labels_norm
    )

    def _local_value_for(label: str) -> str:
        if label == "Doc. Identidad":
            tipo = str(local_values.get("idTipoDoc", "") or "").strip()
            num = str(local_values.get("numDoc", "") or "").strip()
            return " ".join([t for t in [tipo, num] if t]).strip()
        if label == "Fec. Nac":
            raw = str(local_values.get("fechaNac", "") or "").strip()
            return _norm_date_ddmmyyyy(raw)
        if label == "N° Historia Clínica":
            return ""
        if label == "Sexo":
            val = str(local_values.get("sexo", "") or "").strip()
            return _norm_sexo_fm(val)
        mapping = {
            "Nombre": "nombre",
            "Apellido": "apellido",
            "Email": "mail",
            "Dirección": "direccion",
            "Localidad": "localidad",
            "Obra Social": "obraSocial",
            "Plan": "plan",
            "Afiliado": "afiliado",
            "Teléfono": "telefono",
            "Celular": "celular",
            "Profesión": "profesion",
            "Médico Referente": "referente",
        }
        key = mapping.get(label)
        return str(local_values.get(key, "") or "").strip()

    comparisons = []
    for f in legacy_fields:
        legacy_val = f["value"]
        if f["label"] == "Fec. Nac":
            legacy_val = _norm_date_ddmmyyyy(legacy_val)
        if f["label"] == "Sexo":
            legacy_val = _norm_sexo_fm(legacy_val)

        local_val = _local_value_for(f["label"])
        comparisons.append(
            {
                "label": f["label"],
                "legacy_value": legacy_val,
                "local_value": local_val,
                "match": _norm(legacy_val) == _norm(local_val),
            }
        )

    report = {
        "legacy_pdf": str(legacy_pdf),
        "local_edit_url": args.local_edit_url,
        "legacy_fields": legacy_fields,
        "local_labels": local_labels,
        "local_fields": local_fields,
        "local_values": local_values,
        "missing_in_local_labels": missing_in_local,
        "extra_in_local_labels": extra_in_local,
        "comparisons": comparisons,
    }

    json_path = out_dir / "compare_legacy_7544_vs_local_edit.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = []
    md_lines.append("# Comparación legacy 7544 vs local (Datos Personales)")
    md_lines.append("")
    md_lines.append(f"- Legacy PDF: `{legacy_pdf}`")
    md_lines.append(f"- Local edit URL: `{args.local_edit_url}`")
    md_lines.append("")
    md_lines.append("## Campos legacy (Datos Personales)")
    for f in legacy_fields:
        md_lines.append(f"- {f['label']}: {f['value']}")
    md_lines.append("")
    md_lines.append("## Labels local detectados")
    for l in local_labels:
        md_lines.append(f"- {l}")
    md_lines.append("")
    md_lines.append("## Comparación de valores (legacy vs local)")
    for c in comparisons:
        mark = "OK" if c["match"] else "DIFF"
        md_lines.append(
            f"- {c['label']}: legacy='{c['legacy_value']}' | local='{c['local_value']}' => {mark}"
        )
    md_lines.append("")
    md_lines.append("## Falta en local (labels legacy sin match)")
    for l in missing_in_local:
        md_lines.append(f"- {l}")
    md_lines.append("")
    md_lines.append("## Extra en local (labels no presentes en legacy)")
    for l in extra_in_local:
        md_lines.append(f"- {l}")

    md_path = out_dir / "compare_legacy_7544_vs_local_edit.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
