import streamlit as st


# -------------------------------------------------------------------
# Page config
# -------------------------------------------------------------------
PAGE_TITLE = "Public Health Misinformation Fact-Checking"
PAGE_BROWSER_TITLE = "Public Health Fact-Checking"
PAGE_DESCRIPTION = (
    "Check whether a public health claim is supported by trusted evidence "
    "from public health sources."
)
TOP_BANNER_LINES = [
    "AI-powered fact-checking for public health claims.",
    "Get a clear verdict, explanation, and evidence from trusted sources.",
]


def configure_page() -> None:
    """Configure the Streamlit page metadata.

    We keep browser-level metadata separate from on-page headings so the app can
    present a concise tab title while retaining a more descriptive product title.
    """
    st.set_page_config(
        page_title=PAGE_BROWSER_TITLE,
        page_icon="🩺",
        layout="wide",
    )


# -------------------------------------------------------------------
# Constants / fake data
# -------------------------------------------------------------------
EXAMPLE_CLAIMS = [
    "Select an example",
    "Vaccines cause infertility",
    "Masks reduce oxygen intake",
    "Antibiotics treat viral infections",
]
SOURCE_FILTERS = ["All sources", "WHO only", "CDC only"]

FAKE_RESULTS = {
    "Vaccines cause infertility": {
        "verdict": "False",
        "explanation": (
            "There is no credible evidence that approved vaccines cause infertility. "
            "Public health agencies and large clinical studies have found no link between "
            "vaccination and reduced fertility in women or men. This claim often stems "
            "from misinformation that misrepresents immune responses or reproductive biology."
        ),
        "confidence": 0.96,
        "evidence": [
            {
                "source": "WHO",
                "stance": "Refutes claim",
                "title": "Vaccine Safety Basics",
                "text": (
                    "The WHO explains that vaccines used in immunization programs are "
                    "carefully evaluated for safety and there is no evidence that they "
                    "cause infertility."
                ),
                "score": 0.92,
                "url": "https://www.who.int/news-room/questions-and-answers/item/vaccines-and-immunization-vaccine-safety",
            },
            {
                "source": "CDC",
                "stance": "Refutes claim",
                "title": "COVID-19 Vaccines and Fertility",
                "text": (
                    "The CDC states that there is currently no evidence showing that "
                    "any vaccines, including COVID-19 vaccines, cause fertility problems."
                ),
                "score": 0.89,
                "url": "https://www.cdc.gov/coronavirus/2019-ncov/vaccines/planning-for-pregnancy.html",
            },
            {
                "source": "WHO",
                "stance": "Refutes claim",
                "title": "Myths and Misconceptions about Immunization",
                "text": (
                    "WHO myth-busting materials describe infertility claims as unsupported "
                    "and inconsistent with available clinical and population-level evidence."
                ),
                "score": 0.85,
                "url": "https://www.who.int/",
            },
        ],
        "seq2seq_answer": (
            "This claim is false. Vaccines are generally considered safe and there is no "
            "evidence that they cause infertility."
        ),
        "rag_answer": (
            "This claim is false. WHO and CDC materials both report that approved vaccines "
            "have not been shown to cause infertility, and public health guidance consistently "
            "rejects this myth based on clinical safety evidence."
        ),
    },
    "Masks reduce oxygen intake": {
        "verdict": "False",
        "explanation": (
            "Standard face masks are designed to be breathable while blocking respiratory droplets. "
            "Studies and public health guidance show that masks do not meaningfully reduce oxygen "
            "levels for the general public during normal use. People with specific medical concerns "
            "should still follow personalized clinical advice."
        ),
        "confidence": 0.93,
        "evidence": [
            {
                "source": "WHO",
                "stance": "Refutes claim",
                "title": "Mask Use in the Context of COVID-19",
                "text": (
                    "WHO guidance indicates that prolonged use of medical masks by healthy people "
                    "does not cause carbon dioxide intoxication or oxygen deficiency."
                ),
                "score": 0.91,
                "url": "https://www.who.int/",
            },
            {
                "source": "CDC",
                "stance": "Refutes claim",
                "title": "About Masks",
                "text": (
                    "The CDC explains that masks are made from materials that allow normal airflow "
                    "while helping reduce the spread of infectious particles."
                ),
                "score": 0.87,
                "url": "https://www.cdc.gov/",
            },
            {
                "source": "WHO",
                "stance": "Refutes claim",
                "title": "Coronavirus Disease Advice for the Public",
                "text": (
                    "Public-facing WHO materials note that masks can be worn safely and should not "
                    "cause oxygen deprivation in routine community settings."
                ),
                "score": 0.84,
                "url": "https://www.who.int/",
            },
        ],
        "seq2seq_answer": (
            "This claim is false. Masks do not significantly reduce oxygen intake during normal use."
        ),
        "rag_answer": (
            "This claim is false. WHO and CDC guidance both indicate that masks remain breathable "
            "and do not cause meaningful oxygen deprivation for most people in normal settings."
        ),
    },
    "Antibiotics treat viral infections": {
        "verdict": "False",
        "explanation": (
            "Antibiotics are used to treat bacterial infections, not viral infections. "
            "Using antibiotics when they are not needed does not help patients recover from viruses "
            "and can contribute to antimicrobial resistance. Viral illnesses often require supportive "
            "care or other targeted treatments instead."
        ),
        "confidence": 0.98,
        "evidence": [
            {
                "source": "CDC",
                "stance": "Refutes claim",
                "title": "Antibiotic Use and Antimicrobial Resistance Facts",
                "text": (
                    "The CDC states that antibiotics do not work on viruses such as those that "
                    "cause colds, flu, and most sore throats."
                ),
                "score": 0.95,
                "url": "https://www.cdc.gov/antibiotic-use/",
            },
            {
                "source": "WHO",
                "stance": "Refutes claim",
                "title": "Antimicrobial Resistance",
                "text": (
                    "WHO explains that misuse and overuse of antibiotics accelerate antimicrobial "
                    "resistance and includes taking antibiotics for viral infections as an example of misuse."
                ),
                "score": 0.90,
                "url": "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance",
            },
            {
                "source": "CDC",
                "stance": "Refutes claim",
                "title": "Be Antibiotics Aware",
                "text": (
                    "CDC campaign materials emphasize that antibiotics are not effective against viruses "
                    "and should only be used when medically appropriate."
                ),
                "score": 0.86,
                "url": "https://www.cdc.gov/antibiotic-use/week/",
            },
        ],
        "seq2seq_answer": (
            "This claim is false. Antibiotics are not effective against viral infections."
        ),
        "rag_answer": (
            "This claim is false. CDC and WHO sources both explain that antibiotics target bacteria, "
            "not viruses, and using them for viral illness can worsen antimicrobial resistance."
        ),
    },
}


# -------------------------------------------------------------------
# State init
# -------------------------------------------------------------------
def initialize_session_state() -> None:
    """Initialize session keys used by the app.

    Session state is preserved because the current demo already relies on it,
    and it will also be useful later for storing API responses and request state.
    """
    st.session_state.setdefault("claim_input", "")
    st.session_state.setdefault("example_claim", EXAMPLE_CLAIMS[0])
    st.session_state.setdefault("source_filter", SOURCE_FILTERS[0])
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("checked_claim", "")


# -------------------------------------------------------------------
# Data functions
# -------------------------------------------------------------------
def handle_example_selection() -> None:
    """Sync the selected example into the text input for a smoother demo flow."""
    selected_example = st.session_state.example_claim
    if selected_example != EXAMPLE_CLAIMS[0]:
        st.session_state.claim_input = selected_example


def filter_evidence_by_source(evidence_list: list[dict], source_filter: str) -> list[dict]:
    """Filter evidence items based on the selected source."""
    if source_filter == "All sources":
        return evidence_list

    source_name = source_filter.replace(" only", "")
    return [item for item in evidence_list if item["source"] == source_name]


def build_default_result(claim: str) -> dict:
    """Return a fallback result when the claim is not in the demo database."""
    return {
        "verdict": "Uncertain",
        "explanation": "No matching result in demo database.",
        "confidence": 0.50,
        "evidence": [],
        "seq2seq_answer": "No matching result in demo database.",
        "rag_answer": "No matching result in demo database.",
        "claim": claim,
    }


def reset_app_state() -> None:
    """Reset the app back to its initial demo state."""
    st.session_state.claim_input = ""
    st.session_state.example_claim = EXAMPLE_CLAIMS[0]
    st.session_state.source_filter = SOURCE_FILTERS[0]
    st.session_state.result = None
    st.session_state.checked_claim = ""


def get_fact_check_result(claim: str, source_filter: str) -> dict:
    """Return a fact-check result for the given claim.

    This is the single integration point for data retrieval. Right now it uses
    local fake data only. If we connect a real backend later, we should update
    this function and keep the render layer unchanged.
    """
    normalized_claim = claim.strip()
    base_result = FAKE_RESULTS.get(normalized_claim)

    if not base_result:
        return build_default_result(normalized_claim)

    filtered_evidence = filter_evidence_by_source(base_result["evidence"], source_filter)

    return {
        **base_result,
        "claim": normalized_claim,
        "evidence": filtered_evidence,
    }


# -------------------------------------------------------------------
# Render functions
# -------------------------------------------------------------------
def render_header() -> None:
    """Render the top page header and product description."""
    st.title(PAGE_TITLE)
    st.write(PAGE_DESCRIPTION)

    # A short trusted-systems banner makes the page feel more product-like
    # without changing the underlying business logic.
    with st.container():
        st.info("\n".join(TOP_BANNER_LINES))


def render_theme_hint() -> None:
    """Placeholder for future theme customization guidance.

    If we want a more branded visual style later, we can configure it in
    `.streamlit/config.toml` without changing the app logic below.
    """


def format_confidence(confidence: float) -> str:
    """Format confidence as a percentage for a more product-like UI."""
    return f"{round(confidence * 100):d}%"


def get_confidence_level(confidence: float) -> str:
    """Translate a numeric confidence score into a more readable label."""
    if confidence >= 0.80:
        return "High"
    if confidence >= 0.50:
        return "Medium"
    return "Low"


def get_verdict_summary(verdict: str) -> tuple[str, str]:
    """Return the product-style verdict headline and a one-line interpretation."""
    verdict_map = {
        "False": (
            "❌ This claim is FALSE",
            "There is no credible scientific evidence supporting this claim.",
        ),
        "True": (
            "✅ This claim is TRUE",
            "This claim is supported by credible public health evidence.",
        ),
        "Uncertain": (
            "⚠️ This claim is UNCERTAIN",
            "There is not enough credible evidence in the current knowledge base.",
        ),
    }
    return verdict_map.get(
        verdict,
        (
            "⚠️ This claim is UNCERTAIN",
            "There is not enough credible evidence in the current knowledge base.",
        ),
    )


def get_verdict_display(verdict: str) -> str:
    """Return a larger visual verdict label so users can identify the result quickly."""
    verdict_icons = {
        "False": "❌",
        "True": "✅",
        "Uncertain": "⚠️",
    }
    icon = verdict_icons.get(verdict, "⚠️")
    return f"## {icon} {verdict}"


def render_verdict(verdict: str) -> None:
    """Render the verdict headline without repeating the same message below."""
    # A larger verdict headline creates a clear visual focal point for the result area.
    verdict_title, verdict_summary = get_verdict_summary(verdict)
    st.markdown(f"## {verdict_title}")
    st.caption(verdict_summary)


def render_results_summary(result: dict) -> None:
    """Render verdict, explanation, and confidence in the left column."""
    # This heading helps the assessment read like a standalone decision card.
    st.markdown("### 🧾 Claim Assessment")

    if result.get("claim"):
        st.caption(f"Claim checked: {result['claim']}")

    st.divider()
    render_verdict(result["verdict"])
    st.divider()

    # A metric plus progress bar makes confidence feel more like a product KPI.
    confidence_label = get_confidence_level(result["confidence"])
    st.markdown("### 📊 Confidence")
    st.metric(
        label="Confidence",
        value=f"{confidence_label} ({format_confidence(result['confidence'])})",
    )
    st.progress(result["confidence"])

    st.markdown("### 💡 Explanation")
    st.write(result["explanation"])


def summarize_evidence(evidence_list: list[dict]) -> str:
    """Summarize how many evidence items were retrieved and what stance they take."""
    if not evidence_list:
        return "No supporting sources found in the current demo."

    total_sources = len(evidence_list)
    stance_counts: dict[str, int] = {}
    for evidence in evidence_list:
        stance = evidence.get("stance", "Unspecified")
        stance_counts[stance] = stance_counts.get(stance, 0) + 1

    if len(stance_counts) == 1:
        only_stance = next(iter(stance_counts))
        return f"{total_sources} sources found · All {only_stance.lower()}"

    stance_summary = " / ".join(
        f"{count} {stance.lower()}" for stance, count in stance_counts.items()
    )
    return f"{total_sources} sources found · {stance_summary}"


def render_claim_input_panel() -> None:
    """Render the interactive controls and results in the left column."""
    st.text_input(
        "Enter a health-related claim",
        placeholder="e.g. Vaccines cause infertility",
        key="claim_input",
    )

    st.selectbox(
        "Try an example claim",
        EXAMPLE_CLAIMS,
        index=EXAMPLE_CLAIMS.index(st.session_state.example_claim),
        key="example_claim",
        on_change=handle_example_selection,
    )

    st.radio(
        "Source filter",
        SOURCE_FILTERS,
        index=SOURCE_FILTERS.index(st.session_state.source_filter),
        key="source_filter",
    )

    # Putting actions side by side gives the input area a more app-like control bar.
    action_col, clear_col = st.columns([3, 1], gap="small")

    with action_col:
        check_clicked = st.button("Check Claim", type="primary", use_container_width=True)

    with clear_col:
        clear_clicked = st.button("Clear", use_container_width=True)

    if check_clicked:
        # Show a short loading state so the interaction feels closer to a real product flow.
        with st.spinner("Checking claim..."):
            result = get_fact_check_result(
                st.session_state.claim_input,
                st.session_state.source_filter,
            )
        st.session_state.result = result
        st.session_state.checked_claim = st.session_state.claim_input.strip()

    if clear_clicked:
        reset_app_state()

    if st.session_state.result:
        render_results_summary(st.session_state.result)


def render_evidence_panel() -> None:
    """Render the evidence area in the right column."""
    st.subheader("Supporting Evidence")
    # Keep this subtitle concise and product-like while preserving the layout.
    st.caption("Evidence retrieved from trusted public health sources.")

    result = st.session_state.result
    if not result:
        st.info("Evidence will appear here after you check a claim.")
        return

    evidence_list = result["evidence"]
    st.caption(summarize_evidence(evidence_list))

    if not evidence_list:
        st.info("No supporting evidence is available for this claim in the current demo.")
        return

    for index, evidence in enumerate(evidence_list, start=1):
        expander_title = (
            f"Evidence {index} · {evidence['source']} · "
            f"{evidence.get('stance', 'Unspecified')} · Score {evidence['score']:.2f}"
        )
        # Open the strongest evidence by default so users immediately see grounded content.
        with st.expander(expander_title, expanded=index == 1):
            # Highlight the source name first to make the evidence feel more authoritative.
            source_badges = {
                "WHO": "🟦",
                "CDC": "🟩",
            }
            source_icon = source_badges.get(evidence["source"], "🟦")
            st.markdown(f"### {source_icon} {evidence['source']}")
            st.caption(evidence.get("stance", "Unspecified"))
            st.markdown(f"**Title:** {evidence['title']}")
            st.markdown("**Retrieved Text**")
            st.write(evidence["text"])
            st.markdown(f"**URL:** [Open source]({evidence['url']})")


def render_model_comparison() -> None:
    """Render the model comparison section at the bottom of the page."""
    result = st.session_state.result

    # Keep secondary comparisons below the fold so the first screen emphasizes
    # input, verdict, and evidence. This render block can later show live API outputs.
    with st.expander("See model comparison"):
        left_col, right_col = st.columns(2, gap="large")

        with left_col:
            st.markdown("**Vanilla Seq2Seq**")
            if result:
                st.write(result["seq2seq_answer"])
            else:
                st.write("Vanilla Seq2Seq answer will appear here.")

        with right_col:
            st.markdown("**RAG with Evidence**")
            if result:
                st.write(result["rag_answer"])
            else:
                st.write("RAG answer with evidence will appear here.")


def render_footer() -> None:
    """Render the bottom disclaimer."""
    st.caption(
        "This demo is for educational purposes only and does not provide medical advice."
    )


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main() -> None:
    """Build and render the full page."""
    configure_page()
    initialize_session_state()
    render_theme_hint()

    render_header()

    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        render_claim_input_panel()

    with right_col:
        render_evidence_panel()

    st.divider()
    render_model_comparison()
    st.divider()
    render_footer()


if __name__ == "__main__":
    main()
