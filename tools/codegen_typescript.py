"""Render the JavaScript package's catalogue and TypeScript identities."""

import json


def render(catalogue: dict) -> dict[str, str]:
    data = json.dumps(catalogue, ensure_ascii=False, indent=2)
    fact_types = []
    for entry in catalogue["entries"]:
        fields = {}
        for rule in entry["match_any"]:
            fields.update(rule.get("required_parameters", {}))
            fields.update(rule.get("capture_types", {}))
        # A field is required only when every alternative supplies it.
        alternatives = [
            set(rule.get("required_parameters", {}))
            | set(rule.get("capture_types", {}))
            for rule in entry["match_any"]
        ]
        required = set.intersection(*alternatives)
        members = " ".join(
            f"readonly {json.dumps(name)}{'?' if name not in required else ''}: number;"
            for name in sorted(fields)
        )
        fact_types.append(f'  {json.dumps(entry["id"])}: {{ {members} }};')
    output = (
        "// Generated from catalogue/errors.json. Run make generate to update.\n"
        'import { deepFreeze } from "./freeze.js";\n'
        'import type { Catalogue, DiagnosticBase, ApiErrorResponse } from "./types.js";\n\n'
        f"const data = {data} as const satisfies Catalogue;\n\n"
        "export const catalogue = deepFreeze(data);\n"
        "export const catalogueVersion = catalogue.catalogue_version;\n"
        "export type Entry = (typeof catalogue.entries)[number];\n"
        'export type ConditionId = Entry["id"];\n'
        "export type EntryFor<I extends ConditionId> = Extract<Entry, { readonly id: I }>;\n\n"
        "export interface FactsById {\n" + "\n".join(fact_types) + "\n}\n\n"
        "export type MatchedClassification = {\n"
        '  [I in ConditionId]: Omit<DiagnosticBase, "facts"> & {\n'
        '    readonly status: "matched";\n'
        "    readonly id: I;\n"
        "    readonly entry: EntryFor<I>;\n"
        "    readonly facts: FactsById[I];\n"
        "    readonly response: ApiErrorResponse;\n"
        "  };\n"
        "}[ConditionId];\n"
    )
    return {"js/src/catalogue.ts": output}
