/** The failure body returned by Telegram. error_code is not an HTTP status. */
export interface ApiErrorResponse {
  readonly ok: false;
  readonly error_code: number;
  readonly description: string;
  readonly parameters?: Readonly<Record<string, unknown>>;
  readonly [key: string]: unknown;
}

export type IntegerKind = "positive_integer" | "nonzero_integer";

export interface MatchRule {
  readonly error_code: number;
  readonly description_exact?: string;
  readonly description_template?: string;
  readonly capture_types?: Readonly<Record<string, IntegerKind>>;
  readonly method?: string;
  readonly required_parameters?: Readonly<Record<string, IntegerKind>>;
}

export interface CatalogueEntry {
  readonly id: string;
  readonly category: string;
  readonly summary: string;
  readonly match_any: readonly MatchRule[];
  readonly [key: string]: unknown;
}

/** Catalogue overrides must follow the published JSON schema. */
export interface Catalogue {
  readonly schema_version: string;
  readonly catalogue_version: string;
  readonly entries: readonly CatalogueEntry[];
  readonly matching: {
    readonly exclusive_parameter_groups: readonly (readonly string[])[];
  };
  readonly [key: string]: unknown;
}

export interface DiagnosticBase {
  readonly catalogue_version: string;
  readonly facts: Readonly<Record<string, number>>;
  readonly candidates: readonly string[];
}

export type UnmatchedClassification =
  | (DiagnosticBase & {
      readonly status: "unknown" | "ambiguous" | "insufficient_context";
      readonly response: ApiErrorResponse;
    })
  | (DiagnosticBase & {
      readonly status: "not_api_error";
      readonly response: unknown;
    });

export type GenericMatchedClassification = DiagnosticBase & {
  readonly status: "matched";
  readonly id: string;
  readonly entry: CatalogueEntry;
  readonly response: ApiErrorResponse;
};

export type GenericClassification =
  | GenericMatchedClassification
  | UnmatchedClassification;

export interface ClassifyOptions {
  readonly method?: string;
  readonly catalogue?: Catalogue;
}
