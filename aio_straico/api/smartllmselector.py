from enum import Enum
from dataclasses import dataclass


class _PricingMethod(Enum):
    quality = "quality"
    balance = "balance"
    budget = "budget"


@dataclass(frozen=True)
class ModelSelector:
    pricing_method: _PricingMethod
    quantity: int = 1

    @classmethod
    def balance(cls, quantity=1):
        return cls(pricing_method=_PricingMethod.balance, quantity=quantity)

    @classmethod
    def budget(cls, quantity=1):
        return cls(pricing_method=_PricingMethod.budget, quantity=quantity)

    @classmethod
    def quality(cls, quantity=1):
        return cls(pricing_method=_PricingMethod.quality, quantity=quantity)


if __name__ == "__main__":
    q1 = ModelSelector.quality(1)
    q2 = ModelSelector.quality(2)
    q3 = ModelSelector.quality(3)
    q4 = ModelSelector.quality(4)

    ba4 = ModelSelector.balance(4)

    bu4 = ModelSelector.budget(4)

    model = ModelSelector.quality()
    print(model.pricing_method.value)
    print(model.quantity)

    models = ModelSelector.balance(4)
    print(models.pricing_method.value)
    print(models.quantity)

    # will raise error
    # models.quantity = 5
    # print(models.quantity)
