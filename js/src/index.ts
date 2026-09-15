import { catalogue as bundledCatalogue } from "./catalogue.js";
import type { MatchedClassification } from "./catalogue.js";
import type {
  ApiErrorResponse,
  Catalogue,
  CatalogueEntry,
  ClassifyOptions,
  GenericClassification,
  IntegerKind,
  MatchRule,
  UnmatchedClassification,
} from "./types.js";

export { catalogue, catalogueVersion } from "./catalogue.js";
export type { ConditionId, Entry, EntryFor, FactsById, MatchedClassification } from "./catalogue.js";
export type {
  ApiErrorResponse, Catalogue, CatalogueEntry, ClassifyOptions,
  GenericClassification, GenericMatchedClassification, IntegerKind, MatchRule,
  UnmatchedClassification,
} from "./types.js";

export type Classification = MatchedClassification | UnmatchedClassification;

function isObject(value: unknown): value is Record<string, unknown> {
  if (value === null || typeof value !== "object") return false;
  const prototype: unknown = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function integer(value: unknown, kind: IntegerKind): value is number {
  return typeof value === "number" && Number.isSafeInteger(value) &&
    (kind === "positive_integer" ? value > 0 : value !== 0);
}

function isApiError(value: unknown): value is ApiErrorResponse {
  return isObject(value) && value.ok === false &&
    integer(value.error_code, "positive_integer") && typeof value.description === "string" &&
    (!("parameters" in value) || isObject(value.parameters));
}

function asciiLower(value: string): string {
  return value.replace(/[A-Z]/g, (character) => character.toLowerCase());
}

function escapePattern(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function matchTemplate(description: string, rule: MatchRule): Record<string, number> | undefined {
  const template = rule.description_template!;
  const fields: string[] = [];
  let offset = 0;
  let pattern = "^";
  for (const field of template.matchAll(/\{([a-z][a-z0-9_]*)\}/g)) {
    pattern += escapePattern(template.slice(offset, field.index)) + "(-?[0-9]+)";
    fields.push(field[1]!);
    offset = field.index + field[0].length;
  }
  pattern += escapePattern(template.slice(offset)) + "$";
  const match = new RegExp(pattern).exec(description);
  // JavaScript's $ also matches before a final newline; the full text must match.
  if (!match || match[0] !== description) return undefined;
  const facts: Record<string, number> = {};
  for (const [index, name] of fields.entries()) {
    const kind = rule.capture_types?.[name];
    const value = Number(match[index + 1]);
    if (!kind || !integer(value, kind)) return undefined;
    if (name in facts && facts[name] !== value) return undefined;
    facts[name] = value;
  }
  return facts;
}

function matchBody(response: ApiErrorResponse, rule: MatchRule): Record<string, number> | undefined {
  if (response.error_code !== rule.error_code) return undefined;
  if (rule.description_exact !== undefined && rule.description_exact !== response.description) return undefined;
  let facts: Record<string, number> = {};
  if (rule.description_template !== undefined) {
    const captures = matchTemplate(response.description, rule);
    if (!captures) return undefined;
    facts = captures;
  }
  for (const [key, kind] of Object.entries(rule.required_parameters ?? {})) {
    const value = response.parameters?.[key];
    if (!integer(value, kind)) return undefined;
    if (key in facts && facts[key] !== value) return undefined;
    facts[key] = value;
  }
  return facts;
}

interface Candidate {
  entry: CatalogueEntry;
  facts: Record<string, number>;
  priority: number;
  missingMethod: boolean;
}

/** Classify a Bot API failure without changing the response or taking action. */
export function classify(response: unknown, options?: { readonly method?: string }): Classification;
export function classify(response: unknown, options: { readonly catalogue: Catalogue; readonly method?: string }): GenericClassification;
export function classify(response: unknown, options: ClassifyOptions = {}): GenericClassification {
  const catalogue: Catalogue = options.catalogue ?? bundledCatalogue;
  const base = { catalogue_version: catalogue.catalogue_version, facts: {}, candidates: [] };
  if (!isApiError(response)) return { ...base, response, status: "not_api_error" };

  const parameterKinds = new Map<string, Set<IntegerKind>>();
  for (const entry of catalogue.entries) {
    for (const rule of entry.match_any) {
      for (const [key, kind] of Object.entries(rule.required_parameters ?? {})) {
        const kinds = parameterKinds.get(key) ?? new Set<IntegerKind>();
        kinds.add(kind);
        parameterKinds.set(key, kinds);
      }
    }
  }
  const present = new Set<string>();
  for (const [key, kinds] of parameterKinds) {
    if (response.parameters && Object.hasOwn(response.parameters, key)) {
      const value = response.parameters[key];
      if (![...kinds].some((kind) => integer(value, kind))) return { ...base, response, status: "unknown" };
      present.add(key);
    }
  }
  for (const group of catalogue.matching.exclusive_parameter_groups) {
    const conflicting = group.filter((key) => present.has(key));
    if (conflicting.length < 2) continue;
    const candidates = catalogue.entries.filter((entry) =>
      entry.match_any.some((rule) => conflicting.some((key) => Object.hasOwn(rule.required_parameters ?? {}, key))),
    ).map((entry) => entry.id);
    return { ...base, response, status: "ambiguous", candidates: [...new Set(candidates)].sort() };
  }

  const method = typeof options.method === "string" ? asciiLower(options.method) : undefined;
  const candidates: Candidate[] = [];
  for (const entry of catalogue.entries) {
    for (const rule of entry.match_any) {
      const structured = Object.keys(rule.required_parameters ?? {}).length > 0;
      // A recognized recovery field cannot be ignored in favor of a text match.
      if (present.size > 0 && !structured) continue;
      const facts = matchBody(response, rule);
      if (!facts) continue;
      if (rule.method !== undefined && method !== undefined && asciiLower(rule.method) !== method) continue;
      candidates.push({ entry, facts, priority: structured ? 1 : 0, missingMethod: rule.method !== undefined && method === undefined });
    }
  }
  if (candidates.length === 0) return { ...base, response, status: "unknown" };
  const priority = Math.max(...candidates.map((candidate) => candidate.priority));
  const best = candidates.filter((candidate) => candidate.priority === priority);
  const complete = new Set(best.filter((candidate) => !candidate.missingMethod).map((candidate) => candidate.entry.id));
  const ids = [...new Set(best.map((candidate) => candidate.entry.id))].sort();
  if (best.some((candidate) => candidate.missingMethod && !complete.has(candidate.entry.id))) {
    return { ...base, response, status: "insufficient_context", candidates: ids };
  }
  if (ids.length > 1) return { ...base, response, status: "ambiguous", candidates: ids };
  const matched = best.find((candidate) => !candidate.missingMethod)!;
  return { ...base, response, status: "matched", id: matched.entry.id, entry: matched.entry, facts: matched.facts };
}
