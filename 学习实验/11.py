def describe_pet(pet_name, animal_type):
    """显示宠物的信息"""
    print(f"I have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

# 使用默认参数
describe_pet(pet_name='willie', animal_type = 'hamster')

# # 明确指定所有参数
# describe_pet(pet_name='harry', animal_type='hamster')