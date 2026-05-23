from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from investment_lab.engine.report_builder import export_html_report_from_bundle, build_report_bundle

router = APIRouter()

class ReportBuildRequest(BaseModel):
    result: dict

@router.post('/build')
def build_report(req: ReportBuildRequest):
    bundle = build_report_bundle(req.result)
    html = export_html_report_from_bundle(bundle)
    return {'report_id': bundle.report_id, 'html': html, 'sections': bundle.sections, 'created_at': bundle.created_at}
