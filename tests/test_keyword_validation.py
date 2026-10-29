import pytest
from pydantic import ValidationError
from ads_mcp.extensions.search import Keyword, Keywords


def test_keyword_ten_words_valid():
    """Verify that keywords up to 10 words are accepted."""
    valid_text = "one two three four five six seven eight nine ten"
    kw = Keyword(text=valid_text, match_type="EXACT")
    assert kw.text == valid_text
    assert len(kw.text.split()) == 10


def test_keyword_eleven_words_raises_validation_error():
    """Verify that a keyword exceeding 10 words is rejected before reaching Google Ads API."""
    invalid_text = "one two three four five six seven eight nine ten eleven"
    with pytest.raises(ValidationError) as exc_info:
        Keyword(text=invalid_text, match_type="BROAD")
    
    assert "Google Ads hard constraint: Keywords cannot exceed 10 terms/words" in str(exc_info.value)
    assert "Received 11 words" in str(exc_info.value)


def test_keyword_whitespace_handling():
    """Verify that multiple consecutive spaces don't bypass the 10-word constraint."""
    valid_with_spaces = "  one   two  three four five six seven eight nine ten  "
    kw = Keyword(text=valid_with_spaces, match_type="PHRASE")
    assert len(kw.text.split()) == 10

    invalid_with_spaces = "  one   two  three four five six seven eight nine ten eleven  "
    with pytest.raises(ValidationError):
        Keyword(text=invalid_with_spaces, match_type="PHRASE")


def test_keywords_schema_has_media_buyer_descriptions():
    """Verify that Pydantic schema includes traffic sculpting and bleeder shield descriptions for the LLM."""
    schema = Keywords.model_json_schema()
    props = schema["properties"]
    
    assert "traffic sculpting" in props["ad_group_id"]["description"].lower()
    assert "budget protection" in props["campaign_id"]["description"].lower()
