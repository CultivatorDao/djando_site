class BattleManager:

    def __init__(self, models):
        self.models = models
        self.player_model = models['player']
        self.enemy_model = models['enemy']

    # get player id from request
    def get_player(self, request):
        pass

    def fight_info(self, player: int = None, enemy: int = None):
        """
        Return information about player and enemy as dictionary.
        :return:
        """
        return {}

    def arena_fight_calculate(self, player: int = None, enemy: int = None):
        """
        Calculates outcome of arena battle. Return data dictionary.
        :return:
        """
        if not (player and enemy):
            return {}

        player = self.player_model.objects.get(pk=player)
        enemy = self.enemy_model.objects.get(pk=enemy)

        data = self.fight_info(player, enemy)

        data['outcome'] = \
            'victory' \
            if enemy.health // (player.damage - enemy.defence) <= player.max_hp //\
            (enemy.damage - player.defence) else 'lose'

        return data
