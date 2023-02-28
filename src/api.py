import config
from uplink import Consumer, get, post, json, Body, returns


class OriRandoApi(Consumer):
    @json
    @returns.json
    @post("/api/seeds")
    def generate_seed(self, universe_preset: Body):
        """Generate a seed"""

    @get("/api/world-seeds/{world_seed_id}/file")
    def get_world_seed_file(self, world_seed_id: int):
        """Get the seed file for a world seed"""


def get_base_url():
    protocol = 'https' if config.SECURE else 'http'
    host = config.HOST
    return f'{protocol}://{host}'


api = OriRandoApi(base_url=get_base_url())
