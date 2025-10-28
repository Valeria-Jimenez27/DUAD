import pytest
from Logic import FinancialManager

def test_add_category_success():
    #arrange
    manager=FinancialManager()
    manager.categories=[]
    #act
    manager.add_category("Expense")
    #assert
    assert "Expense" in manager.categories


def test_add_category_empty():
    #arrange
    manager=FinancialManager()
    manager.categories=[]
    #act y #assert
    with pytest.raises (ValueError):
        manager.add_category("")


def test_add_movement_success():
    #arrange
    manager=FinancialManager()
    manager.categories=["Groceries"]
    manager.datastorage=[]
    #act
    manager.add_movement("Shopping", 15000, "Groceries", "27-10-2025", "Expense")
    #assert
    assert len(manager.datastorage) == 1


def test_add_category_duplicate():
    #arrange
    manager=FinancialManager()
    manager.categories=["Income"]
    #act y #assert
    with pytest.raises(ValueError):
        manager.add_category("Income")


def test_add_movement_invalid_amount_negative():
    #arrange
    manager=FinancialManager()
    manager.categories=["Groceries"]
    manager.datastorage=[]
    #act y assert
    with pytest.raises(ValueError):
        manager.add_movement("Shopping", -5000, "Groceries", "27-10-2025", "Expense")


def test_add_movement_invalid_amount_non_numeric():
    #arrange
    manager=FinancialManager()
    manager.categories=["Groceries"]
    manager.datastorage=[]
    #act y assert
    with pytest.raises(ValueError):
        manager.add_movement("Shopping", "Diez mil colones", "Groceries", "27-10-2025", "Expense")


def test_add_movement_no_categories():
    #arrange
    manager=FinancialManager()
    manager.categories=[]
    #act y assert
    with pytest.raises(ValueError):
        manager.add_movement("Shopping", 15000, "Groceries", "27-10-2025", "Expense")


def test_add_multiple_movements():
    #arrange
    manager=FinancialManager()
    manager.datastorage =[]
    manager.categories=["Groceries"]
    #act
    manager.add_movement("Masxmenos", 93000, "Groceries", "27-01-2025", "Expense")
    manager.add_movement("Ice cream", 2000, "Groceries", "27-10-2025", "Expense")
    #assert
    assert len(manager.datastorage)==2
