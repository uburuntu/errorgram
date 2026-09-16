import { catalogue, classify, type Classification } from "../../../js/src/index.ts";

const MAX_RESPONSE_LENGTH = 32_768;
const explanations: Record<Exclude<Classification["status"], "matched">, string> = {
  unknown: "This API error does not match a condition in this catalogue. Its wording, method, or structured parameters may be unsupported.",
  insufficient_context: "The response may match a known condition. Add the API method you called, then classify it again.",
  ambiguous: "The response has competing matches or conflicting structured parameters. No single condition can be selected.",
  not_api_error: 'This JSON is not a Bot API error response. It needs "ok": false, a positive integer error_code, and a string description. If present, parameters must be an object.',
};

const form = document.querySelector<HTMLFormElement>("#playground-form");
if (form) {
  const field = <T extends HTMLElement>(id: string) => document.getElementById(`playground-${id}`) as T;
  const response = field<HTMLTextAreaElement>("response");
  const method = field<HTMLInputElement>("method");
  const error = field<HTMLParagraphElement>("error");
  const result = field<HTMLElement>("result");
  const status = field<HTMLElement>("status");
  const summary = field<HTMLElement>("summary");
  const matched = field<HTMLElement>("match");
  const condition = field<HTMLElement>("condition");
  const reference = field<HTMLAnchorElement>("reference");
  const candidates = field<HTMLElement>("candidates");
  const candidateList = field<HTMLUListElement>("candidate-list");
  const facts = field<HTMLElement>("facts");
  const report = field<HTMLElement>("report");

  function resetResult() {
    result.hidden = true;
    error.hidden = true;
    error.textContent = "";
    response.removeAttribute("aria-invalid");
    matched.hidden = true;
    candidates.hidden = true;
    report.hidden = true;
    status.textContent = "";
    summary.textContent = "";
    condition.textContent = "";
    facts.textContent = "";
    reference.removeAttribute("href");
    candidateList.replaceChildren();
  }

  function showInputError(message: string) {
    error.textContent = message;
    error.hidden = false;
    response.setAttribute("aria-invalid", "true");
    response.focus();
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    resetResult();
    if (!response.value.trim()) {
      showInputError("Paste a JSON response, or choose Load example to try one.");
      return;
    }
    if (response.value.length > MAX_RESPONSE_LENGTH) {
      showInputError("This response is too large. Use at most 32,768 characters of JSON.");
      return;
    }
    let parsed: unknown;
    try {
      parsed = JSON.parse(response.value);
    } catch {
      // Parser messages can contain pasted text; keep the error message fixed.
      showInputError("This is not valid JSON. Use double quotes around keys and strings, remove trailing commas, and paste only the response body.");
      return;
    }
    const methodName = method.value.trim();
    const classification = classify(parsed, methodName ? { method: methodName } : undefined);
    status.textContent = classification.status;
    facts.textContent = JSON.stringify(classification.facts, null, 2);
    if (classification.status === "matched") {
      summary.textContent = classification.entry.summary;
      condition.textContent = classification.id;
      reference.href = `/errors/${encodeURIComponent(classification.id)}/`;
      matched.hidden = false;
    } else {
      summary.textContent = explanations[classification.status];
      for (const id of classification.candidates) {
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.textContent = id;
        link.href = `/errors/${encodeURIComponent(id)}/`;
        item.append(link);
        candidateList.append(item);
      }
      candidates.hidden = classification.candidates.length === 0;
      report.hidden = classification.status !== "unknown";
    }
    result.hidden = false;
    result.focus();
  });

  form.addEventListener("input", resetResult);
  field<HTMLButtonElement>("example").addEventListener("click", () => {
    resetResult();
    // The synthetic example comes from the same bundled catalogue as the SDK.
    const example = catalogue.entries.find((entry) => entry.id === "request.retry_after")!.example;
    response.value = JSON.stringify(example.response, null, 2);
    method.value = example.method ?? "";
    response.focus();
  });
  field<HTMLButtonElement>("clear").addEventListener("click", () => {
    resetResult();
    response.value = "";
    method.value = "";
    response.focus();
  });

  // Clear transient input when the page is left, including a back/forward-cache visit.
  window.addEventListener("pagehide", () => {
    resetResult();
    response.value = "";
    method.value = "";
  });
  form.querySelector("fieldset")!.disabled = false;
}
