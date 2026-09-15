import { GrammyError } from "grammy";
import { classify } from "./index.js";
import type { ConditionId, MatchedClassification } from "./catalogue.js";

/** A known API failure that remains catchable as GrammyError. */
export class EnrichedGrammyError extends GrammyError {
  readonly id: ConditionId;
  readonly classification: MatchedClassification;
  readonly facts: Readonly<Record<string, number | undefined>>;
  readonly original: GrammyError;
  override readonly cause: GrammyError;
  readonly fidelity = Object.freeze({
    description: "preserved",
    parameters: "framework_normalized",
    method: "preserved",
    response: "reconstructed",
  } as const);

  constructor(original: GrammyError, classification: MatchedClassification) {
    super(original.message, original, original.method, original.payload);
    // GrammyError formats its message in the constructor. Retain the original text.
    this.message = original.message;
    this.name = "EnrichedGrammyError";
    if (original.stack !== undefined) this.stack = original.stack;
    this.id = classification.id;
    this.classification = classification;
    this.facts = classification.facts;
    this.original = original;
    this.cause = original;
  }
}

/** Add a diagnostic to a known GrammyError. Other values pass through unchanged. */
export function enrich<T>(error: T): T | EnrichedGrammyError {
  if (!(error instanceof GrammyError) || error instanceof EnrichedGrammyError) return error;
  const classification = classify({
    ok: false,
    error_code: error.error_code,
    description: error.description,
    parameters: error.parameters,
  }, { method: error.method });
  return classification.status === "matched" ? new EnrichedGrammyError(error, classification) : error;
}
