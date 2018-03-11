from gym.envs.registration import register

register(
    id='cms-v0',
    entry_point='gym_cms.envs:CmsEnv',
)

register(
    id='hot-v0',
    entry_point='gym_cms.envs:HotterColder',
)
