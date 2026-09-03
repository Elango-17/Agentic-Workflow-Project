from enterprise_agent_framework.utils.slug import slugify
from enterprise_agent_framework.schemas.agent import AgentSpec
def test_slugify(): assert slugify("GitHub Failure Analyzer")=="github_failure_analyzer"
def test_agent_schema():
    spec=AgentSpec.model_validate({"id":"test_agent","agent":{"name":"Test Agent","details":"Details","practice_area":"Testing","good_at":"Analysis"},"behaviour":{"role":"Tester","goal":"Test","back_story":"Experienced tester","description":"Testing agent","expected_output":"Report"},"llm_configuration":{"model":"gpt-4o","temperature":0.7,"top_p":0.9,"max_iteration":10,"max_rpm":60,"max_execution_time":120},"tools":[]})
    assert spec.id=="test_agent"
