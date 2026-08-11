from app.rag.engine import RAGEngine

def test_rag(tmp_path):
    d = tmp_path / "data"; d.mkdir()
    (d/"policy.txt").write_text("Lost cards should be blocked immediately.", encoding="utf-8")
    rag = RAGEngine(str(d))
    assert rag.search("What should I do about a lost card?")
