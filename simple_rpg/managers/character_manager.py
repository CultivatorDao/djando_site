class CharacterManager:

    def __init__(self):
        self.next_level_multiplication = 0.2
        self.next_level_attributes_quantity = 2

    def level_up(self, player):
        if player.exp_current >= player.exp_next:
            player.level += 1
            player.exp_current -= player.exp_next
            player.attribute_points += self.next_level_attributes_quantity
            player.exp_next += player.exp_next * self.next_level_multiplication

    def get_reward(self, player, reward=0, reward_type: str = 'gold'):
        if reward_type == 'exp':
            player.exp_current += reward
            self.level_up(player)
            player.save()
