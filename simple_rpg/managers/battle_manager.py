class BattleManager:

    def __init__(self, next_url=None):
        self.next = next_url

    def get_info(self, options: dict = None, **kwargs):
        # TODO: add docstring
        if not kwargs:
            return {}

        data = {}
        for key, value in kwargs.items():
            data[key] = value.__dict__
            if options.get('except'):
                for exclude in options.get('except'):
                    data[key].pop(exclude)

        if options.get('next'):
            # TODO: make this more general for universal use
            data['next'] = f"{self.next}?outcome={options['next'][0]}&reward={data['enemy']['exp_reward']}"

        return data

    def arena_fight_calculate(self, player, enemy):
        """
        Calculates outcome of arena battle. Return data dictionary.
        :return:
        """
        if not (player and enemy):
            return {}

        player_damage = 1 if not (player.damage - enemy.defence) else player.damage - enemy.defence
        enemy_damage = 1 if not (enemy.damage - player.defence) else enemy.damage - player.defence
        outcome = "victory" if enemy.health // player_damage <= player.max_hp // enemy_damage else "lose",

        data = self.get_info(
            options={
                'next': outcome,
                'except': ["_state", "id"]
            },
            character=player,
            enemy=enemy)

        return data
