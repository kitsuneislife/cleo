from services.worldmodel.dreams import generate_dream, generate_dreams


def test_generate_dream_length_and_agent():
    traj = generate_dream('test-agent', length=10)
    assert isinstance(traj, list)
    assert len(traj) == 10
    assert traj[0]['agent_id'] == 'test-agent'


def test_generate_dreams_multi():
    ds = generate_dreams(num_agents=3, length=5)
    assert len(ds) == 3
    for i, traj in enumerate(ds):
        assert traj[0]['agent_id'] == f'agent-{i+1}'
        assert len(traj) == 5
