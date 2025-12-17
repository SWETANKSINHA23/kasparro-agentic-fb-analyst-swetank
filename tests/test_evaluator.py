import pytest
import sys
import os
import yaml

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.evaluator import EvaluatorAgent
from src.agents.insight_agent import InsightAgent
from src.agents.data_agent import DataAgent

def load_test_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@pytest.fixture
def data_agent(test_config):
    if test_config is None:
        return DataAgent(load_test_config())
    return DataAgent(test_config)

@pytest.fixture
def test_config():
    return load_test_config()

@pytest.fixture
def evaluator_agent(data_agent, test_config):
    return EvaluatorAgent(data_agent, test_config)


@pytest.fixture
def sample_aggregates():
    recent_aggs = {
        'spend': 1200.0,
        'impressions': 120000,
        'clicks': 1800,
        'purchases': 50,
        'revenue': 3000.0,
        'ctr': 0.015,  # 1.5%
        'cpm': 10.0,
        'roas': 2.5,
        'cpc': 0.67
    }
    
    previous_aggs = {
        'spend': 1000.0,
        'impressions': 100000,
        'clicks': 2000,
        'purchases': 60,
        'revenue': 3600.0,
        'ctr': 0.020,  # 2.0%
        'cpm': 10.0,
        'roas': 3.6,
        'cpc': 0.50
    }
    
    return recent_aggs, previous_aggs


class TestEvaluatorConfidenceScores:
    
    def test_roas_hypothesis_confidence_range(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "ROAS dropped indicating performance decline"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert 'confidence' in result
        assert isinstance(result['confidence'], (int, float))
        assert 0.0 <= result['confidence'] <= 1.0
        
    def test_ctr_hypothesis_confidence_range(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "CTR declined indicating engagement issues"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        confidence = result['confidence']
        assert 0.0 <= confidence <= 1.0
        
    def test_ad_fatigue_hypothesis_confidence_range(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "Ad fatigue detected with CTR drop and CPM rise"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        confidence = result['confidence']
        assert 0.0 <= confidence <= 1.0


class TestEvaluatorOutputStructure:
    
    def test_output_contains_required_fields(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "ROAS dropped indicating performance decline"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        required_fields = ['hypothesis', 'confidence', 'validated', 'evidence']
        for field in required_fields:
            assert field in result, f"Result should contain '{field}' field"
            assert result[field] is not None, f"'{field}' should not be None"
    
    def test_confidence_is_numeric(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "Test hypothesis"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert isinstance(result['confidence'], (int, float))
    
    def test_validated_is_boolean(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "ROAS dropped"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert isinstance(result['validated'], bool)
    
    def test_evidence_is_string(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "ROAS dropped"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert isinstance(result['evidence'], str)
        assert len(result['evidence']) > 0


class TestEvaluatorKeywordMatching:
    
    def test_roas_keyword_detection(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "ROAS performance has changed"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert 'roas' in result['evidence'].lower() or 'ROAS' in result['evidence']
    
    def test_ctr_keyword_detection(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "CTR has declined significantly"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert 'ctr' in result['evidence'].lower() or 'CTR' in result['evidence']
    
    def test_fatigue_keyword_detection(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "Ad fatigue is impacting performance"
        
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        # Should check both CTR and CPM
        evidence_lower = result['evidence'].lower()
        assert 'ctr' in evidence_lower or 'cpm' in evidence_lower


class TestEvaluatorDeterminism:
    
    def test_same_input_same_output(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "ROAS dropped indicating performance decline"
        
        # Run twice
        result1 = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        result2 = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert result1 == result2
    
    def test_confidence_reproducibility(self, evaluator_agent, sample_aggregates):
        recent_aggs, previous_aggs = sample_aggregates
        hypothesis = "CTR declined"
        
        results = []
        for _ in range(5):
            result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
            results.append(result['confidence'])
        
        # All confidence scores should be identical
        assert len(set(results)) == 1


class TestEvaluatorEdgeCases:
    
    def test_zero_previous_values(self, evaluator_agent):
        recent_aggs = {
            'spend': 100.0,
            'roas': 2.0,
            'ctr': 0.01,
            'cpm': 10.0
        }
        
        previous_aggs = {
            'spend': 0.0,  # Zero value
            'roas': 0.0,
            'ctr': 0.0,
            'cpm': 0.0
        }
        
        hypothesis = "ROAS improved"
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        # Should handle gracefully without errors
        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0
    
    def test_negative_changes(self, evaluator_agent):
        recent_aggs = {'roas': 2.0, 'ctr': 0.01, 'spend': 80.0}
        previous_aggs = {'roas': 3.0, 'ctr': 0.02, 'spend': 100.0}
        
        hypothesis = "Performance declined"
        result = evaluator_agent.evaluate_hypothesis(hypothesis, recent_aggs, previous_aggs)
        
        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0

    def test_mixed_signals(self, evaluator_agent):
        hypothesis = "Mixed signals detected"
        
        recent_stats = {
            'ctr': 0.008,  # 0.8% CTR
            'purchases': 500,
            'cpm': 12.0
        }
        previous_stats = {
            'ctr': 0.012,  # 1.2% CTR  
            'purchases': 490,
            'cpm': 10.0
        }
        
        result = evaluator_agent.evaluate_hypothesis(
            hypothesis=hypothesis,
            recent_aggs=recent_stats,
            previous_aggs=previous_stats
        )
        
        # Lower CTR but similar purchases - interesting pattern
        assert 'confidence' in result
        assert result['confidence'] > 0.0

def run_demo():
    from datetime import timedelta
    import pandas as pd
    
    cfg = load_test_config()
    data_agent = DataAgent(cfg)
    insight_agent = InsightAgent(cfg)
    evaluator = EvaluatorAgent(data_agent, cfg)
    
    # Setup dates
    data_info = data_agent.get_data_info()
    end_date = pd.to_datetime(data_info['date_range']['end'])
    recent_start = end_date - timedelta(days=7)
    prev_start = recent_start - timedelta(days=7)
    
    print("Running InsightAgent...")
    insights = insight_agent.analyze(
        data_agent,
        recent_start.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        prev_start.strftime('%Y-%m-%d'),
        recent_start.strftime('%Y-%m-%d')
    )
    
    print("Running EvaluatorAgent...")
    print("\n--- VALIDATED HYPOTHESES ---")
    
    for h in insights.get('hypotheses', []):
        res = evaluator.evaluate_hypothesis(
            h['hypothesis'],
            insights['recent_window'],
            insights['previous_window']
        )
        
        print(f"- {res['hypothesis']}")
        print(f"  evidence: {res['evidence'].replace(chr(10), '; ')}")
        print(f"  confidence: {res['confidence']:.3f}")
        print(f"  validated: {res['validated']}")
        
    print("\nSaved insights to reports/insights.json")

if __name__ == "__main__":
    run_demo()




