"""Source fixtures test extraction boundaries rather than live Telegram behavior."""

from tools.source_scan import group_candidates, scan_source


def extract(source):
    return scan_source(source, "telegram-bot-api/Client.cpp")


def test_comments_strings_and_log_statements_do_not_create_candidates():
    source = r"""
        // fail_query(400, "fake comment", query);
        /* td::Status::Error(400, "fake block comment"); */
        auto text = "fail_query(400, \"fake string\", query)";
        auto raw = R"cpp(fail_query(400, "fake raw string", query))cpp";
        LOG(ERROR) << td::Status::Error(400, "log only");
        VLOG(2) << JsonQueryError(400, "verbose log only");
        return fail_query(400, "Bad Request: real", query);
    """
    sites = extract(source)["sites"]
    assert len(sites) == 1
    assert sites[0]["message"] == {"kind": "literal", "value": "Bad Request: real"}


def test_definitions_and_declarations_are_excluded_but_their_calls_remain():
    source = """
        void fail_query(int code, td::CSlice message, Query query);
        void set_retry_after_error(int retry_after);
        void fail_query_conflict(td::CSlice message, PromisedQueryPtr query);
        void fail_query_with_error(PromisedQueryPtr &&query, Error error);
        void send_http_error(int code, td::CSlice message) const;
        void Client::fail_query_with_error(Query query, int32 error_code,
                                          td::CSlice error_message) {
            fail_query(error_code, error_message, query);
        }
        void Query::set_retry_after_error(int retry_after) {
            JsonQueryError(429, PSLICE() << "Too Many Requests: retry after " << retry_after);
        }
    """
    sites = extract(source)["sites"]
    assert [site["role"] for site in sites] == ["direct_response", "response_serialization"]


def test_adjacent_multiline_raw_and_escaped_literals():
    source = r"""
        fail_query(400,
            "Bad Request: " /* joining comment */
            u8"a \"quote\" and " R"tag(backslash \)tag" "\n\u03b1", query);
    """
    [site] = extract(source)["sites"]
    assert site["message"] == {
        "kind": "literal",
        "value": 'Bad Request: a "quote" and backslash \\\nα',
    }
    assert site["occurrence"]["line"] == 2
    assert site["occurrence"]["end_line"] == 4


def test_dynamic_expressions_retain_fragments_and_are_not_treated_as_literals():
    source = """
        fail_query(code(), PSLICE() << "Bad Request: field " << field << " is invalid", query);
        fail_query_with_error(query, error, "fallback message");
        query->set_retry_after_error(retry_after);
    """
    direct, normalized, retry = extract(source)["sites"]
    assert direct["code"]["kind"] == "dynamic"
    assert direct["message"]["kind"] == "dynamic"
    assert direct["message"]["literal_fragments"] == ["Bad Request: field ", " is invalid"]
    assert normalized["message"] is None
    assert normalized["forwarded_error"]["expression"] == "error"
    assert normalized["fallback"]["value"] == "fallback message"
    assert retry["code"]["value"] == 429
    assert retry["retry_after"]["kind"] == "dynamic"


def test_unsupported_cpp_escapes_remain_unevaluated():
    source = r'fail_query(400, "Bad Request: \e", query);'
    [site] = extract(source)["sites"]
    assert site["message"]["kind"] == "dynamic"


def test_non_ascii_numeric_escapes_are_not_guessed_from_execution_encoding():
    source = r'fail_query(400, "Bad Request: \377\xff", query);'
    [site] = extract(source)["sites"]
    assert site["message"]["kind"] == "dynamic"


def test_cpp_cast_expressions_are_not_mistaken_for_declarations():
    source = """
        fail_query(int(400), "Bad Request: cast", query);
        fail_query_with_error(PromisedQueryPtr(std::move(query)), 400, "cast query");
    """
    direct, normalized = extract(source)["sites"]
    assert direct["code"]["kind"] == "dynamic"
    assert normalized["message"]["value"] == "cast query"


def test_normalizer_inputs_outputs_and_scalar_overload_are_distinct():
    source = """
        void Client::fail_query_with_error(Query query, int32 error_code,
                                          td::CSlice error_message) {
            if (error_message == "MESSAGE_NOT_MODIFIED" || "ALIAS" == error_message) {
                error_message = "message is not modified";
            }
            LOG(ERROR) << "LOG_ONLY";
            fail_query(error_code, error_message, query);
        }
        fail_query_with_error(query, 400, "MESSAGE_NOT_MODIFIED");
        fail_query_with_error(query, error.code(), error.message());
        fail_query_with_error(query, error, "fallback");
    """
    extracted = extract(source)
    sites = extracted["sites"]
    inputs = [site["message"]["value"] for site in sites if site["role"] == "normalization_input"]
    outputs = [site["message"]["value"] for site in sites if site["role"] == "normalization_output"]
    assert inputs == ["MESSAGE_NOT_MODIFIED", "ALIAS"]
    assert outputs == ["message is not modified"]
    normalized = [site for site in sites if site["role"] == "normalized_response"]
    assert normalized[0]["code"] == {"kind": "literal", "value": 400}
    assert normalized[1]["code"]["expression"] == "error . code ( )"
    assert normalized[2]["forwarded_error"]["expression"] == "error"
    assert len(extracted["normalizers"]) == 1


def test_duplicate_candidates_group_without_losing_occurrences():
    sites = extract("""
        fail_query(400, "Bad Request: chat not found", query1);
        fail_query(400, "Bad Request: " "chat not found", query2);
    """)["sites"]
    [candidate] = group_candidates(sites)
    assert len(candidate["occurrences"]) == 2
    assert candidate["occurrences"][0]["line"] == 2
    assert candidate["occurrences"][1]["line"] == 3


def test_token_spacing_does_not_change_dynamic_candidate_identity():
    first = group_candidates(extract('fail_query(400, PSLICE()<<"bad: "<<id, query);')["sites"])
    second = group_candidates(
        extract("""
        fail_query( 400, PSLICE() << "bad: " /* context */ << id, query );
    """)["sites"]
    )
    assert first[0]["id"] == second[0]["id"]


def test_registered_methods_ignore_strings_and_comments():
    extracted = extract("""
        // methods_.emplace("fake", &Client::fake);
        methods_.emplace("sendmessage", &Client::send);
        methods_.emplace("sendmessage", &Client::send);
        methods_.emplace("getme", &Client::get_me);
    """)
    assert extracted["registered_methods"] == ["getme", "sendmessage"]


def test_nested_call_arguments_and_literals_with_delimiters():
    [site] = extract("""
        fail_query(400, build("comma, parenthesis) brace}", nested(1, 2)), query);
    """)["sites"]
    assert site["message"]["kind"] == "dynamic"
    assert site["message"]["literal_fragments"] == ["comma, parenthesis) brace}"]
