import { classify, catalogue, type Catalogue, type ConditionId } from "errorgram";
import { enrich, EnrichedGrammyError } from "errorgram/grammy";
import { GrammyError, HttpError } from "grammy";

declare const input: unknown;
const diagnostic = classify(input, { method: "sendMessage" });

if (diagnostic.status === "matched") {
  const id: ConditionId = diagnostic.id;
  const description: string = diagnostic.response.description;
  void [id, description];
  if (diagnostic.id === "request.retry_after") {
    const seconds: number = diagnostic.facts.retry_after;
    const category: "backoff" = diagnostic.entry.category;
    const sameId: "request.retry_after" = diagnostic.entry.id;
    void [seconds, category, sameId];
    // @ts-expect-error A retry delay is a number, not a string.
    const wrong: string = diagnostic.facts.retry_after;
    // @ts-expect-error Migration facts do not exist on retry errors.
    diagnostic.facts.migrate_to_chat_id;
    void wrong;
  }
  if (diagnostic.id === "chat.migrated") {
    const replacement: number = diagnostic.facts.migrate_to_chat_id;
    void replacement;
    // @ts-expect-error A migration does not imply a retry delay.
    diagnostic.facts.retry_after;
  }
  if (diagnostic.id === "webhook.certificate_too_large") {
    const bytes: number = diagnostic.facts.size_bytes;
    void bytes;
  }
  if (diagnostic.id === "message.not_modified") {
    // @ts-expect-error This condition has no extracted size.
    diagnostic.facts.size_bytes;
  }
} else {
  // @ts-expect-error Uncertain outcomes do not have a stable condition ID.
  diagnostic.id;
}

// @ts-expect-error Stable IDs are generated from the catalogue.
const typo: ConditionId = "chat.not_fond";
// @ts-expect-error Bundled metadata is immutable.
catalogue.entries[0].summary = "Changed";
void typo;

declare const override: Catalogue;
const extension = classify(input, { catalogue: override });
if (extension.status === "matched") {
  const customId: string = extension.id;
  // @ts-expect-error A custom catalogue can contain IDs unknown to this package.
  const builtin: ConditionId = extension.id;
  void [customId, builtin];
}

const original = new GrammyError("Failed", { ok: false, error_code: 400, description: "Bad Request: chat not found" }, "getChat", {});
const enhanced = enrich(original);
const frameworkCompatible: GrammyError = enhanced;
void frameworkCompatible;
if (enhanced instanceof EnrichedGrammyError) {
  const id: ConditionId = enhanced.id;
  const previous: GrammyError = enhanced.original;
  void [id, previous];
  if (enhanced.classification.id === "request.retry_after") {
    const delay: number = enhanced.classification.facts.retry_after;
    void delay;
  }
}

const transport = new HttpError("Offline", new Error("No connection"));
const passed = enrich(transport);
if (passed instanceof HttpError) {
  const network: unknown = passed.error;
  void network;
}
