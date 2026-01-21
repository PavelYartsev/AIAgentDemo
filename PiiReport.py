from dataclasses import dataclass
from typing import List, Dict, Any
from collections import defaultdict


@dataclass
class PiiReport:
    """Отчет о найденных PII (Personally Identifiable Information)"""
    findings: List[str] = None
    counts: Dict[str, int] = None

    def __post_init__(self):
        if self.findings is None:
            self.findings = []
        if self.counts is None:
            self.counts = defaultdict(int)

    def add(self, finding: str):
        """Добавляет найденное PII в отчет"""
        self.findings.append(finding)
        pii_type = finding.split(': ', 1)[0]
        self.counts[pii_type] += 1

    def to_dict(self) -> Dict[str, Any]:
        """Возвращает отчет в формате словаря"""
        return {
            'total_findings': len(self.findings),
            'findings_by_type': dict(self.counts),
            'all_findings': self.findings
        }

    def __str__(self) -> str:
        lines = [f"PII Report: {len(self.findings)} findings found"]
        for pii_type, count in sorted(self.counts.items()):
            lines.append(f"  {pii_type}: {count}")
        if self.findings:
            lines.append("\nDetails:")
            lines.extend(f"  - {f}" for f in self.findings)
        return '\n'.join(lines)
