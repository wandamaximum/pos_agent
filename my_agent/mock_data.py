mock_menu_items = {
    # BURGERS & SIDES
    "classic beef burger": {
        "name": "Classic Beef Burger",
        "price": 16.00,
        "ingredients": ["beef patty"] # flour for the bun
    },
    "double trouble burger": {
        "name": "Double Trouble Burger",
        "price": 22.00,
        "ingredients": ["beef patty"] # uses 2x patties
    },
    "french fries": {
        "name": "Hand-Cut Fries",
        "price": 5.00,
        "ingredients": ["potatoes", "cooking oil"]
    },

    # PIZZA & BREAD
    "margherita pizza": {
        "name": "Margherita Pizza",
        "price": 14.00,
        "ingredients": ["pizza dough"]
    },
    "garlic bread": {
        "name": "Garlic Bread Basket",
        "price": 6.00,
        "ingredients": ["flour"]
    },

    # MAINS (FISH & CHICKEN)
    "fish and chips": {
        "name": "Fish and Chips",
        "price": 15.00,
        "ingredients": ["flour", "potatoes", "cooking oil"]
    },
    "grilled salmon": {
        "name": "Grilled Salmon",
        "price": 24.00,
        "ingredients": ["salmon fillet"]
    },
    "chicken pasta": {
        "name": "Creamy Chicken Pasta",
        "price": 18.00,
        "ingredients": ["chicken breast", "whole milk", "flour"]
    },

    # BEVERAGES
    "latte": {
        "name": "Caffè Latte",
        "price": 4.50,
        "ingredients": ["coffee beans", "whole milk"]
    },
    "espresso": {
        "name": "Double Espresso",
        "price": 3.00,
        "ingredients": ["coffee beans"]
    },
    "orange juice": {
        "name": "Fresh Orange Juice",
        "price": 5.00,
        "ingredients": ["fresh oranges"] # Assuming fresh_oranges is in materials
    }
}


mock_raw_materials = {
    "beef patty": {
        "name": "Beef Patty",
        "sku": "BF-202",
        "cost": 45.00,
        "current_stock": 12,
        "status": "Low Stock",
        "correlated_menu_items": ["classic_beef_burger", "double_trouble_burger"]
    },
    "pizza dough": {
        "name": "Pizza Dough",
        "sku": "PD-185",
        "cost": 0.85,
        "current_stock": 45,
        "status": "Good",
        "correlated_menu_items": ["margherita_pizza", "pepperoni_pizza", "veggie_pizza"]
    },
    "flour": {
        "name": "All-Purpose Flour",
        "sku": "GR-012",
        "cost": 0.90,
        "current_stock": 5,
        "status": "Critical",
        "correlated_menu_items": ["garlic_bread", "fish_and_chips", "pancakes"]
    },
    "whole milk": {
        "name": "Whole Milk",
        "sku": "DA-112",
        "cost": 3.50,
        "current_stock": 8,
        "status": "Low Stock",
        "correlated_menu_items": ["garlic_mashed_potatoes", "latte", "milkshake"]
    },
    "chicken breast": {
        "name": "Chicken Breast",
        "sku": "MT-505",
        "cost": 12.00,
        "current_stock": 15,
        "status": "Good",
        "correlated_menu_items": ["spicy_wings", "grilled_chicken_salad", "chicken_pasta"]
    },
    "potatoes": {
        "name": "Russet Potatoes",
        "sku": "VG-502",
        "cost": 1.20,
        "current_stock": 25,
        "status": "Good",
        "correlated_menu_items": ["fish_and_chips", "garlic_mashed_potatoes", "french_fries"]
    },
    "salmon fillet": {
        "name": "Atlantic Salmon",
        "sku": "FS-901",
        "cost": 28.00,
        "current_stock": 6,
        "status": "Low Stock",
        "correlated_menu_items": ["grilled_salmon", "salmon_salad"]
    },
    "coffee beans": {
        "name": "Espresso Roast",
        "sku": "BV-500",
        "cost": 22.00,
        "current_stock": 12,
        "status": "Good",
        "correlated_menu_items": ["espresso", "latte", "cappuccino"]
    },
    "cooking oil": {
        "name": "Vegetable Oil",
        "sku": "PN-003",
        "cost": 18.50,
        "current_stock": 10,
        "status": "Good",
        "correlated_menu_items": ["fish_and_chips", "spicy_wings", "french_fries"]
    }
}