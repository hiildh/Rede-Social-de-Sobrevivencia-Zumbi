from django.db import models

class Survivor(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    last_location = models.CharField(max_length=255) 
    infected = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def is_infected(self):
        return self.infected

    def mark_as_infected(self):
        self.infected = True
        self.save()

class InfectionReport(models.Model):
    reported_survivor = models.ForeignKey(Survivor, related_name='reports', on_delete=models.CASCADE)
    reporter = models.ForeignKey(Survivor, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)


class Inventory(models.Model):
    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE)
    water = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    medication = models.IntegerField(default=0)
    ammunition = models.IntegerField(default=0)

    def __str__(self):
        return f"Inventorio de {self.survivor.name}"

    @property
    def total_points(self):
        return (self.water * 4) + (self.food * 3) + (self.medication * 2) + (self.ammunition * 1)

    def trade_items(self, other_inventory, offered_items, requested_items):
        if self.survivor.is_infected or other_inventory.survivor.is_infected:
            return False, "Sobreventes infectados não podem trocar itens."

        if self.calculate_points(offered_items) != self.calculate_points(requested_items):
            return False, "Pontos de troca não correspondem."

        self.update_inventory(offered_items, decrease=True)
        self.update_inventory(requested_items, decrease=False)

        other_inventory.update_inventory(requested_items, decrease=True)
        other_inventory.update_inventory(offered_items, decrease=False)

        return True, "Troca realizada com sucesso."

    def trade_items_with(self, other_inventory, offered_items, requested_items):
        if self.survivor.is_infected or other_inventory.survivor.is_infected:
            return False, "Sobreviventes infectados não podem trocar itens."

        offered_items_dict = {item['name'].lower(): item['quantity'] for item in offered_items}
        requested_items_dict = {item['name'].lower(): item['quantity'] for item in requested_items}

        if self.calculate_points(offered_items_dict) != other_inventory.calculate_points(requested_items_dict):
            return False, "Pontos de troca não correspondem."

        self.update_inventory(offered_items_dict, decrease=True)
        self.update_inventory(requested_items_dict, decrease=False)

        other_inventory.update_inventory(requested_items_dict, decrease=True)
        other_inventory.update_inventory(offered_items_dict, decrease=False)

        return True, "Troca realizada com sucesso."

    def calculate_points(self, items):
        points = 0
        points += items.get('water', 0) * 4
        points += items.get('food', 0) * 3
        points += items.get('medication', 0) * 2
        points += items.get('ammunition', 0) * 1
        return points

    def update_inventory(self, items, decrease=True):
        for item, amount in items.items():
            current_amount = getattr(self, item)
            if decrease:
                setattr(self, item, current_amount - amount)
            else:
                setattr(self, item, current_amount + amount)
        self.save()
