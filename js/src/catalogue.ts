// Generated from catalogue/errors.json. Run make generate to update.
import { deepFreeze } from "./freeze.js";
import type { Catalogue, DiagnosticBase, ApiErrorResponse } from "./types.js";

const data = {
  "schema_version": "1.0.0",
  "reviewed_on": "2026-09-15",
  "coverage": {
    "complete": false,
    "live_verified": false,
    "scope": "Telegram Bot API error responses. Source-derived; hosted deployment behavior is unverified.",
    "examples": "Synthetic examples derived from the cited source."
  },
  "sources": {
    "server-10.3": {
      "kind": "server_source",
      "repository": "https://github.com/tdlib/telegram-bot-api",
      "revision": "e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1",
      "version_label": "10.3"
    },
    "response-parameters": {
      "kind": "official_documentation",
      "url": "https://core.telegram.org/bots/api#responseparameters",
      "accessed_on": "2026-09-15"
    }
  },
  "entries": [
    {
      "id": "message.not_modified",
      "category": "message_state",
      "summary": "The requested message content and reply markup are unchanged.",
      "match_any": [
        {
          "error_code": 400,
          "description_exact": "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
        }
      ],
      "scope": {
        "method_examples": [
          "editMessageText",
          "editMessageCaption",
          "editMessageReplyMarkup"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "The requested edit repeats the current content and markup."
      ],
      "diagnostic_limits": "The response does not include the current message or establish the history of concurrent edits.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            106,
            113
          ],
          "note": "MESSAGE_NOT_MODIFIED is rewritten here; prefix and initial-case handling are at lines 165-205."
        }
      ],
      "example": {
        "method": "editMessageText",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "accept_existing_state_if_intended",
        "repeat_request": "unhelpful_without_change",
        "preconditions": [
          "The application considers an already-applied desired state a successful outcome."
        ]
      }
    },
    {
      "id": "message.delete_forbidden",
      "category": "operation_not_allowed",
      "summary": "Telegram rejected deletion of the message.",
      "match_any": [
        {
          "error_code": 400,
          "description_exact": "Bad Request: message can't be deleted"
        }
      ],
      "scope": {
        "method_examples": [
          "deleteMessage",
          "deleteMessages"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "A permissions, message-type or message-age restriction may prevent deletion."
      ],
      "diagnostic_limits": "The source proves the response mapping, not which deletion restriction caused a particular failure. The causes above are diagnostic hypotheses.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            151,
            153
          ],
          "note": "MESSAGE_DELETE_FORBIDDEN is rewritten before the Bad Request prefix is added."
        }
      ],
      "example": {
        "method": "deleteMessage",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: message can't be deleted"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "check_deletion_eligibility",
        "repeat_request": "after_relevant_change",
        "preconditions": [
          "Check the current deleteMessage rules and bot permissions; a permanent message restriction may have no repair."
        ]
      }
    },
    {
      "id": "query.invalid_or_expired",
      "category": "query_state",
      "summary": "The query ID is invalid or its response window has expired.",
      "match_any": [
        {
          "error_code": 400,
          "description_exact": "Bad Request: query is too old and response timeout expired or query ID is invalid"
        }
      ],
      "scope": {
        "method_examples": [
          "answerCallbackQuery"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "The query identifier is invalid.",
        "The response arrived after the query's response window."
      ],
      "diagnostic_limits": "The description explicitly combines causes; it does not establish a universal timeout duration.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            148,
            150
          ],
          "note": "QUERY_ID_INVALID is deliberately expanded to a description containing alternatives."
        }
      ],
      "example": {
        "method": "answerCallbackQuery",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: query is too old and response timeout expired or query ID is invalid"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "verify_identifier_and_response_timing",
        "repeat_request": "unhelpful_for_expired_identifier",
        "preconditions": [
          "Use the identifier from the correct incoming query and respond promptly to future queries."
        ]
      }
    },
    {
      "id": "chat.not_found",
      "category": "target_resolution",
      "summary": "The bot could not resolve this chat.",
      "match_any": [
        {
          "error_code": 400,
          "description_exact": "Bad Request: chat not found"
        }
      ],
      "scope": {
        "method_examples": [
          "sendMessage",
          "getChat"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "An upstream lookup error was replaced with the generic chat lookup message.",
        "A username resolved to a chat type that this lookup does not allow."
      ],
      "diagnostic_limits": "This is not proof that the chat was deleted, the bot was blocked, or the identifier is permanently unusable.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            7239,
            7266
          ],
          "note": "A fallback masks upstream 400-class errors, and a separate local branch emits the same description."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            85,
            108
          ],
          "note": "Some upstream codes are converted to 400 before the fallback description is applied."
        }
      ],
      "example": {
        "method": "getChat",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: chat not found"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "inspect_target_and_access",
        "repeat_request": "after_relevant_change",
        "preconditions": [
          "Verify the identifier, target type and bot access before changing stored chat records."
        ]
      }
    },
    {
      "id": "chat.migrated",
      "category": "target_migration",
      "summary": "The group has moved to a supergroup with a new ID.",
      "match_any": [
        {
          "error_code": 400,
          "required_parameters": {
            "migrate_to_chat_id": "nonzero_integer"
          }
        }
      ],
      "scope": {
        "method_examples": [
          "sendMessage"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "The request addresses a group that was upgraded to a supergroup."
      ],
      "diagnostic_limits": "Use the structured replacement identifier; a description alone does not supply the new target.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            8821,
            8827
          ],
          "note": "The replacement chat ID is placed in response parameters."
        },
        {
          "source": "response-parameters",
          "note": "Documents migrate_to_chat_id, including its maximum of 52 significant bits."
        }
      ],
      "example": {
        "method": "sendMessage",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: group chat was upgraded to a supergroup chat",
          "parameters": {
            "migrate_to_chat_id": -1001234567890
          }
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "migrate_chat_reference",
        "repeat_request": "after_target_update",
        "preconditions": [
          "Update the intended chat reference from parameters.migrate_to_chat_id, account for concurrent updates, and bound retries."
        ]
      }
    },
    {
      "id": "bot.blocked_by_user",
      "category": "access",
      "summary": "The user has blocked the bot.",
      "match_any": [
        {
          "error_code": 403,
          "description_exact": "Forbidden: bot was blocked by the user"
        }
      ],
      "scope": {
        "method_examples": [
          "sendMessage"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "The recipient has blocked the bot."
      ],
      "diagnostic_limits": "The response establishes the current rejection, not that access can never be restored.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            127,
            129
          ],
          "note": "USER_IS_BLOCKED changes both the code (to 403) and the description."
        }
      ],
      "example": {
        "method": "sendMessage",
        "response": {
          "ok": false,
          "error_code": 403,
          "description": "Forbidden: bot was blocked by the user"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "suspend_sends_until_access_changes",
        "repeat_request": "after_access_change",
        "preconditions": [
          "Use application policy to track reachability and resume only when there is evidence that access changed."
        ]
      }
    },
    {
      "id": "request.retry_after",
      "category": "backoff",
      "summary": "The server asks the bot to wait before trying again.",
      "match_any": [
        {
          "error_code": 429,
          "required_parameters": {
            "retry_after": "positive_integer"
          }
        }
      ],
      "scope": {
        "method_examples": [
          "sendMessage",
          "setWebhook",
          "close"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "Flood limiting.",
        "Authorization or startup throttling.",
        "An unfinished query being disposed, including during shutdown."
      ],
      "diagnostic_limits": "The response does not identify whether the limit is per chat, per bot, per method or caused by server lifecycle handling.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Query.cpp",
          "lines": [
            120,
            126
          ],
          "note": "Builds both the description and structured retry_after parameter."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Query.h",
          "lines": [
            238,
            242
          ],
          "note": "The query deleter also produces this response with a five-second delay."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17529,
            17550
          ],
          "note": "Flood and authorization paths share the response shape."
        },
        {
          "source": "response-parameters",
          "note": "Documents retry_after in seconds."
        }
      ],
      "example": {
        "method": "sendMessage",
        "response": {
          "ok": false,
          "error_code": 429,
          "description": "Too Many Requests: retry after 5",
          "parameters": {
            "retry_after": 5
          }
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "schedule_bounded_retry",
        "repeat_request": "after_server_delay_and_policy_check",
        "delay_parameter": "retry_after",
        "preconditions": [
          "Wait at least the supplied delay, coordinate with any framework retry plugin, and bound attempts."
        ]
      }
    },
    {
      "id": "updates.webhook_active",
      "category": "update_delivery_configuration",
      "summary": "Polling was requested while a webhook is active or being configured.",
      "match_any": [
        {
          "error_code": 409,
          "description_exact": "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"
        }
      ],
      "scope": {
        "method_examples": [
          "getUpdates"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "The bot has an active or pending webhook configuration."
      ],
      "diagnostic_limits": "This is a different condition from two simultaneous getUpdates requests.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            16926,
            16931
          ],
          "note": "Checks configured and pending webhook state before polling."
        }
      ],
      "example": {
        "method": "getUpdates",
        "response": {
          "ok": false,
          "error_code": 409,
          "description": "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "choose_update_delivery_mode",
        "repeat_request": "after_configuration_change",
        "preconditions": [
          "If polling is intended, remove the webhook deliberately; if webhooks are intended, stop polling."
        ]
      }
    },
    {
      "id": "updates.concurrent_poll",
      "category": "update_delivery_concurrency",
      "summary": "Another getUpdates request interrupted the pending long poll.",
      "match_any": [
        {
          "error_code": 409,
          "description_exact": "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running"
        }
      ],
      "scope": {
        "method_examples": [
          "getUpdates"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "Overlapping getUpdates requests for the same bot."
      ],
      "diagnostic_limits": "Overlapping requests may originate in one process or multiple deployments; the response does not prove how many bot processes exist.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17493,
            17514
          ],
          "note": "The alternate branch emits a different description for termination by setWebhook."
        }
      ],
      "example": {
        "method": "getUpdates",
        "response": {
          "ok": false,
          "error_code": 409,
          "description": "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "ensure_single_polling_owner",
        "repeat_request": "after_concurrency_change",
        "preconditions": [
          "Stop competing polling loops or establish ownership before resuming."
        ]
      }
    },
    {
      "id": "auth.invalid_token_format",
      "category": "authentication",
      "summary": "The server rejected the token during local validation.",
      "match_any": [
        {
          "error_code": 401,
          "description_exact": "Unauthorized: invalid token specified"
        }
      ],
      "scope": {
        "method_examples": [
          "getMe"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "A locally checked token structure or numeric identifier constraint failed."
      ],
      "diagnostic_limits": "This signature is narrower than generic Unauthorized. Other malformed-token paths may produce different codes.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/ClientManager.cpp",
          "lines": [
            73,
            84
          ],
          "note": "Two local checks return this exact response; the intervening check can return 421."
        }
      ],
      "example": {
        "method": "getMe",
        "response": {
          "ok": false,
          "error_code": 401,
          "description": "Unauthorized: invalid token specified"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "correct_token_configuration",
        "repeat_request": "after_configuration_change",
        "preconditions": [
          "Verify the configured token without placing it in logs or inventory submissions."
        ]
      }
    },
    {
      "id": "file.download_too_large",
      "category": "download_limit",
      "summary": "The file exceeds the server’s non-local download limit.",
      "match_any": [
        {
          "error_code": 400,
          "method": "getfile",
          "description_exact": "Bad Request: file is too big"
        }
      ],
      "scope": {
        "method_examples": [
          "getFile"
        ],
        "exhaustive": false,
        "deployment": "Source guard applies when local_mode is false."
      },
      "possible_causes": [
        "Expected or downloaded file size exceeds MAX_DOWNLOAD_FILE_SIZE while local mode is disabled."
      ],
      "diagnostic_limits": "A bare file-is-too-big description without method context is insufficient for this download-specific classification. This is not an upload-size rule.",
      "facts": {
        "verified_limit_bytes": 20971520,
        "limit_version_source": "server-10.3"
      },
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17032,
            17049
          ],
          "note": "getFile reaches the size check guarded by local_mode."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            9373,
            9383
          ],
          "note": "The download update path enforces the same limit."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.h",
          "lines": [
            72,
            72
          ],
          "note": "The constant is 20 << 20 bytes in this revision."
        }
      ],
      "example": {
        "method": "getFile",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: file is too big"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "change_download_strategy",
        "repeat_request": "after_relevant_change",
        "preconditions": [
          "Use a suitable smaller file or deliberately configure a server with the required local-mode download capability."
        ]
      }
    },
    {
      "id": "server.restarting",
      "category": "server_lifecycle",
      "summary": "The bot client is closing for a server restart.",
      "match_any": [
        {
          "error_code": 500,
          "description_exact": "Internal Server Error: restart"
        }
      ],
      "scope": {
        "method_examples": [],
        "exhaustive": false
      },
      "possible_causes": [
        "The bot client is closing without taking the logout branches."
      ],
      "diagnostic_limits": "An exception wrapper that discarded the original 5xx description cannot recover this distinction from the status alone.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17560,
            17564
          ],
          "note": "The closing error is passed directly to fail_query by fail_query_closing."
        }
      ],
      "example": {
        "method": "getMe",
        "response": {
          "ok": false,
          "error_code": 500,
          "description": "Internal Server Error: restart"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "backoff_and_reassess_operation",
        "repeat_request": "policy_dependent",
        "preconditions": [
          "Apply bounded backoff and evaluate whether repeating the particular operation is safe; do not derive replay safety from a 5xx status alone."
        ]
      }
    },
    {
      "id": "routing.token_not_served",
      "category": "token_routing",
      "summary": "The token failed the server’s bot-ID or routing check.",
      "match_any": [
        {
          "error_code": 421,
          "description_exact": "Misdirected Request: forbidden token specified"
        }
      ],
      "scope": {
        "method_examples": [
          "getMe"
        ],
        "exhaustive": false,
        "deployment": "Relevant to the open-source server's token-range routing; hosted occurrence is unverified."
      },
      "possible_causes": [
        "The bot ID is outside the server’s configured token range.",
        "The token’s numeric prefix could not be parsed."
      ],
      "diagnostic_limits": "The same response covers a routing failure and a token-format failure; it does not prove that Telegram revoked the token.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/ClientManager.cpp",
          "lines": [
            78,
            80
          ],
          "note": "Both sides of the condition emit the same 421 response."
        }
      ],
      "example": {
        "method": "getMe",
        "response": {
          "ok": false,
          "error_code": 421,
          "description": "Misdirected Request: forbidden token specified"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "inspect_token_prefix_and_server_routing",
        "repeat_request": "after_configuration_change",
        "preconditions": [
          "Check token formatting and, when operating a local server, its token-range configuration."
        ]
      }
    },
    {
      "id": "session.logged_out",
      "category": "server_lifecycle",
      "summary": "The bot session has logged out.",
      "match_any": [
        {
          "error_code": 400,
          "description_exact": "Logged out"
        }
      ],
      "scope": {
        "method_examples": [],
        "exhaustive": false
      },
      "possible_causes": [
        "The server is completing a bot logout."
      ],
      "diagnostic_limits": "Not every 400 response begins with Bad Request. This signature alone does not explain why logout was initiated.",
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17553,
            17555
          ],
          "note": "Stores a 400 description with no Bad Request prefix."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17520,
            17525
          ],
          "note": "The direct fail_query path preserves that description."
        }
      ],
      "example": {
        "method": "getMe",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Logged out"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "reconcile_bot_session_lifecycle",
        "repeat_request": "after_lifecycle_resolution",
        "preconditions": [
          "Determine whether logout or a server move was intentional before resuming requests."
        ]
      }
    },
    {
      "id": "webhook.certificate_too_large",
      "category": "webhook_configuration",
      "summary": "The uploaded webhook certificate exceeds the server’s size limit.",
      "match_any": [
        {
          "error_code": 400,
          "description_template": "Bad Request: certificate size is too big ({size_bytes} bytes)",
          "capture_types": {
            "size_bytes": "positive_integer"
          }
        }
      ],
      "scope": {
        "method_examples": [
          "setWebhook"
        ],
        "exhaustive": false
      },
      "possible_causes": [
        "The uploaded certificate file is larger than MAX_CERTIFICATE_FILE_SIZE."
      ],
      "diagnostic_limits": "The captured size describes the rejected upload; it is not the configured limit or a Telegram media limit.",
      "facts": {
        "verified_limit_bytes": 3145728,
        "limit_version_source": "server-10.3"
      },
      "evidence": [
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.cpp",
          "lines": [
            17261,
            17266
          ],
          "note": "The description interpolates the actual file size; one literal string cannot represent all responses."
        },
        {
          "source": "server-10.3",
          "path": "telegram-bot-api/Client.h",
          "lines": [
            71,
            71
          ],
          "note": "The constant is 3 << 20 bytes in this revision."
        }
      ],
      "example": {
        "method": "setWebhook",
        "response": {
          "ok": false,
          "error_code": 400,
          "description": "Bad Request: certificate size is too big (4194304 bytes)"
        }
      },
      "evidence_level": "source_derived",
      "guidance": {
        "action": "correct_webhook_certificate_file",
        "repeat_request": "after_payload_change",
        "preconditions": [
          "Verify that the uploaded file is the intended certificate and satisfies this server revision's limit."
        ]
      }
    }
  ],
  "catalogue_version": "0.1.0",
  "name": "Errorgram",
  "matching": {
    "exclusive_parameter_groups": [
      [
        "retry_after",
        "migrate_to_chat_id"
      ]
    ]
  }
} as const satisfies Catalogue;

export const catalogue = deepFreeze(data);
export const catalogueVersion = catalogue.catalogue_version;
export type Entry = (typeof catalogue.entries)[number];
export type ConditionId = Entry["id"];
export type EntryFor<I extends ConditionId> = Extract<Entry, { readonly id: I }>;

export interface FactsById {
  "message.not_modified": {  };
  "message.delete_forbidden": {  };
  "query.invalid_or_expired": {  };
  "chat.not_found": {  };
  "chat.migrated": { readonly "migrate_to_chat_id": number; };
  "bot.blocked_by_user": {  };
  "request.retry_after": { readonly "retry_after": number; };
  "updates.webhook_active": {  };
  "updates.concurrent_poll": {  };
  "auth.invalid_token_format": {  };
  "file.download_too_large": {  };
  "server.restarting": {  };
  "routing.token_not_served": {  };
  "session.logged_out": {  };
  "webhook.certificate_too_large": { readonly "size_bytes": number; };
}

export type MatchedClassification = {
  [I in ConditionId]: Omit<DiagnosticBase, "facts"> & {
    readonly status: "matched";
    readonly id: I;
    readonly entry: EntryFor<I>;
    readonly facts: FactsById[I];
    readonly response: ApiErrorResponse;
  };
}[ConditionId];
