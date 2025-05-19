import pytest
from src.eyetype4you.core.typing_engine import TypingEngine
from src.eyetype4you.bot.bot_personality import BotPersonality

class TestTypingEngine:
    @pytest.fixture
    def engine(self):
        return TypingEngine()
        
    @pytest.fixture
    def custom_personality(self):
        return BotPersonality.create_custom(
            name="Test Bot",
            base_typing_speed=0.05,
            error_rate=0.0
        )
        
    def test_initialization(self, engine):
        assert engine is not None
        assert engine.personality is not None
        
    def test_stop_typing(self, engine):
        engine._running = True
        engine.stop()
        assert not engine._running
        
    def test_custom_personality(self, custom_personality):
        engine = TypingEngine(custom_personality)
        assert engine.personality.name == "Test Bot"
        assert engine.personality.base_typing_speed == 0.05
        assert engine.personality.error_rate == 0.0