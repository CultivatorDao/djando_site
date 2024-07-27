from shared.base64_converter import Base64Converter


class BattleManager:
    converter = Base64Converter()

    def __init__(self, next_url=None):
        self.next = next_url

    def get_info(self, options=None, **kwargs):
        # TODO: add docstring
        if options is None:
            options = {}
        if not kwargs:
            return {}

        data = {}
        for key, value in kwargs.items():
            data[key] = value.__dict__.copy()
            if options.get('except'):
                for exclude in options.get('except'):
                    if data[key].get(exclude):
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

    def colosseum_fight_calculate(self, battle, battle_log=None):
        # if battle_log:
        #     battle_log = self.converter.dict_from_base64(battle_log['data'])
        #     battle_log['turn'] += 1
        # else:
        #     battle_log = {
        #         "turn": 4,
        #         # In future basic attack will presented as skill
        #         # "skill_id": 1
        #         "type": "Basic Attack"
        #     }

        player = battle.player
        enemy = battle.enemy
        skill = ''

        # in future add battle_log field to colosseum battle model
        if battle_log:
            if battle_log.get('skill'):
                skill = battle_log['skill']

        if skill:
            player.current_hp -= enemy['damage']
            enemy['health'] -= player.damage

        data = self.get_info(
            options={
                'except': ["_state", "id"]
            },
            player=player,
        )

        data["next"] = self.converter.dict_to_base64(battle_log)

        # if enemy['health'] <= 0 or player.current_hp <= 0:
        #     battle.is_finished = True

        data['enemy'] = enemy
        if enemy['health'] <= 0 or player.current_hp <= 0:
            data['status'] = 'Finished'
        else:
            data['status'] = ''

        # In future add colosseum battle model field result
        # and replace this statement
        # instead of statement just assign result to this field
        # if enemy['health'] <= 0:
        #     battle.is_won = True
        # elif player.current_hp <= 0:
        #     battle.is_won = False

        if enemy['health'] <= 0:
            data['result'] = 'win'
        if player.current_hp <= 0:
            data['result'] = 'lose'

        # save all models changes
        player.save()
        battle.enemy = enemy

        battle.save()

        return data
